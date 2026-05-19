# AI Tools Reviews — Automated Blog

Fully automated AI tool review site built with Hugo + Claude API + GitHub Actions + GitHub Pages.

## Stack
- **Hugo** (PaperMod theme) — static site generator
- **Claude API** — daily article generation
- **GitHub Actions** — automation pipeline
- **GitHub Pages** — free hosting

## Setup (One-Time)

### 1. Update `hugo.toml`
Replace `YOUR_USERNAME` with your GitHub username:
```toml
baseURL = "https://YOUR_USERNAME.github.io/AI_Tools_WEB/"
```

### 2. Add Secrets to GitHub
Go to **Settings → Secrets → Actions** and add:
- `ANTHROPIC_API_KEY` — your Claude API key from console.anthropic.com

### 3. Enable GitHub Pages
Go to **Settings → Pages** and set source to `gh-pages` branch.

### 4. Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/AI_Tools_WEB.git
git branch -M main
git push -u origin main
```

### 5. Add AdSense
Replace `ca-pub-XXXXXXXXXXXXXXXX` in `layouts/partials/head-custom.html` with your AdSense publisher ID.

## Monetization
- **AdSense** — display ads (auto-injected via head partial)
- **Affiliate links** — use `{{< cta-button url="..." text="..." >}}` shortcode in articles
- **Recommended programs**: Jasper (30% recurring), Copy.ai (45% recurring), Writesonic (30% recurring)

## Local Development
```bash
hugo server --buildDrafts
```

## Manual Article Generation
```bash
pip install anthropic
export ANTHROPIC_API_KEY=your_key
python scripts/generate_article.py
```
