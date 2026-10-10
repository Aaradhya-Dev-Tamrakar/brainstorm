# Week 11: Vision Transformers, CLIP & Deep Learning CV

---
relevancy_tier: GOLDEN_REFERENCE
mentor_score: 100/100
classroom_id: 870595309296
quiz_id: 870596166627
local_path: F:\FuseAIF2026\M3\WK11
github_repo: https://github.com/AaradhyaDT/fuseAiF_wk11_vision_transformers
---

## 1. Overview & Industrial Setting
- **Scenario**: Computer Vision Engineer at QuickVision AI upgrading warehouse camera perception.
- **Scope**: Complete modern vision stack spanning 5 modules:
  1. **CNN Classification**: ResNet-50 transfer learning (74.1% accuracy) + GradCAM interpretability.
  2. **Object Detection**: IoU and Non-Maximum Suppression (NMS) implemented from scratch + Faster R-CNN inference.
  3. **Semantic Segmentation**: DeepLabv3+ mask generation and mIoU scoring.
  4. **Generative Modeling**: Variational Autoencoder (VAE) with latent-space interpolation.
  5. **Vision Transformers & Deployment**: ViT patch projection, **CLIP zero-shot classification (92.0% accuracy)**, and ONNX deployment export (94.2 MB).

---

## 2. SOTA Industry Best Practices & Production Standards
- **Zero-Shot CLIP as Foundation (`INV-CLIP-BENCH`)**: On cold-start or limited-data industrial visual recognition, zero-shot OpenAI CLIP (`openai/clip-vit-base-patch32`) outscored the fine-tuned ResNet-50 (**92.0% vs. 74.1%**). Always test zero-shot multimodal foundations before spending resources labeling training sets.
- **ONNX Model Export & Quantization**: Convert PyTorch vision models into standardized ONNX graph format with dynamic batch sizes for production deployment across CPU and edge accelerators:
  ```python
  torch.onnx.export(
      model, dummy_input, "model.onnx",
      input_names=["input"], output_names=["output"],
      dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}},
      opset_version=14
  )
  ```
- **GradCAM Tensor Detachment**: When calculating GradCAM activation maps, remember to detach gradient-tracked activation tensors before calling `.cpu().numpy()`, preventing PyTorch `RuntimeError`.

---

## 3. Mentor Evaluation & Quality Rating
- **Assignment Grade**: **100 / 100** ("Computer Vision Assignment").
- **Quiz Score**: **20 / 20** ("'Computer Vision Quiz" — perfect score).
- **Execution Authenticity**: All 20 notebook code cells executed sequentially with output verification, real debugging fixes logged (GradCAM `.detach()`, DeepLab `.squeeze(0)`).

---

## 4. Local-First & GitHub Fallback Resolution (`INV-RESOLVE-FUSE`)
- **Local Directory**: [`F:\FuseAIF2026\M3\WK11`](file:///F:/FuseAIF2026/M3/WK11)
  - `notebooks/W11_CV_Assignment_Notebook.ipynb` — Executed notebook (Run 4).
  - `docs/` — Architectural deployment memo and comparison tables.
- **GitHub Remote Fallback**:
  - `https://github.com/AaradhyaDT/fuseAiF_wk11_vision_transformers`
  - Clone: `gh repo clone AaradhyaDT/fuseAiF_wk11_vision_transformers`

---

## 5. Golden Implementation Snippets

### IoU and Non-Maximum Suppression (From Scratch)
```python
import numpy as np

def compute_iou(box1, box2):
    """Compute Intersection over Union between two [x1, y1, x2, y2] boxes."""
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    
    intersection = max(0, x2 - x1) * max(0, y2 - y1)
    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union = area1 + area2 - intersection
    return intersection / union if union > 0 else 0.0

def nms_from_scratch(boxes, scores, iou_threshold=0.5):
    """Greedy Non-Maximum Suppression."""
    indices = np.argsort(scores)[::-1]
    keep = []
    while len(indices) > 0:
        current = indices[0]
        keep.append(current)
        if len(indices) == 1:
            break
        ious = np.array([compute_iou(boxes[current], boxes[i]) for i in indices[1:]])
        indices = indices[1:][ious < iou_threshold]
    return keep
```

---

## 6. Classroom Quiz Analysis & Conceptual Traps
- **Quiz ID**: `870596166627` (20/20).
- **Vision Transformer Patch Embedding**: ViT converts an image of shape $(H, W, C)$ into $N = \frac{HW}{P^2}$ patches of size $(P, P, C)$ and projects each patch linearly into dimension $D$. Unlike CNNs, self-attention has global receptive field from layer 1.
