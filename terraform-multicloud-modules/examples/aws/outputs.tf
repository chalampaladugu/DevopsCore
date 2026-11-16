output "vpc_id" {
  value = module.vpc.vpc_id
}

output "eks_cluster_name" {
  value = module.eks.cluster_name
}

output "rds_endpoint" {
  value = module.database.endpoint
}

output "s3_bucket" {
  value = module.assets.bucket_id
}
