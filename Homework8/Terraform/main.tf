provider "aws" {
    region = "us-east-1"
}

module "s3_bucket" {
    source = "./modules/s3_bucket"
    bucket_name = "assignment8-s3-mi"
}

module "ec2_instance" {
    source = "./modules/EC2"
    ami = "ami-0f3f13f145e66a0a3"
    instance_type = "t3.micro"
    key_name = "mi-assignment8"
    instance_name = "assignment8-ec2-mi"
}

module "rds_instance" {
    source = "./modules/RDS"
    allocated_storage = 20
    db_instance_class = "db.t3.micro"
    db_name = "assignment8rdsmi"
    engine = "MySQL"
    engine_version = "8.0.33"
    username = "usermi"
    password = "mi123456"
    vpc_id = "vpc-09155e992773617fb"
}