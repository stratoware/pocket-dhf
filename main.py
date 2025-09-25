# Copyright (c) 2025 Stratoware LLC. All rights reserved.

"""Main entry point for the Pocket DHF application."""

import argparse
import os
import sys

from app import create_app

def main():
    """Main entry point with command line argument support."""
    parser = argparse.ArgumentParser(description="Pocket DHF - Device History File Management")
    parser.add_argument(
        "--data-file",
        type=str,
        help="Path to the YAML data file (default: sample-data/dhf_data.yaml)"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Port to bind to (default: 8080)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )
    
    args = parser.parse_args()
    
    # Create app with data file path
    app = create_app(data_file_path=args.data_file)
    
    # Override debug setting if specified
    if args.debug:
        app.config["DEBUG"] = True
    
    print(f"Starting Pocket DHF server...")
    if args.data_file:
        print(f"Using data file: {args.data_file}")
    else:
        print(f"Using default data file: sample-data/dhf_data.yaml")
    
    app.run(debug=app.config["DEBUG"], host=args.host, port=args.port)

if __name__ == "__main__":
    main()
