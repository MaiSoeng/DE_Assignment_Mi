from awsglue.blueprint.job import Job
from awsglue.blueprint.crawler import Crawler, S3Target
from awsglue.blueprint.workflow import Workflow, Entities
import boto3

s3_client = boto3.client('s3')

def generate_layout(user_params, system_params):
    
    # get the parameters from the yaml file
    workflow_name = user_params['WorkflowName']
    worker_type = user_params.get('WorkerType', "G.1X")
    worker_size = int(user_params.get('DPU'))
    s3_input = user_params['S3Path']
    s3_output = user_params['TargetS3Path']
    IAM_role = user_params['PassRole']
    source_dataset = user_params.get("SourceDatabase", "titanic-dataset-ori")
    target_dataset = user_params.get("TargetDatabase", "titanic-dataset-tra")

    s3_location = "s3://hw17-part2/blueprint_script/conversion.py"

    # Source dataset crawler
    source_crawler = Crawler(Name = f"{workflow_name}_source_crawler",
                      Role = IAM_role,
                      DatabaseName = source_dataset,
                      Targets = {"S3Targets": [{"Path": s3_input}]}
    )

    # Glue ETL job
    etl_job = Job(Name = f"{workflow_name}_job",
                  Command = {
                      "Name": "glueetl",
                      "ScriptLocation": s3_location,
                      "PythonVersion": "3"
                  },
                  GlueVersion = "5.0",
                  WorkerType = worker_type,
                  NumberOfWorkers = worker_size,
                  DefaultArguments={
                                    "--input_path": s3_input,
                                    "--job-language": "python",
                                    "--enable-continuous-cloudwatch-log": "true",
                                    "--region_name": system_params['region'],
                                    "--output_path": s3_output,
                                    "--enable-spark-ui": "true",
                                    "--job-bookmark-option": "job-bookmark-enable",
                                    },
                  Role = IAM_role,
                  Timeout = 60,
                  MaxRetries = 1)
    
    # target crawler
    target_crawler = Crawler(Name = f"{workflow_name}_target_crawler",
                      Role = IAM_role,
                      DatabaseName = target_dataset,
                      Targets = {"S3Targets": [{"Path": s3_output}]}
    )
    
    # define some triggers to start the crawler
    etl_job.DependsOn = {source_crawler: "SUCCEEDED"}
    target_crawler.DependsOn = {etl_job: "SUCCEEDED"}

    sample_workflow = Workflow(Name = workflow_name, Entities = Entities(Jobs = [etl_job], Crawlers = [source_crawler, target_crawler], Triggers = []))
    
    return sample_workflow