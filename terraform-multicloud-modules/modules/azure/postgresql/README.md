# Azure PostgreSQL Flexible Server

PostgreSQL Flexible Server with private VNet access (delegated subnet + private DNS zone) or public access, optional zone-redundant HA and generated admin password.

## Usage

```hcl
module "postgresql" {
  source = "github.com/chalampaladugu/terraform-multicloud-modules//modules/azure/postgresql?ref=v1.0.0"

  # required inputs - see table below
}
```

See [`examples/azure`](../../../examples/azure) for a complete, working stack.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| `name` | Server name (globally unique). | `string` |  | yes |
| `resource_group_name` | Resource group to deploy into. | `string` |  | yes |
| `location` | Azure region. | `string` |  | yes |
| `postgres_version` | PostgreSQL major version. | `string` | `"16"` | no |
| `sku_name` | Server SKU, e.g. B_Standard_B1ms, GP_Standard_D2ds_v5. | `string` | `"GP_Standard_D2ds_v5"` | no |
| `storage_mb` | Storage size in MB. | `number` | `32768` | no |
| `administrator_login` | Admin username. | `string` | `"pgadmin"` | no |
| `databases` | Names of databases to create. | `list(string)` | `["app"]` | no |
| `delegated_subnet_id` | Subnet delegated to Microsoft.DBforPostgreSQL/flexibleServers (private access). Null = public access. | `string` | `None` | no |
| `virtual_network_id` | VNet ID used to link the private DNS zone (required with delegated_subnet_id). | `string` | `None` | no |
| `zone` | Primary availability zone. | `string` | `"1"` | no |
| `high_availability` | Enable zone-redundant high availability. | `bool` | `false` | no |
| `backup_retention_days` | Days to keep backups (7-35). | `number` | `7` | no |
| `tags` | Tags applied to all resources. | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| `server_id` | ID of the PostgreSQL server. |
| `fqdn` | Server hostname. |
| `administrator_login` | Admin username. |
| `administrator_password` | Generated admin password. Move it to Key Vault for production. |
