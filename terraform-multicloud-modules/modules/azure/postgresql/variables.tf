variable "name" {
  description = "Server name (globally unique)."
  type        = string
}

variable "resource_group_name" {
  description = "Resource group to deploy into."
  type        = string
}

variable "location" {
  description = "Azure region."
  type        = string
}

variable "postgres_version" {
  description = "PostgreSQL major version."
  type        = string
  default     = "16"
}

variable "sku_name" {
  description = "Server SKU, e.g. B_Standard_B1ms, GP_Standard_D2ds_v5."
  type        = string
  default     = "GP_Standard_D2ds_v5"
}

variable "storage_mb" {
  description = "Storage size in MB."
  type        = number
  default     = 32768
}

variable "administrator_login" {
  description = "Admin username."
  type        = string
  default     = "pgadmin"
}

variable "databases" {
  description = "Names of databases to create."
  type        = list(string)
  default     = ["app"]
}

variable "delegated_subnet_id" {
  description = "Subnet delegated to Microsoft.DBforPostgreSQL/flexibleServers (private access). Null = public access."
  type        = string
  default     = null
}

variable "virtual_network_id" {
  description = "VNet ID used to link the private DNS zone (required with delegated_subnet_id)."
  type        = string
  default     = null
}

variable "zone" {
  description = "Primary availability zone."
  type        = string
  default     = "1"
}

variable "high_availability" {
  description = "Enable zone-redundant high availability."
  type        = bool
  default     = false
}

variable "backup_retention_days" {
  description = "Days to keep backups (7-35)."
  type        = number
  default     = 7
}

variable "tags" {
  description = "Tags applied to all resources."
  type        = map(string)
  default     = {}
}
