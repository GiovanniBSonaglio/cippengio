import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def run(command):
    print("+", " ".join(command), flush=True)
    subprocess.run(command, cwd=str(PROJECT_ROOT), check=True)


def main():
    run([
        "git",
        "submodule",
        "update",
        "--init",
        "--recursive",
    ])
    run(["cmake", "--preset", "release"])
    run(["cmake", "--build", "--preset", "release"])
    run(["cmake", "--install", "build/release", "--config", "Release"])
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except FileNotFoundError as error:
        print("Required command not found: " + str(error), file=sys.stderr)
        raise SystemExit(127)
    except subprocess.CalledProcessError as error:
        print(
            "Build command failed with exit code " + str(error.returncode),
            file=sys.stderr,
        )
        raise SystemExit(error.returncode)
