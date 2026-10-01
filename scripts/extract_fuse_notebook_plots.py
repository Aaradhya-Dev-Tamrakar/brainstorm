import json
import os
import sys
import base64
from pathlib import Path
from PIL import Image
import io

sys.stdout.reconfigure(encoding='utf-8')

def inspect_notebook(nb_path):
    with open(nb_path, encoding='utf-8') as f:
        nb = json.load(f)
    print(f"\n--- Notebook: {nb_path.name} ---")
    cells = nb.get('cells', [])
    img_idx = 0
    for i, c in enumerate(cells):
        src_preview = "".join(c.get('source', []))[:60].replace("\n", " ")
        for o in c.get('outputs', []):
            if 'data' in o and 'image/png' in o['data']:
                img_data = o['data']['image/png']
                # if list of strings, join
                if isinstance(img_data, list):
                    img_data = "".join(img_data)
                raw_bytes = base64.b64decode(img_data)
                im = Image.open(io.BytesIO(raw_bytes))
                print(f"  [Cell {i:2d} | Img {img_idx}] size: {im.size}, mode: {im.mode} | Src: {src_preview}")
                img_idx += 1
            elif 'text' in o:
                t = "".join(o['text'])[:70].replace("\n", " ")
                # print first text output if any
                if o.get('output_type') == 'stream' and 'epoch' in t.lower():
                    print(f"  [Cell {i:2d} | Stream] {t}")

root = Path(r"C:\Users\Aaradhya\Downloads\_Organized\Fuse AI Fellowship")
notebooks = [
    root / "M1" / "WK1" / "notebooks" / "Wk_1_Data_Wrangling_HeartAttack.ipynb",
    root / "M1" / "WK1" / "notebooks" / "DataWranglingPreW1.ipynb",
    root / "M1" / "WK4" / "W4_Linear_Models_Assignment_executed.ipynb",
    root / "M2" / "WK5" / "W5_Tree-Based Models & Ensembles_Assignment.ipynb",
    root / "M2" / "WK6" / "W6_Probabilistic_Models_Assignment.ipynb",
    root / "M2" / "WK7" / "Week_7_Clustering_Assignment_executed.ipynb",
    root / "M2" / "WK8" / "W8_Forecasting_Assignment.ipynb",
    root / "M3" / "WK9" / "W9_NEU_Defect_CNN_Assignment.ipynb",
    root / "M3" / "WK10" / "W10_Image_Processing_Assignment_executed.ipynb",
    root / "M3" / "WK11" / "notebooks" / "W11_CV_Assignment_Notebook.ipynb",
    root / "M3" / "WK12" / "notebooks" / "Assignment3_NER_CustomerSupport.ipynb",
    root / "M4" / "WK13" / "LSTMs_for_Text_Classification.ipynb",
    root / "M4" / "WK14" / "support_routing.ipynb",
]

for nb in notebooks:
    if nb.exists():
        inspect_notebook(nb)
    else:
        print(f"Not found: {nb}")
