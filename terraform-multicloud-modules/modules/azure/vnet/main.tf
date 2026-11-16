locals {
  delegation_actions = {
    "Microsoft.DBforPostgreSQL/flexibleServers"   = ["Microsoft.Network/virtualNetworks/subnets/join/action"]
    "Microsoft.Web/serverFarms"                   = ["Microsoft.Network/virtualNetworks/subnets/action"]
    "Microsoft.ContainerInstance/containerGroups" = ["Microsoft.Network/virtualNetworks/subnets/action"]
  }

  nsg_subnets = var.create_nsg ? { for k, v in var.subnets : k => v if v.delegation == null } : {}
}

resource "azurerm_virtual_network" "this" {
  name                = var.name
  resource_group_name = var.resource_group_name
  location            = var.location
  address_space       = var.address_space
  tags                = var.tags
}

resource "azurerm_subnet" "this" {
  for_each = var.subnets

  name                 = each.key
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.this.name
  address_prefixes     = each.value.address_prefixes
  service_endpoints    = each.value.service_endpoints

  dynamic "delegation" {
    for_each = each.value.delegation == null ? [] : [each.value.delegation]
    content {
      name = "delegation"
      service_delegation {
        name    = delegation.value
        actions = lookup(local.delegation_actions, delegation.value, ["Microsoft.Network/virtualNetworks/subnets/action"])
      }
    }
  }
}

resource "azurerm_network_security_group" "this" {
  count = var.create_nsg ? 1 : 0

  name                = "${var.name}-nsg"
  resource_group_name = var.resource_group_name
  location            = var.location
  tags                = var.tags
}

resource "azurerm_subnet_network_security_group_association" "this" {
  for_each = local.nsg_subnets

  subnet_id                 = azurerm_subnet.this[each.key].id
  network_security_group_id = azurerm_network_security_group.this[0].id
}
