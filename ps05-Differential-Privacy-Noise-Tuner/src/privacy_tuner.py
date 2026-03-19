import numpy as np
import matplotlib.pyplot as plt

class PrivacyTuner:
    def __init__(self, sensitivity=1.0):
        self.sensitivity = sensitivity

    def generate_noise(self, epsilon, size=1000):
        """
        Calculates Laplace noise: scale = sensitivity / epsilon
        """
        # Differential Privacy Formula: scale = Δf / ε
        scale = self.sensitivity / epsilon
        return np.random.laplace(0, scale, size)

    def calculate_accuracy_loss(self, original_data, epsilon):
        """
        Simulates how much the average value shifts due to privacy noise.
        """
        noise = self.generate_noise(epsilon, size=len(original_data))
        perturbed_data = original_data + noise
        
        error = np.abs(np.mean(original_data) - np.mean(perturbed_data))
        return error

if __name__ == "__main__":
    tuner = PrivacyTuner(sensitivity=1.0)
    data_points = np.ones(100) * 50 # Base value of 50
    
    epsilons = [0.1, 1.0, 5.0]
    results = {}

    print("--- Differential Privacy Calibration ---")
    for eps in epsilons:
        loss = tuner.calculate_accuracy_loss(data_points, eps)
        results[eps] = loss
        print(f"Epsilon {eps}: Avg Accuracy Error = {loss:.4f}")

    # Visualizing the "Noise Cloud"
    plt.figure(figsize=(10, 5))
    for i, eps in enumerate(epsilons):
        noise = tuner.generate_noise(eps, size=100)
        plt.scatter(np.ones(100) * i, noise, label=f"ε={eps}")
    
    plt.xticks(range(len(epsilons)), [f"ε={e}" for e in epsilons])
    plt.title("Noise Magnitude vs. Epsilon Budget")
    plt.ylabel("Noise Value (Perturbation)")
    plt.legend()
    plt.savefig("privacy_tuner_plot.png")
    plt.show()