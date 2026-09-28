#!/usr/bin/env python3
"""
Generate adaptive SVG Animated Casino Royale Hero Marquee for GitHub Profile.
Theme: High-Stakes Monte Carlo Casino & Quantitative Systems Lab.
Features:
  - Authentic Las Vegas / Monte Carlo 3-phase chasing marquee light bulbs.
  - Ornate Casino Royale gold trim with corner card suits (♠ ♥ ♦ ♣).
  - Luxury gold chrome illuminated typography with 3D drop shadow.
  - 4 Mechanical Slot Reels / Lucky 777 telemetry indicators.
  - Dual theme: Dark (Midnight Emerald Felt & Gold) / Light (Royal Ivory Club & Brass).
"""

from pathlib import Path


def generate_marquee_lights(width: int, height: int, num_top: int = 24, num_side: int = 5):
    """Generate 3-phase chasing lights around the marquee border."""
    bulbs = []
    
    # Top edge
    step_x = (width - 60) / (num_top - 1)
    for i in range(num_top):
        bulbs.append((30 + i * step_x, 14, i % 3))
        
    # Right edge
    step_y = (height - 28) / (num_side + 1)
    for i in range(1, num_side + 1):
        bulbs.append((width - 16, 14 + i * step_y, (num_top + i) % 3))
        
    # Bottom edge (right to left)
    for i in range(num_top - 1, -1, -1):
        bulbs.append((30 + i * step_x, height - 14, (num_top + num_side + (num_top - 1 - i)) % 3))
        
    # Left edge (bottom to top)
    for i in range(num_side, 0, -1):
        bulbs.append((16, 14 + i * step_y, (num_top * 2 + num_side + (num_side - i)) % 3))
        
    return bulbs


