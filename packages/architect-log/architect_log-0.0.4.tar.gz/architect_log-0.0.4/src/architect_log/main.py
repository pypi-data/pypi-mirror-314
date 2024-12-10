import argparse
from pathlib import Path

from .templates import ADR_TEMPLATE, ADR_TEMPLATE_MINIMAL


def get_next_adr_number(directory: str = "docs/adr") -> int:
    output_dir = Path(directory)
    if not output_dir.exists():
        return 1

    adr_files = list(output_dir.glob("*.md"))
    numbers = []
    for file in adr_files:
        try:
            number = int(file.stem.split("-", 1)[0])
            numbers.append(number)
        except (ValueError, IndexError):
            continue

    return max(numbers, default=0) + 1


def add(
    title: str,
    status: str = "Proposed",
    template: str = "normal",
    directory: str = "docs/adr",
) -> None:
    try:
        number = f"{get_next_adr_number(directory):03}"
        adr_content = template.format(number=number, title=title, status=status)

        output_dir = Path(directory)
        output_dir.mkdir(parents=True, exist_ok=True)

        filename = output_dir / f"{number}-{title.lower().replace(' ', '-')}.md"
        filename.write_text(adr_content, encoding="utf-8")

        print(f"✅ ADR created successfully: {filename}")

    except Exception as e:
        print(f"❌ Error creating ADR: {e}")


def main():
    parser = argparse.ArgumentParser(description="CLI for managing ADRs.")
    subparsers = parser.add_subparsers(title="commands", dest="command", required=True)

    parser_add = subparsers.add_parser("add", help="Create a new ADR")
    parser_add.add_argument("title", type=str, help="The title of the ADR.")
    parser_add.add_argument(
        "--status",
        type=str,
        default="Proposed",
        choices=["Proposed", "Accepted", "Deprecated"],
        help="The status of the ADR. Options: Proposed, Accepted, Deprecated (default: Proposed).",
    )
    parser_add.add_argument(
        "--template",
        type=str,
        choices=["normal", "minimal"],
        default="normal",
        help="The template to use. Options: normal, minimal (default: normal).",
    )

    args = parser.parse_args()

    # Select the appropriate template
    template = ADR_TEMPLATE if args.template == "normal" else ADR_TEMPLATE_MINIMAL

    if args.command == "add":
        add(args.title, args.status, template)


if __name__ == "__main__":
    main()
