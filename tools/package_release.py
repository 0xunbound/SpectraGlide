import zipfile
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dist_dir = os.path.join(base_dir, "dist")
zip_path = os.path.join(base_dir, "SpectraGlide_v2.0.zip")

if os.path.exists(zip_path):
    os.remove(zip_path)

added_names = set()

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(dist_dir):
        for file in files:
            if file.endswith(".old") or file.endswith(".log") or "warp_gemini" in file:
                continue
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, dist_dir)
            arc_name = os.path.join("SpectraGlide", rel_path).replace("\\", "/")
            if arc_name not in added_names:
                zf.write(full_path, arc_name)
                added_names.add(arc_name)
    
    # Also include LICENSE from root if not added
    license_path = os.path.join(base_dir, "LICENSE")
    if os.path.exists(license_path) and "SpectraGlide/LICENSE" not in added_names:
        zf.write(license_path, "SpectraGlide/LICENSE")
        added_names.add("SpectraGlide/LICENSE")

print(f"Created archive: {zip_path}, Size: {os.path.getsize(zip_path) / (1024*1024):.2f} MB")
