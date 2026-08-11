resource "yandex_kubernetes_cluster" "this" {
  name        = var.cluster_name
  description = var.cluster_description
  network_id  = var.network_id
  folder_id   = var.folder_id

  master {
    version   = var.k8s_version
    public_ip = true
    master_location {
      zone = var.zone
    }
  }

  service_account_id      = var.service_account_id
  node_service_account_id = var.node_service_account_id
}

resource "yandex_kubernetes_node_group" "main" {
  cluster_id = yandex_kubernetes_cluster.this.id
  name       = var.node_group_name

  scale_policy {
    fixed_scale {
      size = var.node_count
    }
  }

  instance_template {
    platform_id = var.node_platform
    resources {
      memory = var.node_memory
      cores  = var.node_cores
    }
    boot_disk {
      size = var.node_disk_size
      type = var.node_disk_type
    }
    network_interface {
      subnet_ids = [var.subnet_id]
    }
    metadata = {
      ssh-keys = "ubuntu:${var.ssh_public_key}"
    }
  }

  maintenance_policy {
    auto_upgrade = true
    auto_repair  = true
  }
}
