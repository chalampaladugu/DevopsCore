variable "project_id" {
  description = "GCP project ID."
  type        = string
}

variable "region" {
  description = "GCP region."
  type        = string
  default     = "us-central1"
}

variable "project" {
  description = "Short project name used in resource names."
  type        = string
  default     = "demo"
}

variable "environment" {
  description = "Environment name (dev, stage, prod)."
  type        = string
  default     = "dev"
}

variable "bucket_suffix" {
  description = "Unique suffix to make the bucket name globally unique."
  type        = string
}
