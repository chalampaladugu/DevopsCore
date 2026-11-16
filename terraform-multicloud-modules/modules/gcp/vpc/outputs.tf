output "network_id" {
  description = "ID of the VPC network."
  value       = google_compute_network.this.id
}

output "network_name" {
  description = "Name of the VPC network."
  value       = google_compute_network.this.name
}

output "network_self_link" {
  description = "Self link of the VPC network."
  value       = google_compute_network.this.self_link
}

output "subnet_ids" {
  description = "Map of subnet name => ID."
  value       = { for k, s in google_compute_subnetwork.this : k => s.id }
}

output "subnet_self_links" {
  description = "Map of subnet name => self link."
  value       = { for k, s in google_compute_subnetwork.this : k => s.self_link }
}

output "private_service_connection" {
  description = "Service networking connection (depend on this for Cloud SQL private IP)."
  value       = try(google_service_networking_connection.this[0].id, null)
}
