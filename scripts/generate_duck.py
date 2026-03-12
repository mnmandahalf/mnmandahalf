import requests
import datetime

USER = "mnmandahalf"

# Get today's date in JST (UTC+9)
jst = datetime.timezone(datetime.timedelta(hours=9))
today = datetime.datetime.now(jst).date()

# Scrape GitHub contribution graph
url = f"https://github.com/users/{USER}/contributions"
response = requests.get(url)

# Convert contribution data to a dictionary indexed by date
contributions = {}
if response.status_code == 200:
    import re
    # Extract data-date and data-level attributes
    pattern = r'data-date="([^"]+)"[^>]*data-level="(\d+)"'
    matches = re.findall(pattern, response.text)
    for date, level in matches:
        contributions[date] = int(level)

svg = f"""
<svg width="720" height="84" xmlns="http://www.w3.org/2000/svg">

<style>
.water0 {{ fill:none }}
.water1 {{ fill:#4dd2ff }}
.water2 {{ fill:#1aa3ff }}
.water3 {{ fill:#0088ff }}
.water4 {{ fill:#0066cc }}
.duck {{
  animation: swim 15s ease-in-out infinite;
}}

@keyframes swim {{
  0% {{ transform: translate(0px, 0px); }}
  10% {{ transform: translate(80px, -3px); }}
  20% {{ transform: translate(150px, 2px); }}
  30% {{ transform: translate(230px, -4px); }}
  40% {{ transform: translate(310px, 1px); }}
  50% {{ transform: translate(390px, -2px); }}
  60% {{ transform: translate(470px, 3px); }}
  70% {{ transform: translate(540px, -1px); }}
  80% {{ transform: translate(600px, 2px); }}
  90% {{ transform: translate(640px, -3px); }}
  100% {{ transform: translate(680px, 0px); }}
}}
</style>

"""

size = 10
gap = 2

# Display contributions for the past 350 days (50 weeks x 7 days)
# GitHub graph: Sunday(0) at top, Saturday(6) at bottom
# Get today's weekday (0=Mon, 6=Sun) -> Convert to GitHub format (0=Sun, 6=Sat)
today_weekday = (today.weekday() + 1) % 7  # Sunday=0, Monday=1, ..., Saturday=6

# Calculate from the oldest date (leftmost)
oldest_date = today - datetime.timedelta(days=349)
oldest_weekday = (oldest_date.weekday() + 1) % 7

for week in range(50):
    for day in range(7):
        # Calculate the date
        days_from_oldest = week * 7 + day - oldest_weekday
        if days_from_oldest < 0:
            # First week, dates before oldest_date are blank
            color = "water0"
        else:
            date = (oldest_date + datetime.timedelta(days=days_from_oldest)).strftime("%Y-%m-%d")
            # Determine color based on contribution level (0-4)
            level = contributions.get(date, 0)
            color = f"water{level}"

        svg += f'<rect class="{color}" x="{week*(size+gap)}" y="{day*(size+gap)}" width="{size}" height="{size}" rx="2"/>'

svg += """

<g class="duck">
  <!-- Smooth rubber duck illustration (facing right) -->

  <!-- Body (using path for flat bottom) -->
  <path d="M 1 28 Q 1 20, 15 20 Q 29 20, 29 28 Q 29 36, 15 36 Q 1 36, 1 28 Z" fill="#ffdd00"/>

  <!-- Head -->
  <circle cx="22" cy="18" r="9" fill="#ffdd00"/>

  <!-- Beak -->
  <ellipse cx="29" cy="18" rx="4" ry="3" fill="#ff9500"/>

  <!-- Eye -->
  <circle cx="25" cy="16" r="1.5" fill="#000000"/>

  <!-- Highlight on eye -->
  <circle cx="25.5" cy="15.5" r="0.5" fill="#ffffff"/>

  <!-- Shadow under body -->
  <ellipse cx="15" cy="36" rx="12" ry="2" fill="#000000" opacity="0.15"/>

  <!-- Shading on body -->
  <ellipse cx="18" cy="30" rx="6" ry="4" fill="#ffcc00" opacity="0.3"/>

  <!-- Highlight on head -->
  <ellipse cx="20" cy="15" rx="3" ry="2" fill="#ffff99" opacity="0.6"/>

  <!-- Wing -->
  <ellipse cx="10" cy="27" rx="3" ry="5" fill="#ffcc00" opacity="0.5"/>
</g>

<!-- Pink and white striped floatie ring -->
<g style="animation: swim 30s ease-in-out infinite;">
  <!-- Floatie ring with stripes using clipPath -->
  <defs>
    <clipPath id="ringClip">
      <path d="M -30 30 A 16 13 0 0 1 -30 56 A 16 13 0 0 1 -30 30 M -30 37 A 7 5.5 0 0 0 -30 49 A 7 5.5 0 0 0 -30 37 Z" fill-rule="evenodd"/>
    </clipPath>
  </defs>

  <!-- Background (full donut) -->
  <ellipse cx="-30" cy="43" rx="16" ry="13" fill="#ff69b4" clip-path="url(#ringClip)"/>

  <!-- White stripes -->
  <g clip-path="url(#ringClip)">
    <rect x="-46" y="30" width="6" height="26" fill="#ffffff"/>
    <rect x="-36" y="30" width="6" height="26" fill="#ffffff"/>
    <rect x="-26" y="30" width="6" height="26" fill="#ffffff"/>
    <rect x="-16" y="30" width="6" height="26" fill="#ffffff"/>
  </g>

  <!-- Inner shadow -->
  <ellipse cx="-30" cy="44" rx="7" ry="5.5" fill="#000000" opacity="0.15" clip-path="url(#ringClip)"/>

  <!-- Inner hole (transparent) -->
  <ellipse cx="-30" cy="43" rx="7" ry="5.5" fill="none"/>

  <!-- Outer shadow on ring -->
  <ellipse cx="-28" cy="49" rx="12" ry="4" fill="#ff1493" opacity="0.3" clip-path="url(#ringClip)"/>

  <!-- Highlight on top -->
  <ellipse cx="-33" cy="36" rx="5" ry="2.5" fill="#ffffff" opacity="0.6" clip-path="url(#ringClip)"/>

  <!-- Shadow under floatie -->
  <ellipse cx="-30" cy="54" rx="13" ry="2.5" fill="#000000" opacity="0.1"/>
</g>

</svg>
"""

open("duck.svg","w").write(svg)
