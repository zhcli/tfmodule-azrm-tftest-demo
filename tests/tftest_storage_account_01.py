"""Demo test cases for tfmodule storage account"""
import os
import random
import time
import pytest
import tftest
from azure.identity import EnvironmentCredential
from azure.mgmt.storage import StorageManagementClient

RANDOM_ID = random.randint(0, 1000)
EXPECTED_RG = 'test-aea-rg' + str(RANDOM_ID)
EXPECTED_SA_NAME = 'testaeasa' + str(RANDOM_ID)

def connect_storage_client():
    """return azurerm storage client"""
    subscription_id = os.environ["ARM_SUBSCRIPTION_ID"]
    credential = EnvironmentCredential()
    return StorageManagementClient(credential, subscription_id)

@pytest.fixture(scope='session')
def apply(fixtures_dir='../fixture/'):
    """terraform apply fixture at session level"""
    tf_test = tftest.TerraformTest('.', fixtures_dir, enable_cache=True)
    tf_test.setup(enable_cache=True)
    tf_test.apply(input=True, output=True, tf_vars={'random_id': RANDOM_ID}, enable_cache=True)
    yield tf_test.output(enable_cache=True)
    tf_test.destroy(input=True, output=True, tf_vars={'random_id': RANDOM_ID}, enable_cache=True)

def test_minimum_tls_version(apply):
    """tls minimum version is TLS 1.2"""
    storage_client = connect_storage_client()
    minimum_tls_version = storage_client.storage_accounts.get_properties(EXPECTED_RG, EXPECTED_SA_NAME).minimum_tls_version
    assert minimum_tls_version == 'TLS1_2'

def test_enable_https_traffic_only(apply):
    """enable https traffics only is true"""
    storage_client = connect_storage_client()
    enable_https_traffic_only = storage_client.storage_accounts.get_properties(EXPECTED_RG, EXPECTED_SA_NAME).enable_https_traffic_only
    assert enable_https_traffic_only is True

def test_public_network_access(apply):
    """public network access is disable"""
    storage_client = connect_storage_client()
    public_network_access = storage_client.storage_accounts.get_properties(EXPECTED_RG, EXPECTED_SA_NAME).public_network_access
    assert public_network_access == 'Disabled'

def test_network_rule_set(apply):
    """tests for network rule set"""
    storage_client = connect_storage_client()
    network_rule_set = storage_client.storage_accounts.get_properties(EXPECTED_RG, EXPECTED_SA_NAME).network_rule_set
    assert network_rule_set.default_action == 'Deny'
    assert network_rule_set.bypass == 'AzureServices'
    ip_rule = [ip_rule.ip_address_or_range for ip_rule in network_rule_set.ip_rules]
    ip_rule.sort()
    """intentionally failed this test"""
    assert ip_rule == ['100.0.0.12', '134.124.0.1', '66.16.1.1']
