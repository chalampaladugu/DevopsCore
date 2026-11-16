resource "azurerm_kubernetes_cluster" "this" {
  name                = var.name
  resource_group_name = var.resource_group_name
  location            = var.location
  dns_prefix          = var.name
  kubernetes_version  = var.kubernetes_version
  sku_tier            = var.sku_tier

  oidc_issuer_enabled       = true
  workload_identity_enabled = true

  default_node_pool {
    name                        = "system"
    vm_size                     = var.node_vm_size
    vnet_subnet_id              = var.vnet_subnet_id
    zones                       = var.zones
    auto_scaling_enabled        = var.enable_auto_scaling
    node_count                  = var.enable_auto_scaling ? null : var.node_count
    min_count                   = var.enable_auto_scaling ? var.min_count : null
    max_count                   = var.enable_auto_scaling ? var.max_count : null
    os_disk_type                = "Managed"
    temporary_name_for_rotation = "systemtmp"

    upgrade_settings {
      max_surge = "33%"
    }
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin      = "azure"
    network_plugin_mode = "overlay"
    network_policy      = "calico"
    service_cidr        = var.service_cidr
    dns_service_ip      = var.dns_service_ip
    pod_cidr            = var.pod_cidr
    load_balancer_sku   = "standard"
  }

  dynamic "oms_agent" {
    for_each = var.log_analytics_workspace_id == null ? [] : [1]
    content {
      log_analytics_workspace_id = var.log_analytics_workspace_id
    }
  }

  tags = var.tags

  lifecycle {
    ignore_changes = [default_node_pool[0].node_count]
  }
}
