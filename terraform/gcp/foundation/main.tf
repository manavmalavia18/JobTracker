terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

resource "google_artifact_registry_repository" "api" {
  repository_id = var.project_name
  location      = var.gcp_region
  format        = "DOCKER"

  labels = {
    project = var.project_name
  }

  lifecycle {
    prevent_destroy = true
  }
}
