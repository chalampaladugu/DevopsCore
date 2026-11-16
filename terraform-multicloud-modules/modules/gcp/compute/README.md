# GCP Compute Instance

Compute Engine VM with a dedicated service account, Shielded VM, OS Login and an optional external IP.

## Usage

```hcl
module "compute" {
  source = "github.com/chalampaladugu/terraform-multicloud-modules//modules/gcp/compute?ref=v1.0.0"

  # required inputs - see table below
}
```

See [`examples/gcp`](../../../examples/gcp) for a complete, working stack.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| `project_id` | GCP project ID. | `string` |  | yes |
| `name` | Instance name. | `string` |  | yes |
| `zone` | Zone, e.g. us-central1-a. | `string` |  | yes |
| `machine_type` | Machine type. | `string` | `"e2-standard-2"` | no |
| `subnetwork` | Subnetwork self link or ID. | `string` |  | yes |
| `image` | Boot image. | `string` | `"debian-cloud/debian-12"` | no |
| `boot_disk_size_gb` | Boot disk size in GB. | `number` | `30` | no |
| `boot_disk_type` | pd-balanced, pd-ssd or pd-standard. | `string` | `"pd-balanced"` | no |
| `assign_public_ip` | Attach an ephemeral external IP. | `bool` | `false` | no |
| `network_tags` | Network tags (used by firewall rules). | `list(string)` | `[]` | no |
| `startup_script` | Optional startup script. | `string` | `None` | no |
| `labels` | Labels applied to the instance. | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| `instance_id` | ID of the instance. |
| `private_ip` | Internal IP address. |
| `public_ip` | External IP address (if assigned). |
| `service_account_email` | Service account attached to the instance. |
