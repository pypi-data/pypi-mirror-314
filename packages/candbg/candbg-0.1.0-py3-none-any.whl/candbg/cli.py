#!/usr/bin/env python3

import argparse
from pathlib import Path
from candbg import inspector


def main():
    parser = argparse.ArgumentParser(description="candbg CLI")
    parser.add_argument("dbc_file", help="Path to the DBC file")
    parser.add_argument(
        "-i",
        "--interface",
        default="socketcan",
        help="Interface type (default: %(default)s)",
    )
    parser.add_argument(
        "-c", "--channel", default="can0", help="CAN channel (default: %(default)s)"
    )

    args = parser.parse_args()

    # Show the parsed arguments
    print(f"DBC File: {args.dbc_file}")
    print(f"Interface: {args.interface}")
    print(f"Channel: {args.channel}")

    # Check if the DBC file exists
    dbc_file = Path(args.dbc_file)
    if not dbc_file.exists():
        print(f"Error: DBC file not found: {dbc_file}")
        return

    try:
        inspector.main(dbc_file, args.interface, args.channel)
    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    main()
