# 🧹 **Git History Cleanup Guide - Remove Secrets from ALL Commits**

## ⚠️ **CRITICAL: Follow this order exactly!**

### **Step 1: Verify Backups (Already Done ✅)**
- ✅ Backup at: `c:\Users\rupes\Project\django-chat-app-backup`
- ✅ Clean backup at: `c:\Users\rupes\django-chat-clean-backup`

### **Step 2: Check Current Remote URL**
```powershell
cd c:\Users\rupes\Project\django-chat-app-main
git remote -v
```

### **Step 3: Create Secrets Removal Script**
Create a file called `secrets.txt` with the exact secrets to remove:

**Option A: If you know the exact secret values, create secrets.txt:**
```
your-actual-google-client-id-here.apps.googleusercontent.com
GOCSPX-your-actual-secret-here
your-actual-email@gmail.com
your-actual-app-password
psql://your-actual-database-url
django-insecure-your-actual-secret-key
```

**Option B: Use pattern-based removal (safer, recommended):**

### **Step 4: Remove Secrets Using git-filter-repo**

#### **Method 1: Remove by exact text patterns (RECOMMENDED)**
```powershell
cd c:\Users\rupes\Project\django-chat-app-main

# Remove Google OAuth Client IDs (pattern: ends with .apps.googleusercontent.com)
git filter-repo --force --replace-text <(echo "regex:[\w-]+\.apps\.googleusercontent\.com=>[REDACTED-CLIENT-ID]")

# Remove Google OAuth Secrets (pattern: starts with GOCSPX-)
git filter-repo --force --replace-text <(echo "regex:GOCSPX-[\w-]+=>[REDACTED-CLIENT-SECRET]")

# Remove email addresses
git filter-repo --force --replace-text <(echo "regex:[\w.-]+@gmail\.com=>[REDACTED-EMAIL]")

# Remove Django secret keys
git filter-repo --force --replace-text <(echo "regex:django-insecure-[\w-+=!$()^&*@#%]+=[REDACTED-SECRET-KEY]")

# Remove PostgreSQL URLs
git filter-repo --force --replace-text <(echo "regex:postgresql://[\w:@.-/]+=[REDACTED-DATABASE-URL]")
```

#### **Method 2: Remove specific files from history (if patterns don't work)**
```powershell
# Remove specific files completely from history
git filter-repo --force --path GOOGLE_OAUTH_PRODUCTION.md --invert-paths
git filter-repo --force --path mysite/chatapp/management/commands/setup_production_oauth.py --invert-paths
```

### **Step 5: Clean up references**
```powershell
# Remove all remote references (they're now invalid)
git remote remove origin

# Clean up any remaining references
git for-each-ref --format="delete %(refname)" refs/original | git update-ref --stdin
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

### **Step 6: Re-add clean versions of important files**

Since we might have removed important files, let's restore them with clean content:

```powershell
# Copy clean files from our backup
cp c:\Users\rupes\django-chat-clean-backup\GOOGLE_OAUTH_PRODUCTION.md .
cp c:\Users\rupes\django-chat-clean-backup\mysite\chatapp\management\commands\setup_production_oauth.py mysite\chatapp\management\commands\

# Add and commit clean versions
git add .
git commit -m "docs: Add clean production deployment guides with placeholders only"
```

### **Step 7: Re-add remote and force push**
```powershell
# Add your GitHub remote back (replace with your actual repo URL)
git remote add origin https://github.com/yourusername/yourrepo.git

# Force push the cleaned history
git push --force-with-lease origin master
```

### **Step 8: Verify cleanup worked**
```powershell
# Search entire history for any remaining secrets
git log --all -p -S "GOCSPX-" --source --all
git log --all -p -S ".apps.googleusercontent.com" --source --all

# If these return nothing, you're clean!
```

---

## 🚨 **If the above PowerShell commands don't work, use Git Bash:**

### **Alternative: Use Git Bash (recommended for complex regex)**
```bash
cd /c/Users/rupes/Project/django-chat-app-main

# Create replacement file
cat > replacements.txt << 'EOF'
regex:[0-9]+-[a-zA-Z0-9]+\.apps\.googleusercontent\.com=>[REDACTED-CLIENT-ID]
regex:GOCSPX-[a-zA-Z0-9_-]+==>[REDACTED-CLIENT-SECRET]
regex:[a-zA-Z0-9._%+-]+@gmail\.com==>[REDACTED-EMAIL]
regex:django-insecure-[a-zA-Z0-9=+!@#$%^&*()_-]+==>[REDACTED-SECRET-KEY]
regex:postgresql://[^\\s]+==>[REDACTED-DATABASE-URL]
EOF

# Apply replacements
git filter-repo --force --replace-text replacements.txt

# Clean up
git remote remove origin
git for-each-ref --format="delete %(refname)" refs/original | git update-ref --stdin
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Re-add remote and push
git remote add origin https://github.com/yourusername/yourrepo.git
git push --force-with-lease origin master
```

---

## 🎯 **Quick One-Liner Solution (if you're confident):**

```bash
cd /c/Users/rupes/Project/django-chat-app-main
echo -e 'regex:[0-9]+-[a-zA-Z0-9]+\.apps\.googleusercontent\.com==>REDACTED-CLIENT-ID\nregex:GOCSPX-[a-zA-Z0-9_-]+===>REDACTED-CLIENT-SECRET\nregex:[a-zA-Z0-9._%+-]+@gmail\.com===>REDACTED-EMAIL\nregex:django-insecure-[a-zA-Z0-9=+!@#$%^&*()_-]+===>REDACTED-SECRET-KEY\nregex:postgresql://[^\\s]+===>REDACTED-DATABASE-URL' | git filter-repo --force --replace-text /dev/stdin && git remote remove origin && git for-each-ref --format="delete %(refname)" refs/original | git update-ref --stdin && git reflog expire --expire=now --all && git gc --prune=now --aggressive
```

---

## ✅ **Final Verification Steps:**

1. **Check that secrets are gone:**
   ```bash
   git log --all --full-history -- . | grep -i "GOCSPX"
   git log --all --full-history -- . | grep -i "apps.googleusercontent.com"
   ```

2. **Verify file contents are clean:**
   ```bash
   git show HEAD:GOOGLE_OAUTH_PRODUCTION.md | grep -i "client"
   ```

3. **Test push to GitHub:**
   ```bash
   git remote add origin https://github.com/yourusername/yourrepo.git
   git push --force-with-lease origin master
   ```

---

## 🆘 **If GitHub Still Blocks:**

If GitHub still detects secrets, it means:
1. The regex didn't match exactly
2. Secrets exist in other files
3. Need to create a completely new repo

**Nuclear Option - New Repository:**
1. Create a new GitHub repository
2. Push only the clean current state:
   ```bash
   git remote set-url origin https://github.com/yourusername/new-repo.git
   git push origin master
   ```

---

## 📝 **Notes:**
- `git filter-repo` rewrites ALL commit history
- All commit hashes will change
- Anyone who has cloned your repo will need to re-clone
- This is irreversible (that's why we made backups!)
- The `--force-with-lease` is safer than `--force` as it checks for conflicts

**Ready to proceed? Start with Step 2!** 🚀
