resource "aws_security_group" "rds_sg" {
    description = "Enable MySQL connection with EC2"
    vpc_id = var.vpc_id
    ingress {
        protocol = "tcp"
        from_port = 3306
        to_port = 3306
        cidr_blocks = ["0.0.0.0/0"]
    }
}

resource "aws_db_instance" "app_server" {
    allocated_storage = var.allocated_storage
    instance_class = var.db_instance_class
    identifier = var.db_name
    engine = var.engine
    engine_version = var.engine_version
    username = var.username
    password = var.password
    vpc_security_group_ids = [aws_security_group.rds_sg.id]
    publicly_accessible = true
}

