from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class PhishingAnalyzer:
    def __init__(self):
        # Known phishing patterns for similarity comparison
        self.malicious_templates = [
            "Your account has been suspended. Click here to verify your identity immediately.",
            "Urgent: Unauthorised login detected. Update your password now at this link.",
            "Final notice: Your invoice is overdue. Open the attached file to avoid fees."
        ]
        self.vectorizer = TfidfVectorizer()
        # Fit the vectorizer on our templates
        self.template_vectors = self.vectorizer.fit_transform(self.malicious_templates)

    def analyze_email(self, body):
        """
        Calculates how similar an email is to known phishing templates.
        """
        email_vector = self.vectorizer.transform([body])
        # Compare email to all templates and get the highest similarity score
        scores = cosine_similarity(email_vector, self.template_vectors)
        max_score = scores.max()
        
        # Heuristic: Check for common "Urgency" keywords
        urgency_keywords = ["immediate", "urgent", "suspended", "action required"]
        urgency_count = sum(1 for word in urgency_keywords if word in body.lower())
        
        # Final decision logic
        is_phish = max_score > 0.4 or urgency_count >= 2
        return {"is_phish": is_phish, "confidence": round(float(max_score), 2)}

if __name__ == "__main__":
    analyzer = PhishingAnalyzer()
    
    test_email = "Your Netflix account is suspended! Please click here to update your billing info immediately."
    result = analyzer.analyze_email(test_email)
    
    status = "🚨 PHISHING DETECTED" if result["is_phish"] else "✅ CLEAN"
    print(f"Result: {status} (Score: {result['confidence']})")