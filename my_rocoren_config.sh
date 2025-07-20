#!/bin/bash
# Personal ROCOREN configuration for your system
# Generated on Sun Jul 20 08:34:25 AM +07 2025

# Your wireless interface name
export WIFI_INTERFACE="wlp2s0"

# Quick commands for your system
echo "=== Your ROCOREN Commands ==="
echo "Interface: $WIFI_INTERFACE"
echo

if [ -n "$WIFI_INTERFACE" ]; then
    echo "Enable monitor mode:"
    echo "  sudo ip link set $WIFI_INTERFACE down"
    echo "  sudo iw dev $WIFI_INTERFACE set type monitor"
    echo "  sudo ip link set $WIFI_INTERFACE up"
    echo
    
    echo "Disable monitor mode:"
    echo "  sudo ip link set $WIFI_INTERFACE down"
    echo "  sudo iw dev $WIFI_INTERFACE set type managed"
    echo "  sudo ip link set $WIFI_INTERFACE up"
    echo
    
    echo "Check status:"
    echo "  iwconfig $WIFI_INTERFACE"
    echo "  iw dev $WIFI_INTERFACE info"
    echo
    
    echo "Start game:"
    echo "  python3 rocoren_security_game.py -i $WIFI_INTERFACE"
else
    echo "❌ No wireless interface found. Run the diagnostic script again after fixing driver issues."
fi

# Functions for easy use
monitor_enable() {
    if [ -n "$WIFI_INTERFACE" ]; then
        sudo ip link set $WIFI_INTERFACE down
        sudo iw dev $WIFI_INTERFACE set type monitor
        sudo ip link set $WIFI_INTERFACE up
        echo "Monitor mode enabled on $WIFI_INTERFACE"
    else
        echo "No wireless interface configured"
    fi
}

monitor_disable() {
    if [ -n "$WIFI_INTERFACE" ]; then
        sudo ip link set $WIFI_INTERFACE down
        sudo iw dev $WIFI_INTERFACE set type managed
        sudo ip link set $WIFI_INTERFACE up
        echo "Monitor mode disabled on $WIFI_INTERFACE"
    else
        echo "No wireless interface configured"
    fi
}

wifi_status() {
    if [ -n "$WIFI_INTERFACE" ]; then
        echo "Interface: $WIFI_INTERFACE"
        iwconfig $WIFI_INTERFACE 2>/dev/null || iw dev $WIFI_INTERFACE info
    else
        echo "No wireless interface configured"
    fi
}

# Export functions
export -f monitor_enable monitor_disable wifi_status
