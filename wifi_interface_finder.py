#!/bin/bash
#==========================================================================
# WiFi Interface Finder and Fixer
# This script will find your actual wireless interface name and fix common issues
#==========================================================================

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}=== WiFi Interface Detective ===${NC}"
echo "Let's find your wireless interface and fix the issues..."
echo

# Step 1: Check all network interfaces
echo -e "${BLUE}Step 1: All network interfaces on your system:${NC}"
ip link show
echo

# Step 2: Check for wireless interfaces using multiple methods
echo -e "${BLUE}Step 2: Looking for wireless interfaces...${NC}"

# Method 1: Using iw dev
echo "Method 1 - Using 'iw dev':"
if command -v iw >/dev/null 2>&1; then
    IW_OUTPUT=$(iw dev 2>/dev/null)
    if [ -n "$IW_OUTPUT" ]; then
        echo "$IW_OUTPUT"
        WIFI_INTERFACE_IW=$(echo "$IW_OUTPUT" | awk '/Interface/ {print $2}' | head -1)
        if [ -n "$WIFI_INTERFACE_IW" ]; then
            echo -e "${GREEN}Found via iw: $WIFI_INTERFACE_IW${NC}"
        fi
    else
        echo "No output from 'iw dev'"
    fi
else
    echo "iw command not available"
fi
echo

