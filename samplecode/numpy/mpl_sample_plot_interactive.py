# MCS 275 Spring 2023 Emily Dumas
"Show a matplotlib plot interactively"
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 100)

print("Creating plot")

plt.figure(figsize=(8, 6), dpi=120)
plt.plot(x, np.sin(x), label="sine", linewidth=2, color="red")
plt.plot(x, np.cos(x), label="cosine", linewidth=1, linestyle="dashed", color="#5555F8")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.title("Trigonometric functions")
plt.legend()

print("Displaying.")
plt.show(block=True)
print("Done.")
