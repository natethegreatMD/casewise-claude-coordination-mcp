#!/bin/bash
# CCC Quick Start Script
# Gets you up and running with CCC in seconds

set -e

echo "🚀 CCC Quick Start"
echo "=================="
echo ""

# Check if already installed
if [ -f "ccc_venv/bin/activate" ]; then
    echo "✅ CCC already installed"
    echo ""
    echo "Activating environment..."
    source ccc_venv/bin/activate
else
    echo "📦 Installing CCC..."
    ./install.sh
    echo ""
    echo "Activating environment..."
    source ccc_venv/bin/activate
fi

# Show status
echo ""
echo "📊 Current Status:"
ccc status

# Offer options
echo ""
echo "What would you like to do?"
echo "1) Run Todo App demo"
echo "2) Start CCC orchestrator"
echo "3) Open documentation"
echo "4) Exit"
echo ""
read -p "Choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "🎭 Starting Todo App Demo..."
        echo "This will create 3 Claude sessions building a complete app!"
        echo ""
        read -p "Press Enter to continue..."
        
        # Start live monitor in background
        echo "Starting live monitor..."
        gnome-terminal -- bash -c "./scripts/watch_ccc.sh; exec bash" 2>/dev/null || \
        xterm -e "./scripts/watch_ccc.sh" 2>/dev/null || \
        echo "Please run ./scripts/watch_ccc.sh in another terminal"
        
        sleep 2
        
        # Run demo
        ccc demo
        ;;
        
    2)
        echo ""
        echo "🚀 Starting CCC Orchestrator..."
        ccc start
        ;;
        
    3)
        echo ""
        echo "📚 Opening documentation..."
        if command -v xdg-open &> /dev/null; then
            xdg-open README.md
        elif command -v open &> /dev/null; then
            open README.md
        else
            echo "Please open README.md in your editor"
        fi
        ;;
        
    4)
        echo "👋 Goodbye!"
        exit 0
        ;;
        
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "✨ CCC is ready to orchestrate!"