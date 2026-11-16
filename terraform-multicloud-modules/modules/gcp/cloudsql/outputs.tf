output "instance_name" {
  description = "Name of the Cloud SQL instance."
  value       = google_sql_database_instance.this.name
}

output "connection_name" {
  description = "Connection name (project:region:instance) for the Cloud SQL Auth Proxy."
  value       = google_sql_database_instance.this.connection_name
}

output "private_ip" {
  description = "Private IP address."
  value       = google_sql_database_instance.this.private_ip_address
}

output "user_name" {
  description = "Application user name."
  value       = google_sql_user.app.name
}

output "user_password" {
  description = "Generated password. Move it to Secret Manager for production."
  value       = random_password.user.result
  sensitive   = true
}
