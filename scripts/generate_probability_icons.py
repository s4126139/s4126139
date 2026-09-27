#!/usr/bin/env python3
"""
Generate adaptive SVG Animated Probability & Game Theory Icons Widget.
Visualizes:
  - 3D Flipping Coin (Bernoulli Trial / Random Walk)
  - Tumbling Rolling Dice (Discrete Law of Large Numbers)
  - Fanning Playing Cards (Kelly Criterion / Game Theory)
Pure mathematical & visual effect. Zero personal claims.
"""

from pathlib import Path


def build_probability_icons_svg(theme: str = "dark") -> str:
    width = 1000
    height = 76

    if theme == "dark":
        bg_color = "#0D1117"
        border_color = "#30384D"
        card_bg = "#161B22"
        text_primary = "#E8EEF9"
        text_secondary = "#8FB6FF"
        text_muted = "#A3ADC0"
        coin_gold_start = "#FCD34D"
        coin_gold_mid = "#F59E0B"
        coin_gold_end = "#B45309"
        dice_bg = "#FFFFFF"
        dice_dot = "#0D1117"
        dice_border = "#8FB6FF"
        card_white = "#F8FAFC"
        spade_color = "#0D1117"
        heart_color = "#E11D48"
    else:
        bg_color = "#FFFFFF"
        border_color = "#D0D7DE"
        card_bg = "#F6F8FA"
        text_primary = "#24292F"
        text_secondary = "#2547A8"
        text_muted = "#57606A"
        coin_gold_start = "#FBBF24"
        coin_gold_mid = "#D97706"
        coin_gold_end = "#92400E"
        dice_bg = "#FFFFFF"
        dice_dot = "#24292F"
        dice_border = "#2547A8"
        card_white = "#FFFFFF"
        spade_color = "#24292F"
        heart_color = "#CF222E"

    coin_grad_id = f"coinGrad_{theme}"

    svg = f"""<svg width="100%" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="{coin_grad_id}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{coin_gold_start}"/>
      <stop offset="50%" stop-color="{coin_gold_mid}"/>
      <stop offset="100%" stop-color="{coin_gold_end}"/>
    </linearGradient>
  </defs>

  <!-- Container Box -->
  <rect width="{width}" height="{height}" rx="8" fill="{bg_color}" stroke="{border_color}" stroke-width="1"/>

  <!-- Left Header Badge -->
  <rect x="0" y="0" width="168" height="{height}" rx="8" fill="{card_bg}"/>
  <rect x="158" y="0" width="10" height="{height}" fill="{card_bg}"/>
  <line x1="168" y1="0" x2="168" y2="{height}" stroke="{border_color}" stroke-width="1"/>

  <text x="20" y="32" fill="{text_secondary}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', 'JetBrains Mono', monospace" font-size="11" font-weight="800" letter-spacing="0.6">PROBABILITY</text>
  <text x="20" y="47" fill="{text_muted}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', monospace" font-size="9.5" font-weight="600">&amp; GAME THEORY</text>
  <text x="20" y="61" fill="{text_secondary}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', monospace" font-size="8.5" font-weight="700">MIT 18.05 FOUNDATIONS</text>

  <!-- ================= ELEMENT 1: 3D FLIPPING COIN ================= -->
  <g transform="translate(204, {height / 2})">
    <g>
      <animateTransform attributeName="transform" type="scale" values="1 1; 0.08 1; -1 1; 0.08 1; 1 1" dur="2.4s" repeatCount="indefinite" additive="sum"/>
      <circle cx="0" cy="0" r="22" fill="url(#{coin_grad_id})" stroke="{coin_gold_mid}" stroke-width="1.8"/>
      <circle cx="0" cy="0" r="18" fill="none" stroke="#FEF3C7" stroke-width="1" stroke-dasharray="3,2"/>
      <text x="0" y="6.5" fill="#78350F" font-family="'JetBrains Mono', Georgia, serif" font-size="16" font-weight="900" text-anchor="middle">H</text>
    </g>
  </g>
  <text x="242" y="35" fill="{text_primary}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', monospace" font-size="11" font-weight="700">Bernoulli Trial (Coin Flip)</text>
  <text x="242" y="52" fill="{text_muted}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', monospace" font-size="9.5">Fair Coin P(H) = 0.5 · 1D Random Walk</text>

  <!-- Vertical Divider 1 -->
  <line x1="450" y1="12" x2="450" y2="{height - 12}" stroke="{border_color}" stroke-width="1" stroke-dasharray="2,2"/>

  <!-- ================= ELEMENT 2: ROLLING TUMBLING DICE ================= -->
  <g transform="translate(488, {height / 2})">
    <g>
      <animateTransform attributeName="transform" type="rotate" values="0; 18; -12; 360" dur="3.4s" repeatCount="indefinite"/>
      <rect x="-16" y="-16" width="32" height="32" rx="6.5" fill="{dice_bg}" stroke="{dice_border}" stroke-width="1.8"/>
      <circle cx="-7" cy="-7" r="2.8" fill="{dice_dot}"/>
      <circle cx="7" cy="-7" r="2.8" fill="{dice_dot}"/>
      <circle cx="0" cy="0" r="2.8" fill="#E11D48"/>
      <circle cx="-7" cy="7" r="2.8" fill="{dice_dot}"/>
      <circle cx="7" cy="7" r="2.8" fill="{dice_dot}"/>
    </g>
  </g>
  <text x="526" y="35" fill="{text_primary}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', monospace" font-size="11" font-weight="700">Discrete Law of Large Numbers</text>
  <text x="526" y="52" fill="{text_muted}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', monospace" font-size="9.5">Fair Die: E[X] = 3.5 · Var[X] = 35/12</text>

  <!-- Vertical Divider 2 -->
  <line x1="740" y1="12" x2="740" y2="{height - 12}" stroke="{border_color}" stroke-width="1" stroke-dasharray="2,2"/>

  <!-- ================= ELEMENT 3: FANNING PLAYING CARDS ================= -->
  <g transform="translate(778, {height / 2})">
    <!-- Back Card (Ace of Diamonds) -->
    <g>
      <animateTransform attributeName="transform" type="rotate" values="14; 22; 14" dur="2.8s" repeatCount="indefinite"/>
      <rect x="-12" y="-19" width="24" height="36" rx="3" fill="{card_white}" stroke="#CBD5E1" stroke-width="1"/>
      <text x="-6" y="-9" fill="{heart_color}" font-size="7.5" font-weight="800">A</text>
      <text x="-6" y="-1" fill="{heart_color}" font-size="8">♦</text>
      <text x="0" y="6" fill="{heart_color}" font-size="12" text-anchor="middle">♦</text>
    </g>
    <!-- Front Card (Ace of Spades) -->
    <g>
      <animateTransform attributeName="transform" type="rotate" values="-12; -4; -12" dur="2.8s" repeatCount="indefinite"/>
      <rect x="-12" y="-19" width="24" height="36" rx="3" fill="{card_white}" stroke="#94A3B8" stroke-width="1"/>
      <text x="-6" y="-9" fill="{spade_color}" font-size="7.5" font-weight="800">A</text>
      <text x="-6" y="-1" fill="{spade_color}" font-size="8">♠</text>
      <text x="0" y="6" fill="{spade_color}" font-size="12" text-anchor="middle">♠</text>
    </g>
  </g>
  <text x="814" y="35" fill="{text_primary}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', monospace" font-size="11" font-weight="700">Kelly Sizing &amp; Game Theory</text>
  <text x="814" y="52" fill="{text_muted}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', monospace" font-size="9.5">f* = (bp - q) / b · Thorp Blackjack</text>
</svg>"""
    return svg


def main():
    dist_dir = Path("dist")
    dist_dir.mkdir(parents=True, exist_ok=True)

    dark_svg = build_probability_icons_svg(theme="dark")
    light_svg = build_probability_icons_svg(theme="light")

    dark_path = dist_dir / "probability-icons-dark.svg"
    light_path = dist_dir / "probability-icons-light.svg"

    dark_path.write_text(dark_svg, encoding="utf-8")
    light_path.write_text(light_svg, encoding="utf-8")

    print(f"Successfully generated:")
    print(f"  - {dark_path}")
    print(f"  - {light_path}")


if __name__ == "__main__":
    main()
