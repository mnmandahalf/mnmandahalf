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
  <!-- Pixel art rubber duck (facing right) -->
  <!-- Beak -->
  <rect x="28" y="16" width="4" height="4" fill="#ff9500"/>
  <rect x="28" y="20" width="4" height="4" fill="#ff9500"/>

  <!-- Head -->
  <rect x="16" y="12" width="4" height="4" fill="#ffdd00"/>
  <rect x="20" y="12" width="4" height="4" fill="#ffdd00"/>
  <rect x="24" y="12" width="4" height="4" fill="#ffdd00"/>
  <rect x="16" y="16" width="4" height="4" fill="#ffdd00"/>
  <rect x="20" y="16" width="4" height="4" fill="#ffdd00"/>
  <rect x="24" y="16" width="4" height="4" fill="#ffdd00"/>
  <rect x="16" y="20" width="4" height="4" fill="#ffdd00"/>
  <rect x="20" y="20" width="4" height="4" fill="#ffdd00"/>
  <rect x="24" y="20" width="4" height="4" fill="#ffdd00"/>

  <!-- Eye -->
  <rect x="24" y="14" width="2" height="2" fill="#000000"/>

  <!-- Body -->
  <rect x="0" y="24" width="4" height="4" fill="#ffdd00"/>
  <rect x="4" y="24" width="4" height="4" fill="#ffdd00"/>
  <rect x="8" y="24" width="4" height="4" fill="#ffdd00"/>
  <rect x="12" y="24" width="4" height="4" fill="#ffdd00"/>
  <rect x="16" y="24" width="4" height="4" fill="#ffdd00"/>
  <rect x="20" y="24" width="4" height="4" fill="#ffdd00"/>
  <rect x="24" y="24" width="4" height="4" fill="#ffdd00"/>

  <rect x="0" y="28" width="4" height="4" fill="#ffdd00"/>
  <rect x="4" y="28" width="4" height="4" fill="#ffdd00"/>
  <rect x="8" y="28" width="4" height="4" fill="#ffdd00"/>
  <rect x="12" y="28" width="4" height="4" fill="#ffdd00"/>
  <rect x="16" y="28" width="4" height="4" fill="#ffdd00"/>
  <rect x="20" y="28" width="4" height="4" fill="#ffdd00"/>
  <rect x="24" y="28" width="4" height="4" fill="#ffdd00"/>

  <rect x="4" y="32" width="4" height="4" fill="#ffdd00"/>
  <rect x="8" y="32" width="4" height="4" fill="#ffdd00"/>
  <rect x="12" y="32" width="4" height="4" fill="#ffdd00"/>
  <rect x="16" y="32" width="4" height="4" fill="#ffdd00"/>
  <rect x="20" y="32" width="4" height="4" fill="#ffdd00"/>

  <!-- Shadow -->
  <rect x="20" y="28" width="4" height="4" fill="#ffcc00" opacity="0.5"/>
  <rect x="24" y="28" width="4" height="4" fill="#ffcc00" opacity="0.5"/>
  <rect x="16" y="32" width="4" height="4" fill="#ffcc00" opacity="0.5"/>
  <rect x="20" y="32" width="4" height="4" fill="#ffcc00" opacity="0.5"/>
</g>

</svg>
"""

open("duck.svg","w").write(svg)
