# AWS VPC

VPC with public/private subnets across AZs, internet gateway, NAT gateway(s) and route tables. Subnets are pre-tagged for EKS load balancers.

## Usage

```hcl
module "vpc" {
  source = "github.com/chalampaladugu/terraform-multicloud-modules//modules/aws/vpc?ref=v1.0.0"

  # required inputs - see table below
}
```

See [`examples/aws`](../../../examples/aws) for a complete, working stack.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| `name` | Name prefix for all VPC resources. | `string` |  | yes |
| `cidr_block` | CIDR block for the VPC. | `string` | `"10.0.0.0/16"` | no |
| `azs` | Availability zones to spread subnets across. | `list(string)` |  | yes |
| `public_subnet_cidrs` | CIDRs for public subnets (one per AZ). | `list(string)` | `[]` | no |
| `private_subnet_cidrs` | CIDRs for private subnets (one per AZ). | `list(string)` | `[]` | no |
| `enable_nat_gateway` | Create NAT gateway(s) so private subnets can reach the internet. | `bool` | `true` | no |
| `single_nat_gateway` | Use one shared NAT gateway (cheaper) instead of one per AZ (highly available). | `bool` | `true` | no |
| `tags` | Tags applied to all resources. | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| `vpc_id` | ID of the VPC. |
| `vpc_cidr_block` | CIDR block of the VPC. |
| `public_subnet_ids` | IDs of the public subnets. |
| `private_subnet_ids` | IDs of the private subnets. |
| `nat_gateway_ids` | IDs of the NAT gateways. |
