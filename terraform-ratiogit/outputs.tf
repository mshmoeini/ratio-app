output "vm_external_ip" {
  value = google_compute_instance.ratio_vm_v4.network_interface[0].access_config[0].nat_ip
}

output "sql_instance_connection_name" {
  value = google_sql_database_instance.ratio_db_instance.connection_name
}
output "bucket_name" {
  description = "The name of the created bucket"
  value       = google_storage_bucket.ratio_bucket.name
}
