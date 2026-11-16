variable "project_id" {
  description = "GCP project ID."
  type        = string
}

variable "name" {
  description = "Instance name."
  type        = string
}

variable "region" {
  description = "Region."
  type        = string
}

variable "database_version" {
  description = "Database version."
  type        = string
  default     = "POSTGRES_16"
}

variable "tier" {
  description = "Machine tier, e.g. db-custom-2-7680."
  type        = string
  default     = "db-custom-2-7680"
}

variable "disk_size_gb" {
  description = "Initial disk size in GB (auto-grows)."
  type        = number
  default     = 20
}

variable "private_network" {
  description = "VPC self link for private IP. The VPC must have private service access."
  type        = string
}

variable "high_availability" {
  description = "Use REGIONAL availability (standby in another zone)."
  type        = bool
  default     = false
}

variable "databases" {
  description = "Names of databases to create."
  type        = list(string)
  default     = ["app"]
}

variable "user_name" {
  description = "Application user name (password is generated)."
  type        = string
  default     = "app"
}

variable "deletion_protection" {
  description = "Prevent accidental deletion."
  type        = bool
  default     = true
}

variable "labels" {
  description = "User labels."
  type        = map(string)
  default     = {}
}
