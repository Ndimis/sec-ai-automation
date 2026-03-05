import os
import logging
import json
from openai import OpenAI

# It is best practice to store your key in an environment variable
# Windows: setx OPENAI_API_KEY "your-key-here"
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("IncidentAI-Live")

class IncidentSummarizer:
    def generate_summary(self, raw_log):
        """
        Sends raw telemetry to a real LLM to generate a professional incident report.
        """
        # Convert log to string for the prompt
        log_string = json.dumps(raw_log, indent=2)
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o",  # Or "gpt-3.5-turbo" for lower cost
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a Senior Security Operations (SOC) Analyst. Summarize the following technical log into a clear, executive-level incident report. Highlight the threat, the severity, and the automated action taken."
                    },
                    {
                        "role": "user", 
                        "content": f"Analyze this security event log:\n{log_string}"
                    }
                ],
                temperature=0.3, # Low temperature for consistent, factual reporting
                max_tokens=250
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"❌ API Error: {e}")
            return "Failed to generate AI summary. Check API quota or connectivity."

if __name__ == "__main__":
    summarizer = IncidentSummarizer()
    
    # Real-world raw log example
    raw_event = {
        "timestamp": "2026-03-04T22:15:00Z",
        "source_ip": "185.156.177.42",
        "attack_type": "DNS Tunneling (High Entropy)",
        "entropy_score": 4.85,
        "target_port": 53,
        "mitigation": "IP_BLACKLISTED"
    }
    
    report = summarizer.generate_summary(raw_event)
    print("\n" + report)