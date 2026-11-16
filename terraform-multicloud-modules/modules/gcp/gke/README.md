# GCP GKE Cluster

VPC-native GKE cluster with private nodes, workload identity, release channel and an autoscaling node pool on a least-privilege service account.

## Usage

```hcl
module "gke" {
  source = "github.com/chalampaladugu/terraform-multicloud-modules//modules/gcp/gke?ref=v1.0.0"

  # required inputs - see table below
}
```

See [`examples/gcp`](../../../examples/gcp) for a complete, working stack.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| `project_id` | GCP project ID. | `string` |  | yes |
| `name` | Cluster name. | `string` |  | yes |
| `location` | Region (regional cluster) or zone (zonal cluster). | `string` |  | yes |
| `network` | VPC network self link or ID. | `string` |  | yes |
| `subnetwork` | Subnetwork self link or ID. | `string` |  | yes |
| `pods_range_name` | Secondary range name for pods. | `string` | `"pods"` | no |
| `services_range_name` | Secondary range name for services. | `string` | `"services"` | no |
| `release_channel` | RAPID, REGULAR or STABLE. | `string` | `"REGULAR"` | no |
| `enable_private_nodes` | Nodes get internal IPs only. | `bool` | `true` | no |
| `master_ipv4_cidr_block` | /28 range for the control plane when private nodes are enabled. | `string` | `"172.16.0.0/28"` | no |
| `master_authorized_networks` | CIDRs allowed to reach the control plane. Empty = no restriction. | `list(object({cidr_block = string, display_name = string}))` | `[]` | no |
| `machine_type` | Node machine type. | `string` | `"e2-standard-4"` | no |
| `min_node_count` | Minimum nodes per zone. | `number` | `1` | no |
| `max_node_count` | Maximum nodes per zone. | `number` | `3` | no |
| `disk_size_gb` | Node disk size in GB. | `number` | `50` | no |
| `spot` | Use Spot VMs for the node pool. | `bool` | `false` | no |
| `deletion_protection` | Prevent terraform destroy from deleting the cluster. | `bool` | `true` | no |
| `labels` | Resource labels. | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| `cluster_id` | ID of the GKE cluster. |
| `cluster_name` | Name of the GKE cluster. |
| `endpoint` | Control plane endpoint. |
| `ca_certificate` | Base64 cluster CA certificate. |
| `node_service_account` | Service account used by nodes. |
