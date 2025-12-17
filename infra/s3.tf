resource "aws_s3_bucket" "ssis_storage" {
  bucket_prefix = "ssis-storage-" # Random unique name
  force_destroy = true            # Allow deleting bucket even if not empty (for lab purposes)

  tags = {
    Name        = "SSIS Storage"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket_versioning" "ssis_ver" {
  bucket = aws_s3_bucket.ssis_storage.id
  versioning_configuration {
    status = "Enabled"
  }
}
