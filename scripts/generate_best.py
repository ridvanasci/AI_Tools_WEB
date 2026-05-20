#!/usr/bin/env python3
"""
Auto-generates "Best AI Tools for X" list articles using Groq API.
"""

from groq import Groq
import os
import datetime
import random
import re
from pathlib import Path

BEST_LISTS = [
    ("Best AI Writing Tools for Bloggers", "best-ai-writing-tools-bloggers", 210),
    ("Best Free AI Tools 2026", "best-free-ai-tools", 220),
    ("Best AI Tools for Freelancers", "best-ai-tools-freelancers", 230),
    ("Best AI Video Generators", "best-ai-video-generators", 240),
    ("Best AI Image Generators", "best-ai-image-generators", 250),
    ("Best AI Tools for Social Media", "best-ai-tools-social-media", 260),
    ("Best AI Coding Assistants", "best-ai-coding-assistants", 270),
    ("Best AI Tools for Small Business", "best-ai-tools-small-business", 280),
    ("Best AI Transcription Tools", "best-ai-transcription-tools", 290),
    ("Best AI Voice Generators", "best-ai-voice-generators", 300),
]

PROMPT_TEMPLATE = """Write a detailed "{title}" listicle for a blog targeting freelancers, agencies, and developers.

Structure:
1. Introduction (2-3 sentences, why this list matters)
2. Quick Comparison Table (Tool, Best For, Price, Rating)
3. Top 5 tools — for each:
   - Tool name as H3
   - 2-sentence description
   - Key features (3 bullets)
   - Pricing (1 line)
   - Best for (1 line)
4. How to Choose (3-4 sentences)
5. Final Verdict

Rules:
- Write in English
- Be specific, include real tools and pricing
- End with: "{{< cta-button url=\"https://example.com?ref=aitools\" text=\"Try Our Top Pick Free →\" >}}"
- Do NOT include frontmatter, start with ## Introduction
"""

def generate_article(title: str) -> str:
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": PROMPT_TEMPLATE.format(title=title)}],
        max_tokens=1800,
    )
    return response.choices[0].message.content

def save_article(title: str, slug: str, seed: int, content: str) -> Path:
    today = datetime.date.today().isoformat()
    year = datetime.date.today().year
    cover_image = f"https://picsum.photos/seed/{seed}/1200/630"

    frontmatter = f"""---
title: "{title} ({year})"
date: {today}
description: "The best {title.lower()} tested and ranked. Find the right tool for your needs and budget."
tags: ["best", "ai tools"]
categories: ["best"]
cover:
  image: "{cover_image}"
  alt: "{title}"
  relative: false
---

{{{{< affiliate-disclosure >}}}}

"""
    output_dir = Path(__file__).parent.parent / "content" / "best"
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / f"{slug}-{today}.md"
    filepath.write_text(frontmatter + content)
    print(f"✅ Created: {filepath}")
    return filepath

def main():
    title, slug, seed = random.choice(BEST_LISTS)
    print(f"🤖 Generating best list: {title}")
    content = generate_article(title)
    save_article(title, slug, seed, content)

if __name__ == "__main__":
    main()
