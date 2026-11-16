variable "name" {
  description = "Name of the instance."
  type        = string
}

variable "vpc_id" {
  description = "VPC to create the security group in."
  type        = string
}

variable "subnet_id" {
  description = "Subnet to launch the instance in."
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type."
  type        = string
  default     = "t3.medium"
}

variable "ami_id" {
  description = "AMI ID. Leave null to use the latest Amazon Linux 2023."
  type        = string
  default     = null
}

variable "root_volume_size" {
  description = "Root volume size in GiB."
  type        = number
  default     = 30
}

variable "key_name" {
  description = "Optional EC2 key pair name. SSM Session Manager works without one."
  type        = string
  default     = null
}

variable "associate_public_ip" {
  description = "Assign a public IP address."
  type        = bool
  default     = false
}

variable "ingress_rules" {
  description = "Inbound rules for the instance security group."
  type = list(object({
    description = string
    from_port   = number
    to_port     = number
    protocol    = string
    cidr_blocks = list(string)
  }))
  default = []
}

variable "user_data" {
  description = "Optional cloud-init / shell user data."
  type        = string
  default     = null
}

variable "tags" {
  description = "Tags applied to all resources."
  type        = map(string)
  default     = {}
}
