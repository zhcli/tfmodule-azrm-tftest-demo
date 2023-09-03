variable "location" {
  description = "storage account location. i.e. Australia East"
  type        = string
}

variable "target_rg" {
  description = "target rg for the storage account"
  type        = string
}

variable "storage_account_name" {
  description = "storage account name"
  type        = string
}
