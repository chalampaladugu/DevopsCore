variable "name" {
  description = "EKS cluster name."
  type        = string
}

variable "kubernetes_version" {
  description = "Kubernetes version. Leave null for the current AWS default."
  type        = string
  default     = null
}

variable "subnet_ids" {
  description = "Private subnet IDs for the control plane ENIs and worker nodes."
  type        = list(string)
}

variable "endpoint_public_access" {
  description = "Expose the Kubernetes API publicly."
  type        = bool
  default     = true
}

variable "public_access_cidrs" {
  description = "CIDRs allowed to reach the public API endpoint."
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "node_instance_types" {
  description = "Instance types for the managed node group."
  type        = list(string)
  default     = ["t3.large"]
}

variable "node_capacity_type" {
  description = "ON_DEMAND or SPOT."
  type        = string
  default     = "ON_DEMAND"
}

variable "node_min_size" {
  description = "Minimum number of nodes."
  type        = number
  default     = 1
}

variable "node_desired_size" {
  description = "Desired number of nodes."
  type        = number
  default     = 2
}

variable "node_max_size" {
  description = "Maximum number of nodes."
  type        = number
  default     = 4
}

variable "node_disk_size" {
  description = "Node disk size in GiB."
  type        = number
  default     = 50
}

variable "tags" {
  description = "Tags applied to all resources."
  type        = map(string)
  default     = {}
}
