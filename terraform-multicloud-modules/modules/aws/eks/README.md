# AWS EKS Cluster

EKS cluster with IAM roles, control-plane logging, access entries (API auth) and an autoscaling managed node group.

## Usage

```hcl
module "eks" {
  source = "github.com/chalampaladugu/terraform-multicloud-modules//modules/aws/eks?ref=v1.0.0"

  # required inputs - see table below
}
```

See [`examples/aws`](../../../examples/aws) for a complete, working stack.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| `name` | EKS cluster name. | `string` |  | yes |
| `kubernetes_version` | Kubernetes version. Leave null for the current AWS default. | `string` | `None` | no |
| `subnet_ids` | Private subnet IDs for the control plane ENIs and worker nodes. | `list(string)` |  | yes |
| `endpoint_public_access` | Expose the Kubernetes API publicly. | `bool` | `true` | no |
| `public_access_cidrs` | CIDRs allowed to reach the public API endpoint. | `list(string)` | `["0.0.0.0/0"]` | no |
| `node_instance_types` | Instance types for the managed node group. | `list(string)` | `["t3.large"]` | no |
| `node_capacity_type` | ON_DEMAND or SPOT. | `string` | `"ON_DEMAND"` | no |
| `node_min_size` | Minimum number of nodes. | `number` | `1` | no |
| `node_desired_size` | Desired number of nodes. | `number` | `2` | no |
| `node_max_size` | Maximum number of nodes. | `number` | `4` | no |
| `node_disk_size` | Node disk size in GiB. | `number` | `50` | no |
| `tags` | Tags applied to all resources. | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| `cluster_name` | Name of the EKS cluster. |
| `cluster_endpoint` | Kubernetes API endpoint. |
| `cluster_certificate_authority_data` | Base64 cluster CA certificate. |
| `cluster_security_group_id` | Cluster security group created by EKS. |
| `oidc_issuer_url` | OIDC issuer URL (for IRSA). |
| `node_role_arn` | IAM role ARN used by worker nodes. |
