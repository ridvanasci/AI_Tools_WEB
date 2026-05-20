#!/usr/bin/env python3
"""
Auto-generates AI tool comparison articles using Groq API.
"""

from groq import Groq
import os
import datetime
import random
import re
from pathlib import Path

COMPARISONS = [
    ("ChatGPT vs Claude", "chatgpt-vs-claude", 110),
    ("ChatGPT vs Gemini", "chatgpt-vs-gemini", 120),
    ("Jasper vs Copy.ai", "jasper-vs-copy-ai", 130),
    ("Midjourney vs DALL-E 3", "midjourney-vs-dalle-3", 140),
    ("Writesonic vs Jasper", "writesonic-vs-jasper", 150),
    ("ElevenLabs vs Murf", "elevenlabs-vs-murf", 160),
    ("Notion AI vs Mem.ai", "notion-ai-vs-mem-ai", 170),
    ("Runway vs Pika Labs", "runway-vs-pika-labs", 180),
    ("Perplexity vs ChatGPT", "perplexity-vs-chatgpt", 190),
    ("Claude vs Gemini", "claude-vs-gemini", 200),
]

PROMPT_TEMPLATE = """Write a detailed comparison article: "{title}" for a blog targeting freelancers, agencies, and developers.

Structure:
1. Quick Overview (2-3 sentences about both tools)
2. Side-by-side comparison table (Features, Pricing, Best For)
3. Tool A: Key Strengths (3 points)
4. Tool B: Key Strengths (3 points)
5. Which Should You Choose? (clear recommendation by use case)
6. Verdict

Rules:
- Write in English
- Be specific and opinionated
- Include realistic pricing
- End with: "{{< cta-button url=\"https://example.com?ref=aitools\" text=\"Try The Winner Free →\" >}}"
- Do NOT include frontmatter, start with ## Quick Overview
"""

def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9-]", "", text.lower().replace(" ", "-").replace(".", "-"))

def generate_article(title: str) -> str:
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": PROMPT_TEMPLATE.format(title=title)}],
        max_tokens=1500,
    )
    return response.choices[0].message.content

def save_article(title: str, slug: str, seed: int, content: str) -> Path:
    today = datetime.date.today().isoformat()
    year = datetime.date.today().year
    cover_image = f"https://picsum.photos/seed/{seed}/1200/630"

    frontmatter = f"""---
title: "{title}: Which Is Better in {year}?"
date: {today}
description: "Detailed {title} comparison. Features, pricing, pros & cons — find out which AI tool wins."
tags: ["comparison", "ai tools"]
categories: ["comparisons"]
cover:
  image: "{cover_image}"
  alt: "{title} Comparison"
  relative: false
---

{{{{< affiliate-disclosure >}}}}

"""
    output_dir = Path(__file__).parent.parent / "content" / "comparisons"
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / f"{slug}-{today}.md"
    filepath.write_text(frontmatter + content)
    print(f"✅ Created: {filepath}")
    return filepath

def main():
    title, slug, seed = random.choice(COMPARISONS)
    print(f"🤖 Generating comparison: {title}")
    content = generate_article(title)
    save_article(title, slug, seed, content)

if __name__ == "__main__":
    main()
