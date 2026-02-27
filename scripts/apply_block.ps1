# 🛡️ Windows PowerShell Remediation Script
# Generated automatically by Sec-AI-Auto

New-NetFirewallRule -DisplayName 'BLOCK_SEC_AI_1.1.1.1' -Direction Inbound -Action Block -RemoteAddress 1.1.1.1
New-NetFirewallRule -DisplayName 'BLOCK_SEC_AI_2.2.2.2' -Direction Inbound -Action Block -RemoteAddress 2.2.2.2
