provider "google" {
  project     = "YOUR_PROJECT_ID"
  region      = "us-central1"
  zone        = "us-central1-a"
  credentials = file("./msh-cloud-project-0d1258394118.json")
}

# VM جدید
resource "google_compute_instance" "ratio_vm_v4" {
  name         = "ratio-v4-vm"
  machine_type = "e2-medium"
  zone         = "us-central1-a"

  tags = ["http-server"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network       = "default"
    access_config {}
  }

  metadata_startup_script = <<-EOT
    #!/bin/bash
    sudo apt update
    sudo apt install -y docker.io git
    sudo systemctl start docker
    sudo systemctl enable docker
  EOT
}

# فایروال برای باز کردن پورت 8081
resource "google_compute_firewall" "allow-8081" {
  name    = "allow-8081"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["8081"]
  }

  direction     = "INGRESS"
  priority      = 1000
  target_tags   = ["http-server"]
  source_ranges = ["0.0.0.0/0"]
}
