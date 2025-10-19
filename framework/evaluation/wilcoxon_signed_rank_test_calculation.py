import scipy.stats as stats
import numpy as np

# Data: WITH TDD vs WITHOUT TDD (proportions from 5 runs)
problems = [
    "Salary Analyzer", "Patient Risk", "Student GPA", "Inventory Alert",
    "Matrix Eigenvalue", "Portfolio Risk", "IoT Sensor",
    "Movie API", "Book Recommender", "Performance Tracker", "Friend Suggester"
]

with_tdd = [4 / 5, 5 / 5, 5 / 5, 4 / 5, 4 / 5, 5 / 5, 5 / 5, 4 / 5, 5 / 5, 5 / 5, 5 / 5]
without_tdd = [2 / 5, 4 / 5, 4 / 5, 3 / 5, 3 / 5, 4 / 5, 4 / 5, 3 / 5, 4 / 5, 5 / 5, 4 / 5]

print("=" * 80)
print("WILCOXON SIGNED-RANK TEST (Paired comparison: WITH TDD vs WITHOUT TDD)")
print("=" * 80)

# Calculate differences
differences = [with_tdd[i] - without_tdd[i] for i in range(len(with_tdd))]

print("\nDifferences (WITH - WITHOUT):")
for i, prob in enumerate(problems):
    print(f"  {prob:25} {with_tdd[i]:.2f} - {without_tdd[i]:.2f} = {differences[i]:+.2f}")

# Wilcoxon signed-rank test (one-tailed: WITH > WITHOUT)
statistic, p_value = stats.wilcoxon(with_tdd, without_tdd, alternative='greater')

# Calculate effect size r = |Z| / sqrt(n)
n = len([d for d in differences if d != 0])
z_score = stats.norm.ppf(1 - p_value)
effect_size = abs(z_score) / np.sqrt(n)

print(f"\n{'=' * 80}")
print("RESULTS:")
print(f"{'=' * 80}")
print(f"Test Statistic (W+):     {statistic}")
print(f"P-value (one-tailed):    {p_value:.6f}")
print(f"Non-zero differences:    {n}")
print(f"Z-score:                 {z_score:.4f}")
print(f"Effect size (r):         {effect_size:.4f}")

if effect_size < 0.3:
    effect_str = "small"
elif effect_size < 0.5:
    effect_str = "medium"
else:
    effect_str = "large"

print(f"Effect interpretation:   {effect_str}")

if p_value < 0.001:
    sig_str = "p < 0.001"
elif p_value < 0.01:
    sig_str = "p < 0.01"
elif p_value < 0.05:
    sig_str = "p < 0.05"
else:
    sig_str = f"p = {p_value:.3f}"

print(f"Significance:            {sig_str}")

print(f"\n{'=' * 80}")
print("FOR PAPER TABLE ROW:")
print(f"{'=' * 80}")
print(f"Wilcoxon test: W={statistic}, {sig_str}, r={effect_size:.2f} ({effect_str} effect)")
