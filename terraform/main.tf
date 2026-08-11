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

data "yandex_iam_service_account" "k8s_sa" {
  name = "k8s-sa"  
}

module "k8s" {
  source = "./modules/k8s-cluster"

  cluster_name        = "my-k8s-cluster"
  cluster_description = "Managed K8s cluster for myapp"
  network_id          = yandex_vpc_network.default.id
  folder_id           = var.folder_id
  zone                = var.zone
  k8s_version         = "1.31"
  service_account_id  = data.yandex_iam_service_account.k8s_sa.id
  node_service_account_id = data.yandex_iam_service_account.k8s_sa.id
  subnet_id           = yandex_vpc_subnet.default.id
  node_count          = 2
  node_cores          = 2
  node_memory         = 4
  node_disk_size      = 50
  ssh_public_key      = var.ssh_public_key
}

output "cluster_ip" {
  value = module.k8s.cluster_ip
}

output "cluster_id" {
  value = module.k8s.cluster_id
}
