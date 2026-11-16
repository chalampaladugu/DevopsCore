variable "bucket_name" {
  description = "Globally unique bucket name."
  type        = string
}

variable "versioning_enabled" {
  description = "Enable object versioning."
  type        = bool
  default     = true
}

variable "kms_key_arn" {
  description = "Optional KMS key ARN. Leave null for SSE-S3 (AES256)."
  type        = string
  default     = null
}

variable "force_destroy" {
  description = "Allow deleting the bucket even if it contains objects."
  type        = bool
  default     = false
}

variable "transition_to_ia_days" {
  description = "Days before moving objects to STANDARD_IA. Set 0 to disable."
  type        = number
  default     = 30
}

variable "noncurrent_version_expiration_days" {
  description = "Days before deleting old object versions. Set 0 to disable."
  type        = number
  default     = 90
}

variable "tags" {
  description = "Tags applied to all resources."
  type        = map(string)
  default     = {}
}
