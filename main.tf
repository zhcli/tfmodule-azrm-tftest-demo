resource "azurerm_storage_account" "storage_account" {
  name                          = var.storage_account_name
  resource_group_name           = var.target_rg
  account_tier                  = "Standard"
  account_replication_type      = "LRS"
  location                      = var.location
  public_network_access_enabled = false

  network_rules {
    default_action = "Deny"
    bypass         = ["AzureServices"]
    ip_rules       = ["100.0.0.1", "134.124.0.1", "66.16.1.1"]
  }
}
#