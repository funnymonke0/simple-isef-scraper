from datetime import datetime

# Get current time (UTC)
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

with open("README.md", "r") as f:
    content = f.read()

# Markers
start = "<!-- LAST_UPDATE -->"
end = "<!-- END_UPDATE -->"

start_idx = content.find(start) + len(start)
end_idx = content.find(end)

new_content = content[:start_idx] + f" {now} " + content[end_idx:]

with open("README.md", "w") as f:
    f.write(new_content)