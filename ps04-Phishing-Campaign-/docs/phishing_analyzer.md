# Concept Explainer: Phishing Campaign Analyzer

### 🧠 The Core Concept
The **Phishing Campaign Analyzer** uses **Heuristic Analysis** and **TF-IDF (Term Frequency-Inverse Document Frequency)** to identify malicious intent in emails. 

Unlike simple "spam filters" that only look for blacklisted sender addresses, this analyzer examines the underlying "DNA" of the message:
1.  **Urgency & Sentiment:** Identifying high-pressure language (e.g., "Immediate action required," "Account suspended").
2.  **Structural Similarity:** Comparing the incoming email to known malicious templates using **Cosine Similarity**.
3.  **Keyword Density:** Using vectorization to determine if the email "looks" like a password reset or a fake invoice based on word patterns.



### 🛠️ Lessons Learned
1.  **Feature Extraction:** Computers don't read text; they read numbers. We use **Vectorization** to turn sentences into mathematical coordinates that a model can compare.
2.  **Handling False Positives:** Marketing emails often use "Urgent" language. We learn to weight specific combinations—like "Urgent" plus an "External Link"—more heavily than plain text to reduce noise.
3.  **Integration with SOAR:** This project is designed to feed into your **Auto-Remediation** project. If a high-confidence phishing email is flagged, the system can automatically purge it from all user inboxes across the organization.

### 📝 Key Takeaway
> **Email remains the #1 entry point for ransomware.** By automating the analysis of suspicious reports, security teams can stay ahead of mass-mailing campaigns that would otherwise overwhelm a manual review process.

### 🚀 How to Run

1. **Install Dependencies**:
   Ensure you have the scikit-learn library installed:
   ```bash
   pip install -r requirements.txt