import re
import sys
from pathlib import Path


ALLOWED_CATEGORIES = {"feat", "fix", "docs", "refactor", "build", "chore"}
SUBJECT_PATTERN = re.compile(r"^(?P<category>[a-z][a-z0-9-]*): .+\S$")


def main() -> int:
    if len(sys.argv) != 2:
        print("Expected the path to one commit message file.", file=sys.stderr)
        return 2

    message_path = Path(sys.argv[1])
    try:
        message = message_path.read_text(encoding="utf-8")
    except OSError as error:
        print(f"Could not read commit message: {error}", file=sys.stderr)
        return 2

    if message.endswith("\n"):
        message = message[:-1]

    if not message:
        print("Commit message cannot be empty.", file=sys.stderr)
        return 1

    subject, separator, body = message.partition("\n\n")
    subject_match = SUBJECT_PATTERN.fullmatch(subject)
    if subject_match is None:
        print(
            "Commit subject must use 'category: small explanation' "
            "(for example, 'feat: add window support').",
            file=sys.stderr,
        )
        return 1

    category = subject_match.group("category")
    if category not in ALLOWED_CATEGORIES:
        print(
            "Commit category must be one of: "
            + ", ".join(sorted(ALLOWED_CATEGORIES))
            + ".",
            file=sys.stderr,
        )
        return 1

    if separator and not body.strip():
        print("The complementary explanation cannot be empty.", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
