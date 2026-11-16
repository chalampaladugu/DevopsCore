# Azure AKS Cluster

AKS with Azure CNI overlay, network policy, OIDC + workload identity, autoscaling system pool and optional Container Insights.

## Usage

```hcl
module "aks" {
  source = "github.com/chalampaladugu/terraform-multicloud-modules//modules/azure/aks?ref=v1.0.0"

  # required inputs - see table below
}
```

See [`examples/azure`](../../../examples/azure) for a complete, working stack.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| `name` | AKS cluster name. | `string` |  | yes |
| `resource_group_name` | Resource group to deploy into. | `string` |  | yes |
| `location` | Azure region. | `string` |  | yes |
| `kubernetes_version` | Kubernetes version. Leave null for the current AKS default. | `string` | `None` | no |
| `sku_tier` | Free, Standard (uptime SLA) or Premium. | `string` | `"Free"` | no |
| `vnet_subnet_id` | Subnet for nodes and pods (Azure CNI overlay). | `string` |  | yes |
| `node_vm_size` | VM size for the system node pool. | `string` | `"Standard_D4s_v5"` | no |
| `node_count` | Node count when autoscaling is disabled. | `number` | `2` | no |
| `enable_auto_scaling` | Enable the cluster autoscaler on the default pool. | `bool` | `true` | no |
| `min_count` | Minimum nodes when autoscaling. | `number` | `1` | no |
| `max_count` | Maximum nodes when autoscaling. | `number` | `4` | no |
| `zones` | Availability zones for the default pool. | `list(string)` | `None` | no |
| `service_cidr` | Kubernetes service CIDR (must not overlap the VNet). | `string` | `"172.16.0.0/16"` | no |
| `dns_service_ip` | Cluster DNS IP inside service_cidr. | `string` | `"172.16.0.10"` | no |
| `pod_cidr` | Pod CIDR for Azure CNI overlay. | `string` | `"192.168.0.0/16"` | no |
| `log_analytics_workspace_id` | Optional Log Analytics workspace for Container Insights. | `string` | `None` | no |
| `tags` | Tags applied to all resources. | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| `cluster_id` | ID of the AKS cluster. |
| `cluster_name` | Name of the AKS cluster. |
| `kube_config_raw` | Raw kubeconfig for the cluster. |
| `oidc_issuer_url` | OIDC issuer URL (for workload identity). |
| `kubelet_identity_object_id` | Object ID of the kubelet identity (grant ACR pull to this). |
| `node_resource_group` | Resource group holding the node resources. |
