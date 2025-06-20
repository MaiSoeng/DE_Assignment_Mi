resource "aws_s3_bucket" "app_server" {
  bucket = var.bucket_name
}
