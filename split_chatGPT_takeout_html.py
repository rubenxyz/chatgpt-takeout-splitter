import os
import json

def extract_json_data_streaming_sessions(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    start_marker = 'var jsonData = ['
    start = content.find(start_marker)
    if start == -1:
        raise ValueError('Could not find jsonData array in the HTML file.')
    json_start = start + len('var jsonData = ')
    # Find the first [ after the marker
    while content[json_start] != '[':
        json_start += 1
    # Now scan for the matching closing ] at the top level, ignoring brackets inside strings
    idx = json_start
    bracket_count = 0
    in_string = False
    escape = False
    array_start = json_start
    array_end = None
    while idx < len(content):
        c = content[idx]
        if escape:
            escape = False
        elif c == '\\':
            escape = True
        elif c == '"':
            in_string = not in_string
        elif not in_string:
            if c == '[':
                bracket_count += 1
            elif c == ']':
                bracket_count -= 1
                if bracket_count == 0:
                    array_end = idx + 1
                    break
        idx += 1
    else:
        raise ValueError('Could not find the end of the jsonData array.')
    json_str = content[array_start:array_end]
    print(f"[DEBUG] Length of raw jsonData string: {len(json_str)}")
    # Now, stream through the array and extract each session
    sessions = []
    session = ''
    in_obj = False
    obj_brace_count = 0
    in_string = False
    escape = False
    for c in json_str[1:-1]:  # skip the outer [ and ]
        if escape:
            session += c
            escape = False
            continue
        if c == '\\':
            session += c
            escape = True
            continue
        if c == '"':
            session += c
            in_string = not in_string
            continue
        if not in_string:
            if c == '{':
                if not in_obj:
                    in_obj = True
                    session = ''
                obj_brace_count += 1
            if c == '}':
                obj_brace_count -= 1
                session += c
                if obj_brace_count == 0 and in_obj:
                    try:
                        obj = json.loads(session)
                        sessions.append(obj)
                    except Exception as e:
                        print(f"[DEBUG] Skipping malformed session: {e}")
                    in_obj = False
                    session = ''
                continue
            if in_obj:
                session += c
        else:
            if in_obj:
                session += c
    print(f"[DEBUG] Number of sessions found: {len(sessions)}")
    for i, s in enumerate(sessions[:10]):
        print(f"[DEBUG] Session {i+1} title: {s.get('title', 'No title')}")
    return sessions

def get_template_and_json_placeholder(template_path):
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    start_marker = 'var jsonData = ['
    start = template.find(start_marker)
    if start == -1:
        raise ValueError('Could not find jsonData array in the template file.')
    json_start = start + len('var jsonData = ')
    idx = json_start
    bracket_count = 0
    array_start = None
    array_end = None
    while idx < len(template):
        if template[idx] == '[':
            if bracket_count == 0:
                array_start = idx
            bracket_count += 1
        elif template[idx] == ']':
            bracket_count -= 1
            if bracket_count == 0:
                array_end = idx + 1
                break
        idx += 1
    else:
        raise ValueError('Could not find the end of the jsonData array in the template.')
    return template, array_start, array_end

def split_html_by_sessions(input_path, template_path, output_dir):
    sessions = extract_json_data_streaming_sessions(input_path)
    template, array_start, array_end = get_template_and_json_placeholder(template_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for idx, session in enumerate(sessions):
        session_json = json.dumps([session], ensure_ascii=False, indent=None)
        session_html = template[:array_start] + session_json + template[array_end:]
        title = session.get('title', f'session_{idx}').replace(' ', '_').replace('/', '_')
        filename = f"chat_session_{idx+1}_{title[:30]}.html"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as out_f:
            out_f.write(session_html)
        print(f"Created: {filepath}")

if __name__ == "__main__":
    split_html_by_sessions("process/chat.html", "process/chat2.html", "process/chat_sessions")