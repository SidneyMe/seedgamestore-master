# Set required provider
provider "google" {
  project = "booming-splicer-443411-u6"  # Replace with your GCP project ID
  region  = "us-central1"      # Choose your desired region
}

# Define a small MySQL Cloud SQL instance
resource "google_sql_database_instance" "mysql_instance" {
  name             = "mysql-small-db"
  database_version = "MYSQL_8_0"
  region           = "us-central1"

  settings {
    tier = "db-f1-micro" # Smallest instance size

    ip_configuration {
      ipv4_enabled = true
    }
  }
}

# Create a database in the instance
resource "google_sql_database" "database" {
  name     = "sampledb"
  instance = google_sql_database_instance.mysql_instance.name
}

# Set a database user
resource "google_sql_user" "default_user" {
  name     = "admin"
  instance = google_sql_database_instance.mysql_instance.name
  password = "your_secure_password"  # Use a secure password
}

# Define a small Kubernetes cluster
resource "google_container_cluster" "kubernetes_cluster" {
  name     = "small-k8s-cluster"
  location = "us-central1" # Region or zone
  initial_node_count = 1   # Minimum node count for small cluster

  node_config {
    machine_type = "e2-small" # Small machine type
    disk_size_gb = 10        # Small disk size
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
  }
}

# Outputs for reference
output "mysql_instance_connection_name" {
  value = google_sql_database_instance.mysql_instance.connection_name
}

output "kubernetes_cluster_endpoint" {
  value = google_container_cluster.kubernetes_cluster.endpoint
}

output "kubernetes_cluster_name" {
  value = google_container_cluster.kubernetes_cluster.name
}
