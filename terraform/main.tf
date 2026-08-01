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

resource "yandex_compute_instance" "vm" {
  name        = "tofu-vm"
  platform_id = "standard-v3"
  zone        = var.zone

  resources {
    cores  = 2
    memory = 2
  }

  boot_disk {
    initialize_params {
      image_id = "fd8020c5t6gei8d1rpi1"
      size     = 20
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.default.id
    nat       = true
     security_group_ids = [yandex_vpc_security_group.ssh.id]
  }

  metadata = {
    ssh-keys = "ubuntu:${file("~/.ssh/id_ed25519.pub")}"
  }
}

resource "yandex_vpc_network" "default" {
  name = "tofu-network"
}

resource "yandex_vpc_subnet" "default" {
  name           = "tofu-subnet"
  zone           = var.zone
  network_id     = yandex_vpc_network.default.id
  v4_cidr_blocks = ["192.168.10.0/24"]
}

output "vm_ip" {
  value = yandex_compute_instance.vm.network_interface[0].nat_ip_address
}

resource "yandex_vpc_security_group" "ssh" {
  name        = "allow-ssh"
  description = "Allow SSH access"
  network_id  = yandex_vpc_network.default.id

  ingress {
    protocol       = "TCP"
    port           = 22
    v4_cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    protocol       = "ANY"
    v4_cidr_blocks = ["0.0.0.0/0"]
  }
}
