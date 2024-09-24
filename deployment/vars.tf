variable "net_id" {
  type        = string
  description = "The id of the network"
}

variable "ip_pool" {
  type        = string
  description = "The floating ip pool"
}

# https://appdb.egi.eu/store/vappliance/egi.docker
data "openstack_images_image_v2" "egi-docker" {
  most_recent = true
  properties = {
    "ad:appid" = "1006"
  }
}

variable "flavor_id" {
  type        = string
  description = "VM flavor id"
}
