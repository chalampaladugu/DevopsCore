# GCP VPC

Custom-mode VPC with subnets (secondary ranges for GKE), Cloud Router + NAT, internal and IAP-SSH firewall rules and private service access for Cloud SQL.

## Usage

```hcl
module "vpc" {
  source = "github.com/chalampaladugu/terraform-multicloud-modules//modules/gcp/vpc?ref=v1.0.0"

  # required inputs - see table below
}
```

See [`examples/gcp`](../../../examples/gcp) for a complete, working stack.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| `project_id` | GCP project ID. | `string` |  | yes |
| `name` | Name of the VPC network. | `string` |  | yes |
| `region` | Region for subnets, router and NAT. | `string` |  | yes |
| `subnets` | Map of subnets. Key = subnet name. secondary_ranges is used by GKE (pods/services). | `map(object({cidr = string, secondary_ranges = optional(map(string), {}), flow_logs = optional(bool, false)}))` | `{}` | no |
| `enable_nat` | Create Cloud Router + Cloud NAT for outbound internet from private VMs. | `bool` | `true` | no |
| `enable_private_service_access` | Reserve a range and peer with Google services (required for Cloud SQL private IP). | `bool` | `true` | no |
| `private_service_access_prefix_length` | Prefix length of the range reserved for Google managed services. | `number` | `16` | no |

## Outputs

| Name | Description |
|------|-------------|
| `network_id` | ID of the VPC network. |
| `network_name` | Name of the VPC network. |
| `network_self_link` | Self link of the VPC network. |
| `subnet_ids` | Map of subnet name => ID. |
| `subnet_self_links` | Map of subnet name => self link. |
| `private_service_connection` | Service networking connection (depend on this for Cloud SQL private IP). |
