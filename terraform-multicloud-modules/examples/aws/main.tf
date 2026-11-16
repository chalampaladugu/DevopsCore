terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.40, < 7.0"
    }
  }
}

provider "aws" {
  region = var.region
}

locals {
  name = "${var.project}-${var.environment}"
  tags = {
    Project     = var.project
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

data "aws_availability_zones" "available" {
  state = "available"
}

module "vpc" {
  source = "../../modules/aws/vpc"

  name                 = local.name
  cidr_block           = "10.0.0.0/16"
  azs                  = slice(data.aws_availability_zones.available.names, 0, 2)
  public_subnet_cidrs  = ["10.0.0.0/20", "10.0.16.0/20"]
  private_subnet_cidrs = ["10.0.32.0/19", "10.0.64.0/19"]
  single_nat_gateway   = true
  tags                 = local.tags
}

module "app_server" {
  source = "../../modules/aws/ec2"

  name          = "${local.name}-app"
  vpc_id        = module.vpc.vpc_id
  subnet_id     = module.vpc.private_subnet_ids[0]
  instance_type = "t3.medium"
  tags          = local.tags
}

module "eks" {
  source = "../../modules/aws/eks"

  name                = "${local.name}-eks"
  subnet_ids          = module.vpc.private_subnet_ids
  node_instance_types = ["t3.large"]
  node_desired_size   = 2
  tags                = local.tags
}

module "assets" {
  source = "../../modules/aws/s3"

  bucket_name = "${local.name}-assets-${var.bucket_suffix}"
  tags        = local.tags
}

module "database" {
  source = "../../modules/aws/rds"

  name                       = "${local.name}-pg"
  vpc_id                     = module.vpc.vpc_id
  subnet_ids                 = module.vpc.private_subnet_ids
  allowed_security_group_ids = [module.app_server.security_group_id, module.eks.cluster_security_group_id]
  deletion_protection        = false
  skip_final_snapshot        = true
  tags                       = local.tags
}
