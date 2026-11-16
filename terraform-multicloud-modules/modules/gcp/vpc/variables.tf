variable "project_id" {
  description = "GCP project ID."
  type        = string
}

variable "name" {
  description = "Name of the VPC network."
  type        = string
}

variable "region" {
  description = "Region for subnets, router and NAT."
  type        = string
}

variable "subnets" {
  description = "Map of subnets. Key = subnet name. secondary_ranges is used by GKE (pods/services)."
  type = map(object({
    cidr             = string
    secondary_ranges = optional(map(string), {})
    flow_logs        = optional(bool, false)
  }))
  default = {}
}

variable "enable_nat" {
  description = "Create Cloud Router + Cloud NAT for outbound internet from private VMs."
  type        = bool
  default     = true
}

variable "enable_private_service_access" {
  description = "Reserve a range and peer with Google services (required for Cloud SQL private IP)."
  type        = bool
  default     = true
}

variable "private_service_access_prefix_length" {
  description = "Prefix length of the range reserved for Google managed services."
  type        = number
  default     = 16
}
