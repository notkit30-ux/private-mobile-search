from __future__ import annotations

from pathlib import Path


def main() -> None:
    base = Path(__file__).resolve().parent
    print(f"private-mobile-search project scaffold created at: {base.parent}")


if __name__ == "__main__":
    main()
