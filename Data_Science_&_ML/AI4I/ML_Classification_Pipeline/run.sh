#!/bin/bash

# Default config file path
CONFIG_FILE="src/config.json"

# Parse command-line arguments for config file
while getopts ":c:" opt; do
  case $opt in
    c) CONFIG_FILE="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

# Run the main Python script with the specified config file
python3 src/main.py --config "$CONFIG_FILE"
