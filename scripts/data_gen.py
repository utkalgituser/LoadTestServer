"""Generate test payloads in JSON or CSV for k6, JMeter, Postman runner."""
import argparse
import csv
import json
import random
import uuid
from pathlib import Path

CURRENCIES = ["USD", "EUR", "INR", "GBP", "JPY"]
SCENARIOS = ["success", "declined", "timeout", "slow"]


def gen_record() -> dict:
    return {
        "transactionId": f"TXN{uuid.uuid4().hex[:12].upper()}",
        "amount": round(random.uniform(1.0, 10000.0), 2),
        "currency": random.choice(CURRENCIES),
        "scenario": random.choice(SCENARIOS),
    }


def write_json(records: list[dict], out: Path) -> None:
    out.write_text(json.dumps(records, indent=2), encoding="utf-8")


def write_csv(records: list[dict], out: Path) -> None:
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(records[0].keys()))
        w.writeheader()
        w.writerows(records)


def main() -> None:
    p = argparse.ArgumentParser(description="Generate test payload data")
    p.add_argument("--count", type=int, default=100)
    p.add_argument("--format", choices=["json", "csv", "both"], default="both")
    p.add_argument("--out-dir", default="data")
    p.add_argument("--seed", type=int, default=None)
    a = p.parse_args()

    if a.seed is not None:
        random.seed(a.seed)

    out_dir = Path(a.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    records = [gen_record() for _ in range(a.count)]

    if a.format in ("json", "both"):
        write_json(records, out_dir / "payloads.json")
        print(f"wrote {a.count} -> {out_dir / 'payloads.json'}")
    if a.format in ("csv", "both"):
        write_csv(records, out_dir / "payloads.csv")
        print(f"wrote {a.count} -> {out_dir / 'payloads.csv'}")


if __name__ == "__main__":
    main()
