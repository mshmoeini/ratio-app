resource "google_storage_bucket" "ratio_bucket" {
  name          = "ratio-app-storage-bucket"
  location      = var.region
  force_destroy = true

  uniform_bucket_level_access = true

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30
    }
  }
}
