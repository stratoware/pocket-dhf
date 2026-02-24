# Copyright (c) 2025 Stratoware LLC
# Licensed under the MIT License. See LICENSE file in the project root.

"""Main entry point for the Pocket DHF application."""

import argparse

from app import create_app


def main():
    """Main entry point with command line argument support."""
    parser = argparse.ArgumentParser(
        description="Pocket DHF - Device History File Management"
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        help="Path to the data directory containing dhf_data.yaml, analyses/, and report-templates/ (default: sample-data)",
    )
    parser.add_argument(
        "--host", type=str, default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", type=int, default=8080, help="Port to bind to (default: 8080)"
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()

    # Create app with data directory
    app = create_app(data_dir=args.data_dir)

    # Override debug setting if specified
    if args.debug:
        app.config["DEBUG"] = True

    print("Starting Pocket DHF server...")
    if args.data_dir:
        print(f"Using data directory: {args.data_dir}")
    else:
        print("Using default data directory: sample-data")

    app.run(debug=app.config["DEBUG"], host=args.host, port=args.port)


if __name__ == "__main__":
    main()
