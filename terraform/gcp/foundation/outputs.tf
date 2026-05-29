output "artifact_registry_url" {
  value = "${var.gcp_region}-docker.pkg.dev/${var.gcp_project_id}/${var.project_name}"
}

output "api_image" {
  value = "${var.gcp_region}-docker.pkg.dev/${var.gcp_project_id}/${var.project_name}/${var.project_name}-api:latest"
}
