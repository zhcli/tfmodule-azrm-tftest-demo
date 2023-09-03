resource "azurerm_resource_group" "test-aea-rg" {
  name     = "test-aea-rg${var.random_id}"
  location = "Australia East"
}

module "test-storage-account" {
  source               = "../"
  storage_account_name = "testaeasa${var.random_id}"
  target_rg            = azurerm_resource_group.test-aea-rg.name
  location             = azurerm_resource_group.test-aea-rg.location
}