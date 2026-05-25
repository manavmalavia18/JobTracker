output "cluster_name" {
  value = var.project_name
}

output "ecr_repository_url" {
  value = module.ecr.repository_url
}
