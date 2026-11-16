# AWS RDS PostgreSQL

Private RDS PostgreSQL with gp3 storage autoscaling, encryption, backups, Performance Insights and the master password managed in Secrets Manager.

## Usage

```hcl
module "rds" {
  source = "github.com/chalampaladugu/terraform-multicloud-modules//modules/aws/rds?ref=v1.0.0"

  # required inputs - see table below
}
```

See [`examples/aws`](../../../examples/aws) for a complete, working stack.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| `name` | Identifier for the database instance. | `string` |  | yes |
| `vpc_id` | VPC for the database security group. | `string` |  | yes |
| `subnet_ids` | Private subnet IDs (at least two AZs). | `list(string)` |  | yes |
| `allowed_cidr_blocks` | CIDRs allowed to connect on the database port. | `list(string)` | `[]` | no |
| `allowed_security_group_ids` | Security groups allowed to connect on the database port. | `list(string)` | `[]` | no |
| `engine_version` | PostgreSQL major version. | `string` | `"16"` | no |
| `instance_class` | RDS instance class. | `string` | `"db.t4g.medium"` | no |
| `allocated_storage` | Initial storage in GiB. | `number` | `20` | no |
| `max_allocated_storage` | Storage autoscaling ceiling in GiB. | `number` | `100` | no |
| `db_name` | Name of the initial database. | `string` | `"app"` | no |
| `username` | Master username. The password is generated and stored in Secrets Manager. | `string` | `"dbadmin"` | no |
| `multi_az` | Deploy a standby in another AZ. | `bool` | `false` | no |
| `backup_retention_days` | Days to keep automated backups. | `number` | `7` | no |
| `deletion_protection` | Prevent accidental deletion. | `bool` | `true` | no |
| `skip_final_snapshot` | Skip the final snapshot on destroy. | `bool` | `false` | no |
| `tags` | Tags applied to all resources. | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| `endpoint` | Connection endpoint (host:port). |
| `address` | Hostname of the database. |
| `port` | Database port. |
| `master_user_secret_arn` | Secrets Manager ARN holding the master password. |
| `security_group_id` | Database security group ID. |
