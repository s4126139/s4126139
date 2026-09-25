#!/usr/bin/env python3
"""
Generate high-fidelity, adaptive SVG Yearly Contribution Activity Graphs for GitHub Profile.
Emulates the smooth line/area chart of github-activity-graph, styled with user custom theme
and aggregated across the rolling 12 months.
"""

from __future__ import annotations

import json
import math
import os
import subprocess
import sys
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


def get_token() -> str:
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        return token.strip()
    try:
        out = subprocess.check_output(["gh", "auth", "token"], text=True)
        return out.strip()
    except Exception:
        pass
    print("Error: GITHUB_TOKEN not found and gh auth token unavailable.", file=sys.stderr)
    sys.exit(1)


def fetch_contributions(username: str, token: str) -> dict:
    query = """
    query($login: String!) {
      user(login: $login) {
        name
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                date
              }
            }
          }
        }
      }
    }
    """
    req_body = json.dumps({"query": query, "variables": {"login": username}}).encode("utf-8")
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=req_body,
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": "GitHub-Yearly-Activity-Graph",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    if "errors" in data:
        raise RuntimeError(f"GraphQL Errors: {data['errors']}")
    return data["data"]["user"]


def aggregate_monthly(calendar: dict) -> tuple[int, list[tuple[str, int]]]:
    total_contributions = calendar.get("totalContributions", 0)
    month_counts = defaultdict(int)

    for week in calendar.get("weeks", []):
        for day in week.get("contributionDays", []):
            month_key = day["date"][:7]  # YYYY-MM
            month_counts[month_key] += day["contributionCount"]

    sorted_months = sorted(month_counts.keys())
    # Keep the last 12 months
    if len(sorted_months) > 12:
        sorted_months = sorted_months[-12:]

    result = []
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for m in sorted_months:
        dt = datetime.strptime(m, "%Y-%m")
        label = month_names[dt.month - 1]
        result.append((label, month_counts[m]))

    return total_contributions, result


