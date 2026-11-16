output "server_id" {
  description = "ID of the PostgreSQL server."
  value       = azurerm_postgresql_flexible_server.this.id
}

output "fqdn" {
  description = "Server hostname."
  value       = azurerm_postgresql_flexible_server.this.fqdn
}

output "administrator_login" {
  description = "Admin username."
  value       = azurerm_postgresql_flexible_server.this.administrator_login
}

output "administrator_password" {
  description = "Generated admin password. Move it to Key Vault for production."
  value       = random_password.admin.result
  sensitive   = true
}
