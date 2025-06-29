#!/bin/bash
# Git History Cleanup Script
# Run this in Git Bash

echo "🧹 Starting Git History Cleanup..."
echo "📍 Working in: $(pwd)"

# Step 1: Create replacement patterns
cat > replacements.txt << 'EOF'
regex:[0-9]+-[a-zA-Z0-9]+\.apps\.googleusercontent\.com==>REDACTED-CLIENT-ID
regex:GOCSPX-[a-zA-Z0-9_-]+===>REDACTED-CLIENT-SECRET
regex:[a-zA-Z0-9._%+-]+@gmail\.com===>REDACTED-EMAIL
regex:django-insecure-[a-zA-Z0-9=+!@#$%^&*()_-]+===>REDACTED-SECRET-KEY
regex:postgresql://[^\s]+===>REDACTED-DATABASE-URL
regex:psql://[^\s]+===>REDACTED-DATABASE-URL
EOF

echo "✅ Created replacement patterns"

# Step 2: Apply git filter-repo
echo "🔄 Applying git filter-repo..."
git filter-repo --force --replace-text replacements.txt

echo "✅ Git history cleaned"

# Step 3: Clean up references
echo "🧽 Cleaning up git references..."
git remote remove origin
git for-each-ref --format="delete %(refname)" refs/original | git update-ref --stdin 2>/dev/null || true
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo "✅ References cleaned"

# Step 4: Re-add remote
echo "🔗 Re-adding GitHub remote..."
git remote add origin https://github.com/Rupesh-110805/django-chat-app.git

# Step 5: Verify cleanup
echo "🔍 Verifying cleanup..."
SECRETS_FOUND=$(git log --all --oneline | xargs -I {} git show {} | grep -c "GOCSPX-\|\.apps\.googleusercontent\.com" 2>/dev/null || echo "0")

if [ "$SECRETS_FOUND" -eq 0 ]; then
    echo "✅ No secrets found in history!"
    echo "🚀 Ready to push. Run: git push --force-with-lease origin master"
else
    echo "⚠️  Still found $SECRETS_FOUND potential secrets. Manual review needed."
fi

echo "🎉 Cleanup complete!"
echo ""
echo "Next steps:"
echo "1. Run: git push --force-with-lease origin master"
echo "2. If GitHub still blocks, the secrets might be in different format"
echo "3. Check the GIT_HISTORY_CLEANUP.md file for troubleshooting"

# Clean up temp file
rm -f replacements.txt
