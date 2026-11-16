terraform {
  required_version = ">= 1.5.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 4.9, < 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.5"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}

locals {
  name = "${var.project}-${var.environment}"
  tags = {
    Project     = var.project
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "azurerm_resource_group" "this" {
  name     = "rg-${local.name}"
  location = var.location
  tags     = local.tags
}

module "vnet" {
  source = "../../modules/azure/vnet"

  name                = "vnet-${local.name}"
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
  address_space       = ["10.10.0.0/16"]

  subnets = {
    "snet-app" = {
      address_prefixes  = ["10.10.0.0/24"]
      service_endpoints = ["Microsoft.Storage"]
    }
    "snet-aks" = {
      address_prefixes = ["10.10.16.0/20"]
    }
    "snet-db" = {
      address_prefixes = ["10.10.2.0/24"]
      delegation       = "Microsoft.DBforPostgreSQL/flexibleServers"
    }
  }

  tags = local.tags
}

module "app_vm" {
  source = "../../modules/azure/vm"

  name                = "vm-${local.name}-app"
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
  subnet_id           = module.vnet.subnet_ids["snet-app"]
  ssh_public_key      = var.ssh_public_key
  tags                = local.tags
}

module "aks" {
  source = "../../modules/azure/aks"

  name                = "aks-${local.name}"
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
  vnet_subnet_id      = module.vnet.subnet_ids["snet-aks"]
  tags                = local.tags
}

module "storage" {
  source = "../../modules/azure/storage"

  name                = "st${var.project}${var.environment}${var.storage_suffix}"
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
  containers          = ["assets", "backups"]
  tags                = local.tags
}

module "postgres" {
  source = "../../modules/azure/postgresql"

  name                = "psql-${local.name}-${var.storage_suffix}"
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
  sku_name            = "B_Standard_B1ms"
  delegated_subnet_id = module.vnet.subnet_ids["snet-db"]
  virtual_network_id  = module.vnet.vnet_id
  tags                = local.tags
}
