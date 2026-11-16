output "instance_id" {
  description = "ID of the instance."
  value       = google_compute_instance.this.id
}

output "private_ip" {
  description = "Internal IP address."
  value       = google_compute_instance.this.network_interface[0].network_ip
}

output "public_ip" {
  description = "External IP address (if assigned)."
  value       = try(google_compute_instance.this.network_interface[0].access_config[0].nat_ip, null)
}

output "service_account_email" {
  description = "Service account attached to the instance."
  value       = google_service_account.this.email
}
