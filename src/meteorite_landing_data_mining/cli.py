"""Command-line entry point: regenerate every figure from the raw dataset."""

from __future__ import annotations

from .common import load_landings, use_style
from .figures import MODULES


def main() -> None:
    use_style()
    df = load_landings()
    for module in MODULES:
        print(f"saved {module.main(df)}")


if __name__ == "__main__":
    main()
