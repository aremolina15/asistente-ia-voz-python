variable "github_repo" { type = string } # "org/repo"
variable "github_owner" { type = string } # "org"

resource "google_iam_workload_identity_pool" "gh_pool" {
  project                   = var.project_id
  workload_identity_pool_id = "gh-pool-${var.environment}"
  display_name              = "GitHub OIDC Pool (${var.environment})"
}

resource "google_iam_workload_identity_pool_provider" "gh_provider" {
  project                            = var.project_id
  workload_identity_pool_id          = google_iam_workload_identity_pool.gh_pool.workload_identity_pool_id
  workload_identity_pool_provider_id = "gh-provider-${var.environment}"
  display_name                       = "GitHub OIDC Provider (${var.environment})"

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }

  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.repository" = "assertion.repository"
    "attribute.actor"      = "assertion.actor"
    "attribute.ref"        = "assertion.ref"
  }

  # Recomendado: restringir por repositorio
  attribute_condition = "attribute.repository == \"${var.github_repo}\""
}

# Permitir que identidades de GitHub "impersonen" la SA
resource "google_service_account_iam_member" "wif_impersonation" {
  service_account_id = google_service_account.devops_assistant.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.gh_pool.name}/attribute.repository/${var.github_repo}"
}