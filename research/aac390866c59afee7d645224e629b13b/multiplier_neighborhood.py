"""Exhaust a fixed-radius edit of the [172,21] QC multiplier."""
import copy
import hashlib
import itertools
import json
import math
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import codes
import large_verify
from prepare_structured import SPECS, construct

PARENT = ROOT / "research/readiness-20261021/certificates/172_21_66.json"
SEED = "aac390866c59afee7d645224e629b13b"


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: multiplier_neighborhood.py RADIUS OUTPUT_DIRECTORY")
    radius = int(sys.argv[1])
    if radius not in (1, 2, 3):
        raise ValueError("radius must be 1, 2 or 3")
    output = Path(sys.argv[2])
    if output.exists():
        raise ValueError("output exists; preserve experiment")
    output.mkdir(parents=True)
    spec = next(s for s in SPECS if s[0] == 172)
    n, k = spec[:2]
    assert (n, k) == (172, 21) and len(spec[5]) == 2
    history = []
    best = None
    best_distance = 0
    temp = output / ".candidate.tmp.json"
    start = time.perf_counter()
    for toggles in itertools.combinations(range(k), radius):
        proposed = copy.deepcopy(spec)
        proposed[5][1] = sorted(set(spec[5][1]).symmetric_difference(toggles), reverse=True)
        try:
            rows = construct(proposed)
        except ValueError as error:
            history.append({"toggles": toggles, "multiplier": proposed[5], "invalid": str(error)})
            continue
        spectrum = codes.spectrum(rows, n)
        distance = next(i for i in range(1, n + 1) if spectrum[i])
        cert = {
            "format": "binary-generator-v1", "q": 2, "n": n, "k": k, "d": distance,
            "rows": ["".join(str(r >> j & 1) for j in range(n)) for r in rows],
            "provenance": {
                "kind": "bounded-structured-search", "parent": str(PARENT.relative_to(ROOT)),
                "round_seed": SEED, "method": "toggle QC multiplier exponents", "toggles": toggles,
                "construction": proposed,
            },
        }
        temp.write_text(json.dumps(cert, indent=2) + "\n")
        assert large_verify.check(temp)["spectrum"] == spectrum
        history.append({
            "toggles": toggles, "multiplier": proposed[5], "d": distance,
            "minimum_words": spectrum[distance],
            "spectrum_sha256": hashlib.sha256(json.dumps(spectrum).encode()).hexdigest(),
        })
        if distance > best_distance:
            best_distance, best = distance, cert
    temp.unlink()
    assert len(history) == math.comb(k, radius) and best is not None
    best_path = output / "best-mutated.json"
    best_path.write_text(json.dumps(best, indent=2) + "\n")
    result = {
        "round_seed": SEED, "base": "76267c387538b4fb0e802278530b575bab4d1f76",
        "parent": str(PARENT.relative_to(ROOT)),
        "parent_sha256": hashlib.sha256(PARENT.read_bytes()).hexdigest(),
        "domain": f"All {math.comb(k, radius)} {radius}-exponent toggles of the second QC multiplier",
        "radius": radius,
        "target_d": 67, "best_mutated_d": best_distance,
        "best_mutated_sha256": hashlib.sha256(best_path.read_bytes()).hexdigest(),
        "valid": sum("d" in row for row in history),
        "invalid": sum("invalid" in row for row in history),
        "wins": sum(row.get("d", 0) > 66 for row in history),
        "ties": sum(row.get("d", 0) == 66 for row in history),
        "losses": sum(0 < row.get("d", 0) < 66 for row in history),
        "seconds": time.perf_counter() - start,
        "checker": "codes.spectrum and large_verify.check agreed on every valid proposal",
        "source_sha256": {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in (ROOT / "scripts/prepare_structured.py", ROOT / "scripts/codes.py",
                                       ROOT / "scripts/large_verify.py")},
        "history": history,
        "claim": "Finite search result for this multiplier neighborhood only; no optimality or record claim",
    }
    (output / f"radius{radius}-result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in ("radius", "valid", "invalid", "best_mutated_d", "wins", "ties", "losses", "seconds")}))


if __name__ == "__main__":
    main()
