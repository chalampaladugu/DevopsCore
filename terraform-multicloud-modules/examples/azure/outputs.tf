output "resource_group" {
  value = azurerm_resource_group.this.name
}

output "aks_cluster_name" {
  value = module.aks.cluster_name
}

output "postgres_fqdn" {
  value = module.postgres.fqdn
}

output "storage_account" {
  value = module.storage.storage_account_name
}
