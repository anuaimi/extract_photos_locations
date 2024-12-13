# Extract Photos Locations

This script will extract the geo info for a set of photos for a given date range.

## Setup

You need to give the terminal access to the photos database.

- Open System Settings
- Go to Apple Menu > System Settings > Privacy & Security.
- Navigate to Full Disk Access
- Scroll down and click Full Disk Access under the Privacy section.
- Add Your Terminal Application
- Click the + button.
- Navigate to the Terminal app (or any other terminal you're using, e.g., iTerm).
- Select it and confirm.
- Restart Your Terminal
- Close and reopen your terminal for the changes to take effect.

## Usage

```bash
python extract_geo.py --start-date 2024-01-01 --end-date 2024-01-31
```
