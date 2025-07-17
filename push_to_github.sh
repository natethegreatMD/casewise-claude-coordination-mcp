#!/bin/bash
# Push CCC to GitHub after creating repo

echo "🚀 Pushing CCC to GitHub"
echo "======================="
echo ""
echo "First, create the repo at: https://github.com/new"
echo "Repository name: casewise-claude-coordination-mcp"
echo ""
echo "Then press Enter to continue..."
read

# Add remote and push
git remote add origin https://github.com/natethegreatMD/casewise-claude-coordination-mcp.git
git push -u origin main

echo "✅ Done! CCC is now on GitHub"