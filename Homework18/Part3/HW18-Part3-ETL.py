import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as f
from pyspark.sql.types import IntegerType, DoubleType

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
JOB_NAME = "HW18-Part3-ETL"
args = {'JOB_NAME': JOB_NAME}

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

S3_INPUT = "s3://hw18-part3/data/"
S3_OUTPUT = "s3://hw18-part3/processed_data/"

# get the dataset from the S3 bucket
df = spark.read.option("header", "true").option("inferSchema", "true").csv(S3_INPUT)

# define the key indicators and year we want to analyze
key_indicators = [
    "NY.GDP.MKTP.CD", # GDP in US currency
    "SP.POP.GROW", # population growth annually
    "SH.XPD.CHEX.GD.ZS", # current health expenditure
]

year_start = 1960
year_end = 2024

# keep the key indicators
df = df.filter(f.col("Indicator Code").isin(key_indicators))

# find the columns representing years and clean the value in year columns
year_cols = [c for c in df.columns if c.isdigit() and len(c) == 4]
for years in year_cols:
    df = df.withColumn(
        years,
        f.when(
            f.trim(f.col(years).cast("string")) == "", None   # set the blank to be null
        ).otherwise(
            f.regexp_replace(f.col(years).cast("string"), "^'", "")  # clear the ' in the beginning of the value
             .cast("double")                                    
        )
    )

# exchange the format of the chart
pairs = []
for years in year_cols:
    pairs += [f"'{years}'", f"`{years}`"]
stack_expr = f"stack({len(year_cols)}, {', '.join(pairs)}) as (year_str, raw_value)"
    
df = (df.selectExpr("`Country Name`", "`Country Code`", "`Indicator Name`", "`Indicator Code`", stack_expr)
        .withColumn("year", f.col("year_str").cast(IntegerType()))
        .withColumn("value", f.col("raw_value").cast(DoubleType()))
        .drop("year_str", "raw_value")
        )

# filter out the null value
df = df.filter(f.col("year").between(year_start, year_end)).filter(f.col("value").isNotNull())

# drop the duplicated records
df = df.dropDuplicates(["Country Code", "Indicator Code", "year"])
# df.write.mode("append").option("header", "true").csv(S3_OUTPUT)

out_csv = S3_OUTPUT.rstrip("/") + "/csv_by_indicator/"
(df.repartition("Indicator Name", "year")
   .write.mode("append")
   .option("header", "true")
   .partitionBy("Indicator Name", "year")
   .csv(out_csv))

job.commit()