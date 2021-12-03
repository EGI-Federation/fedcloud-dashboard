variable "net_id" {
  type        = string
  description = "The id of the network"
}

variable "ip_pool" {
  type        = string
  description = "The floating ip pool"
}

variable "image_id" {
  type        = string
  description = "VM image id"
}

variable "flavor_id" {
  type        = string
  description = "VM flavor id"
}
