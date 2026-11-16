# GCP Cloud Storage Bucket

Bucket with uniform access, public access prevention, versioning, optional CMEK and lifecycle rules.

## Usage

```hcl
module "gcs" {
  source = "github.com/chalampaladugu/terraform-multicloud-modules//modules/gcp/gcs?ref=v1.0.0"

  # required inputs - see table below
}
```

See [`examples/gcp`](../../../examples/gcp) for a complete, working stack.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| `project_id` | GCP project ID. | `string` |  | yes |
| `name` | Globally unique bucket name. | `string` |  | yes |
| `location` | Region (e.g. us-central1) or multi-region (e.g. US). | `string` |  | yes |
| `storage_class` | STANDARD, NEARLINE, COLDLINE or ARCHIVE. | `string` | `"STANDARD"` | no |
| `versioning_enabled` | Enable object versioning. | `bool` | `true` | no |
| `nearline_after_days` | Days before moving objects to NEARLINE. Set 0 to disable. | `number` | `30` | no |
| `noncurrent_version_expiration_days` | Days before deleting old versions. Set 0 to disable. | `number` | `90` | no |
| `kms_key_name` | Optional Cloud KMS key for default encryption. | `string` | `None` | no |
| `force_destroy` | Allow deleting a non-empty bucket. | `bool` | `false` | no |
| `labels` | Labels applied to the bucket. | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_name` | Name of the bucket. |
| `bucket_url` | gs:// URL of the bucket. |
| `bucket_self_link` | Self link of the bucket. |
