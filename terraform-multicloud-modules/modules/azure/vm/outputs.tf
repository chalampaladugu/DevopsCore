output "vm_id" {
  description = "ID of the virtual machine."
  value       = azurerm_linux_virtual_machine.this.id
}

output "private_ip" {
  description = "Private IP address."
  value       = azurerm_network_interface.this.private_ip_address
}

output "public_ip" {
  description = "Public IP address (if created)."
  value       = try(azurerm_public_ip.this[0].ip_address, null)
}

output "principal_id" {
  description = "Principal ID of the VM's managed identity."
  value       = azurerm_linux_virtual_machine.this.identity[0].principal_id
}
