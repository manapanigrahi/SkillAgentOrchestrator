from __future__ import annotations

import argparse
from pathlib import Path

from .orchestrator import TestCycleOrchestrator


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a traceable QA pack from SRS and SDS DOCX files.")
    parser.add_argument("--srs", required=True, type=Path)
    parser.add_argument("--sds", required=True, type=Path)
    parser.add_argument("--out", default=Path("Output"), type=Path)
    args = parser.parse_args()
    cycle = TestCycleOrchestrator().run(args.srs, args.sds, args.out)
    print(f"Generated {len(cycle.scenarios)} scenarios and {len(cycle.cases)} test cases in {args.out}")


if __name__ == "__main__":
    main()
