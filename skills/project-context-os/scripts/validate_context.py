from __future__ import annotations

from context_ops import build_validate_parser, validate_context


def main() -> int:
    parser = build_validate_parser()
    args = parser.parse_args()
    result = validate_context(args.project_root)
    if result.ok:
        print("context is valid")
        return 0
    for error in result.errors:
        print(error)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
