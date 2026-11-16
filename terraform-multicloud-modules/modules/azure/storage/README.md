# Azure Storage Account

StorageV2 account with TLS 1.2, no public blobs, versioning, soft delete and private containers.

## Usage

```hcl
module "storage" {
  source = "github.com/chalampaladugu/terraform-multicloud-modules//modules/azure/storage?ref=v1.0.0"

  # required inputs - see table below
}
```

See [`examples/azure`](../../../examples/azure) for a complete, working stack.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| `name` | Storage account name (3-24 lowercase letters and numbers, globally unique). | `string` |  | yes |
| `resource_group_name` | Resource group to deploy into. | `string` |  | yes |
| `location` | Azure region. | `string` |  | yes |
| `account_tier` | Standard or Premium. | `string` | `"Standard"` | no |
| `replication_type` | LRS, ZRS, GRS, RAGRS, GZRS or RAGZRS. | `string` | `"ZRS"` | no |
| `access_tier` | Hot or Cool. | `string` | `"Hot"` | no |
| `containers` | Names of private blob containers to create. | `list(string)` | `[]` | no |
| `versioning_enabled` | Enable blob versioning. | `bool` | `true` | no |
| `soft_delete_days` | Days to retain deleted blobs and containers. | `number` | `7` | no |
| `public_network_access_enabled` | Allow access from public networks. | `bool` | `true` | no |
| `tags` | Tags applied to all resources. | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| `storage_account_id` | ID of the storage account. |
| `storage_account_name` | Name of the storage account. |
| `primary_blob_endpoint` | Primary blob endpoint URL. |
| `container_ids` | Map of container name => ID. |
