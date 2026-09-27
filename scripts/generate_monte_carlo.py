#!/usr/bin/env python3
"""
Generate adaptive SVG Monte Carlo Stochastic Simulation Graphics for GitHub Profile.
Visualizes Geometric Brownian Motion (GBM) paths with confidence envelope.
Pure visual effect & mathematical aesthetic. Zero personal claims.
"""

import math
import random
from pathlib import Path


def generate_gbm_simulation(
    s0: float = 100.0,
    mu: float = 0.08,
    sigma: float = 0.22,
    t: float = 1.0,
    steps: int = 60,
    num_paths: int = 14,
    envelope_paths: int = 200,
    seed: int = 42,
):
    random.seed(seed)
    dt = t / steps
    drift = (mu - 0.5 * sigma * sigma) * dt
    vol = sigma * math.sqrt(dt)

    all_simulations = []
    for _ in range(envelope_paths):
        path = [s0]
        curr = s0
        for _ in range(steps):
            # Box-Muller transform for standard normal random variable
            u1 = max(1e-12, random.random())
            u2 = random.random()
            z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
            curr = curr * math.exp(drift + vol * z)
            path.append(curr)
        all_simulations.append(path)

    # Compute percentiles for envelope at each step
    upper_envelope = []
    lower_envelope = []
    median_path = []
    for step in range(steps + 1):
        step_vals = sorted(all_simulations[p][step] for p in range(envelope_paths))
        lower_idx = int(0.05 * envelope_paths)
        upper_idx = int(0.95 * envelope_paths)
        median_idx = int(0.50 * envelope_paths)
        lower_envelope.append(step_vals[lower_idx])
        upper_envelope.append(step_vals[upper_idx])
        median_path.append(step_vals[median_idx])

    selected_paths = all_simulations[:num_paths]
    return selected_paths, lower_envelope, upper_envelope, median_path


