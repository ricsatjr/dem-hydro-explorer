import json
import glob

for path in glob.glob("**/*.ipynb", recursive=True):
    with open(path, "r") as f:
        nb = json.load(f)

    changed = False

    if "widgets" in nb.get("metadata", {}):
        del nb["metadata"]["widgets"]
        changed = True

    for cell in nb.get("cells", []):
        for output in cell.get("outputs", []):
            if output.get("metadata"):
                output["metadata"] = {}
                changed = True

    if changed:
        with open(path, "w") as f:
            json.dump(nb, f, indent=1)
        print(f"cleaned: {path}")
    else:
        print(f"ok: {path}")

print("Done.")
