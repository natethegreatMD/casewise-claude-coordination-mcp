# How to Watch CCC Sessions Live

## Where to Run: Ubuntu (WSL) Terminal

**NOT PowerShell** - Must be Ubuntu/WSL terminal

## Step-by-Step Instructions

### Terminal 1 (This Claude session):
```bash
# Already here - I'll run CCC and spawn Claude sessions
cd /mnt/c/Users/Mike/Documents/CasewiseMD-workspace/Claude\ Code\ Coordinator
```

### Terminal 2 (Your monitoring terminal):
1. Open a new **Ubuntu/WSL terminal** (not PowerShell)
2. Run these commands:

```bash
# Navigate to CCC directory
cd /mnt/c/Users/Mike/Documents/CasewiseMD-workspace/Claude\ Code\ Coordinator

# Make sure the watcher script is executable
chmod +x watch_ccc.sh

# Run the live watcher
./watch_ccc.sh
```

Or if you prefer the direct Python command:
```bash
# Navigate to CCC directory
cd /mnt/c/Users/Mike/Documents/CasewiseMD-workspace/Claude\ Code\ Coordinator

# Activate the CCC environment
source activate_ccc.sh

# Run the watcher
python ccc_live_watcher.py .
```

## What You'll See

When I spawn Claude sessions, your monitoring terminal will show:
- 🔴 New sessions starting
- 📁 Files being created in real-time
- 📥 Live output from Claude sessions
- ✨ Progress updates with timestamps

## Quick Test

Want to see it work right now? 
1. Open your Ubuntu terminal
2. Navigate to the directory above
3. Run `./watch_ccc.sh`
4. Tell me when you're ready and I'll spawn a test session!