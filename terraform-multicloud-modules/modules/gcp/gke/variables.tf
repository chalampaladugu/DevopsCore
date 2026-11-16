variable "project_id" {
  description = "GCP project ID."
  type        = string
}

variable "name" {
  description = "Cluster name."
  type        = string
}

variable "location" {
  description = "Region (regional cluster) or zone (zonal cluster)."
  type        = string
}

variable "network" {
  description = "VPC network self link or ID."
  type        = string
}

variable "subnetwork" {
  description = "Subnetwork self link or ID."
  type        = string
}

variable "pods_range_name" {
  description = "Secondary range name for pods."
  type        = string
  default     = "pods"
}

variable "services_range_name" {
  description = "Secondary range name for services."
  type        = string
  default     = "services"
}

variable "release_channel" {
  description = "RAPID, REGULAR or STABLE."
  type        = string
  default     = "REGULAR"
}

variable "enable_private_nodes" {
  description = "Nodes get internal IPs only."
  type        = bool
  default     = true
}

variable "master_ipv4_cidr_block" {
  description = "/28 range for the control plane when private nodes are enabled."
  type        = string
  default     = "172.16.0.0/28"
}

variable "master_authorized_networks" {
  description = "CIDRs allowed to reach the control plane. Empty = no restriction."
  type = list(object({
    cidr_block   = string
    display_name = string
  }))
  default = []
}

variable "machine_type" {
  description = "Node machine type."
  type        = string
  default     = "e2-standard-4"
}

variable "min_node_count" {
  description = "Minimum nodes per zone."
  type        = number
  default     = 1
}

variable "max_node_count" {
  description = "Maximum nodes per zone."
  type        = number
  default     = 3
}

variable "disk_size_gb" {
  description = "Node disk size in GB."
  type        = number
  default     = 50
}

variable "spot" {
  description = "Use Spot VMs for the node pool."
  type        = bool
  default     = false
}

variable "deletion_protection" {
  description = "Prevent terraform destroy from deleting the cluster."
  type        = bool
  default     = true
}

variable "labels" {
  description = "Resource labels."
  type        = map(string)
  default     = {}
}
