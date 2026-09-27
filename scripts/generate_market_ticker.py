#!/usr/bin/env python3
"""
Generate adaptive SVG Animated Financial Market Ticker Tape for GitHub Profile.
Pure visual aesthetic / finance theme. Displays marquee of global market benchmarks.
Zero personal claims.
"""

from pathlib import Path


def build_market_ticker_svg(theme: str = "dark") -> str:
    width = 1000
    height = 38
    badge_width = 105

    if theme == "dark":
        bg_color = "#0D1117"
        border_color = "#30384D"
        badge_bg = "#2547A8"
        badge_accent = "#A32170"
        badge_text = "#FFFFFF"
        live_dot = "#3FB950"
        symbol_color = "#8FB6FF"
        price_color = "#E8EEF9"
        green_color = "#3FB950"
        red_color = "#F85149"
        sep_color = "#30384D"
        fade_start = "rgba(13, 17, 23, 1)"
        fade_end = "rgba(13, 17, 23, 0)"
    else:
        bg_color = "#FFFFFF"
        border_color = "#D0D7DE"
        badge_bg = "#2547A8"
        badge_accent = "#A32170"
        badge_text = "#FFFFFF"
        live_dot = "#1A7F37"
        symbol_color = "#2547A8"
        price_color = "#24292F"
        green_color = "#1A7F37"
        red_color = "#CF222E"
        sep_color = "#D0D7DE"
        fade_start = "rgba(255, 255, 255, 1)"
        fade_end = "rgba(255, 255, 255, 0)"

    # Diversified market benchmark assets
    items = [
        ("SPY", "581.42", "+0.84%", True),
        ("QQQ", "487.10", "+1.22%", True),
        ("BTC", "65,840", "+3.15%", True),
        ("NVDA", "123.80", "+2.40%", True),
        ("ETH", "2,645", "+1.78%", True),
        ("GOLD", "2,658", "+0.65%", True),
        ("VIX", "15.40", "-4.20%", False),
        ("AAPL", "227.50", "-0.32%", False),
        ("US10Y", "3.74%", "-1.10%", False),
        ("MSFT", "428.15", "+0.45%", True),
        ("DXY", "100.80", "-0.25%", False),
        ("BRENT", "71.30", "+1.05%", True),
    ]

    item_spacing = 168
    loop_width = item_spacing * len(items)

    def render_items(x_offset: int) -> str:
        chunks = []
        for i, (sym, price, chg, is_up) in enumerate(items):
            x = x_offset + (i * item_spacing)
            arrow = "▲" if is_up else "▼"
            color = green_color if is_up else red_color
            chunks.append(
                f'<g transform="translate({x}, 0)">'
                f'<text x="0" y="24" fill="{symbol_color}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', \'JetBrains Mono\', Consolas, monospace" font-size="12" font-weight="700">{sym}</text>'
                f'<text x="48" y="24" fill="{price_color}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', \'JetBrains Mono\', Consolas, monospace" font-size="12" font-weight="500">{price}</text>'
                f'<text x="104" y="24" fill="{color}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', \'JetBrains Mono\', Consolas, monospace" font-size="11.5" font-weight="600">{arrow} {chg}</text>'
                f'<circle cx="158" cy="20" r="1.5" fill="{sep_color}"/>'
                f'</g>'
            )
        return "\n      ".join(chunks)

    track_1 = render_items(0)
    track_2 = render_items(loop_width)

    fade_left_id = f"fadeLeft_{theme}"
    fade_right_id = f"fadeRight_{theme}"

    svg = f"""<svg width="100%" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="{fade_left_id}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{fade_start}"/>
      <stop offset="100%" stop-color="{fade_end}"/>
    </linearGradient>
    <linearGradient id="{fade_right_id}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{fade_end}"/>
      <stop offset="100%" stop-color="{fade_start}"/>
    </linearGradient>
    <clipPath id="tickerClipWindow">
      <rect x="{badge_width + 1}" y="1" width="{width - badge_width - 2}" height="{height - 2}"/>
    </clipPath>
  </defs>

  <style>
    @keyframes tickerScroll {{
      0% {{ transform: translate(0px, 0px); }}
      100% {{ transform: translate(-{loop_width}px, 0px); }}
    }}
    .ticker-content {{
      animation: tickerScroll 28s linear infinite;
    }}
  </style>

  <!-- Container Box -->
  <rect width="{width}" height="{height}" rx="6" fill="{bg_color}" stroke="{border_color}" stroke-width="1"/>

  <!-- Left Header Badge: LIVE MARKETS -->
  <rect x="0" y="0" width="{badge_width}" height="{height}" rx="6" fill="{badge_bg}"/>
  <rect x="{badge_width - 8}" y="0" width="8" height="{height}" fill="{badge_bg}"/>
  <line x1="{badge_width}" y1="0" x2="{badge_width}" y2="{height}" stroke="{border_color}" stroke-width="1"/>

  <!-- Pulsing Live Dot -->
  <circle cx="16" cy="19" r="3.5" fill="{live_dot}">
    <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>
  </circle>

  <!-- Badge Text -->
  <text x="27" y="23" fill="{badge_text}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', 'JetBrains Mono', Consolas, monospace" font-size="10.5" font-weight="800" letter-spacing="0.8">MARKETS</text>

  <!-- Marquee Area with Clip Mask -->
  <g clip-path="url(#tickerClipWindow)">
    <g class="ticker-content">
      <animateTransform attributeName="transform" type="translate" from="0 0" to="-{loop_width} 0" dur="28s" repeatCount="indefinite"/>
      {track_1}
      {track_2}
    </g>
  </g>

  <!-- Edge Soft Fades for Seamless Transition -->
  <rect x="{badge_width + 1}" y="1" width="30" height="{height - 2}" fill="url(#{fade_left_id})" pointer-events="none"/>
  <rect x="{width - 32}" y="1" width="30" height="{height - 2}" fill="url(#{fade_right_id})" pointer-events="none"/>
</svg>"""
    return svg


def main():
    dist_dir = Path("dist")
    dist_dir.mkdir(parents=True, exist_ok=True)

    dark_svg = build_market_ticker_svg(theme="dark")
    light_svg = build_market_ticker_svg(theme="light")

    dark_path = dist_dir / "market-ticker-dark.svg"
    light_path = dist_dir / "market-ticker-light.svg"

    dark_path.write_text(dark_svg, encoding="utf-8")
    light_path.write_text(light_svg, encoding="utf-8")

    print(f"Successfully generated:")
    print(f"  - {dark_path}")
    print(f"  - {light_path}")


if __name__ == "__main__":
    main()
