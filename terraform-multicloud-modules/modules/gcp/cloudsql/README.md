# GCP Cloud SQL PostgreSQL

Private-IP Cloud SQL PostgreSQL with SSL enforced, backups + PITR, Query Insights, databases and a generated app user.

## Usage

```hcl
module "cloudsql" {
  source = "github.com/chalampaladugu/terraform-multicloud-modules//modules/gcp/cloudsql?ref=v1.0.0"

  # required inputs - see table below
}
```

See [`examples/gcp`](../../../examples/gcp) for a complete, working stack.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| `project_id` | GCP project ID. | `string` |  | yes |
| `name` | Instance name. | `string` |  | yes |
| `region` | Region. | `string` |  | yes |
| `database_version` | Database version. | `string` | `"POSTGRES_16"` | no |
| `tier` | Machine tier, e.g. db-custom-2-7680. | `string` | `"db-custom-2-7680"` | no |
| `disk_size_gb` | Initial disk size in GB (auto-grows). | `number` | `20` | no |
| `private_network` | VPC self link for private IP. The VPC must have private service access. | `string` |  | yes |
| `high_availability` | Use REGIONAL availability (standby in another zone). | `bool` | `false` | no |
| `databases` | Names of databases to create. | `list(string)` | `["app"]` | no |
| `user_name` | Application user name (password is generated). | `string` | `"app"` | no |
| `deletion_protection` | Prevent accidental deletion. | `bool` | `true` | no |
| `labels` | User labels. | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| `instance_name` | Name of the Cloud SQL instance. |
| `connection_name` | Connection name (project:region:instance) for the Cloud SQL Auth Proxy. |
| `private_ip` | Private IP address. |
| `user_name` | Application user name. |
| `user_password` | Generated password. Move it to Secret Manager for production. |
