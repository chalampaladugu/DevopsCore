# AWS S3 Bucket

Private S3 bucket with versioning, encryption (SSE-S3 or KMS), public access blocked, bucket-owner-enforced ownership and lifecycle rules.

## Usage

```hcl
module "s3" {
  source = "github.com/chalampaladugu/terraform-multicloud-modules//modules/aws/s3?ref=v1.0.0"

  # required inputs - see table below
}
```

See [`examples/aws`](../../../examples/aws) for a complete, working stack.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| `bucket_name` | Globally unique bucket name. | `string` |  | yes |
| `versioning_enabled` | Enable object versioning. | `bool` | `true` | no |
| `kms_key_arn` | Optional KMS key ARN. Leave null for SSE-S3 (AES256). | `string` | `None` | no |
| `force_destroy` | Allow deleting the bucket even if it contains objects. | `bool` | `false` | no |
| `transition_to_ia_days` | Days before moving objects to STANDARD_IA. Set 0 to disable. | `number` | `30` | no |
| `noncurrent_version_expiration_days` | Days before deleting old object versions. Set 0 to disable. | `number` | `90` | no |
| `tags` | Tags applied to all resources. | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_id` | Name of the bucket. |
| `bucket_arn` | ARN of the bucket. |
| `bucket_regional_domain_name` | Regional domain name of the bucket. |
