# ChatGPT HTML Session Splitter

This Python script splits a large ChatGPT data export HTML file (such as `chat.html`) into individual HTML files, each containing a single chat session. Each output file preserves the original HTML structure and can be opened in a web browser.

## Features
- Handles very large ChatGPT export files (tens of MB, hundreds of sessions)
- Robustly extracts all sessions, even with complex or nested JSON
- Uses a template HTML (e.g., `chat2.html`) to ensure output files are valid and lightweight
- Outputs one HTML file per session, named by session title

## Requirements
- Python 3.7+
- No external dependencies (uses only the Python standard library)

## Usage
1. Place your large ChatGPT export file (e.g., `chat.html`) and a small template file (e.g., `chat2.html`) in the `process/` directory.
2. Place the script `split_chatGPT_takeout_html.py` in the same directory.
3. Run the script from the project root:

```bash
python3 process/split_chatGPT_takeout_html.py
```

4. The script will create a folder `process/chat_sessions/` containing one HTML file per chat session.

## How it Works
- The script scans `chat.html` for the `jsonData` array containing all chat sessions.
- It robustly parses the array, even if there are nested brackets or brackets inside strings.
- For each session, it writes a new HTML file using the structure of `chat2.html` as a template, replacing the `jsonData` array with just that session.
- Output files are named using the session index and title.

## Troubleshooting
- If you see far fewer sessions than expected, your `chat.html` may be malformed or truncated. The script will skip malformed sessions and print debug info.
- If you want to filter sessions by topic, you can further process the output files or ask for a filtering script.

## Example
After running the script, you will find files like:

```
process/chat_sessions/
  chat_session_1_Exporting_ChatGPT_Memories.html
  chat_session_2_Gamla_stugor_i_skärgården.html
  ...
```

Each file can be opened in your browser and contains only one chat session.

## License
MIT License 