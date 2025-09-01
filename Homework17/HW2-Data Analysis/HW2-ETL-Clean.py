import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as f

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
JOB_NAME = "HW17-ETL-Part2"
args = {'JOB_NAME': JOB_NAME}

S3_INPUT = "s3://hw17-part2/data/"
S3_OUTPUT = "s3://hw17-part2/processed_data/"

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# get the dataset from the S3 bucket
df = spark.read.option("header", "true").option("inferSchema", "true").csv(S3_INPUT)

# perform dataset clean and transformations
df = df.select("PassengerID", "Survived", "Pclass", "Name", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked")
df = df.withColumn("family_size", f.col("SibSp") + f.col("Parch") + 1).filter(f.col("age").isNotNull())
df.show()

# write the data to the S3 bucket
df.write.mode("append").parquet(S3_OUTPUT)

job.commit()