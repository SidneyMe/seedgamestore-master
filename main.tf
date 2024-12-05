provider "google" {
  project     = "booming-splicer-443411-u6"
  region      = "us-central1"
  credentials = var.credentials_json
}

variable "credentials_json" {
  type        = string
  description = "The contents of the service account JSON file"
  sensitive   = true
}

resource "google_sql_database_instance" "mysql_instance" {
  name             = "mysql-small-db"
  database_version = "MYSQL_8_0"
  region           = "us-central1"

  settings {
    tier = "db-f1-micro"
    ip_configuration {
      ipv4_enabled = true
    }
  }
}

resource "google_sql_database" "database" {
  name     = "sampledb"
  instance = google_sql_database_instance.mysql_instance.name
}

resource "google_sql_user" "default_user" {
  name     = "admin"
  instance = google_sql_database_instance.mysql_instance.name
  password = "your_secure_password"
}

resource "google_container_cluster" "kubernetes_cluster" {
  name               = "small-k8s-cluster"
  location           = "us-central1"
  initial_node_count = 1

  node_config {
    machine_type = "e2-small"
    disk_size_gb = 10
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}

output "mysql_instance_connection_name" {
  value = google_sql_database_instance.mysql_instance.connection_name
}

output "kubernetes_cluster_endpoint" {
  value = google_container_cluster.kubernetes_cluster.endpoint
}

output "kubernetes_cluster_name" {
  value = google_container_cluster.kubernetes_cluster.name
}