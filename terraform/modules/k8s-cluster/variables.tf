variable "cluster_name" {
  description = "Name of the Kubernetes cluster"
}

variable "cluster_description" {
  description = "Description of the cluster"
  default     = "Managed Kubernetes cluster"
}

variable "network_id" {
  description = "ID of the VPC network"
}

variable "folder_id" {
  description = "Yandex Cloud folder ID"
}

variable "zone" {
  description = "Availability zone"
  default     = "ru-central1-a"
}

variable "k8s_version" {
  description = "Kubernetes version"
  default     = "1.34"
}

variable "service_account_id" {
  description = "Service account ID for cluster"
}

variable "node_service_account_id" {
  description = "Service account ID for nodes"
}

variable "node_group_name" {
  description = "Name of the node group"
  default     = "main-node-group"
}

variable "node_count" {
  description = "Number of worker nodes"
  default     = 2
}

variable "node_platform" {
  description = "Platform for nodes"
  default     = "standard-v3"
}

variable "node_cores" {
  description = "vCPU per node"
  default     = 2
}

variable "node_memory" {
  description = "Memory per node (GB)"
  default     = 4
}

variable "node_disk_size" {
  description = "Disk size per node (GB)"
  default     = 50
}

variable "node_disk_type" {
  description = "Disk type"
  default     = "network-ssd"
}

variable "subnet_id" {
  description = "Subnet ID for nodes"
}

variable "ssh_public_key" {
  description = "Public SSH key for nodes"
  sensitive   = true
}
