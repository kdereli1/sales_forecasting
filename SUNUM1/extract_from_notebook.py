"""SARIMA.ipynb icindeki gomulu gorselleri ve metin ciktilarini SUNUM1/gorseller altina cikarir."""

import base64
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK = ROOT / "notebooks" / "SARIMA.ipynb"
OUT_DIR = Path(__file__).resolve().parent
IMAGE_DIR = OUT_DIR / "gorseller"
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]

manifest = []
text_dump = []

for cell_index, cell in enumerate(cells, start=1):
    source = "".join(cell["source"])
    # Hucreyi tanimlayan ilk yorum satiri ve savefig hedefleri
    first_comment = next((line.strip("# ").strip() for line in source.splitlines()
                          if line.strip().startswith("#")), "")
    savefig_names = re.findall(r'savefig\(OUTPUT_DIR / "([^"]+)"', source)
    savefig_names += re.findall(r'savefig\(output_dir / "([^"]+)"', source)

    image_counter = 0
    for output in cell.get("outputs", []):
        data = output.get("data", {})
        if "image/png" in data:
            payload = data["image/png"]
            if isinstance(payload, list):
                payload = "".join(payload)
            if image_counter < len(savefig_names):
                name = Path(savefig_names[image_counter]).stem
            else:
                name = f"cell{cell_index:02d}_img{image_counter + 1}"
            file_name = f"{cell_index:02d}_{name}.png"
            (IMAGE_DIR / file_name).write_bytes(base64.b64decode(payload))
            manifest.append({
                "cell": cell_index,
                "file": file_name,
                "comment": first_comment,
            })
            image_counter += 1

        text = output.get("text")
        if text:
            joined = "".join(text)
            if joined.strip():
                text_dump.append(f"===== CELL {cell_index:02d} | {first_comment} =====\n{joined}")

(OUT_DIR / "notebook_text_outputs.txt").write_text("\n".join(text_dump), encoding="utf-8")
(OUT_DIR / "gorsel_manifest.json").write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
)

print(f"Cikarilan gorsel: {len(manifest)}")
for entry in manifest:
    print(f"  {entry['file']}  <- cell {entry['cell']}: {entry['comment'][:60]}")
print(f"\nMetin cikti blogu: {len(text_dump)}")
