output "endpoint" {
  description = "Connection endpoint (host:port)."
  value       = aws_db_instance.this.endpoint
}

output "address" {
  description = "Hostname of the database."
  value       = aws_db_instance.this.address
}

output "port" {
  description = "Database port."
  value       = aws_db_instance.this.port
}

output "master_user_secret_arn" {
  description = "Secrets Manager ARN holding the master password."
  value       = try(aws_db_instance.this.master_user_secret[0].secret_arn, null)
}

output "security_group_id" {
  description = "Database security group ID."
  value       = aws_security_group.this.id
}
