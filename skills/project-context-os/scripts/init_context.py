from __future__ import annotations

from pathlib import Path

from context_ops import build_init_parser, initialize_context


def main() -> int:
    parser = build_init_parser()
    args = parser.parse_args()
    project_root = Path(args.project_root).resolve()
    project_name = args.project_name or project_root.name
    created = initialize_context(project_root, project_name=project_name)
    for path in created:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
