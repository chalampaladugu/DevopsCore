resource "google_storage_bucket" "this" {
  project       = var.project_id
  name          = var.name
  location      = var.location
  storage_class = var.storage_class
  force_destroy = var.force_destroy
  labels        = var.labels

  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"

  versioning {
    enabled = var.versioning_enabled
  }

  dynamic "encryption" {
    for_each = var.kms_key_name == null ? [] : [1]
    content {
      default_kms_key_name = var.kms_key_name
    }
  }

  dynamic "lifecycle_rule" {
    for_each = var.nearline_after_days > 0 ? [1] : []
    content {
      condition {
        age = var.nearline_after_days
      }
      action {
        type          = "SetStorageClass"
        storage_class = "NEARLINE"
      }
    }
  }

  dynamic "lifecycle_rule" {
    for_each = var.noncurrent_version_expiration_days > 0 ? [1] : []
    content {
      condition {
        days_since_noncurrent_time = var.noncurrent_version_expiration_days
        with_state                 = "ARCHIVED"
      }
      action {
        type = "Delete"
      }
    }
  }
}
