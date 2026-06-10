from __future__ import annotations

from context_ops import append_decision, build_decision_parser


def main() -> int:
    parser = build_decision_parser()
    args = parser.parse_args()
    append_decision(
        args.project_root,
        {
            "number": args.number,
            "title": args.title,
            "status": args.status,
            "date": args.date,
            "context": args.context,
            "decision": args.decision,
            "tradeoffs": args.tradeoffs,
            "consequences": args.consequences,
            "supersedes": args.supersedes,
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
