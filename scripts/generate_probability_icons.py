#!/usr/bin/env python3
"""
Generate adaptive SVG Animated Probability & Game Theory Icons Widget.
Visualizes:
  - True 2-sided 3D Flipping Coin: Alternates between Heads ('H') and Tails ('T') on each half-turn!
  - Tumbling Rolling Dice: Discrete Law of Large Numbers (E[X] = 3.5).
  - Dynamic 3-Card Fanning & Dealing Hand: Ace of Spades ♠, King of Hearts ♥, Ace of Diamonds ♦ with corner indices & float animation.
Pure mathematical & visual effect. Zero personal claims.
"""

from pathlib import Path


def build_probability_icons_svg(theme: str = "dark") -> str:
    width = 1000
    height = 82

    if theme == "dark":
        bg_color = "#0D1117"
        border_color = "#30384D"
        card_bg = "#161B22"
        text_primary = "#E8EEF9"
        text_secondary = "#8FB6FF"
        text_muted = "#A3ADC0"
        coin_rim = "#F59E0B"
        coin_text = "#78350F"
        dice_bg = "#FFFFFF"
        dice_dot = "#0D1117"
        dice_border = "#8FB6FF"
        card_white = "#F8FAFC"
        card_border = "#475569"
        spade_color = "#0D1117"
        heart_color = "#E11D48"
        diamond_color = "#E11D48"
        shadow_opacity = "0.45"
    else:
        bg_color = "#FFFFFF"
        border_color = "#D0D7DE"
        card_bg = "#F6F8FA"
        text_primary = "#24292F"
        text_secondary = "#2547A8"
        text_muted = "#57606A"
        coin_rim = "#D97706"
        coin_text = "#78350F"
        dice_bg = "#FFFFFF"
        dice_dot = "#24292F"
        dice_border = "#2547A8"
        card_white = "#FFFFFF"
        card_border = "#CBD5E1"
        spade_color = "#1E293B"
        heart_color = "#CF222E"
        diamond_color = "#CF222E"
        shadow_opacity = "0.20"

    coin_grad_id = f"coinGrad_{theme}"
    card_glow_id = f"cardShadow_{theme}"

    svg = f"""<svg width="100%" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Coin Gold Gradient -->
    <linearGradient id="{coin_grad_id}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FDE68A"/>
      <stop offset="45%" stop-color="#F59E0B"/>
      <stop offset="100%" stop-color="#B45309"/>
    </linearGradient>

    <!-- Card Drop Shadow Filter -->
    <filter id="{card_glow_id}" x="-30%" y="-30%" width="160%" height="160%">
      <feDropShadow dx="0" dy="2.5" stdDeviation="2.5" flood-color="#000000" flood-opacity="{shadow_opacity}"/>
    </filter>
  </defs>

  <!-- Container Box -->
  <rect width="{width}" height="{height}" rx="8" fill="{bg_color}" stroke="{border_color}" stroke-width="1"/>

  <!-- Left Header Badge -->
  <rect x="0" y="0" width="168" height="{height}" rx="8" fill="{card_bg}"/>
  <rect x="158" y="0" width="10" height="{height}" fill="{card_bg}"/>
  <line x1="168" y1="0" x2="168" y2="{height}" stroke="{border_color}" stroke-width="1"/>

  <text x="20" y="33" fill="{text_secondary}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', 'JetBrains Mono', monospace" font-size="11" font-weight="800" letter-spacing="0.6">PROBABILITY</text>
  <text x="20" y="49" fill="{text_muted}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', monospace" font-size="9.5" font-weight="600">&amp; GAME THEORY</text>
  <text x="20" y="65" fill="{text_secondary}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', monospace" font-size="8.5" font-weight="700">MIT 18.05 FOUNDATIONS</text>

  <!-- ================= ELEMENT 1: TRUE 2-SIDED 3D COIN FLIP (H & T) ================= -->
  <g transform="translate(206, {height / 2})">
    <g>
      <!-- ScaleX oscillates: 1 (H) -> 0.05 (edge) -> 1 (T) -> 0.05 (edge) -> 1 (H) -->
      <animateTransform attributeName="transform" type="scale" values="1 1; 0.06 1; 1 1; 0.06 1; 1 1" dur="2.4s" repeatCount="indefinite" additive="sum"/>
      
      <!-- Coin Body -->
      <circle cx="0" cy="0" r="23" fill="url(#{coin_grad_id})" stroke="{coin_rim}" stroke-width="1.8"/>
      <circle cx="0" cy="0" r="19" fill="none" stroke="#FEF3C7" stroke-width="1" stroke-dasharray="3,2"/>

      <!-- Face H (Heads): Active during first half of rotation -->
      <g>
        <animate attributeName="opacity" values="1; 1; 0; 0; 0; 0; 1; 1" keyTimes="0; 0.23; 0.27; 0.73; 0.77; 0.99; 1" dur="2.4s" repeatCount="indefinite"/>
        <text x="0" y="7" fill="{coin_text}" font-family="'JetBrains Mono', Georgia, serif" font-size="18" font-weight="900" text-anchor="middle">H</text>
      </g>

      <!-- Face T (Tails): Active during second half of rotation -->
      <g>
        <animate attributeName="opacity" values="0; 0; 1; 1; 1; 1; 0; 0" keyTimes="0; 0.23; 0.27; 0.73; 0.77; 0.99; 1" dur="2.4s" repeatCount="indefinite"/>
        <text x="0" y="7" fill="{coin_text}" font-family="'JetBrains Mono', Georgia, serif" font-size="18" font-weight="900" text-anchor="middle">T</text>
      </g>
    </g>
  </g>
  <text x="246" y="37" fill="{text_primary}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', monospace" font-size="11" font-weight="700">Bernoulli Trial (Coin Flip: H / T)</text>
  <text x="246" y="54" fill="{text_muted}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', monospace" font-size="9.5">Fair Coin P(H) = P(T) = 0.5 · Random Walk</text>

  <!-- Vertical Divider 1 -->
  <line x1="445" y1="12" x2="445" y2="{height - 12}" stroke="{border_color}" stroke-width="1" stroke-dasharray="2,2"/>

  <!-- ================= ELEMENT 2: ROLLING TUMBLING DICE ================= -->
  <g transform="translate(484, {height / 2})">
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
  <text x="522" y="37" fill="{text_primary}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', monospace" font-size="11" font-weight="700">Discrete Law of Large Numbers</text>
  <text x="522" y="54" fill="{text_muted}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', monospace" font-size="9.5">Fair Die: E[X] = 3.5 · Var[X] = 35/12</text>

  <!-- Vertical Divider 2 -->
  <line x1="730" y1="12" x2="730" y2="{height - 12}" stroke="{border_color}" stroke-width="1" stroke-dasharray="2,2"/>

  <!-- ================= ELEMENT 3: DYNAMIC 3-CARD FANNING & DEALING HAND ================= -->
  <!-- Hand Cluster Center: 778 -->
  <g transform="translate(776, {height / 2})">
    
    <!-- Card 1: Left - Ace of Diamonds ♦ (Slides & Fans Left) -->
    <g filter="url(#{card_glow_id})">
      <animateTransform attributeName="transform" type="rotate" values="-16; -28; -16" dur="3.2s" repeatCount="indefinite" additive="sum"/>
      <animateTransform attributeName="transform" type="translate" values="-8 -2; -16 -5; -8 -2" dur="3.2s" repeatCount="indefinite" additive="sum"/>
      
      <rect x="-13" y="-21" width="26" height="42" rx="3.5" fill="{card_white}" stroke="{card_border}" stroke-width="1"/>
      <text x="-7.5" y="-10.5" fill="{diamond_color}" font-family="'JetBrains Mono', Georgia, serif" font-size="8.5" font-weight="800">A</text>
      <text x="-7.5" y="-1.5" fill="{diamond_color}" font-size="8.5">♦</text>
      <text x="0" y="8" fill="{diamond_color}" font-size="14" text-anchor="middle">♦</text>
      <!-- Bottom right inverted index -->
      <text x="7.5" y="16" fill="{diamond_color}" font-family="'JetBrains Mono', Georgia, serif" font-size="7" font-weight="800" text-anchor="end" transform="rotate(180 5.5 13)">A</text>
    </g>

    <!-- Card 3: Right - King of Hearts ♥ (Slides & Fans Right) -->
    <g filter="url(#{card_glow_id})">
      <animateTransform attributeName="transform" type="rotate" values="16; 28; 16" dur="3.2s" repeatCount="indefinite" additive="sum"/>
      <animateTransform attributeName="transform" type="translate" values="8 -2; 16 -5; 8 -2" dur="3.2s" repeatCount="indefinite" additive="sum"/>
      
      <rect x="-13" y="-21" width="26" height="42" rx="3.5" fill="{card_white}" stroke="{card_border}" stroke-width="1"/>
      <text x="-7.5" y="-10.5" fill="{heart_color}" font-family="'JetBrains Mono', Georgia, serif" font-size="8.5" font-weight="800">K</text>
      <text x="-7.5" y="-1.5" fill="{heart_color}" font-size="8.5">♥</text>
      <text x="0" y="8" fill="{heart_color}" font-size="14" text-anchor="middle">♥</text>
      <!-- Bottom right inverted index -->
      <text x="7.5" y="16" fill="{heart_color}" font-family="'JetBrains Mono', Georgia, serif" font-size="7" font-weight="800" text-anchor="end" transform="rotate(180 5.5 13)">K</text>
    </g>

    <!-- Card 2: Center - Ace of Spades ♠ (Leading Card, Floats & Lifts Upwards) -->
    <g filter="url(#{card_glow_id})">
      <animateTransform attributeName="transform" type="translate" values="0 -3; 0 -12; 0 -3" dur="3.2s" repeatCount="indefinite"/>
      
      <rect x="-14" y="-22" width="28" height="44" rx="4" fill="{card_white}" stroke="{text_secondary}" stroke-width="1.4"/>
      <text x="-8" y="-11" fill="{spade_color}" font-family="'JetBrains Mono', Georgia, serif" font-size="9" font-weight="900">A</text>
      <text x="-8" y="-1.5" fill="{spade_color}" font-size="9">♠</text>
      <text x="0" y="9" fill="{spade_color}" font-size="16" text-anchor="middle">♠</text>
      <!-- Bottom right inverted index -->
      <text x="8" y="17" fill="{spade_color}" font-family="'JetBrains Mono', Georgia, serif" font-size="7.5" font-weight="900" text-anchor="end" transform="rotate(180 6 14)">A</text>
    </g>
  </g>

  <text x="820" y="37" fill="{text_primary}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', monospace" font-size="11" font-weight="700">Kelly Sizing &amp; Game Theory</text>
  <text x="820" y="54" fill="{text_muted}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', monospace" font-size="9.5">f* = (bp - q) / b · Blackjack Odds</text>
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
