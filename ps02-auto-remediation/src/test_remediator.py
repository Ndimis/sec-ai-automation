import pytest
import os
import sys
from remediator import RemediationEngine

@pytest.fixture
def setup_test_data():
    if not os.path.exists("data"): os.makedirs("data")
    test_ips = "1.1.1.1\n2.2.2.2"
    with open("data/blacklist.txt", "w") as f:
        f.write(test_ips)
    return "data/blacklist.txt"

def test_remediation_logic(setup_test_data):
    remediator = RemediationEngine(threat_log=setup_test_data)
    remediator.generate_remediation_tasks()
    
    # Check if script exists
    assert os.path.exists(remediator.output_script)
    
    # Check for correct content based on OS
    with open(remediator.output_script, "r", encoding='utf-8') as f:
        content = f.read()
        if sys.platform == 'win32':
            assert "New-NetFirewallRule" in content
            assert "1.1.1.1" in content
        else:
            assert "iptables" in content
            assert "2.2.2.2" in content

def test_empty_log_handling():
    # Ensure it doesn't crash if the log is empty
    with open("data/empty.txt", "w") as f: f.write("")
    remediator = RemediationEngine(threat_log="data/empty.txt")
    remediator.generate_remediation_tasks()
    # Should exit gracefully