variable "name" {
  description = "Name of the virtual network."
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

variable "address_space" {
  description = "Address space for the VNet."
  type        = list(string)
  default     = ["10.10.0.0/16"]
}

variable "subnets" {
  description = "Map of subnets. Key = subnet name. Optional delegation, e.g. Microsoft.DBforPostgreSQL/flexibleServers."
  type = map(object({
    address_prefixes  = list(string)
    service_endpoints = optional(list(string), [])
    delegation        = optional(string)
  }))
  default = {}
}

variable "create_nsg" {
  description = "Create a network security group and attach it to non-delegated subnets."
  type        = bool
  default     = true
}

variable "tags" {
  description = "Tags applied to all resources."
  type        = map(string)
  default     = {}
}
