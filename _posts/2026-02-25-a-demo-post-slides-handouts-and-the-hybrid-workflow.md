---
layout: post
title: "A Demo Post: Slides, Handouts, and the Hybrid Workflow"
date: 2026-02-25
tags: ["demo", "workflow", "writing"]
math: true
---

This is a demo article repurposed from a presentation draft. It exercises the kinds of content I typically write about: mathematical formulations, code, and experimental results. It also serves as a test of the new org → blog pipeline.

# Motivation

Building complex models requires bridging theory and computation. A few themes that keep coming up:

- Transformer architectures and their structural limits on reasoning
- Biological regulatory networks as a lens on emergent computation
- The tension between model expressiveness and interpretability

The interesting question is rarely "does this work?" but "under what assumptions does it work, and when do those assumptions break?"

# A Mathematical Formulation

Let $x$ and $y$ be random variables with joint distribution $p(x, y)$. By the product rule:

$$p(x, y) = p(x)\, p(y \mid x)$$

The objective minimised during training is the regularised negative log-likelihood:

$$\mathcal{L}(\theta) = -\sum_{i=1}^{n} \log p(y_i \mid x_i;\, \theta) + \lambda \lVert \theta \rVert_2^2$$

where $\theta$ are the model parameters and $\lambda$ controls regularisation strength. We initialise parameters from $\mathcal{N}(0, 0.01)$ and optimise with Adam ($\alpha = 0.001$).[^1] Convergence typically occurs within 100 epochs.

# Code Example

A minimal reproducible example that generates the sine/cosine plot referenced in the results section:

``` python
import matplotlib.pyplot as plt
import numpy as np

x  = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

plt.figure(figsize=(8, 4))
plt.plot(x, y1, label="sin(x)", linewidth=2)
plt.plot(x, y2, label="cos(x)", linewidth=2)
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("sincos.png", dpi=150, bbox_inches="tight")
```

# Experimental Results

## Setup

- **Dataset**: ImageNet subset (10 K images, stratified, 10 classes)
- **Metrics**: Top-1 accuracy and macro F1
- **Baselines**: ResNet-50, EfficientNet-B0
- Each experiment repeated 5 times with different random seeds; 95% CIs via bootstrap (10 000 samples)

## Results

| Method       | Accuracy | F1 Score |
|--------------|----------|----------|
| ResNet-50    | 0.85     | 0.83     |
| EfficientNet | 0.88     | 0.86     |
| **Ours**     | **0.92** | **0.90** |

All improvements are statistically significant ($p < 0.001$, paired $t$-test with Bonferroni correction for multiple comparisons, Cohen's $d > 0.89$).

## Robustness Checks

1.  **Cross-validation**: 5-fold CV confirms the pattern holds across splits
2.  **Ablation**: each component contributes 1–3 percentage points of accuracy
3.  **Sensitivity**: results are stable across the hyperparameter ranges we swept
4.  **Failure modes**: errors concentrate in visually similar classes, as expected

# Conclusion

Three takeaways:

1.  Combining structural priors with data-driven learning improves sample efficiency.
2.  The gains are robust across seeds, splits, and reasonable hyperparameter choices.
3.  Open questions remain around scaling beyond $n = 100\text{K}$ (the algorithm is currently $O(n^2)$) and handling distribution shift.

Future directions include developing PAC-learning bounds, adapting the method to semi-supervised settings, and testing on sequence and graph-structured data.

[^1]: Adam is generally preferred over SGD here because it adapts the learning rate per parameter, which matters when gradients vary significantly in scale across layers.
