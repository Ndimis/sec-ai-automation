import logging
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("IncidentAI")

class IncidentSummarizer:
    def __init__(self):
        self.severity_map = {1: "LOW", 2: "MEDIUM", 3: "HIGH", 4: "CRITICAL"}

    def generate_summary(self, raw_log):
        """
        Simulates an LLM 'Reasoning' process to turn technical logs 
        into a human-readable executive summary.
        """
        try:
            # Parse the incoming technical data
            source_ip = raw_log.get("ip", "Unknown")
            threat_type = raw_log.get("type", "Unknown Anomaly")
            hits = raw_log.get("count", 1)
            severity = self.severity_map.get(raw_log.get("level", 1), "UNKNOWN")
            
            # THE PROMPT LOGIC: This mimics how an LLM organizes information
            summary = (
                f"--- 🛡️ EXECUTIVE INCIDENT SUMMARY ---\n"
                f"TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"SEVERITY: {severity}\n\n"
                f"DETECTION: Our systems identified a {threat_type} originating from {source_ip}.\n"
                f"BEHAVIOR: The actor attempted {hits} unauthorized interactions with production services.\n"
                f"ACTION TAKEN: The source IP has been flagged for automated blacklisting. "
                f"No data exfiltration was confirmed during this session.\n"
                f"------------------------------------"
            )
            return summary
        except Exception as e:
            return f"Error generating summary: {e}"

if __name__ == "__main__":
    summarizer = IncidentSummarizer()
    
    # Raw log from our Anomaly Detector or Honeypot
    raw_event = {
        "ip": "192.168.45.10",
        "type": "Brute Force Attempt",
        "count": 42,
        "level": 3
    }
    
    report = summarizer.generate_summary(raw_event)
    print(report)