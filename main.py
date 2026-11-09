import json
from datetime import datetime
import gspread
import yt_dlp
from parishes import WESTERN_PARISHES, EASTERN_PARISHES, ROTATION_ORDER

# 1. Update/Load Rotation State
def get_next_rotation():
    with open("rotation_state.json", "r") as f:
        state = json.load(f)
    
    current_week = state.get("week_number", 1)
    # Map week to Eastern Rite index (0 through 5)
    eastern_index = (current_week - 1) % len(ROTATION_ORDER)
    selected_eastern_rite = ROTATION_ORDER[eastern_index]
    
    # Save updated state for next execution
    state["week_number"] = current_week + 1
    state["last_eastern_rite"] = selected_eastern_rite
    
    with open("rotation_state.json", "w") as f:
        json.dump(state, f, indent=2)
        
    return selected_eastern_rite

# 2. Extract Streams via yt-dlp
def fetch_upcoming_or_live_stream(channel_url):
    ydl_opts = {
        'extract_flat': True,
        'skip_download': True,
        'quiet': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(channel_url, download=False)
            if 'entries' in info:
                for entry in info['entries']:
                    is_live = entry.get('is_live')
                    live_status = entry.get('live_status')
                    
                    # Check if stream is live or upcoming
                    if is_live or live_status in ['is_live', 'is_upcoming']:
                        title = entry.get('title', 'Sunday Mass Stream')
                        url = entry.get('url') or f"https://www.youtube.com/watch?v={entry.get('id')}"
                        
                        # Time filtering (9:00 AM - 11:00 AM window validation)
                        release_timestamp = entry.get('release_timestamp')
                        if release_timestamp:
                            stream_time = datetime.fromtimestamp(release_timestamp)
                            # Checks if scheduled between 9 AM (9) and 11 AM (11)
                            if 9 <= stream_time.hour <= 11:
                                return title, url, stream_time.strftime('%I:%M %p')
                        
                        # Return live stream fallback
                        return title, url, "Live Now"
        except Exception as e:
            print(f"Error fetching {channel_url}: {e}")
            
    return None, None, None

# 3. Main Workflow
def main():
    selected_rite = get_next_rotation()
    print(f"--- Running Scraper for Eastern Rite Rotation: {selected_rite} ---")
    
    # Collect targeted channels for this week
    target_parishes = []
    for p in WESTERN_PARISHES:
        target_parishes.append({"rite": "Western", "name": p["name"], "url": p["url"]})
        
    for p in EASTERN_PARISHES.get(selected_rite, []):
        target_parishes.append({"rite": f"Eastern ({selected_rite})", "name": p["name"], "url": p["url"]})
        
    results = []
    
    for parish in target_parishes:
        print(f"Checking {parish['name']}...")
        title, url, time_str = fetch_upcoming_or_live_stream(parish["url"])
        if url:
            results.append([parish["rite"], parish["name"], title, time_str, url])
            
    # Authenticate with Google Sheets using local OAuth credentials
    gc = gspread.oauth(
        credentials_filename="credentials.json",
        authorized_user_filename="token.json"
    )
    
    # Open Google Sheet
    sh = gc.open("Sunday Mass Stream Tracker")
    worksheet = sh.sheet1
    
    # Header check and row insertion
    if not worksheet.get_all_values():
        worksheet.append_row(["Rite", "Parish Name", "Stream Title", "Time Window", "Stream Link"])
        
    for row in results:
        worksheet.append_row(row)
        
    print(f"Successfully appended {len(results)} active streams to Google Sheets!")

if __name__ == "__main__":
    main()
    