from __future__ import annotations

from context_ops import build_bug_parser, record_bug


def main() -> int:
    parser = build_bug_parser()
    args = parser.parse_args()
    record_bug(
        args.project_root,
        {
            "title": args.title,
            "symptom": args.symptom,
            "trigger": args.trigger,
            "impact": args.impact,
            "root_cause": args.root_cause,
            "resolution": args.resolution,
            "prevention": args.prevention,
            "status": args.status,
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
