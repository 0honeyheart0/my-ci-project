terraform {
  required_providers {
    yandex = {
      source  = "yandex-cloud/yandex"
      version = "0.220.0"
    }
  }
}

provider "yandex" {
  service_account_key_file = "/home/kali/.config/yandex/authorized_key.json"
  cloud_id  = var.cloud_id
  folder_id = var.folder_id
  zone      = var.zone
}

resource "yandex_vpc_network" "default" {
  name = "k8s-network"
}

resource "yandex_vpc_subnet" "default" {
  name = "k8s-subnet"
  zone = var.zone
  network_id = yandex_vpc_network.default.id
  v4_cidr_blocks = ["192.168.10.0/24"]
  }

resource "yandex_iam_service_account" "k8s_sa" {
  name = "k8s-sa"
}

resource "yandex_resourcemanager_folder_iam_member" "k8s_editor" {
  folder_id = var.folder_id
  role      = "editor"
  member    = "serviceAccount:${yandex_iam_service_account.k8s_sa.id}"
}

resource "yandex_kubernetes_cluster" "my_cluster" {
  name        = "my-k8s-cluster"
  description = "Managed Kubernetes cluster for myapp"
  network_id  = yandex_vpc_network.default.id
  folder_id   = var.folder_id

  master {
    version   = "1.30"         
    public_ip = true            
  }

   service_account_id      = yandex_iam_service_account.k8s_sa.id
  node_service_account_id = yandex_iam_service_account.k8s_sa.id
}

resource "yandex_kubernetes_node_group" "main" {
  cluster_id = yandex_kubernetes_cluster.my_cluster.id
  name       = "main-node-group"
  
  scale_policy {
    fixed_scale {
      size = 2
    }
  }
  
   instance_template {
    platform_id = "standard-v3"

    resources {
      memory = 4
      cores  = 2
    }

    boot_disk {
      size = 20
      type = "network-ssd"
    }

    network_interface {
      subnet_ids = [yandex_vpc_subnet.default.id]
    }
    
    metadata = {
      ssh-keys = "ubuntu:${file("~/.ssh/id_ed25519.pub")}"
    }
  }
  
  maintenance_policy {
    auto_upgrade = true
    auto_repair  = true
  }
}

output "cluster_ip" {
  value = yandex_kubernetes_cluster.my_cluster.master[0].public_ip
}

output "kubeconfig_command" {
  value = "yc managed-kubernetes cluster get-credentials my-k8s-cluster --external"
}
