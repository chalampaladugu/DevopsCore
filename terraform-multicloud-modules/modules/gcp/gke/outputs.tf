output "cluster_id" {
  description = "ID of the GKE cluster."
  value       = google_container_cluster.this.id
}

output "cluster_name" {
  description = "Name of the GKE cluster."
  value       = google_container_cluster.this.name
}

output "endpoint" {
  description = "Control plane endpoint."
  value       = google_container_cluster.this.endpoint
  sensitive   = true
}

output "ca_certificate" {
  description = "Base64 cluster CA certificate."
  value       = google_container_cluster.this.master_auth[0].cluster_ca_certificate
  sensitive   = true
}

output "node_service_account" {
  description = "Service account used by nodes."
  value       = google_service_account.nodes.email
}
