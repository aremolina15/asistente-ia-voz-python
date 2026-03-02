# Gestión correcta de Service Accounts en GCP con Terraform (sin pasos manuales)

Este estándar reemplaza el enfoque manual (“crear SA en consola”, “descargar JSON”) por un flujo **100% reproducible** con **Terraform** y **credenciales sin llaves** (Workload Identity Federation).  
El objetivo es cumplir **mínimo privilegio**, trazabilidad y evitar fuga de secretos.

---

## Principios (2026)

- **No manual:** nada de crear cuentas/roles a mano en consola.
- **Sin llaves JSON estáticas:** evitar `service account keys` (alto riesgo).
- **Identidad federada:** usar **Workload Identity Federation (WIF)** para GitHub Actions / CI/CD.
- **Mínimo privilegio:** roles por función, con alcance mínimo (proyecto/dataset/repositorio).
- **Auditable:** todo queda en Git (PR + code review) y en Terraform state.

---

## Flujo recomendado (Terraform + WIF)

### 1) Crear Service Account con Terraform
- Se define una SA por entorno (qa/st/prod) y por servicio (ej. `devops-assistant`).
- La SA se crea con Terraform, con naming estándar.

### 2) Otorgar roles mínimos necesarios con Terraform
- Asignar **solo** los permisos requeridos (evitar `Owner`, `Editor`, `Service Account Admin`).
- Preferir roles específicos (y si es necesario, **custom roles**).

### 3) Autenticación sin JSON (GitHub Actions → GCP)
- Configurar **Workload Identity Pool + Provider** con Terraform.
- Permitir “impersonation” a la SA desde GitHub OIDC, sin llaves.

---

## Ejemplo Terraform (Service Account + IAM mínimo)

> Ajusta roles a tu caso real. Este ejemplo es intencionalmente conservador.

```hcl
# variables.tf
variable "project_id" { type = string }
variable "environment" { type = string } # qa|st|prod

locals {
  sa_name = "sa-${var.environment}-devops-assistant"
}

resource "google_service_account" "devops_assistant" {
  project      = var.project_id
  account_id   = local.sa_name
  display_name = "DevOps Assistant (${var.environment})"
  description  = "SA para el asistente DevOps inteligente"
}

# Roles mínimos ejemplo (ajústalos)
resource "google_project_iam_member" "logging_writer" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.devops_assistant.email}"
}

resource "google_project_iam_member" "monitoring_writer" {
  project = var.project_id
  role    = "roles/monitoring.metricWriter"
  member  = "serviceAccount:${google_service_account.devops_assistant.email}"
}

# Si el asistente usa Secret Manager para leer secretos (NO para keys)
resource "google_project_iam_member" "secret_accessor" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.devops_assistant.email}"
}