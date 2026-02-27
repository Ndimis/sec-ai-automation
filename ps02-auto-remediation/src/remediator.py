import os
import logging
import sys

# Ensure UTF-8 support for security emojis on Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')
logger = logging.getLogger("AutoRemediator")

class RemediationEngine:
    def __init__(self, threat_log="data/blacklist.txt"):
        self.threat_log = threat_log
        self.os_type = sys.platform
        self.output_script = "scripts/apply_block" + (".ps1" if self.os_type == 'win32' else ".sh")

    def generate_remediation_tasks(self):
        """
        Parses threat data and translates it into OS-native firewall commands.
        """
        if not os.path.exists(self.threat_log):
            logger.error(f"❌ Threat log not found at {self.threat_log}")
            return

        with open(self.threat_log, "r", encoding='utf-8') as f:
            # Clean up IPs and remove duplicates
            ips = sorted(list(set(line.strip() for line in f if line.strip())))

        if not ips:
            logger.info("✅ No active threats require remediation.")
            return

        if not os.path.exists("scripts"):
            os.makedirs("scripts")

        with open(self.output_script, "w", encoding='utf-8') as script:
            if self.os_type == 'win32':
                script.write("# 🛡️ Windows PowerShell Remediation Script\n")
                script.write("# Generated automatically by Sec-AI-Auto\n\n")
                for ip in ips:
                    script.write(f"New-NetFirewallRule -DisplayName 'BLOCK_SEC_AI_{ip}' -Direction Inbound -Action Block -RemoteAddress {ip}\n")
            else:
                script.write("#!/bin/bash\n")
                script.write("# 🛡️ Linux Iptables Remediation Script\n\n")
                for ip in ips:
                    script.write(f"iptables -A INPUT -s {ip} -j DROP\n")

        logger.info(f"🚀 Remediation script generated: {self.output_script} with {len(ips)} rules.")

if __name__ == "__main__":
    # Simulate a threat log if one doesn't exist for testing
    if not os.path.exists("data"): os.makedirs("data")
    with open("data/blacklist.txt", "w") as f:
        f.write("192.168.1.50\n10.0.0.99\n")

    remediator = RemediationEngine()
    remediator.generate_remediation_tasks()