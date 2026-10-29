"""
Real Chest X-Ray Dataset Preparer (Kermany / Kaggle Dataset via HuggingFace)
Part of Multimodal Fused Clinical Decision Support System (CDSS)
VTU 5th Sem Mini Project - Dept. of CSE (Data Science)
"""

import os
import io
from PIL import Image
import pyarrow.parquet as pq
from huggingface_hub import hf_hub_download


def prepare_real_dataset(target_dir: str = "data/chest_xray"):
    """
    Downloads and extracts real frontal chest radiographs (Normal vs Pneumonia).
    Splits into train, val, and test subsets ready for PyTorch ImageFolder.
    """
    print("[*] Downloading benchmark Chest X-Ray dataset from HuggingFace...")
    parquet_path = hf_hub_download(
        repo_id="hf-vision/chest-xray-pneumonia",
        filename="data/test-00000-of-00001.parquet",
        repo_type="dataset"
    )
    print(f"[+] Downloaded dataset archive to: {parquet_path}")

    print("[*] Parsing Parquet table and extracting radiographic scans...")
    table = pq.read_table(parquet_path)
    total_rows = len(table)
    print(f"[*] Total real X-ray scans in partition: {total_rows}")

    # Create destination directories
    splits = ["train", "val", "test"]
    categories = ["NORMAL", "PNEUMONIA"]
    for s in splits:
        for c in categories:
            os.makedirs(os.path.join(target_dir, s, c), exist_ok=True)

    normal_count = 0
    pneumonia_count = 0

    # Read rows and distribute into train (60%), val (20%), test (20%)
    for idx in range(total_rows):
        label_val = table["label"][idx].as_py()
        label_name = "PNEUMONIA" if label_val == 1 else "NORMAL"
        
        img_dict = table["image"][idx].as_py()
        img_bytes = img_dict["bytes"]
        
        # Determine split
        if idx % 5 in [0, 1, 2]:
            split_name = "train"
        elif idx % 5 == 3:
            split_name = "val"
        else:
            split_name = "test"

        if label_name == "NORMAL":
            normal_count += 1
            filename = f"normal_{normal_count:04d}.jpeg"
        else:
            pneumonia_count += 1
            filename = f"pneumonia_{pneumonia_count:04d}.jpeg"

        out_path = os.path.join(target_dir, split_name, label_name, filename)
        with open(out_path, "wb") as f:
            f.write(img_bytes)

    print("\n[+] Real dataset prepared successfully!")
    print(f"Total Normal X-rays: {normal_count}")
    print(f"Total Pneumonia X-rays: {pneumonia_count}")
    print(f"Folder structure ready at: {os.path.abspath(target_dir)}")


if __name__ == "__main__":
    prepare_real_dataset()
