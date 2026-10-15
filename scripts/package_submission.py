"""
Packaging and Verification Script for PCCOE Capstone Submission.
Creates clean ZIP archive excluding caches, secrets, and virtual environments.
"""

import os
import shutil
import zipfile
from pathlib import Path

def package():
    sub_dir = Path("PCCOE_StudentName_PRN_CS1_AIML")
    zip_path = Path("PCCOE_StudentName_PRN_CS1_AIML.zip")

    # 1. Clean __pycache__ inside submission folder
    for p in sub_dir.rglob("__pycache__"):
        shutil.rmtree(p, ignore_errors=True)

    # 2. Clean temporary vector_store_data caches
    v_cache = sub_dir / "Code" / "vector_store_data"
    if v_cache.exists():
        shutil.rmtree(v_cache, ignore_errors=True)

    # 3. Clean any stray .env (ensure only .env.example exists)
    stray_env = sub_dir / "Code" / ".env"
    if stray_env.exists():
        stray_env.unlink()

    # 4. Create ZIP
    if zip_path.exists():
        zip_path.unlink()

    print(f"Compressing '{sub_dir}' into '{zip_path.name}'...")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root_dir, dirs, files in os.walk(sub_dir):
            for file in files:
                full_path = Path(root_dir) / file
                arcname = full_path.relative_to(sub_dir.parent)
                zf.write(full_path, arcname)

    # 5. Verify ZIP
    size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"Archive successfully created: {size_mb:.2f} MB")
    
    with zipfile.ZipFile(zip_path, "r") as zf:
        bad_file = zf.testzip()
        names = zf.namelist()
        if bad_file is None:
            print("Zip integrity test: PASSED (Archive verified healthy, no corruption)")
        else:
            print(f"Zip integrity test: FAILED at {bad_file}")

        print(f"Total archived files: {len(names)}")
        subdirs = sorted(list(set(n.split("/")[1] for n in names if "/" in n)))
        print(f"Archived subdirectories: {subdirs}")

if __name__ == "__main__":
    package()
