import sys
from pyspark.sql import functions as f
from pyspark.context import SparkContext
from awsgluedq.transforms import EvaluateDataQuality
from awsglue.context import GlueContext
from awsglue.transforms import SelectFromCollection
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from awsglue.dynamicframe import DynamicFrame
import boto3

args = getResolvedOptions(sys.argv, [
    'JOB_NAME',
    'region_name',
    'input_path',
    'output_path'])

job_name = args['JOB_NAME']
region_name = args.get('region_name', 'us-east-1')
input_path = args['input_path']
output_path = args['output_path']

glue = boto3.client('glue', region_name = region_name)

sc = SparkContext.getOrCreate()
glue_context = GlueContext(sc)
spark = glue_context.spark_session
job = Job(glue_context)
job.init(args['JOB_NAME'], args)

# get the dataset from the S3 bucket
df = spark.read.option("header", "true").option("inferSchema", "true").csv(input_path)

# perform dataset clean and transformations
df = df.select("PassengerID", "Survived", "Pclass", "Name", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked")
df = df.withColumn("family_size", f.col("SibSp") + f.col("Parch") + 1).filter(f.col("Age").isNotNull())

# categorize the dataframe into different age groups
df_age_groups = df.withColumn("age_groups",
                              f.when(f.col("Age") < 5, "baby")
                               .when((f.col("Age") >= 5) & (f.col("Age") < 18), "teenagers")
                               .when((f.col("Age") >= 18) & (f.col("Age") < 28), "youth")
                               .when((f.col("Age") >= 28) & (f.col("Age") < 40), "adults")
                               .when((f.col("Age") >= 40) & (f.col("Age") < 65), "middle-aged")
                               .when(f.col("Age") >= 65, "elderly")
)

# perform data quality checks
# data_quality_fail = False
titanic_dyf = DynamicFrame.fromDF(df_age_groups, glue_context, "titanic_dyf")

# use DQDL Language to create rules set
EvaluateDataQuality_ruleset = """
    Rules = [
        ColumnExists "PassengerID",
        ColumnExists "Survived",
        ColumnExists "Pclass",
        ColumnExists "Sex",
        ColumnExists "Embarked",
        IsComplete "PassengerID",
        IsComplete "Age",
        IsComplete "Fare",
        IsComplete "Embarked",
        ColumnValues "Age" between 0 and 100,
        ColumnValues "Survived" in [0, 1],
        ColumnValues "Pclass" in [1, 2, 3],
        ColumnValues "Embarked" in ["Q", "C", "S"]
        ]
"""               

# verify the dataset using the rules
EvaluateDataQualityMultiframe = EvaluateDataQuality().process_rows(
    frame = titanic_dyf,
    ruleset = EvaluateDataQuality_ruleset,
    publishing_options = {
        "dataQualityEvaluationContext": "EvaluateDataQualityMultiframe",
        "enableDataQualityCloudWatchMetrics": True,
        "enableDataQualityResultsPublishing": True,
        "publishingMode": "VALUED"
    },
    additional_options={"performanceTuning.caching": "CACHE_NOTHING",
                        "primaryKeys": ["PassengerID"],},
)      

rule_outcomes = SelectFromCollection.apply(
    dfc = EvaluateDataQualityMultiframe,
    key = "ruleOutcomes",
    transformation_ctx = "rule_outcomes",
)

# select the data that passes the data quality rules
rowLevelOutcomes = SelectFromCollection.apply(
    dfc = EvaluateDataQualityMultiframe,
    key = "rowLevelOutcomes",
    transformation_ctx = "rowLevelOutcomes",
)

# maintain only the passed records
transformed_df = rowLevelOutcomes.toDF() # convert Glue DynamicFrame to SparkSQL DataFrame

# find the failed record
row_df = transformed_df.groupBy("PassengerID") \
      .agg(f.max(f.when(f.col("DataQualityEvaluationResult") == "Failed", 1).otherwise(0)).alias("failed"))

# filter out the records that passed the rules
passed_keys = row_df.filter(f.col("failed") == 0).select("PassengerID")

# join with the previous table to filter out the passed record
out_df = df_age_groups.join(passed_keys, on = "PassengerID", how = "inner")

# write the transformed data back to S3 bucket
out_df.write.mode("append").parquet(output_path)

job.commit()