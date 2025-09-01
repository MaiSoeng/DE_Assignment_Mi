import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
from pyspark.sql import functions as f

# data schema
schema = StructType([
    StructField("timestamp", StringType(), True),
    StructField("user_id", StringType(), True),
    StructField("session_id", StringType(), True),
    StructField("action", StringType(), True),
    StructField("item_id", IntegerType(), True),
    StructField("price", DoubleType(), True),
])

JOB_NAME = "HW17-ETL-MSK"
args = {'JOB_NAME': JOB_NAME}
sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(JOB_NAME, args)

kafka_options ={ 
      "connectionName": "msk-glue", 
      "topicName": "Part1", 
      "startingOffsets": "earliest", 
    }
    
raw_df = glueContext.create_data_frame.from_options(connection_type = "kafka", connection_options = kafka_options, transformation_ctx="kafka_dyf")
payload_col = "$remove$record_timestamp$_temporary$" # data is stored in this column
df = (
    raw_df
    .withColumn("value_str", f.col(f"`{payload_col}`").cast("string")) 
    .select(f.from_json("value_str", schema).alias("data"))
    .select(
        f.col("data.timestamp").alias("event_time"),
        f.col("data.user_id").alias("user_id"),
        f.col("data.action").alias("action"),
        f.col("data.item_id").alias("item_id"),
        f.col("data.price").alias("price")
    )
    )
df = df.filter(f.col("price").isNotNull())
df.printSchema()

output_dir = "s3://hw17-msk-part1/processed_data/"
checkpoint_dir = "s3://hw17-msk-part1/checkpoints/"

df.writeStream.format("parquet").option("path", output_dir).option("checkpointLocation", checkpoint_dir).outputMode("append").start()

job.commit()