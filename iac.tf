provider "aws" {
  region     = "us-east-1"
  # FAIL: Hardcoded Secrets
  access_key = "AKIAEXAMPLE123456789"
  secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
}

# FAIL: S3 Bucket with Public Access (IaC Violation)
resource "aws_s3_bucket" "research_data" {
  bucket = "deep-sea-research-logs"
}

resource "aws_s3_bucket_public_access_block" "fail" {
  bucket = aws_s3_bucket.research_data.id

  # Setting these to false creates a massive security "hole"
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# FAIL: Security Group allowing all traffic on port 22 (SSH)
resource "aws_security_group" "ssh_open" {
  name = "allow_all_ssh"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # The "Shadow Crew" loves this
  }
}