resource "google_compute_network" "this" {
  project                 = var.project_id
  name                    = var.name
  auto_create_subnetworks = false
  routing_mode            = "REGIONAL"
}

resource "google_compute_subnetwork" "this" {
  for_each = var.subnets

  project                  = var.project_id
  name                     = each.key
  region                   = var.region
  network                  = google_compute_network.this.id
  ip_cidr_range            = each.value.cidr
  private_ip_google_access = true

  dynamic "secondary_ip_range" {
    for_each = each.value.secondary_ranges
    content {
      range_name    = secondary_ip_range.key
      ip_cidr_range = secondary_ip_range.value
    }
  }

  dynamic "log_config" {
    for_each = each.value.flow_logs ? [1] : []
    content {
      aggregation_interval = "INTERVAL_5_MIN"
      flow_sampling        = 0.5
      metadata             = "INCLUDE_ALL_METADATA"
    }
  }
}

resource "google_compute_router" "this" {
  count = var.enable_nat ? 1 : 0

  project = var.project_id
  name    = "${var.name}-router"
  region  = var.region
  network = google_compute_network.this.id
}

resource "google_compute_router_nat" "this" {
  count = var.enable_nat ? 1 : 0

  project                            = var.project_id
  name                               = "${var.name}-nat"
  router                             = google_compute_router.this[0].name
  region                             = var.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"

  log_config {
    enable = true
    filter = "ERRORS_ONLY"
  }
}

resource "google_compute_firewall" "allow_internal" {
  project = var.project_id
  name    = "${var.name}-allow-internal"
  network = google_compute_network.this.id

  allow {
    protocol = "tcp"
  }

  allow {
    protocol = "udp"
  }

  allow {
    protocol = "icmp"
  }

  source_ranges = [for s in var.subnets : s.cidr]
}

resource "google_compute_firewall" "allow_iap_ssh" {
  project = var.project_id
  name    = "${var.name}-allow-iap-ssh"
  network = google_compute_network.this.id

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  # Google Identity-Aware Proxy range for SSH without public IPs.
  source_ranges = ["35.235.240.0/20"]
}

resource "google_compute_global_address" "private_services" {
  count = var.enable_private_service_access ? 1 : 0

  project       = var.project_id
  name          = "${var.name}-private-services"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = var.private_service_access_prefix_length
  network       = google_compute_network.this.id
}

resource "google_service_networking_connection" "this" {
  count = var.enable_private_service_access ? 1 : 0

  network                 = google_compute_network.this.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_services[0].name]
}