def build_svg(
    months_data: list[tuple[str, int]],
    total_contribs: int,
    username: str,
    theme: str = "dark",
) -> str:
    width = 1200
    height = 420
    padding_top = 88
    padding_bottom = 60
    padding_left = 90
    padding_right = 60

    plot_width = width - padding_left - padding_right
    plot_height = height - padding_top - padding_bottom

    if theme == "dark":
        bg_color = "#060913"
        card_stroke = "#1e293b"
        title_color = "#2dd4bf"
        text_color = "#94a3b8"
        grid_color = "rgba(148, 163, 184, 0.12)"
        line_color = "#2dd4bf"
        point_fill = "#2dd4bf"
        point_stroke = "#060913"
        area_opacity = 0.42
    else:
        bg_color = "#ffffff"
        card_stroke = "#e2e8f0"
        title_color = "#0d9488"
        text_color = "#475569"
        grid_color = "rgba(71, 85, 105, 0.10)"
        line_color = "#0d9488"
        point_fill = "#0d9488"
        point_stroke = "#ffffff"
        area_opacity = 0.35

    counts = [c for _, c in months_data]
    max_count = max(counts) if counts else 100

    # Determine Y-axis ceiling with nice rounding
    if max_count <= 50:
        y_max = 60
        y_step = 10
    elif max_count <= 100:
        y_max = 100
        y_step = 20
    elif max_count <= 300:
        y_max = 300
        y_step = 50
    elif max_count <= 700:
        y_max = 700
        y_step = 100
    else:
        y_max = math.ceil(max_count / 200) * 200
        y_step = y_max // 5

    n_points = len(months_data)
    points = []
    for i, (label, count) in enumerate(months_data):
        x = padding_left + (i / max(n_points - 1, 1)) * plot_width
        y = padding_top + plot_height - (count / y_max) * plot_height
        points.append((x, y, count, label))

    # Catmull-Rom to Cubic Bezier smooth spline
    path_d = f"M {points[0][0]:.2f},{points[0][1]:.2f}"
    for i in range(len(points) - 1):
        p0 = points[i - 1] if i > 0 else points[i]
        p1 = points[i]
        p2 = points[i + 1]
        p3 = points[i + 2] if i + 2 < len(points) else p2

        cp1x = p1[0] + (p2[0] - p0[0]) / 6.0
        cp1y = p1[1] + (p2[1] - p0[1]) / 6.0
        cp2x = p2[0] - (p3[0] - p1[0]) / 6.0
        cp2y = p2[1] - (p3[1] - p1[1]) / 6.0

        # Clamp control point y within bounds
        cp1y = max(padding_top, min(padding_top + plot_height, cp1y))
        cp2y = max(padding_top, min(padding_top + plot_height, cp2y))

        path_d += f" C {cp1x:.2f},{cp1y:.2f} {cp2x:.2f},{cp2y:.2f} {p2[0]:.2f},{p2[1]:.2f}"

    bottom_y = padding_top + plot_height
    area_d = f"{path_d} L {points[-1][0]:.2f},{bottom_y:.2f} L {points[0][0]:.2f},{bottom_y:.2f} Z"

    # Y-axis ticks and grid lines
    y_elements = []
    val = 0
    while val <= y_max:
        y_pos = padding_top + plot_height - (val / y_max) * plot_height
        y_elements.append(
            f'<line x1="{padding_left}" y1="{y_pos:.1f}" x2="{width - padding_right}" y2="{y_pos:.1f}" stroke="{grid_color}" stroke-dasharray="4,4" stroke-width="1" />'
        )
        y_elements.append(
            f'<text x="{padding_left - 14}" y="{y_pos + 4:.1f}" fill="{text_color}" font-size="12" font-weight="600" text-anchor="end" font-family="-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,sans-serif">{val}</text>'
        )
        val += y_step

    # X-axis ticks, labels, points and pill badges
    x_elements = []
    point_elements = []
    for x, y, count, label in points:
        x_elements.append(
            f'<line x1="{x:.1f}" y1="{bottom_y}" x2="{x:.1f}" y2="{bottom_y + 6}" stroke="{grid_color}" stroke-width="1.5" />'
        )
        x_elements.append(
            f'<text x="{x:.1f}" y="{bottom_y + 24}" fill="{text_color}" font-size="13" font-weight="600" text-anchor="middle" font-family="-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,sans-serif">{label}</text>'
        )

        point_elements.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="{point_fill}" stroke="{point_stroke}" stroke-width="2.5" />'
        )
        if count > 0:
            point_elements.append(
                f'<text x="{x:.1f}" y="{y - 10:.1f}" fill="{title_color}" font-size="11.5" font-weight="700" text-anchor="middle" font-family="-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,sans-serif">{count}</text>'
            )

    grad_id = f"yearlyAreaGradient_{theme}"

    title_text = "Kai Nguyen's Yearly Contribution Graph"
    subtitle_text = f"Total {total_contribs:,} Contributions across past 12 months · Peak: {max_count:,} in a single month"

    svg_content = f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="{grad_id}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{line_color}" stop-opacity="{area_opacity}" />
      <stop offset="100%" stop-color="{line_color}" stop-opacity="0.0" />
    </linearGradient>
  </defs>

  <!-- Background Card -->
  <rect width="{width}" height="{height}" rx="12" fill="{bg_color}" stroke="{card_stroke}" stroke-width="1" />

  <!-- Header Section -->
  <text x="{width / 2}" y="38" fill="{title_color}" font-size="20" font-weight="700" text-anchor="middle" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif">{title_text}</text>
  <text x="{width / 2}" y="60" fill="{text_color}" font-size="12" font-weight="500" text-anchor="middle" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif">{subtitle_text}</text>

  <!-- Axis Titles -->
  <text x="25" y="{padding_top + plot_height / 2}" fill="{text_color}" font-size="13" font-weight="600" text-anchor="middle" transform="rotate(-90 25 {padding_top + plot_height / 2})" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif">Contributions</text>
  <text x="{width / 2}" y="{height - 12}" fill="{text_color}" font-size="13" font-weight="600" text-anchor="middle" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif">Months</text>

  <!-- Grid Lines & Y Labels -->
  {' '.join(y_elements)}

  <!-- Area Fill -->
  <path d="{area_d}" fill="url(#{grad_id})" />

  <!-- Smooth Curve Line -->
  <path d="{path_d}" fill="none" stroke="{line_color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />

  <!-- X Labels -->
  {' '.join(x_elements)}

  <!-- Points & Values -->
  {' '.join(point_elements)}
</svg>"""
    return svg_content


def main():
    username = os.environ.get("GITHUB_USER", "s4126139")
    token = get_token()

    print(f"Fetching contribution data for {username}...")
    user_data = fetch_contributions(username, token)
    calendar = user_data["contributionsCollection"]["contributionCalendar"]
    total_contribs, months_data = aggregate_monthly(calendar)

    print(f"Total Contributions: {total_contribs}")
    for label, count in months_data:
        print(f"  {label}: {count}")

    dist_dir = Path("dist")
    dist_dir.mkdir(parents=True, exist_ok=True)

    dark_svg = build_svg(months_data, total_contribs, username, theme="dark")
    light_svg = build_svg(months_data, total_contribs, username, theme="light")

    dark_path = dist_dir / "github-contribution-yearly-dark.svg"
    light_path = dist_dir / "github-contribution-yearly.svg"

    dark_path.write_text(dark_svg, encoding="utf-8")
    light_path.write_text(light_svg, encoding="utf-8")

    print(f"Successfully generated:")
    print(f"  - {dark_path}")
    print(f"  - {light_path}")


if __name__ == "__main__":
    main()
