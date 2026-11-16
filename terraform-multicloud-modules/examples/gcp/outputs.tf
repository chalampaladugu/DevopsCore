output "network" {
  value = module.vpc.network_name
}

output "gke_cluster_name" {
  value = module.gke.cluster_name
}

output "cloudsql_connection_name" {
  value = module.cloudsql.connection_name
}

output "bucket" {
  value = module.assets.bucket_url
}
