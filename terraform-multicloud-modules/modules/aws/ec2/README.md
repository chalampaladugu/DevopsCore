# AWS EC2 Instance

EC2 instance on the latest Amazon Linux 2023, with an encrypted gp3 root disk, IMDSv2 enforced, its own security group and an IAM role with SSM Session Manager access (no SSH keys needed).

## Usage

```hcl
module "ec2" {
  source = "github.com/chalampaladugu/terraform-multicloud-modules//modules/aws/ec2?ref=v1.0.0"

  # required inputs - see table below
}
```

See [`examples/aws`](../../../examples/aws) for a complete, working stack.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| `name` | Name of the instance. | `string` |  | yes |
| `vpc_id` | VPC to create the security group in. | `string` |  | yes |
| `subnet_id` | Subnet to launch the instance in. | `string` |  | yes |
| `instance_type` | EC2 instance type. | `string` | `"t3.medium"` | no |
| `ami_id` | AMI ID. Leave null to use the latest Amazon Linux 2023. | `string` | `None` | no |
| `root_volume_size` | Root volume size in GiB. | `number` | `30` | no |
| `key_name` | Optional EC2 key pair name. SSM Session Manager works without one. | `string` | `None` | no |
| `associate_public_ip` | Assign a public IP address. | `bool` | `false` | no |
| `ingress_rules` | Inbound rules for the instance security group. | `list(object({description = string, from_port = number, to_port = number, protocol = string, cidr_blocks = list(string)}))` | `[]` | no |
| `user_data` | Optional cloud-init / shell user data. | `string` | `None` | no |
| `tags` | Tags applied to all resources. | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| `instance_id` | ID of the EC2 instance. |
| `private_ip` | Private IP address. |
| `public_ip` | Public IP address (if assigned). |
| `security_group_id` | ID of the instance security group. |
| `iam_role_name` | Name of the instance IAM role (attach extra policies to it). |