# Method 2: Check /sys/class/net for wireless interfaces
echo "Method 2 - Checking /sys/class/net/*/wireless:"
WIFI_INTERFACE_SYS=""
for iface in /sys/class/net/*; do
    if [ -d "$iface/wireless" ]; then
        INTERFACE_NAME=$(basename "$iface")
        echo -e "${GREEN}Found wireless interface: $INTERFACE_NAME${NC}"
        WIFI_INTERFACE_SYS="$INTERFACE_NAME"
        break
    fi
done

if [ -z "$WIFI_INTERFACE_SYS" ]; then
    echo "No wireless interfaces found in /sys/class/net/"
fi
echo

# Method 3: Look for common wireless interface patterns
echo "Method 3 - Looking for common wireless patterns (wlan*, wlp*, wlx*):"
WIFI_INTERFACE_PATTERN=""
for pattern in wlan wlp wlx; do
    FOUND_IFACE=$(ip link show | grep -o "${pattern}[^:]*" | head -1)
    if [ -n "$FOUND_IFACE" ]; then
        echo -e "${GREEN}Found pattern match: $FOUND_IFACE${NC}"
        WIFI_INTERFACE_PATTERN="$FOUND_IFACE"
        break
    fi
done

if [ -z "$WIFI_INTERFACE_PATTERN" ]; then
    echo "No common wireless patterns found"
fi
echo

# Step 3: Determine the best interface
echo -e "${BLUE}Step 3: Determining your wireless interface...${NC}"

WIFI_INTERFACE=""
if [ -n "$WIFI_INTERFACE_IW" ]; then
    WIFI_INTERFACE="$WIFI_INTERFACE_IW"
    echo -e "${GREEN}Using interface from iw: $WIFI_INTERFACE${NC}"
elif [ -n "$WIFI_INTERFACE_SYS" ]; then
    WIFI_INTERFACE="$WIFI_INTERFACE_SYS"
    echo -e "${GREEN}Using interface from /sys: $WIFI_INTERFACE${NC}"
elif [ -n "$WIFI_INTERFACE_PATTERN" ]; then
    WIFI_INTERFACE="$WIFI_INTERFACE_PATTERN"
    echo -e "${GREEN}Using pattern match: $WIFI_INTERFACE${NC}"
else
    echo -e "${RED}❌ No wireless interface found!${NC}"
fi

# Step 4: Check USB and driver status
echo
echo -e "${BLUE}Step 4: Checking USB adapter and driver status...${NC}"

echo "USB Realtek devices:"
USB_REALTEK=$(lsusb | grep -i realtek)
if [ -n "$USB_REALTEK" ]; then
    echo -e "${GREEN}✅ $USB_REALTEK${NC}"
else
    echo -e "${RED}❌ No Realtek USB devices found${NC}"
    echo "   This means your USB adapter isn't detected"
fi

echo
echo "Loaded RTL modules:"
RTL_MODULES=$(lsmod | grep -E "(rtl|8821|8811)")
if [ -n "$RTL_MODULES" ]; then
    echo -e "${GREEN}✅ RTL modules loaded:${NC}"
    echo "$RTL_MODULES"
else
    echo -e "${RED}❌ No RTL modules loaded${NC}"
    echo "   This means the driver isn't loaded"
fi

echo
echo "Kernel messages about RTL:"
RTL_DMESG=$(dmesg | grep -i rtl | tail -5)
if [ -n "$RTL_DMESG" ]; then
    echo "$RTL_DMESG"
else
    echo "No RTL messages in kernel log"
fi

# Step 5: Provide specific solutions
echo
echo -e "${CYAN}=== DIAGNOSIS AND SOLUTIONS ===${NC}"

if [ -n "$WIFI_INTERFACE" ]; then
    echo -e "${GREEN}🎉 SUCCESS: Found your wireless interface!${NC}"
    echo -e "${GREEN}Your interface name is: $WIFI_INTERFACE${NC}"
    echo
    echo "✅ Correct commands for your system:"
    echo "   sudo ip link set $WIFI_INTERFACE down"
    echo "   sudo iw dev $WIFI_INTERFACE set type monitor"
    echo "   sudo ip link set $WIFI_INTERFACE up"
    echo
    echo "✅ Check interface status:"
    echo "   iwconfig $WIFI_INTERFACE"
    echo "   iw dev $WIFI_INTERFACE info"
    echo
    echo "✅ For the game, use:"
    echo "   python3 rocoren_security_game.py -i $WIFI_INTERFACE"
    
    # Test the interface
    echo
    echo -e "${BLUE}Testing your interface...${NC}"
    if iwconfig "$WIFI_INTERFACE" 2>/dev/null | grep -q "IEEE 802.11"; then
        echo -e "${GREEN}✅ Interface is working with iwconfig${NC}"
    else
        echo -e "${YELLOW}⚠️  iwconfig test failed, trying iw...${NC}"
        if iw dev "$WIFI_INTERFACE" info >/dev/null 2>&1; then
            echo -e "${GREEN}✅ Interface is working with iw${NC}"
        else
            echo -e "${RED}❌ Interface tests failed${NC}"
        fi
    fi
    
else
    echo -e "${RED}❌ PROBLEM: No wireless interface found${NC}"
    echo
    echo "This usually means:"
    echo "1. 🔌 USB adapter not properly connected"
    echo "2. 🚫 Driver not installed or loaded"
    echo "3. ⚡ USB power issue"
    echo
    echo "🔧 Troubleshooting steps:"
    
    if [ -z "$USB_REALTEK" ]; then
        echo "1. USB CONNECTION ISSUE:"
        echo "   - Unplug and reconnect the USB adapter"
        echo "   - Try a different USB port"
        echo "   - Check if the adapter LED lights up (if it has one)"
        echo "   - Test the adapter on another computer"
        echo
    fi
    
    if [ -z "$RTL_MODULES" ]; then
        echo "2. DRIVER NOT LOADED:"
        echo "   - Install the driver:"
        echo "     git clone https://github.com/morrownr/8821cu-20210916.git"
        echo "     cd 8821cu-20210916"
        echo "     sudo ./install-driver.sh"
        echo
        echo "   - Or try loading manually:"
        echo "     sudo modprobe 8821cu"
        echo
        echo "   - Check for conflicts:"
        echo "     sudo modprobe -r rtl8xxxu"
        echo "     sudo modprobe 8821cu"
        echo
    fi
    
    echo "3. GENERAL FIXES:"
    echo "   - Reboot your system"
    echo "   - Update your kernel: sudo pacman -Syu"
    echo "   - Check dmesg for errors: dmesg | grep -i usb"
    echo
fi

# Step 6: Create a personal config file
echo
echo -e "${BLUE}Creating personal configuration...${NC}"

cat > ~/my_rocoren_config.sh << EOF
#!/bin/bash
# Personal ROCOREN configuration for your system
# Generated on $(date)

# Your wireless interface name
export WIFI_INTERFACE="$WIFI_INTERFACE"

# Quick commands for your system
echo "=== Your ROCOREN Commands ==="
echo "Interface: \$WIFI_INTERFACE"
echo

if [ -n "\$WIFI_INTERFACE" ]; then
    echo "Enable monitor mode:"
    echo "  sudo ip link set \$WIFI_INTERFACE down"
    echo "  sudo iw dev \$WIFI_INTERFACE set type monitor"
    echo "  sudo ip link set \$WIFI_INTERFACE up"
    echo
    
    echo "Disable monitor mode:"
    echo "  sudo ip link set \$WIFI_INTERFACE down"
    echo "  sudo iw dev \$WIFI_INTERFACE set type managed"
    echo "  sudo ip link set \$WIFI_INTERFACE up"
    echo
    
    echo "Check status:"
    echo "  iwconfig \$WIFI_INTERFACE"
    echo "  iw dev \$WIFI_INTERFACE info"
    echo
    
    echo "Start game:"
    echo "  python3 rocoren_security_game.py -i \$WIFI_INTERFACE"
else
    echo "❌ No wireless interface found. Run the diagnostic script again after fixing driver issues."
fi

# Functions for easy use
monitor_enable() {
    if [ -n "\$WIFI_INTERFACE" ]; then
        sudo ip link set \$WIFI_INTERFACE down
        sudo iw dev \$WIFI_INTERFACE set type monitor
        sudo ip link set \$WIFI_INTERFACE up
        echo "Monitor mode enabled on \$WIFI_INTERFACE"
    else
        echo "No wireless interface configured"
    fi
}

monitor_disable() {
    if [ -n "\$WIFI_INTERFACE" ]; then
        sudo ip link set \$WIFI_INTERFACE down
        sudo iw dev \$WIFI_INTERFACE set type managed
        sudo ip link set \$WIFI_INTERFACE up
        echo "Monitor mode disabled on \$WIFI_INTERFACE"
    else
        echo "No wireless interface configured"
    fi
}

wifi_status() {
    if [ -n "\$WIFI_INTERFACE" ]; then
        echo "Interface: \$WIFI_INTERFACE"
        iwconfig \$WIFI_INTERFACE 2>/dev/null || iw dev \$WIFI_INTERFACE info
    else
        echo "No wireless interface configured"
    fi
}

# Export functions
export -f monitor_enable monitor_disable wifi_status
EOF

chmod +x ~/my_rocoren_config.sh

echo -e "${GREEN}✅ Personal config saved to ~/my_rocoren_config.sh${NC}"
echo

# Final summary
echo -e "${CYAN}=== SUMMARY ===${NC}"
if [ -n "$WIFI_INTERFACE" ]; then
    echo -e "${GREEN}🎉 SUCCESS!${NC}"
    echo "• Your wireless interface: $WIFI_INTERFACE"
    echo "• Use this name instead of 'wlan0' in all commands"
    echo "• Load your config: source ~/my_rocoren_config.sh"
    echo "• Quick commands: monitor_enable, monitor_disable, wifi_status"
else
    echo -e "${RED}❌ NEEDS ATTENTION${NC}"
    echo "• No wireless interface found"
    echo "• Follow the troubleshooting steps above"
    echo "• Run this script again after fixing the driver"
fi

echo
echo "Next steps:"
echo "1. Fix any issues identified above"
echo "2. Run: source ~/my_rocoren_config.sh"
echo "3. Test: wifi_status"
echo "4. Enable monitor: monitor_enable"
