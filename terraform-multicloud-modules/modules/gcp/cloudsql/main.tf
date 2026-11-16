resource "random_password" "user" {
  length  = 24
  special = false
}

resource "google_sql_database_instance" "this" {
  project             = var.project_id
  name                = var.name
  region              = var.region
  database_version    = var.database_version
  deletion_protection = var.deletion_protection

  settings {
    tier              = var.tier
    edition           = "ENTERPRISE"
    availability_type = var.high_availability ? "REGIONAL" : "ZONAL"
    disk_type         = "PD_SSD"
    disk_size         = var.disk_size_gb
    disk_autoresize   = true
    user_labels       = var.labels

    ip_configuration {
      ipv4_enabled    = false
      private_network = var.private_network
      ssl_mode        = "ENCRYPTED_ONLY"
    }

    backup_configuration {
      enabled                        = true
      point_in_time_recovery_enabled = true
      start_time                     = "03:00"
    }

    maintenance_window {
      day  = 7
      hour = 4
    }

    insights_config {
      query_insights_enabled = true
    }
  }
}

resource "google_sql_database" "this" {
  for_each = toset(var.databases)

  project  = var.project_id
  name     = each.value
  instance = google_sql_database_instance.this.name
}

resource "google_sql_user" "app" {
  project  = var.project_id
  name     = var.user_name
  instance = google_sql_database_instance.this.name
  password = random_password.user.result
}
