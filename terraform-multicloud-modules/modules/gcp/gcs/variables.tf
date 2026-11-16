variable "project_id" {
  description = "GCP project ID."
  type        = string
}

variable "name" {
  description = "Globally unique bucket name."
  type        = string
}

variable "location" {
  description = "Region (e.g. us-central1) or multi-region (e.g. US)."
  type        = string
}

variable "storage_class" {
  description = "STANDARD, NEARLINE, COLDLINE or ARCHIVE."
  type        = string
  default     = "STANDARD"
}

variable "versioning_enabled" {
  description = "Enable object versioning."
  type        = bool
  default     = true
}

variable "nearline_after_days" {
  description = "Days before moving objects to NEARLINE. Set 0 to disable."
  type        = number
  default     = 30
}

variable "noncurrent_version_expiration_days" {
  description = "Days before deleting old versions. Set 0 to disable."
  type        = number
  default     = 90
}

variable "kms_key_name" {
  description = "Optional Cloud KMS key for default encryption."
  type        = string
  default     = null
}

variable "force_destroy" {
  description = "Allow deleting a non-empty bucket."
  type        = bool
  default     = false
}

variable "labels" {
  description = "Labels applied to the bucket."
  type        = map(string)
  default     = {}
}
