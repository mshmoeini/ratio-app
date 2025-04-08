resource "google_sql_database_instance" "ratio_db_instance" {
  name             = "ratio-sql-instance-terraform"
  region           = var.region
  database_version = "POSTGRES_14"

  settings {
    tier = "db-f1-micro"
    ip_configuration {
      ipv4_enabled    = true
      authorized_networks {
        name  = "allow-all"
        value = "0.0.0.0/0"
      }
    }
  }
}

resource "google_sql_database" "ratio_db" {
  name     = "ratios"
  instance = google_sql_database_instance.ratio_db_instance.name
}

resource "google_sql_user" "app_user" {
  name     = "appuser"
  instance = google_sql_database_instance.ratio_db_instance.name
  password = "StrongPassword123"
}