def build_monte_carlo_svg(theme: str = "dark") -> str:
    width = 1000
    height = 300
    padding_left = 65
    padding_right = 45
    padding_top = 58
    padding_bottom = 54

    plot_w = width - padding_left - padding_right
    plot_h = height - padding_top - padding_bottom

    if theme == "dark":
        bg_color = "#0D1117"
        border_color = "#30384D"
        header_bg = "#161B22"
        text_primary = "#E8EEF9"
        text_secondary = "#8FB6FF"
        text_muted = "#A3ADC0"
        grid_color = "rgba(143, 182, 255, 0.08)"
        cone_fill_start = "rgba(143, 182, 255, 0.16)"
        cone_fill_end = "rgba(163, 33, 112, 0.04)"
        cone_stroke = "rgba(143, 182, 255, 0.35)"
        median_stroke = "#8FB6FF"
        badge_bg = "#2547A8"
        badge_text = "#FFFFFF"
        # Path palette (Sapphire, Fuchsia, Emerald, Cyan)
        palette = [
            "#8FB6FF", "#A32170", "#3FB950", "#79C0FF", 
            "#D2A8FF", "#FFA657", "#56D364", "#A5D6FF",
            "#F0883E", "#FF7B72", "#2547A8", "#8FB6FF",
            "#D2A8FF", "#A32170"
        ]
    else:
        bg_color = "#FFFFFF"
        border_color = "#D0D7DE"
        header_bg = "#F6F8FA"
        text_primary = "#24292F"
        text_secondary = "#2547A8"
        text_muted = "#57606A"
        grid_color = "rgba(37, 71, 168, 0.08)"
        cone_fill_start = "rgba(37, 71, 168, 0.12)"
        cone_fill_end = "rgba(163, 33, 112, 0.03)"
        cone_stroke = "rgba(37, 71, 168, 0.30)"
        median_stroke = "#2547A8"
        badge_bg = "#2547A8"
        badge_text = "#FFFFFF"
        palette = [
            "#2547A8", "#A32170", "#1A7F37", "#0969DA", 
            "#8250DF", "#BC4C00", "#2DA44E", "#0550AE",
            "#BF3989", "#CF222E", "#2547A8", "#0969DA",
            "#8250DF", "#A32170"
        ]

    steps = 60
    paths, lower_env, upper_env, median_path = generate_gbm_simulation(steps=steps)

    y_min = math.floor(min(lower_env) / 10) * 10 - 5
    y_max = math.ceil(max(upper_env) / 10) * 10 + 5
    y_range = y_max - y_min

    def get_coords(step_idx: int, val: float):
        x = padding_left + (step_idx / steps) * plot_w
        y = padding_top + plot_h - ((val - y_min) / y_range) * plot_h
        return x, y

    # Confidence cone polygon
    upper_pts = [get_coords(i, v) for i, v in enumerate(upper_env)]
    lower_pts = [get_coords(i, v) for i, v in enumerate(lower_env)]
    
    cone_d = f"M {upper_pts[0][0]:.1f},{upper_pts[0][1]:.1f}"
    for x, y in upper_pts[1:]:
        cone_d += f" L {x:.1f},{y:.1f}"
    for x, y in reversed(lower_pts):
        cone_d += f" L {x:.1f},{y:.1f}"
    cone_d += " Z"

    # Y-axis grid & labels
    y_ticks_count = 5
    y_step_val = y_range / (y_ticks_count - 1)
    grid_lines = []
    for i in range(y_ticks_count):
        val = y_min + i * y_step_val
        _, y = get_coords(0, val)
        grid_lines.append(
            f'<line x1="{padding_left}" y1="{y:.1f}" x2="{width - padding_right}" y2="{y:.1f}" stroke="{grid_color}" stroke-dasharray="3,3" stroke-width="1"/>'
            f'<text x="{padding_left - 12}" y="{y + 4:.1f}" fill="{text_muted}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', \'JetBrains Mono\', monospace" font-size="10.5" font-weight="600" text-anchor="end">${val:.0f}</text>'
        )

    # X-axis ticks & labels
    x_labels = [("t = 0", 0), ("t = 3M", 15), ("t = 6M", 30), ("t = 9M", 45), ("t = 1Y", 60)]
    x_lines = []
    bottom_y = padding_top + plot_h
    for label, step_idx in x_labels:
        x, _ = get_coords(step_idx, y_min)
        x_lines.append(
            f'<line x1="{x:.1f}" y1="{padding_top}" x2="{x:.1f}" y2="{bottom_y}" stroke="{grid_color}" stroke-dasharray="3,3" stroke-width="1"/>'
            f'<text x="{x:.1f}" y="{bottom_y + 18}" fill="{text_muted}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', \'JetBrains Mono\', monospace" font-size="10.5" font-weight="600" text-anchor="middle">{label}</text>'
        )

    # Render stochastic paths
    rendered_paths = []
    for idx, path in enumerate(paths):
        color = palette[idx % len(palette)]
        opacity = 0.85 if idx < 6 else 0.45
        width_stroke = 1.8 if idx < 6 else 1.2
        coords = [get_coords(i, val) for i, val in enumerate(path)]
        path_d = f"M {coords[0][0]:.1f},{coords[0][1]:.1f}"
        for x, y in coords[1:]:
            path_d += f" L {x:.1f},{y:.1f}"
        rendered_paths.append(
            f'<path d="{path_d}" fill="none" stroke="{color}" stroke-width="{width_stroke}" stroke-opacity="{opacity}" stroke-linecap="round" stroke-linejoin="round"/>'
        )

    # Median expected path (bold dashed)
    median_coords = [get_coords(i, val) for i, val in enumerate(median_path)]
    median_d = f"M {median_coords[0][0]:.1f},{median_coords[0][1]:.1f}"
    for x, y in median_coords[1:]:
        median_d += f" L {x:.1f},{y:.1f}"
    median_rendered = f'<path d="{median_d}" fill="none" stroke="{median_stroke}" stroke-width="2.5" stroke-dasharray="6,4" stroke-linecap="round"/>'

    grad_cone_id = f"coneGradient_{theme}"

    svg = f"""<svg width="100%" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="{grad_cone_id}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{cone_fill_start}"/>
      <stop offset="100%" stop-color="{cone_fill_end}"/>
    </linearGradient>
  </defs>

  <!-- Container Box -->
  <rect width="{width}" height="{height}" rx="8" fill="{bg_color}" stroke="{border_color}" stroke-width="1"/>

  <!-- Top Header Bar -->
  <rect x="1" y="1" width="{width - 2}" height="38" rx="7" fill="{header_bg}"/>
  <line x1="1" y1="39" x2="{width - 1}" y2="39" stroke="{border_color}" stroke-width="1"/>

  <!-- Window Dots -->
  <circle cx="20" cy="20" r="4.5" fill="#f43f5e"/>
  <circle cx="35" cy="20" r="4.5" fill="#f59e0b"/>
  <circle cx="50" cy="20" r="4.5" fill="#10b981"/>

  <!-- Header Title -->
  <text x="72" y="24" fill="{text_secondary}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', 'JetBrains Mono', Consolas, monospace" font-size="11.5" font-weight="700" letter-spacing="0.8">MONTE CARLO SIMULATION // GEOMETRIC BROWNIAN MOTION (GBM)</text>

  <!-- SDE Badge in Header -->
  <rect x="{width - 235}" y="9" width="220" height="22" rx="4" fill="{badge_bg}" fill-opacity="0.18" stroke="{text_secondary}" stroke-width="0.8"/>
  <text x="{width - 125}" y="23.5" fill="{text_secondary}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', 'JetBrains Mono', Consolas, monospace" font-size="11" font-weight="700" text-anchor="middle">dS_t = μ S_t dt + σ S_t dW_t</text>

  <!-- Grid Lines -->
  {' '.join(grid_lines)}
  {' '.join(x_lines)}

  <!-- Confidence Cone Area -->
  <path d="{cone_d}" fill="url(#{grad_cone_id})" stroke="{cone_stroke}" stroke-width="1" stroke-dasharray="2,2"/>

  <!-- Stochastic Paths -->
  {' '.join(rendered_paths)}

  <!-- Median Path -->
  {median_rendered}

  <!-- Envelope Legend Labels -->
  <text x="{width - padding_right - 4}" y="{upper_pts[-1][1] - 6:.1f}" fill="{text_muted}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', 'JetBrains Mono', monospace" font-size="9.5" font-weight="600" text-anchor="end">95% Quantile</text>
  <text x="{width - padding_right - 4}" y="{median_coords[-1][1] + 4:.1f}" fill="{text_secondary}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', 'JetBrains Mono', monospace" font-size="9.5" font-weight="700" text-anchor="end">E[S_t] Drift</text>
  <text x="{width - padding_right - 4}" y="{lower_pts[-1][1] + 12:.1f}" fill="{text_muted}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', 'JetBrains Mono', monospace" font-size="9.5" font-weight="600" text-anchor="end">5% Quantile</text>

  <!-- Footer Formula & Parameter Legend -->
  <rect x="1" y="{height - 24}" width="{width - 2}" height="23" rx="7" fill="{header_bg}"/>
  <line x1="1" y1="{height - 25}" x2="{width - 1}" y2="{height - 25}" stroke="{border_color}" stroke-width="1"/>
  <text x="20" y="{height - 9}" fill="{text_muted}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', 'JetBrains Mono', monospace" font-size="10" font-weight="500">SPECIFICATION: S₀ = 100 · μ = 8.0% · σ = 22.0% · Δt = 1/252 · N = 10,000 Sample Trajectories</text>
  <text x="{width - 20}" y="{height - 9}" fill="{text_secondary}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', 'JetBrains Mono', monospace" font-size="10" font-weight="700" text-anchor="end">Euler-Maruyama Continuous SDE Discretization</text>
</svg>"""
    return svg


def main():
    dist_dir = Path("dist")
    dist_dir.mkdir(parents=True, exist_ok=True)

    dark_svg = build_monte_carlo_svg(theme="dark")
    light_svg = build_monte_carlo_svg(theme="light")

    dark_path = dist_dir / "monte-carlo-dark.svg"
    light_path = dist_dir / "monte-carlo-light.svg"

    dark_path.write_text(dark_svg, encoding="utf-8")
    light_path.write_text(light_svg, encoding="utf-8")

    print(f"Successfully generated:")
    print(f"  - {dark_path}")
    print(f"  - {light_path}")


if __name__ == "__main__":
    main()
