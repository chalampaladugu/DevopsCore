variable "subscription_id" {
  description = "Azure subscription ID."
  type        = string
}

variable "location" {
  description = "Azure region."
  type        = string
  default     = "eastus"
}

variable "project" {
  description = "Project name (lowercase letters and numbers; used in storage account name)."
  type        = string
  default     = "demo"
}

variable "environment" {
  description = "Environment name (dev, stage, prod)."
  type        = string
  default     = "dev"
}

variable "storage_suffix" {
  description = "Short unique suffix (lowercase letters/numbers) for globally unique names."
  type        = string
}

variable "ssh_public_key" {
  description = "SSH public key for the VM admin user."
  type        = string
}
