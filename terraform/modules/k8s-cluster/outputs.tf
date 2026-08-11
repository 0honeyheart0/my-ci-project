output "cluster_id" {
  value = yandex_kubernetes_cluster.this.id
}

output "cluster_ip" {
  value = yandex_kubernetes_cluster.this.master[0].public_ip
}

output "node_group_id" {
  value = yandex_kubernetes_node_group.main.id
}
