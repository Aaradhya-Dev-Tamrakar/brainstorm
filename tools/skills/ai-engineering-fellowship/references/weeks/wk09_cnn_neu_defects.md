# Week 9: Neural Network Foundations & NEU Steel Defect CNN

---
relevancy_tier: GOLDEN_REFERENCE
mentor_score: 100/100
classroom_id: 868825306318
quiz_id: 868824098582
local_path: F:\FuseAIF2026\M3\WK9
github_repo: https://github.com/AaradhyaDT/fuseAiF_wk9_neu_defect_cnn
---

## 1. Overview & Dataset Context
- **Scenario**: Junior ML Engineer at SmartForge Manufacturing automating visual quality control on steel strips.
- **Dataset**: NEU Surface Defect Database (Kaggle), 1,800 grayscale images ($200 \times 200$), 6 balanced classes (300/class): Rolled-in scale, Patches, Crazing, Pitted surface, Inclusion, Scratches.
- **Phases**:
  - Part 0: From-scratch 2-layer NN in PyTorch `nn.Module` (30,721,798 parameters).
  - Part A: CNN Classifier (Conv2D $\to$ MaxPool $\to$ Linear).
  - Part B: Hardening with torchvision augmentations, BatchNorm2d, and Dropout(0.4).
  - Part C: Grid search vs. Optuna Bayesian optimization with StepLR scheduling.

---

## 2. SOTA Industry Best Practices & Production Standards
- **Explicit `nn.Module` Subclassing**: Always structure models using modular classes inheriting from `torch.nn.Module`. Explicitly instantiate layers in `__init__` and forward execution in `forward()`.
- **Training vs. Inference Modes**: Never evaluate without calling `model.eval()` and wrapping the loop in `with torch.no_grad():`. Otherwise, BatchNorm continues calculating batch statistics and Dropout randomly zeros features.
- **Data Augmentation Guard**: Augmentations (`RandomHorizontalFlip`, `RandomRotation(15)`, `RandomCrop`) must be applied exclusively to `train_loader`, never to validation or test loaders.
- **Hyperparameter Optimization with Optuna**: Deploy `optuna.create_study(direction="maximize", pruner=optuna.pruners.MedianPruner())` to search learning rate ($10^{-4}$ to $10^{-1}$ log-uniform) and batch sizes ($16$ to $64$).

---

## 3. Mentor Evaluation & Quality Rating
- **Assignment Grade**: **100 / 100** ("Neural Network Assignments").
- **Quiz Status**: Handed in ("Neural Networks").
- **Metrics Verified**: Final train accuracy 0.988 / validation accuracy 0.789; best Optuna configuration ($\text{lr} \approx 0.0157, \text{batch\_size} = 42$). Executed on Google Colab T4 GPU runtime.

---

## 4. Local-First & GitHub Fallback Resolution (`INV-RESOLVE-FUSE`)
- **Local Directory**: [`F:\FuseAIF2026\M3\WK9`](file:///F:/FuseAIF2026/M3/WK9)
  - `data/NEU-DET/` — Dataset images.
  - `docs/resources/Neural Network Assignments - Classroom.pdf` — Assignment rubric.
  - `plots/` — Convergence and confusion matrix plots.
- **GitHub Remote Fallback**:
  - `https://github.com/AaradhyaDT/fuseAiF_wk9_neu_defect_cnn`
  - Clone: `gh repo clone AaradhyaDT/fuseAiF_wk9_neu_defect_cnn`

---

## 5. Golden Implementation Snippets

### Hardened PyTorch Defect Classifier
```python
import torch
import torch.nn as nn

class HardenedDefectCNN(nn.Module):
    def __init__(self, num_classes: int = 6):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),  # 100x100
            
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),  # 50x50
            
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),  # 25x25
        )
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d((4, 4)),
            nn.Flatten(),
            nn.Dropout(0.4),
            nn.Linear(128 * 4 * 4, 128),
            nn.ReLU(inplace=True),
            nn.Dropout(0.4),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        return self.classifier(self.features(x))
```

---

## 6. Classroom Quiz Analysis & Conceptual Traps
- **Quiz ID**: `868824098582` (Neural Networks).
- **ReLU vs Sigmoid in Deep Nets**: Sigmoid saturates at both tails with gradients approaching zero ($\sigma'(x) = \sigma(x)(1 - \sigma(x)) \le 0.25$), triggering vanishing gradients across multi-layer networks. ReLU maintains a constant gradient of $1.0$ for all $x > 0$.
