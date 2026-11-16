variable "name" {
  description = "Name of the virtual machine."
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

variable "subnet_id" {
  description = "Subnet for the VM network interface."
  type        = string
}

variable "size" {
  description = "VM size."
  type        = string
  default     = "Standard_D2s_v5"
}

variable "admin_username" {
  description = "Admin username."
  type        = string
  default     = "azureuser"
}

variable "ssh_public_key" {
  description = "SSH public key for the admin user."
  type        = string
}

variable "os_disk_size_gb" {
  description = "OS disk size in GB."
  type        = number
  default     = 30
}

variable "os_disk_type" {
  description = "OS disk storage type."
  type        = string
  default     = "Premium_LRS"
}

variable "image" {
  description = "Marketplace image reference."
  type = object({
    publisher = string
    offer     = string
    sku       = string
    version   = string
  })
  default = {
    publisher = "Canonical"
    offer     = "ubuntu-24_04-lts"
    sku       = "server"
    version   = "latest"
  }
}

variable "create_public_ip" {
  description = "Attach a static public IP."
  type        = bool
  default     = false
}

variable "zone" {
  description = "Availability zone (\"1\", \"2\", \"3\") or null."
  type        = string
  default     = null
}

variable "custom_data" {
  description = "Optional cloud-init content (plain text; encoded by the module)."
  type        = string
  default     = null
}

variable "tags" {
  description = "Tags applied to all resources."
  type        = map(string)
  default     = {}
}
