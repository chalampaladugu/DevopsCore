# Azure Linux VM

Linux VM (Ubuntu 24.04 by default) with SSH-key auth, managed identity, boot diagnostics and an optional public IP.

## Usage

```hcl
module "vm" {
  source = "github.com/chalampaladugu/terraform-multicloud-modules//modules/azure/vm?ref=v1.0.0"

  # required inputs - see table below
}
```

See [`examples/azure`](../../../examples/azure) for a complete, working stack.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| `name` | Name of the virtual machine. | `string` |  | yes |
| `resource_group_name` | Resource group to deploy into. | `string` |  | yes |
| `location` | Azure region. | `string` |  | yes |
| `subnet_id` | Subnet for the VM network interface. | `string` |  | yes |
| `size` | VM size. | `string` | `"Standard_D2s_v5"` | no |
| `admin_username` | Admin username. | `string` | `"azureuser"` | no |
| `ssh_public_key` | SSH public key for the admin user. | `string` |  | yes |
| `os_disk_size_gb` | OS disk size in GB. | `number` | `30` | no |
| `os_disk_type` | OS disk storage type. | `string` | `"Premium_LRS"` | no |
| `image` | Marketplace image reference. | `object({publisher = string, offer = string, sku = string, version = string})` | _see variables.tf_ | no |
| `create_public_ip` | Attach a static public IP. | `bool` | `false` | no |
| `zone` | Availability zone (\"1\", \"2\", \"3\") or null. | `string` | `None` | no |
| `custom_data` | Optional cloud-init content (plain text; encoded by the module). | `string` | `None` | no |
| `tags` | Tags applied to all resources. | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| `vm_id` | ID of the virtual machine. |
| `private_ip` | Private IP address. |
| `public_ip` | Public IP address (if created). |
| `principal_id` | Principal ID of the VM's managed identity. |