def build_casino_hero_svg(theme: str = "dark") -> str:
    width = 1000
    height = 245
    
    if theme == "dark":
        bg_felt_center = "#0D2318"
        bg_felt_edge = "#060F0A"
        outer_frame = "#040A07"
        gold_bright = "#FFE57F"
        gold_mid = "#F59E0B"
        gold_dark = "#92400E"
        gold_stroke = "#D4AF37"
        suit_red = "#EF4444"
        suit_black = "#F59E0B"
        reel_bg = "#08130D"
        reel_border = "#B45309"
        reel_text = "#FFFBEB"
        sub_text = "#93C5FD"
        tag_text = "#FDE68A"
        bulb_on = "#FFFBEB"
        bulb_glow = "#F59E0B"
        bulb_off = "#374151"
        shadow_opacity = "0.7"
        live_dot = "#10B981"
    else:
        bg_felt_center = "#F0FDF4"
        bg_felt_edge = "#DCFCE7"
        outer_frame = "#14532D"
        gold_bright = "#B45309"
        gold_mid = "#D97706"
        gold_dark = "#78350F"
        gold_stroke = "#B45309"
        suit_red = "#DC2626"
        suit_black = "#1E293B"
        reel_bg = "#FFFFFF"
        reel_border = "#D97706"
        reel_text = "#1E293B"
        sub_text = "#1D4ED8"
        tag_text = "#92400E"
        bulb_on = "#F59E0B"
        bulb_glow = "#D97706"
        bulb_off = "#D1D5DB"
        shadow_opacity = "0.3"
        live_dot = "#059669"

    gold_grad_id = f"goldGrad_{theme}"
    reel_grad_id = f"reelGrad_{theme}"
    glow_id = f"casinoGlow_{theme}"
    felt_id = f"feltGrad_{theme}"

    # Generate chasing bulbs
    bulbs = generate_marquee_lights(width, height, num_top=28, num_side=5)
    
    bulb_svg_elements = []
    for cx, cy, phase in bulbs:
        if phase == 0:
            anim = '<animate attributeName="opacity" values="1;0.25;0.25;1" keyTimes="0;0.33;0.66;1" dur="1.2s" repeatCount="indefinite"/>'
        elif phase == 1:
            anim = '<animate attributeName="opacity" values="0.25;1;0.25;0.25" keyTimes="0;0.33;0.66;1" dur="1.2s" repeatCount="indefinite"/>'
        else:
            anim = '<animate attributeName="opacity" values="0.25;0.25;1;0.25" keyTimes="0;0.33;0.66;1" dur="1.2s" repeatCount="indefinite"/>'
        
        bulb_svg_elements.append(
            f'<g transform="translate({cx:.1f},{cy:.1f})">'
            f'<circle cx="0" cy="0" r="3.2" fill="{bulb_glow}" opacity="0.4"/>'
            f'<circle cx="0" cy="0" r="2.2" fill="{bulb_on}">{anim}</circle>'
            f'</g>'
        )
    bulbs_rendered = "\n    ".join(bulb_svg_elements)

    # 4 Slot Reels Data
    reels = [
        ("♠", "APPLIED AI", "DEEP LEARNING"),
        ("🎰", "97.6% MATH", "ENG MATHEMATICS"),
        ("💎", "50% MERIT", "RMIT SCHOLARSHIP"),
        ("⚡", "SYSTEMS ARCH", "PROBLEM → PROD"),
    ]
    
    reel_elements = []
    reel_w = 180
    reel_h = 44
    gap = 16
    total_reels_w = 4 * reel_w + 3 * gap
    start_x = (width - total_reels_w) / 2
    reel_y = 144

    for idx, (icon, title, desc) in enumerate(reels):
        rx = start_x + idx * (reel_w + gap)
        reel_elements.append(f"""
    <!-- Reel {idx+1}: {title} -->
    <g transform="translate({rx}, {reel_y})">
      <!-- Reel Frame -->
      <rect x="0" y="0" width="{reel_w}" height="{reel_h}" rx="6" fill="{reel_bg}" stroke="{reel_border}" stroke-width="1.6"/>
      <!-- Inner shadow gradient top/bottom for cylinder effect -->
      <rect x="1" y="1" width="{reel_w-2}" height="10" rx="4" fill="#000000" opacity="0.22"/>
      <rect x="1" y="{reel_h-11}" width="{reel_w-2}" height="10" rx="4" fill="#000000" opacity="0.22"/>
      
      <!-- Icon Badge -->
      <text x="18" y="28" font-size="18" text-anchor="middle">{icon}</text>
      <!-- Reel Value -->
      <text x="36" y="22" fill="{reel_text}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', 'JetBrains Mono', Consolas, monospace" font-size="12" font-weight="800" letter-spacing="0.5">{title}</text>
      <!-- Sub-label -->
      <text x="36" y="36" fill="{gold_mid}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', monospace" font-size="9" font-weight="700" letter-spacing="0.8">{desc}</text>
    </g>""")

    reels_rendered = "\n".join(reel_elements)

    svg = f"""<svg width="100%" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Background Velvet Felt Gradient -->
    <radialGradient id="{felt_id}" cx="50%" cy="40%" r="65%">
      <stop offset="0%" stop-color="{bg_felt_center}"/>
      <stop offset="100%" stop-color="{bg_felt_edge}"/>
    </radialGradient>

    <!-- Chrome Gold Text Gradient -->
    <linearGradient id="{gold_grad_id}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{gold_bright}"/>
      <stop offset="48%" stop-color="{gold_mid}"/>
      <stop offset="52%" stop-color="{gold_bright}"/>
      <stop offset="100%" stop-color="{gold_dark}"/>
    </linearGradient>

    <!-- Metallic Reel Rim Gradient -->
    <linearGradient id="{reel_grad_id}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{gold_bright}"/>
      <stop offset="50%" stop-color="{gold_mid}"/>
      <stop offset="100%" stop-color="{gold_dark}"/>
    </linearGradient>

    <!-- Drop Shadow Filter for 3D Text & Panels -->
    <filter id="{glow_id}" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#000000" flood-opacity="{shadow_opacity}"/>
    </filter>
  </defs>

  <!-- Outer Cabinet Frame -->
  <rect x="2" y="2" width="{width - 4}" height="{height - 4}" rx="12" fill="{outer_frame}" stroke="{gold_stroke}" stroke-width="2"/>
  
  <!-- Gaming Velvet Felt Surface -->
  <rect x="8" y="8" width="{width - 16}" height="{height - 16}" rx="8" fill="url(#{felt_id})"/>

  <!-- Ornate Inner Gold Inlay Border -->
  <rect x="22" y="22" width="{width - 44}" height="{height - 44}" rx="6" fill="none" stroke="{gold_stroke}" stroke-width="1.2" opacity="0.6"/>
  <rect x="26" y="26" width="{width - 52}" height="{height - 52}" rx="4" fill="none" stroke="{gold_stroke}" stroke-width="0.8" stroke-dasharray="6,4" opacity="0.4"/>

  <!-- Corner Card Suits (Art Deco Ornaments) -->
  <text x="36" y="44" fill="{suit_black}" font-size="16" font-family="Georgia, serif" opacity="0.85">♠</text>
  <text x="{width - 48}" y="44" fill="{suit_red}" font-size="16" font-family="Georgia, serif" opacity="0.85">♥</text>
  <text x="36" y="{height - 32}" fill="{suit_red}" font-size="16" font-family="Georgia, serif" opacity="0.85">♦</text>
  <text x="{width - 48}" y="{height - 32}" fill="{suit_black}" font-size="16" font-family="Georgia, serif" opacity="0.85">♣</text>

  <!-- Top Marquee Header Arch -->
  <g transform="translate({width / 2}, 48)">
    <rect x="-240" y="-14" width="480" height="24" rx="12" fill="{outer_frame}" stroke="{gold_stroke}" stroke-width="1.2" opacity="0.9"/>
    <text x="0" y="3" fill="{gold_mid}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', 'JetBrains Mono', Consolas, monospace" font-size="10.5" font-weight="900" letter-spacing="2.2" text-anchor="middle">★ CASINO ROYALE ★ MONTE CARLO QUANT &amp; SYSTEMS LAB ★</text>
  </g>

  <!-- Giant Glowing Gold Title: KAI NGUYEN -->
  <g transform="translate({width / 2}, 98)" filter="url(#{glow_id})">
    <text x="0" y="0" fill="url(#{gold_grad_id})" font-family="Georgia, 'Times New Roman', 'Playfair Display', serif" font-size="44" font-weight="900" letter-spacing="4" text-anchor="middle">KAI NGUYEN</text>
  </g>

  <!-- Subtitle Tagline -->
  <text x="{width / 2}" y="122" fill="{tag_text}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', 'JetBrains Mono', Consolas, monospace" font-size="11.5" font-weight="700" letter-spacing="1.8" text-anchor="middle">
    HIGH-STAKES AI ENGINEERING · PROBABILITY &amp; GAME THEORY · PRODUCTION SYSTEMS
  </text>

  <!-- 4 Slot Machine Reels (Live Accomplishment Indicators) -->
  {reels_rendered}

  <!-- Bottom Telemetry Ticker Status Line -->
  <g transform="translate({width / 2}, 216)">
    <circle cx="-250" cy="-3.5" r="3.5" fill="{live_dot}">
      <animate attributeName="opacity" values="1;0.3;1" dur="1.5s" repeatCount="indefinite"/>
    </circle>
    <text x="-240" y="0" fill="{tag_text}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', 'JetBrains Mono', Consolas, monospace" font-size="9" font-weight="800" letter-spacing="1">STATUS: AT THE TABLES</text>
    <text x="0" y="0" fill="{sub_text}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', 'JetBrains Mono', Consolas, monospace" font-size="9" font-weight="700" letter-spacing="0.8" text-anchor="middle">HOUSE EDGE: DETERMINISTIC QUANT</text>
    <text x="240" y="0" fill="{gold_mid}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', 'JetBrains Mono', Consolas, monospace" font-size="9" font-weight="800" letter-spacing="1" text-anchor="end">JACKPOT: MAXIMUM PRODUCTION RIGOR ♠</text>
  </g>

  <!-- Marquee Chasing Light Bulbs -->
  <g>
    {bulbs_rendered}
  </g>
</svg>"""
    return svg


def main():
    repo_root = Path(__file__).resolve().parent.parent
    dist_dir = repo_root / "dist"
    dist_dir.mkdir(parents=True, exist_ok=True)

    dark_svg = build_casino_hero_svg("dark")
    light_svg = build_casino_hero_svg("light")

    dark_path = dist_dir / "casino-hero-dark.svg"
    light_path = dist_dir / "casino-hero-light.svg"

    dark_path.write_text(dark_svg, encoding="utf-8")
    light_path.write_text(light_svg, encoding="utf-8")

    print(f"Successfully generated:")
    print(f"  - {dark_path.relative_to(repo_root)}")
    print(f"  - {light_path.relative_to(repo_root)}")


if __name__ == "__main__":
    main()
