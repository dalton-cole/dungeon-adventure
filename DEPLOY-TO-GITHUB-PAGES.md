# Deploy Dungeon Adventure to GitHub Pages

## ✅ This Actually Works!

Your Python game will run in the browser, pulling code from your GitHub repo.

---

## Step 1: Push Your Code to GitHub

```bash
cd /Users/daltoncole/Documents/dungeon-adventure

# Initialize git (if not already done)
git init
git add *.py standalone.html
git commit -m "Add Dungeon Adventure game"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

---

## Step 2: Edit standalone.html

Open `standalone.html` and find these lines (around line 170):

```python
GITHUB_USER = "YOUR_USERNAME"  # Change this
GITHUB_REPO = "YOUR_REPO"      # Change this
```

**Replace with your actual GitHub username and repo name:**

```python
GITHUB_USER = "daltoncole"        # Your GitHub username
GITHUB_REPO = "dungeon-adventure"  # Your repo name
```

Also update around line 150 in the `<py-config>` section:

```
files = [
    "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/monsters.py",
    ...
]
```

Replace `YOUR_USERNAME/YOUR_REPO` with your actual values.

---

## Step 3: Commit and Push

```bash
git add standalone.html
git commit -m "Update GitHub repo URLs"
git push
```

---

## Step 4: Enable GitHub Pages

1. Go to your repo on GitHub
2. Click **Settings**
3. Scroll to **Pages** (left sidebar)
4. Under **Source**, select **main** branch
5. Click **Save**

GitHub will give you a URL like:
```
https://YOUR_USERNAME.github.io/YOUR_REPO/
```

---

## Step 5: Access Your Game

Go to:
```
https://YOUR_USERNAME.github.io/YOUR_REPO/standalone.html
```

**Example:**
```
https://daltoncole.github.io/dungeon-adventure/standalone.html
```

---

## 🎮 How It Works

1. Browser loads `standalone.html`
2. PyScript downloads Python runtime (~12MB, cached after first load)
3. PyScript fetches your `.py` files from GitHub
4. Game runs entirely in browser!

---

## ⚙️ What Works

✅ Full game logic
✅ All combat mechanics
✅ Inventory system
✅ Level progression
✅ All character classes
✅ All monsters and items

## ⚠️ What Doesn't Work

❌ Save/load (no file system in browser)
❌ Slow print effect (disabled for better browser UX)

---

## 📝 Making It the Default Page

If you want people to see the game at just `https://YOUR_USERNAME.github.io/YOUR_REPO/`:

**Option 1: Rename the file**
```bash
mv standalone.html index.html
git add index.html
git commit -m "Make game the index page"
git push
```

**Option 2: Create a landing page**
Keep `standalone.html` and create a simple `index.html` that links to it.

---

## 🐛 Troubleshooting

### "Failed to fetch" errors:
- Make sure your repo is **public** (not private)
- Check that branch name is correct (`main` vs `master`)
- Verify filenames match exactly

### Python errors:
- Check browser console (F12) for details
- Make sure all `.py` files are pushed to GitHub
- Verify files don't have syntax errors

### Slow loading:
- First load downloads 12MB Python runtime (normal)
- Subsequent loads use cache (much faster)
- Consider adding loading progress animations

### Game doesn't start:
- Open browser console (F12)
- Look for red error messages
- Verify GitHub URLs are correct in the HTML

---

## 🚀 Optional: Add to Main README

Add a "Play Now" button to your main `README.md`:

```markdown
# Dungeon Adventure

A text-based roguelike RPG with space/cosmic theming.

## 🎮 Play Now

**[Play in Browser](https://YOUR_USERNAME.github.io/YOUR_REPO/standalone.html)**
(First load may take 30 seconds)

**Or run locally:**
\`\`\`bash
python3 main.py
\`\`\`
```

---

## 📊 Performance Notes

- **First load:** 15-45 seconds (downloading Python runtime)
- **Cached load:** 3-5 seconds
- **Gameplay:** Smooth, responsive
- **File size:** ~12MB initial download

---

## 🎯 Summary

**You now have a GitHub Pages deployment that:**
- ✅ Uses your actual Python code (no rewrite!)
- ✅ Runs entirely client-side (no server!)
- ✅ Works on any device with a browser
- ✅ Updates automatically when you push changes
- ✅ Is completely free to host

**Just remember:** Any changes to `.py` files need to be pushed to GitHub for the live site to update!

---

## 🔄 Updating the Game

When you make changes to your Python files:

```bash
# Make your changes to .py files
git add *.py
git commit -m "Update game logic"
git push

# Changes are live immediately!
# Users may need to hard refresh (Ctrl+Shift+R) to clear cache
```

---

Enjoy your GitHub Pages deployment! 🎉
