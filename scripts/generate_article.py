#!/usr/bin/env python3
"""
Auto-generates an AI tool review article using Gemini API
and saves it as a Hugo markdown file.
"""

from google import genai
import os
import datetime
import random
import re
import sys
from pathlib import Path

TOOLS = [
    ("Writesonic", "ai writing", "writesonic"),
    ("Copy.ai", "ai copywriting", "copy-ai"),
    ("Midjourney", "ai image generation", "midjourney"),
    ("Runway ML", "ai video generation", "runway-ml"),
    ("Notion AI", "ai productivity", "notion-ai"),
    ("Perplexity AI", "ai search", "perplexity-ai"),
    ("ElevenLabs", "ai voice generation", "elevenlabs"),
    ("Synthesia", "ai video avatars", "synthesia"),
    ("Descript", "ai audio video editing", "descript"),
    ("Otter.ai", "ai transcription", "otter-ai"),
]

PROMPT_TEMPLATE = """Write a detailed, honest review article for {tool_name} ({niche} tool) for a blog targeting freelancers, agencies, and developers.

Structure:
1. What Is {tool_name}? (2-3 sentences)
2. Pricing table (markdown table with 3 tiers)
3. Key Features (4-5 bullet points)
4. Pros & Cons (3 each)
5. Who Is It Best For? (2-3 sentences)
6. Verdict with score out of 10
7. 3 Alternatives

Rules:
- Write in English
- Be specific, avoid fluff
- Include realistic pricing
- Score honestly (6-9 range)
- End with: "{{{{< cta-button url=\\"https://example.com?ref=aitools\\" text=\\"Try {tool_name} Free →\\" >}}}}"
- Do NOT include frontmatter, just the body content starting with ## What Is
"""

def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9-]", "", text.lower().replace(" ", "-").replace(".", "-"))

def generate_article(tool_name: str, niche: str) -> str:
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=PROMPT_TEMPLATE.format(tool_name=tool_name, niche=niche)
    )
    return response.text

def save_article(tool_name: str, slug: str, content: str) -> Path:
    today = datetime.date.today().isoformat()
    year = datetime.date.today().year

    frontmatter = f"""---
title: "{tool_name} Review {year}: Honest Pros, Cons & Pricing"
date: {today}
description: "In-depth {tool_name} review after hands-on testing. Pricing, features, pros & cons, and best alternatives."
tags: ["{slug}", "ai tools", "review"]
categories: ["reviews"]
---

{{{{< affiliate-disclosure >}}}}

"""
    output_dir = Path(__file__).parent.parent / "content" / "reviews"
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / f"{slug}-review-{today}.md"
    filepath.write_text(frontmatter + content)
    print(f"✅ Created: {filepath}")
    return filepath

def main():
    tool_name, niche, slug = random.choice(TOOLS)
    print(f"🤖 Generating review for: {tool_name}")
    content = generate_article(tool_name, niche)
    save_article(tool_name, slug, content)

if __name__ == "__main__":
    main()
