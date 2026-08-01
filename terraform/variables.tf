#variable "yc_token" {
 # description = "Yandex Cloud API token"
  #sensitive   = true
#}

variable "cloud_id" {
  description = "Yandex Cloud ID"
}

variable "folder_id" {
  description = "Yandex Cloud Folder ID"
}

variable "zone" {
  description = "Yandex Cloud availability zone"
  default     = "ru-central1-a"
}
