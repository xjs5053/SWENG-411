#!/bin/bash

echo "========================================"
echo "Starting FileSense..."
echo "========================================"
echo ""

python3 main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "========================================"
    echo "FileSense crashed!"
    echo "========================================"
    read -p "Press Enter to exit..."
fi
