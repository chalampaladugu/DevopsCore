variable "name" {
  description = "Storage account name (3-24 lowercase letters and numbers, globally unique)."
  type        = string

  validation {
    condition     = can(regex("^[a-z0-9]{3,24}$", var.name))
    error_message = "Storage account name must be 3-24 lowercase letters or numbers."
  }
}

variable "resource_group_name" {
  description = "Resource group to deploy into."
  type        = string
}

variable "location" {
  description = "Azure region."
  type        = string
}

variable "account_tier" {
  description = "Standard or Premium."
  type        = string
  default     = "Standard"
}

variable "replication_type" {
  description = "LRS, ZRS, GRS, RAGRS, GZRS or RAGZRS."
  type        = string
  default     = "ZRS"
}

variable "access_tier" {
  description = "Hot or Cool."
  type        = string
  default     = "Hot"
}

variable "containers" {
  description = "Names of private blob containers to create."
  type        = list(string)
  default     = []
}

variable "versioning_enabled" {
  description = "Enable blob versioning."
  type        = bool
  default     = true
}

variable "soft_delete_days" {
  description = "Days to retain deleted blobs and containers."
  type        = number
  default     = 7
}

variable "public_network_access_enabled" {
  description = "Allow access from public networks."
  type        = bool
  default     = true
}

variable "tags" {
  description = "Tags applied to all resources."
  type        = map(string)
  default     = {}
}
