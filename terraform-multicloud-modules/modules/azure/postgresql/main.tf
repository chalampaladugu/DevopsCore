locals {
  private = var.delegated_subnet_id != null
}

resource "random_password" "admin" {
  length           = 24
  special          = true
  override_special = "!#%*-_=+"
}

resource "azurerm_private_dns_zone" "this" {
  count = local.private ? 1 : 0

  name                = "${var.name}.private.postgres.database.azure.com"
  resource_group_name = var.resource_group_name
  tags                = var.tags
}

resource "azurerm_private_dns_zone_virtual_network_link" "this" {
  count = local.private ? 1 : 0

  name                  = "${var.name}-link"
  resource_group_name   = var.resource_group_name
  private_dns_zone_name = azurerm_private_dns_zone.this[0].name
  virtual_network_id    = var.virtual_network_id
  tags                  = var.tags
}

resource "azurerm_postgresql_flexible_server" "this" {
  name                = var.name
  resource_group_name = var.resource_group_name
  location            = var.location
  version             = var.postgres_version
  sku_name            = var.sku_name
  storage_mb          = var.storage_mb
  zone                = var.zone

  administrator_login    = var.administrator_login
  administrator_password = random_password.admin.result

  delegated_subnet_id           = var.delegated_subnet_id
  private_dns_zone_id           = try(azurerm_private_dns_zone.this[0].id, null)
  public_network_access_enabled = !local.private

  backup_retention_days = var.backup_retention_days

  dynamic "high_availability" {
    for_each = var.high_availability ? [1] : []
    content {
      mode = "ZoneRedundant"
    }
  }

  tags = var.tags

  lifecycle {
    ignore_changes = [zone, high_availability[0].standby_availability_zone]
  }

  depends_on = [azurerm_private_dns_zone_virtual_network_link.this]
}

resource "azurerm_postgresql_flexible_server_database" "this" {
  for_each = toset(var.databases)

  name      = each.value
  server_id = azurerm_postgresql_flexible_server.this.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}
