# Week 10: Classical Image Processing (OpenCV FreshTrack)

---
relevancy_tier: GOLDEN_REFERENCE
mentor_score: 100/100
classroom_id: 870378868125
quiz_id: 855391300639
local_path: F:\FuseAIF2026\M3\WK10
github_repo: https://github.com/AaradhyaDT/fuseAiF_wk10_image_processing
---

## 1. Overview & Industrial Setting
- **Scenario**: Computer Vision Engineer at FreshTrack automating automated sorting and counting of mixed fruit crates.
- **Dataset**: Fruits-360 subset (red_apple, green_apple, banana, strawberry, orange, lime) + composite scenes (`mixed_fruit_bowl.jpeg`, `morphology.png`, `chessboard.png`).
- **Core Pipeline**:
  - Part A: Color-space conversion & HSV segmentation tables (`cv2.inRange`).
  - Part B: Morphological filtering (Opening, Closing, Morphological Gradient).
  - Part C: From-scratch Canny Edge Detector (**96.9% pixel agreement with `cv2.Canny()`**).
  - Part D: Harris corner detector and Hough Circle Transform for fruit counting.

---

## 2. SOTA Industry Best Practices & Production Standards
- **Hue Wrap-Around Handling**: Red color wraps around the $0^\circ$ and $180^\circ$ boundary in OpenCV HSV space ($[0, 10]$ and $[170, 180]$). Always generate two masks and combine them via `cv2.bitwise_or()`.
- **Touching Object Disambiguation (`INV-CV-SEPARATE`)**: Raw color masks merge touching adjacent fruits of the same type into one massive connected component. Resolve individual fruit centroids by computing the **Distance Transform** (`cv2.distanceTransform`) followed by peak thresholding and watershed segmentation.
- **Vectorized Kernel Convolution**: Avoid nested Python spatial loops. Use `cv2.filter2D()` or strided NumPy sliding windows (`numpy.lib.stride_tricks.sliding_window_view`).

---

## 3. Mentor Evaluation & Quality Rating
- **Assignment Grade**: **100 / 100** ("Image Processing").
- **Quiz Status**: Handed in ("Image Processing Quiz").
- **Metrics Verified**: From-scratch Canny edge detector achieved 96.9% exact pixel correspondence with OpenCV; Hough transform cleanly detected 6 round fruits in the mixed bowl benchmark.

---

## 4. Local-First & GitHub Fallback Resolution (`INV-RESOLVE-FUSE`)
- **Local Directory**: [`F:\FuseAIF2026\M3\WK10`](file:///F:/FuseAIF2026/M3/WK10)
  - `W10_Image_Processing_Assignment_executed.ipynb` — Executed notebook.
  - `q14_pipeline_red_apple_1.jpg` — Final deliverable bounding box output.
- **GitHub Remote Fallback**:
  - `https://github.com/AaradhyaDT/fuseAiF_wk10_image_processing`
  - Clone: `gh repo clone AaradhyaDT/fuseAiF_wk10_image_processing`

---

## 5. Golden Implementation Snippets

### Red Fruit Dual-Band HSV Masking
```python
import cv2
import numpy as np

def isolate_red_fruit(bgr_image: np.ndarray) -> np.ndarray:
    """Isolate red objects handling the Hue wrap-around at 0/180."""
    hsv = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
    
    # Lower red band: H in [0, 10]
    mask_low = cv2.inRange(hsv, np.array([0, 100, 100]), np.array([10, 255, 255]))
    # Upper red band: H in [170, 180]
    mask_high = cv2.inRange(hsv, np.array([170, 100, 100]), np.array([180, 255, 255]))
    
    # Combine masks
    combined_mask = cv2.bitwise_or(mask_low, mask_high)
    
    # Morphological cleanup: remove speckles, close holes
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    cleaned = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)
    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel)
    return cleaned
```

---

## 6. Classroom Quiz Analysis & Conceptual Traps
- **Quiz ID**: `855391300639`.
- **Canny Hysteresis Logic**: Why use two thresholds ($T_{\text{low}}, T_{\text{high}}$) in Canny?
  - *Answer*: Edges with gradient magnitude $> T_{\text{high}}$ are immediately declared strong edges. Pixels between $T_{\text{low}}$ and $T_{\text{high}}$ are retained *only* if they are 8-connected to a strong edge. This prevents noise specks from becoming spurious edge fragments.
