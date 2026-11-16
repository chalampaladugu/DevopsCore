variable "name" {
  description = "AKS cluster name."
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

variable "kubernetes_version" {
  description = "Kubernetes version. Leave null for the current AKS default."
  type        = string
  default     = null
}

variable "sku_tier" {
  description = "Free, Standard (uptime SLA) or Premium."
  type        = string
  default     = "Free"
}

variable "vnet_subnet_id" {
  description = "Subnet for nodes and pods (Azure CNI overlay)."
  type        = string
}

variable "node_vm_size" {
  description = "VM size for the system node pool."
  type        = string
  default     = "Standard_D4s_v5"
}

variable "node_count" {
  description = "Node count when autoscaling is disabled."
  type        = number
  default     = 2
}

variable "enable_auto_scaling" {
  description = "Enable the cluster autoscaler on the default pool."
  type        = bool
  default     = true
}

variable "min_count" {
  description = "Minimum nodes when autoscaling."
  type        = number
  default     = 1
}

variable "max_count" {
  description = "Maximum nodes when autoscaling."
  type        = number
  default     = 4
}

variable "zones" {
  description = "Availability zones for the default pool."
  type        = list(string)
  default     = null
}

variable "service_cidr" {
  description = "Kubernetes service CIDR (must not overlap the VNet)."
  type        = string
  default     = "172.16.0.0/16"
}

variable "dns_service_ip" {
  description = "Cluster DNS IP inside service_cidr."
  type        = string
  default     = "172.16.0.10"
}

variable "pod_cidr" {
  description = "Pod CIDR for Azure CNI overlay."
  type        = string
  default     = "192.168.0.0/16"
}

variable "log_analytics_workspace_id" {
  description = "Optional Log Analytics workspace for Container Insights."
  type        = string
  default     = null
}

variable "tags" {
  description = "Tags applied to all resources."
  type        = map(string)
  default     = {}
}
