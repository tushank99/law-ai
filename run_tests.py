"""Run all test cases and save raw, unedited outputs to outputs/."""
import json
import pathlib
from datetime import datetime
from lawyer import respond
from llm import provider_info

out_dir = pathlib.Path("outputs")
out_dir.mkdir(exist_ok=True)
cases = json.loads(pathlib.Path("test_cases.json").read_text(encoding="utf-8"))
report = []

for c in cases:
    kw = {k: c[k] for k in ("doc_type", "other_side") if k in c}
    try:
        res = respond(c["mode"], [{"role": "user", "content": c["input"]}], **kw)
    except Exception as e:
        res = {"reply": f"ERROR: {e}", "categories": [], "unverified": []}
    (out_dir / f"{c['id']}.md").write_text(
        f"# {c['id']} ({c['mode']})\n\n**Model:** {provider_info()}\n\n**Input:**\n> {c['input']}\n\n"
        f"**Detected categories:** {res['categories']}\n\n**Unverified citations flagged:** "
        f"{res['unverified']}\n\n---\n\n{res['reply']}\n", encoding="utf-8")
    report.append({"id": c["id"], "categories": res["categories"], "unverified": res["unverified"]})
    print(f"{c['id']:20s} cats={res['categories']} unverified={res['unverified']}")

(out_dir / "summary.json").write_text(json.dumps(
    {"model": provider_info(), "run_at": datetime.now().isoformat(), "results": report},
    indent=2, ensure_ascii=False), encoding="utf-8")
