"""Évalue Kraken2 sur une communauté mock : précision, rappel, F1,
faux positifs, reads non classifiés et limite de détection."""
import argparse
import csv
import glob
import re
from pathlib import Path


def parse_report(path):
    """Lit un rapport Kraken2 -> (dict espèce -> reads, % non classifiés)."""
    species, unclassified = {}, 0.0
    with open(path) as f:
        for line in f:
            cols = line.rstrip("\n").split("\t")
            if len(cols) < 6:
                continue
            pct, clade_reads, _, rank, _, name = cols[:6]
            name = name.strip()
            if rank == "U":
                unclassified = float(pct)
            elif rank == "S":
                species[name] = int(clade_reads)
    return species, unclassified


def load_truth(path):
    with open(path) as f:
        return {r["species"]: float(r["abundance"]) for r in csv.DictReader(f)}


def evaluate(detected, truth, min_reads=10):
    """Compare espèces détectées (>= min_reads) à la vérité (abondance > 0)."""
    called = {s for s, n in detected.items() if n >= min_reads}
    expected = {s for s, a in truth.items() if a > 0}
    tp, fp, fn = called & expected, called - expected, expected - called
    precision = len(tp) / (len(tp) + len(fp)) if called else 0.0
    recall = len(tp) / len(expected) if expected else 0.0
    f1 = (2 * precision * recall / (precision + recall)
          if precision + recall else 0.0)
    return {"tp": sorted(tp), "fp": sorted(fp), "fn": sorted(fn),
            "precision": precision, "recall": recall, "f1": f1}


def detection_limit(result, truth):
    """Plus basse abondance vraie parmi les espèces détectées (None si aucune)."""
    found = [truth[s] for s in result["tp"]]
    return min(found) if found else None


def genus(name):
    return name.split()[0]


def fp_near_truth(fps, truth):
    """Pour chaque faux positif, indique s'il partage un genre avec une vraie espèce."""
    true_genera = {genus(s) for s, a in truth.items() if a > 0}
    return {s: genus(s) in true_genera for s in fps}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--truth", required=True)
    ap.add_argument("--reports", required=True, help="motif, ex: 'report_c*.txt'")
    ap.add_argument("--min-reads", type=int, default=10)
    ap.add_argument("--out", default="results.csv")
    args = ap.parse_args()

    truth = load_truth(args.truth)
    rows = []
    for rpt in sorted(glob.glob(args.reports)):
        c = float(re.search(r"_c([\d.]+)\.txt$", rpt).group(1))
        detected, unclass = parse_report(rpt)
        res = evaluate(detected, truth, args.min_reads)
        rows.append({
            "confidence": c,
            "precision": round(res["precision"], 3),
            "recall": round(res["recall"], 3),
            "f1": round(res["f1"], 3),
            "unclassified_pct": unclass,
            "detection_limit_pct": detection_limit(res, truth),
            "false_positives": ";".join(
                f"{s}{'*' if near else ''}"
                for s, near in fp_near_truth(res["fp"], truth).items()),
        })
    if not rows:
        raise SystemExit("Aucun rapport trouvé pour ce motif.")
    rows.sort(key=lambda r: r["confidence"])
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    print(Path(args.out).read_text())
    print("* = faux positif du même genre qu'une espèce réellement présente")


if __name__ == "__main__":
    main()
