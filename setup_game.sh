#!/bin/bash
#==========================================================================
# ROCOREN WiFi Security Game - Quick Setup Script
# This script helps you set up all 4 game files quickly
#==========================================================================

echo "🎮 ROCOREN WiFi Security Game Setup"
echo "==================================="
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Step 1: Check if we're in the right directory
print_step "Checking setup..."

if [ ! -f "game_main.py" ]; then
    print_error "game_main.py not found!"
    echo "Please make sure all 4 game files are in the current directory:"
    echo "  - game_main.py"
    echo "  - game_classes.py" 
    echo "  - game_challenges.py"
    echo "  - game_utils.py"
    exit 1
fi

# Step 2: Check required files
print_step "Checking game files..."

required_files=("game_main.py" "game_classes.py" "game_challenges.py" "game_utils.py")
missing_files=()

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        print_success "Found $file"
    else
        missing_files+=("$file")
        print_error "Missing $file"
    fi
done

if [ ${#missing_files[@]} -gt 0 ]; then
    print_error "Missing required files. Please download all 4 parts of the game."
    exit 1
fi

# Step 3: Make files executable
print_step "Making files executable..."
chmod +x game_main.py game_classes.py game_challenges.py game_utils.py
print_success "Files made executable"

# Step 4: Check Python and packages
print_step "Checking Python requirements..."

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
if python3 -c "import sys; exit(0 if sys.version_info >= (3,6) else 1)"; then
    print_success "Python $python_version - OK"
else
    print_error "Python 3.6+ required, found $python_version"
    exit 1
fi

# Check required packages
required_packages=("rich" "colorama")
missing_packages=()

for package in "${required_packages[@]}"; do
    if python3 -c "import $package" 2>/dev/null; then
        print_success "Package $package - OK"
    else
        missing_packages+=("$package")
        print_warning "Package $package - Missing"
    fi
done

# Install missing packages
if [ ${#missing_packages[@]} -gt 0 ]; then
    print_step "Installing missing Python packages..."
    pip3 install --user "${missing_packages[@]}"
    
    # Verify installation
    for package in "${missing_packages[@]}"; do
        if python3 -c "import $package" 2>/dev/null; then
            print_success "Successfully installed $package"
        else
            print_error "Failed to install $package"
        fi
    done
fi

# Step 5: Check optional packages
print_step "Checking optional packages..."

optional_packages=("scapy" "pygame")
for package in "${optional_packages[@]}"; do
    if python3 -c "import $package" 2>/dev/null; then
        print_success "Optional package $package - Available"
    else
        print_warning "Optional package $package - Not installed"
        echo "  Install with: pip3 install --user $package"
    fi
done

# Step 6: Check wireless tools
print_step "Checking wireless tools..."

wireless_tools=("iw" "iwconfig" "iwlist")
for tool in "${wireless_tools[@]}"; do
    if command -v "$tool" >/dev/null 2>&1 || [ -x "/sbin/$tool" ] || [ -x "/usr/sbin/$tool" ]; then
        print_success "Tool $tool - Available"
    else
        print_warning "Tool $tool - Not found"
    fi
done

# Provide installation instructions for missing tools
if ! command -v "iw" >/dev/null 2>&1 && ! [ -x "/sbin/iw" ]; then
    echo
    print_warning "Wireless tools not found. Install with:"
    echo "  Ubuntu/Debian: sudo apt install wireless-tools iw net-tools"
    echo "  Arch Linux:    sudo pacman -S wireless_tools iw net-tools" 
    echo "  Fedora:        sudo dnf install wireless-tools iw net-tools"
fi

# Step 7: Check wireless interfaces
print_step "Checking wireless interfaces..."

# Method 1: Check /sys/class/net
interfaces=()
if [ -d "/sys/class/net" ]; then
    for iface in /sys/class/net/*; do
        if [ -d "$iface/wireless" ]; then
            interface_name=$(basename "$iface")
            interfaces+=("$interface_name")
            print_success "Found wireless interface: $interface_name"
        fi
    done
fi

# Method 2: Try iw dev command
if command -v iw >/dev/null 2>&1; then
    iw_interfaces=$(iw dev 2>/dev/null | awk '/Interface/ {print $2}')
    for iface in $iw_interfaces; do
        if [[ ! " ${interfaces[@]} " =~ " ${iface} " ]]; then
            interfaces+=("$iface")
            print_success "Found wireless interface: $iface"
        fi
    done
elif [ -x "/sbin/iw" ]; then
    iw_interfaces=$(/sbin/iw dev 2>/dev/null | awk '/Interface/ {print $2}')
    for iface in $iw_interfaces; do
        if [[ ! " ${interfaces[@]} " =~ " ${iface} " ]]; then
            interfaces+=("$iface")
            print_success "Found wireless interface: $iface"
        fi
    done
fi

if [ ${#interfaces[@]} -eq 0 ]; then
    print_warning "No wireless interfaces found"
    echo "  Make sure your ROCOREN USB adapter is connected"
    echo "  You can still play in demo mode"
    RECOMMENDED_INTERFACE="wlp2s0"
else
    RECOMMENDED_INTERFACE="${interfaces[0]}"
    print_success "Recommended interface: $RECOMMENDED_INTERFACE"
fi

# Step 8: Create game directories
print_step "Creating game directories..."

mkdir -p ~/rocoren_game_data
mkdir -p ~/rocoren_game_logs
print_success "Game directories created"

# Step 9: Test the game
print_step "Testing game installation..."

if python3 game_main.py --check -i "$RECOMMENDED_INTERFACE" >/dev/null 2>&1; then
    print_success "Game installation test passed"
else
    print_warning "Game installation test had issues (this may be normal)"
fi

# Step 10: Create convenience scripts
print_step "Creating convenience scripts..."

# Create demo mode script
cat > run_demo.sh << EOF
#!/bin/bash
# Run ROCOREN game in demo mode (no hardware needed)
echo "🎭 Starting ROCOREN Game in Demo Mode..."
python3 game_main.py --demo
EOF
chmod +x run_demo.sh

# Create real mode script
cat > run_game.sh << EOF
#!/bin/bash
# Run ROCOREN game with real hardware
echo "🎮 Starting ROCOREN Game..."
if [ "\$EUID" -ne 0 ]; then
    echo "⚠️  Some features require root privileges"
    echo "   Run with: sudo ./run_game.sh"
    echo "   Or use demo mode: ./run_demo.sh"
    echo
fi
python3 game_main.py -i $RECOMMENDED_INTERFACE
EOF
chmod +x run_game.sh

# Create setup check script
cat > check_system.sh << EOF
#!/bin/bash
# Check system requirements for ROCOREN game
echo "🔧 ROCOREN System Check..."
python3 game_main.py --check -i $RECOMMENDED_INTERFACE
EOF
chmod +x check_system.sh

print_success "Created convenience scripts:"
echo "  - run_demo.sh     (demo mode - no hardware needed)"
echo "  - run_game.sh     (real mode - with ROCOREN adapter)"
echo "  - check_system.sh (system diagnostics)"

# Final summary
echo
echo -e "${CYAN}=== SETUP COMPLETE ===${NC}"
echo
print_success "🎉 ROCOREN WiFi Security Game is ready!"
echo
echo "📋 Quick Start Guide:"
echo "  1. Demo Mode (practice):    ./run_demo.sh"
echo "  2. Real Mode (with adapter): ./run_game.sh"
echo "  3. System Check:            ./check_system.sh"
echo "  4. Manual run:              python3 game_main.py --help"
echo
echo "🎯 Recommended Interface: $RECOMMENDED_INTERFACE"
echo "📁 Game data saved to: ~/rocoren_game_data/"
echo "📝 Logs saved to: ~/rocoren_game_logs/"
echo
echo "⚠️  Remember: Only use on networks you own or have permission to test!"
echo "🎓 This tool is for educational purposes only."
echo
echo "🚀 Ready to start learning WiFi security? Run: ./run_demo.sh"
echo
