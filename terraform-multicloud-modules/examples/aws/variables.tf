variable "region" {
  description = "AWS region."
  type        = string
  default     = "us-east-1"
}

variable "project" {
  description = "Project name used in resource names."
  type        = string
  default     = "demo"
}

variable "environment" {
  description = "Environment name (dev, stage, prod)."
  type        = string
  default     = "dev"
}

variable "bucket_suffix" {
  description = "Unique suffix to make the S3 bucket name globally unique."
  type        = string
}
