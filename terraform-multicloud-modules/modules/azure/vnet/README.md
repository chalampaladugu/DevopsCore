# Azure Virtual Network

VNet with a map of subnets (service endpoints, optional delegation) and an NSG attached to non-delegated subnets.

## Usage

```hcl
module "vnet" {
  source = "github.com/chalampaladugu/terraform-multicloud-modules//modules/azure/vnet?ref=v1.0.0"

  # required inputs - see table below
}
```

See [`examples/azure`](../../../examples/azure) for a complete, working stack.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| `name` | Name of the virtual network. | `string` |  | yes |
| `resource_group_name` | Resource group to deploy into. | `string` |  | yes |
| `location` | Azure region. | `string` |  | yes |
| `address_space` | Address space for the VNet. | `list(string)` | `["10.10.0.0/16"]` | no |
| `subnets` | Map of subnets. Key = subnet name. Optional delegation, e.g. Microsoft.DBforPostgreSQL/flexibleServers. | `map(object({address_prefixes = list(string), service_endpoints = optional(list(string), []), delegation = optional(string)}))` | `{}` | no |
| `create_nsg` | Create a network security group and attach it to non-delegated subnets. | `bool` | `true` | no |
| `tags` | Tags applied to all resources. | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| `vnet_id` | ID of the virtual network. |
| `vnet_name` | Name of the virtual network. |
| `subnet_ids` | Map of subnet name => subnet ID. |
| `nsg_id` | ID of the network security group (if created). |
