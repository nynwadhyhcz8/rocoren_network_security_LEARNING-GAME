#!/bin/bash
# Run ROCOREN game with real hardware
echo "🎮 Starting ROCOREN Game..."
if [ "$EUID" -ne 0 ]; then
    echo "⚠️  Some features require root privileges"
    echo "   Run with: sudo ./run_game.sh"
    echo "   Or use demo mode: ./run_demo.sh"
    echo
fi
python3 game_main.py -i wlp2s0
