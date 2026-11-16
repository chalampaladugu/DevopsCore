terraform {
  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 6.0, < 8.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.5"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

locals {
  name = "${var.project}-${var.environment}"
  labels = {
    project     = var.project
    environment = var.environment
    managed-by  = "terraform"
  }
}

module "vpc" {
  source = "../../modules/gcp/vpc"

  project_id = var.project_id
  name       = "${local.name}-vpc"
  region     = var.region

  subnets = {
    "${local.name}-app" = {
      cidr = "10.20.0.0/20"
    }
    "${local.name}-gke" = {
      cidr = "10.20.16.0/20"
      secondary_ranges = {
        pods     = "10.100.0.0/16"
        services = "10.101.0.0/20"
      }
    }
  }
}

module "app_vm" {
  source = "../../modules/gcp/compute"

  project_id = var.project_id
  name       = "${local.name}-app"
  zone       = "${var.region}-a"
  subnetwork = module.vpc.subnet_self_links["${local.name}-app"]
  labels     = local.labels
}

module "gke" {
  source = "../../modules/gcp/gke"

  project_id          = var.project_id
  name                = "${local.name}-gke"
  location            = var.region
  network             = module.vpc.network_self_link
  subnetwork          = module.vpc.subnet_self_links["${local.name}-gke"]
  deletion_protection = false
  labels              = local.labels
}

module "assets" {
  source = "../../modules/gcp/gcs"

  project_id = var.project_id
  name       = "${local.name}-assets-${var.bucket_suffix}"
  location   = var.region
  labels     = local.labels
}

module "cloudsql" {
  source = "../../modules/gcp/cloudsql"

  project_id          = var.project_id
  name                = "${local.name}-pg"
  region              = var.region
  private_network     = module.vpc.network_self_link
  deletion_protection = false
  labels              = local.labels

  depends_on = [module.vpc]
}
