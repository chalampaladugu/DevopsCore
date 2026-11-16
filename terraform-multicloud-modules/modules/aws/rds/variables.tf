variable "name" {
  description = "Identifier for the database instance."
  type        = string
}

variable "vpc_id" {
  description = "VPC for the database security group."
  type        = string
}

variable "subnet_ids" {
  description = "Private subnet IDs (at least two AZs)."
  type        = list(string)
}

variable "allowed_cidr_blocks" {
  description = "CIDRs allowed to connect on the database port."
  type        = list(string)
  default     = []
}

variable "allowed_security_group_ids" {
  description = "Security groups allowed to connect on the database port."
  type        = list(string)
  default     = []
}

variable "engine_version" {
  description = "PostgreSQL major version."
  type        = string
  default     = "16"
}

variable "instance_class" {
  description = "RDS instance class."
  type        = string
  default     = "db.t4g.medium"
}

variable "allocated_storage" {
  description = "Initial storage in GiB."
  type        = number
  default     = 20
}

variable "max_allocated_storage" {
  description = "Storage autoscaling ceiling in GiB."
  type        = number
  default     = 100
}

variable "db_name" {
  description = "Name of the initial database."
  type        = string
  default     = "app"
}

variable "username" {
  description = "Master username. The password is generated and stored in Secrets Manager."
  type        = string
  default     = "dbadmin"
}

variable "multi_az" {
  description = "Deploy a standby in another AZ."
  type        = bool
  default     = false
}

variable "backup_retention_days" {
  description = "Days to keep automated backups."
  type        = number
  default     = 7
}

variable "deletion_protection" {
  description = "Prevent accidental deletion."
  type        = bool
  default     = true
}

variable "skip_final_snapshot" {
  description = "Skip the final snapshot on destroy."
  type        = bool
  default     = false
}

variable "tags" {
  description = "Tags applied to all resources."
  type        = map(string)
  default     = {}
}
