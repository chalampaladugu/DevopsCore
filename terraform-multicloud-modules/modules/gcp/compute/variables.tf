variable "project_id" {
  description = "GCP project ID."
  type        = string
}

variable "name" {
  description = "Instance name."
  type        = string
}

variable "zone" {
  description = "Zone, e.g. us-central1-a."
  type        = string
}

variable "machine_type" {
  description = "Machine type."
  type        = string
  default     = "e2-standard-2"
}

variable "subnetwork" {
  description = "Subnetwork self link or ID."
  type        = string
}

variable "image" {
  description = "Boot image."
  type        = string
  default     = "debian-cloud/debian-12"
}

variable "boot_disk_size_gb" {
  description = "Boot disk size in GB."
  type        = number
  default     = 30
}

variable "boot_disk_type" {
  description = "pd-balanced, pd-ssd or pd-standard."
  type        = string
  default     = "pd-balanced"
}

variable "assign_public_ip" {
  description = "Attach an ephemeral external IP."
  type        = bool
  default     = false
}

variable "network_tags" {
  description = "Network tags (used by firewall rules)."
  type        = list(string)
  default     = []
}

variable "startup_script" {
  description = "Optional startup script."
  type        = string
  default     = null
}

variable "labels" {
  description = "Labels applied to the instance."
  type        = map(string)
  default     = {}
}
