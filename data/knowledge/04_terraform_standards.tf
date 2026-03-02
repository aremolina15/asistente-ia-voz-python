terraform {
  required_version = ">= 1.6"

  backend "gcs" {
    bucket  = "bdb-gcp-tf-states"
    prefix  = "devops-assistant"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_service_account" "assistant_sa" {
  account_id   = "sa-devops-assistant"
  display_name = "DevOps Assistant SA"
}

resource "google_cloud_run_service" "assistant" {
  name     = "devops-assistant"
  location = var.region

  template {
    spec {
      service_account_name = google_service_account.assistant_sa.email
      containers {
        image = var.image
      }
    }
  }
}