#!/usr/bin/env python3
"""
Generate adaptive SVG Quantitative Telemetry Twin-Panel Graphics for GitHub Profile.
Visualizes:
  - Left Panel: Time Domain — Monte Carlo Geometric Brownian Motion (GBM) Paths.
  - Right Panel: Spatial Domain — 3D Implied Volatility Surface Topology σ(K, T).
Pure visual mathematical aesthetic. Zero personal claims.
"""

import math
import random
from pathlib import Path


def generate_gbm_simulation(
    s0: float = 100.0,
    mu: float = 0.08,
    sigma: float = 0.22,
    t: float = 1.0,
    steps: int = 50,
    num_paths: int = 10,
    envelope_paths: int = 150,
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
            u1 = max(1e-12, random.random())
            u2 = random.random()
            z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
            curr = curr * math.exp(drift + vol * z)
            path.append(curr)
        all_simulations.append(path)

    upper_envelope = []
    lower_envelope = []
    median_path = []
    for step in range(steps + 1):
        step_vals = sorted(all_simulations[p][step] for p in range(envelope_paths))
        lower_envelope.append(step_vals[int(0.05 * envelope_paths)])
        upper_envelope.append(step_vals[int(0.95 * envelope_paths)])
        median_path.append(step_vals[int(0.50 * envelope_paths)])

    return all_simulations[:num_paths], lower_envelope, upper_envelope, median_path


def generate_vol_surface(nx: int = 13, ny: int = 10):
    k_vals = [-0.25 + (i / (nx - 1)) * 0.50 for i in range(nx)]
    t_vals = [0.1 + (j / (ny - 1)) * 1.9 for j in range(ny)]

    grid = []
    for j, t in enumerate(t_vals):
        row = []
        for i, k in enumerate(k_vals):
            base_vol = 0.18 + 0.035 * math.sqrt(t)
            skew = -0.10 * k / math.sqrt(t)
            curvature = 0.25 * (k ** 2) / (1.0 + 0.7 * t)
            vol = base_vol + skew + curvature
            row.append((k, t, vol))
        grid.append(row)
    return grid


def project_3d(x, y, z, cx, cy, scale_x, scale_y, scale_z, yaw_deg=34, pitch_deg=22):
    yaw = math.radians(yaw_deg)
    pitch = math.radians(pitch_deg)

    x_rot = x * math.cos(yaw) - y * math.sin(yaw)
    y_rot = x * math.sin(yaw) + y * math.cos(yaw)

    x_screen = x_rot * scale_x
    y_screen = (-y_rot * math.sin(pitch) - z * math.cos(pitch)) * scale_y

    return cx + x_screen, cy + y_screen


def build_monte_carlo_svg(theme: str = "dark") -> str:
    width = 1000
    height = 310

    if theme == "dark":
        bg_color = "#0D1117"
        border_color = "#30384D"
        header_bg = "#161B22"
        text_primary = "#E8EEF9"
        text_secondary = "#8FB6FF"
        text_muted = "#A3ADC0"
        grid_color = "rgba(143, 182, 255, 0.08)"
        cone_fill = "rgba(143, 182, 255, 0.14)"
        cone_stroke = "rgba(143, 182, 255, 0.32)"
        median_stroke = "#8FB6FF"
        badge_bg = "#2547A8"
        wire_row_color = "#8FB6FF"
        wire_col_color = "#A32170"
        palette = [
            "#8FB6FF", "#A32170", "#3FB950", "#79C0FF", 
            "#D2A8FF", "#FFA657", "#56D364", "#A5D6FF",
            "#F0883E", "#FF7B72"
        ]
    else:
        bg_color = "#FFFFFF"
        border_color = "#D0D7DE"
        header_bg = "#F6F8FA"
        text_primary = "#24292F"
        text_secondary = "#2547A8"
        text_muted = "#57606A"
        grid_color = "rgba(37, 71, 168, 0.08)"
        cone_fill = "rgba(37, 71, 168, 0.10)"
        cone_stroke = "rgba(37, 71, 168, 0.28)"
        median_stroke = "#2547A8"
        badge_bg = "#2547A8"
        wire_row_color = "#2547A8"
        wire_col_color = "#A32170"
        palette = [
            "#2547A8", "#A32170", "#1A7F37", "#0969DA", 
            "#8250DF", "#BC4C00", "#2DA44E", "#0550AE",
            "#BF3989", "#CF222E"
        ]

    # ================= LEFT PANEL: MONTE CARLO GBM =================
    left_pad_l = 50
    left_pad_r = 525
    pad_top = 70
    pad_bottom = 48
    left_w = left_pad_r - left_pad_l
    plot_h = height - pad_top - pad_bottom

    steps = 50
    paths, lower_env, upper_env, median_path = generate_gbm_simulation(steps=steps)

    y_min = math.floor(min(lower_env) / 10) * 10 - 5
    y_max = math.ceil(max(upper_env) / 10) * 10 + 5
    y_range = y_max - y_min

    def get_gbm_coords(step_idx: int, val: float):
        x = left_pad_l + (step_idx / steps) * left_w
        y = pad_top + plot_h - ((val - y_min) / y_range) * plot_h
        return x, y

    upper_pts = [get_gbm_coords(i, v) for i, v in enumerate(upper_env)]
    lower_pts = [get_gbm_coords(i, v) for i, v in enumerate(lower_env)]

    cone_d = f"M {upper_pts[0][0]:.1f},{upper_pts[0][1]:.1f}"
    for x, y in upper_pts[1:]:
        cone_d += f" L {x:.1f},{y:.1f}"
    for x, y in reversed(lower_pts):
        cone_d += f" L {x:.1f},{y:.1f}"
    cone_d += " Z"

    left_grid = []
    y_ticks_count = 4
    y_step_val = y_range / (y_ticks_count - 1)
    for i in range(y_ticks_count):
        val = y_min + i * y_step_val
        _, y = get_gbm_coords(0, val)
        left_grid.append(
            f'<line x1="{left_pad_l}" y1="{y:.1f}" x2="{left_pad_r}" y2="{y:.1f}" stroke="{grid_color}" stroke-dasharray="3,3" stroke-width="1"/>'
            f'<text x="{left_pad_l - 8}" y="{y + 3.5:.1f}" fill="{text_muted}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', monospace" font-size="9.5" font-weight="600" text-anchor="end">${val:.0f}</text>'
        )

    left_x_labels = [("t=0", 0), ("t=6M", 25), ("t=1Y", 50)]
    bottom_y = pad_top + plot_h
    for label, step_idx in left_x_labels:
        x, _ = get_gbm_coords(step_idx, y_min)
        left_grid.append(
            f'<line x1="{x:.1f}" y1="{pad_top}" x2="{x:.1f}" y2="{bottom_y}" stroke="{grid_color}" stroke-dasharray="3,3" stroke-width="1"/>'
            f'<text x="{x:.1f}" y="{bottom_y + 14}" fill="{text_muted}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', monospace" font-size="9.5" font-weight="600" text-anchor="middle">{label}</text>'
        )

    rendered_paths = []
    for idx, path in enumerate(paths):
        color = palette[idx % len(palette)]
        opacity = 0.85 if idx < 5 else 0.40
        w_stroke = 1.6 if idx < 5 else 1.1
        coords = [get_gbm_coords(i, val) for i, val in enumerate(path)]
        path_d = f"M {coords[0][0]:.1f},{coords[0][1]:.1f}"
        for x, y in coords[1:]:
            path_d += f" L {x:.1f},{y:.1f}"
        rendered_paths.append(
            f'<path d="{path_d}" fill="none" stroke="{color}" stroke-width="{w_stroke}" stroke-opacity="{opacity}" stroke-linecap="round"/>'
        )

    median_coords = [get_gbm_coords(i, val) for i, val in enumerate(median_path)]
    median_d = f"M {median_coords[0][0]:.1f},{median_coords[0][1]:.1f}"
    for x, y in median_coords[1:]:
        median_d += f" L {x:.1f},{y:.1f}"
    median_rendered = f'<path d="{median_d}" fill="none" stroke="{median_stroke}" stroke-width="2" stroke-dasharray="5,3" stroke-linecap="round"/>'

    # ================= RIGHT PANEL: 3D VOLATILITY SURFACE =================
    grid_3d = generate_vol_surface(nx=13, ny=10)
    all_vols = [pt[2] for row in grid_3d for pt in row]
    v_min, v_max = min(all_vols), max(all_vols)

    cx_3d = 765
    cy_3d = 185
    scale_x = 92
    scale_y = 55
    scale_z = 52

    proj_grid = []
    for row in grid_3d:
        p_row = []
        for k, t, v in row:
            norm_x = (k / 0.25)
            norm_y = ((t - 0.1) / 1.9) * 2.0 - 1.0
            norm_z = ((v - v_min) / (v_max - v_min)) * 1.5 - 0.2
            sx, sy = project_3d(norm_x, norm_y, norm_z, cx=cx_3d, cy=cy_3d, scale_x=scale_x, scale_y=scale_y, scale_z=scale_z)
            p_row.append((sx, sy, norm_y, v))
        proj_grid.append(p_row)

    quad_polys = []
    ny = len(proj_grid)
    nx = len(proj_grid[0])
    for j in range(ny - 1):
        for i in range(nx - 1):
            p1 = proj_grid[j][i]
            p2 = proj_grid[j][i+1]
            p3 = proj_grid[j+1][i+1]
            p4 = proj_grid[j+1][i]
            avg_v = (p1[3] + p2[3] + p3[3] + p4[3]) / 4.0
            ratio = (avg_v - v_min) / (v_max - v_min)
            poly_d = f"M {p1[0]:.1f},{p1[1]:.1f} L {p2[0]:.1f},{p2[1]:.1f} L {p3[0]:.1f},{p3[1]:.1f} L {p4[0]:.1f},{p4[1]:.1f} Z"
            fill_op = 0.08 + 0.14 * ratio
            quad_polys.append(
                f'<path d="{poly_d}" fill="{badge_bg}" fill-opacity="{fill_op:.2f}" stroke="none"/>'
            )

    wire_rows = []
    for j, row in enumerate(proj_grid):
        d = f"M {row[0][0]:.1f},{row[0][1]:.1f}"
        for sx, sy, _, _ in row[1:]:
            d += f" L {sx:.1f},{sy:.1f}"
        op = 0.40 + (j / (ny - 1)) * 0.45
        wire_rows.append(f'<path d="{d}" fill="none" stroke="{wire_row_color}" stroke-width="1.2" stroke-opacity="{op:.2f}" stroke-linecap="round"/>')

    wire_cols = []
    for i in range(nx):
        col = [proj_grid[j][i] for j in range(ny)]
        d = f"M {col[0][0]:.1f},{col[0][1]:.1f}"
        for sx, sy, _, _ in col[1:]:
            d += f" L {sx:.1f},{sy:.1f}"
        dist_from_atm = abs(i - (nx - 1) / 2) / ((nx - 1) / 2)
        c_stroke = wire_col_color if dist_from_atm > 0.6 else wire_row_color
        wire_cols.append(f'<path d="{d}" fill="none" stroke="{c_stroke}" stroke-width="1.2" stroke-opacity="0.65" stroke-linecap="round"/>')

    axis_annotations = [
        f'<text x="{cx_3d - 90}" y="{cy_3d + 68}" fill="{text_secondary}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', monospace" font-size="9.5" font-weight="700">◀ STRIKE (K) - OTM PUTS</text>',
        f'<text x="{cx_3d + 75}" y="{cy_3d + 68}" fill="{text_secondary}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', monospace" font-size="9.5" font-weight="700">OTM CALLS ▶</text>',
        f'<text x="{cx_3d + 125}" y="{cy_3d - 10}" fill="{wire_col_color}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', monospace" font-size="9.5" font-weight="700">MATURITY (T) ↗</text>',
        f'<text x="{cx_3d - 120}" y="{cy_3d - 50}" fill="{text_secondary}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', monospace" font-size="9.5" font-weight="700">▲ VOL σ(K,T)</text>',
    ]

    svg = f"""<svg width="100%" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Container Box -->
  <rect width="{width}" height="{height}" rx="8" fill="{bg_color}" stroke="{border_color}" stroke-width="1"/>

  <!-- Top Terminal Header Bar -->
  <rect x="1" y="1" width="{width - 2}" height="38" rx="7" fill="{header_bg}"/>
  <line x1="1" y1="39" x2="{width - 1}" y2="39" stroke="{border_color}" stroke-width="1"/>

  <!-- Window Dots -->
  <circle cx="20" cy="20" r="4.5" fill="#f43f5e"/>
  <circle cx="35" cy="20" r="4.5" fill="#f59e0b"/>
  <circle cx="50" cy="20" r="4.5" fill="#10b981"/>

  <!-- Header Title -->
  <text x="72" y="24" fill="{text_secondary}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', 'JetBrains Mono', Consolas, monospace" font-size="11.5" font-weight="700" letter-spacing="0.8">QUANTITATIVE LAB // STOCHASTIC PATHS &amp; 3D VOLATILITY TOPOLOGY</text>

  <!-- Right Pill Badge -->
  <rect x="{width - 260}" y="9" width="245" height="22" rx="4" fill="{badge_bg}" fill-opacity="0.18" stroke="{text_secondary}" stroke-width="0.8"/>
  <text x="{width - 138}" y="23.5" fill="{text_secondary}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', 'JetBrains Mono', Consolas, monospace" font-size="10.5" font-weight="700" text-anchor="middle">SDE: dS_t  ·  SURFACE: σ(K, T)</text>

  <!-- Middle Vertical Divider -->
  <line x1="550" y1="40" x2="550" y2="{height - 25}" stroke="{border_color}" stroke-width="1" stroke-dasharray="3,3"/>

  <!-- ================= LEFT PANEL ================= -->
  <text x="{left_pad_l}" y="58" fill="{text_secondary}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', monospace" font-size="10.5" font-weight="700" letter-spacing="0.5">▸ TIME DOMAIN: MONTE CARLO GBM PATHS</text>
  <text x="{left_pad_r}" y="58" fill="{text_muted}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', monospace" font-size="9.5" font-weight="600" text-anchor="end">95% Conf. Cone</text>

  {' '.join(left_grid)}
  <path d="{cone_d}" fill="{cone_fill}" stroke="{cone_stroke}" stroke-width="1" stroke-dasharray="2,2"/>
  {' '.join(rendered_paths)}
  {median_rendered}

  <!-- ================= RIGHT PANEL ================= -->
  <text x="575" y="58" fill="{text_secondary}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', monospace" font-size="10.5" font-weight="700" letter-spacing="0.5">▸ SPATIAL DOMAIN: 3D VOLATILITY SURFACE σ(K, T)</text>
  <text x="{width - 40}" y="58" fill="{wire_col_color}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', monospace" font-size="9.5" font-weight="600" text-anchor="end">Dupire Local PDE</text>

  {' '.join(quad_polys)}
  {' '.join(wire_rows)}
  {' '.join(wire_cols)}
  {' '.join(axis_annotations)}

  <!-- ================= BOTTOM STRIP ================= -->
  <rect x="1" y="{height - 24}" width="{width - 2}" height="23" rx="7" fill="{header_bg}"/>
  <line x1="1" y1="{height - 25}" x2="{width - 1}" y2="{height - 25}" stroke="{border_color}" stroke-width="1"/>
  <text x="20" y="{height - 9}" fill="{text_muted}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', monospace" font-size="9.5" font-weight="500">LEFT: Euler-Maruyama SDE Discretization (S₀=100, μ=8%, σ=22%)</text>
  <text x="{width - 20}" y="{height - 9}" fill="{text_secondary}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', monospace" font-size="9.5" font-weight="700" text-anchor="end">RIGHT: Implied Volatility Smile &amp; Term Structure Topology</text>
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
