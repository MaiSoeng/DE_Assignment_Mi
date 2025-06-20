resource "aws_security_group" "instance_sg" {
    description = "Enable SSH Access"
    ingress {
        protocol = "tcp"
        from_port = 22
        to_port = 22
        cidr_blocks = ["0.0.0.0/0"]
    }
}

resource "aws_instance" "app_server" {
    ami = var.ami
    instance_type = var.instance_type
    key_name = var.key_name
    vpc_security_group_ids = [aws_security_group.instance_sg.id]

    tags = {
        Name = var.instance_name
    }
}

resource "aws_eip" "this" {
    instance = aws_instance.app_server.id
}