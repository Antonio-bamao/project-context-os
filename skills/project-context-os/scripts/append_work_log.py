from __future__ import annotations

from context_ops import append_work_log, build_work_log_parser


def main() -> int:
    parser = build_work_log_parser()
    args = parser.parse_args()
    append_work_log(
        args.project_root,
        {
            "time": args.time,
            "goal": args.goal,
            "actions": args.actions,
            "result": args.result,
            "verification": args.verification,
            "next_step": args.next_step,
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
