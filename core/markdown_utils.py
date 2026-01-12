import re
import os

def transform_hints(content):
    """
    Transforms GitBook hints and GitHub alerts to Starlight asides.
    """
    # GitBook Hints
    # {% hint style="info" %} ... {% endhint %}
    gitbook_style_map = {
        'info': 'note',
        'warning': 'caution',
        'danger': 'danger',
        'success': 'tip'
    }
    
    def gitbook_repl(match):
        style = match.group(1)
        body = match.group(2).strip()
        starlight_type = gitbook_style_map.get(style, 'note')
        return f":::{starlight_type}\n{body}\n:::\n"

    content = re.sub(r'{% hint style="(\w+)" %}\s*([\s\S]*?)\s*{% endhint %}', gitbook_repl, content)

    # GitHub Alerts
    # > [!NOTE]
    # > ...
    alert_map = {
        'NOTE': 'note',
        'TIP': 'tip',
        'IMPORTANT': 'caution',
        'WARNING': 'caution',
        'CAUTION': 'danger'
    }

    def alert_repl(match):
        type_upper = match.group(1)
        body = match.group(2)
        starlight_type = alert_map.get(type_upper, 'note')
        
        # Clean body: remove '> ' prefixes
        lines = body.split('\n')
        cleaned_lines = []
        custom_title = ""
        
        # Check first line for custom title: > ##### Title
        if lines:
            first_line_raw = lines[0].strip()
            # Remove leading '>' and space
            # But the regex group 2 captures the block including '>' so we need to be careful
            # Actually group 2 is the rest of the block.
            pass

        # Easier way: iterate lines, strip '> ?'
        cleaned_body_lines = []
        for line in lines:
            line = re.sub(r'^>\s?', '', line)
            cleaned_body_lines.append(line)
            
        full_cleaned_body = "\n".join(cleaned_body_lines).strip()
        
        # Check title in first line of cleaned body
        if full_cleaned_body.startswith('#'):
            # e.g. ##### My Title
            # Extract title
            parts = full_cleaned_body.split('\n', 1)
            first_line = parts[0]
            rest = parts[1] if len(parts) > 1 else ""
            
            title_match = re.match(r'^#+\s+(.*)$', first_line)
            if title_match:
                custom_title = title_match.group(1).strip()
                full_cleaned_body = rest.strip()
        
        title_part = f"[{custom_title}]" if custom_title else ""
        return f":::{starlight_type}{title_part}\n{full_cleaned_body}\n:::\n"

    content = re.sub(r'^> \[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\n((?:> ?.*\n?)*)', alert_repl, content, flags=re.MULTILINE)
    
    return content

def add_frontmatter(content, title, order=None):
    """
    Injects or updates Starlight frontmatter.
    """
    # Check for existing frontmatter
    fm_regex = r'^---\n([\s\S]*?)\n---\n'
    match = re.match(fm_regex, content)
    
    existing_fm = ""
    body = content
    
    if match:
        existing_fm = match.group(1)
        body = content[match.end():]
    
    # Construct new frontmatter values
    new_fm_lines = []
    
    # Detect title if not in existing FM
    if 'title:' not in existing_fm:
        new_fm_lines.append(f'title: {title}')
    
    # Add sidebar order if provided and not present
    if order is not None and 'sidebar:' not in existing_fm:
        new_fm_lines.append('sidebar:')
        new_fm_lines.append(f'  order: {order}')
    
    # Merge
    if existing_fm:
        # Simple append if we aren't parsing YAML fully
        # This is risky if keys exist. ideally we use yaml parser.
        # But for new files from crawler, existing_fm is usually empty or basic.
        final_fm = existing_fm + "\n" + "\n".join(new_fm_lines)
    else:
        final_fm = "\n".join(new_fm_lines)
    
    return f"---\n{final_fm}\n---\n\n{body}"

def process_markdown(content, file_path, title, order=None):
    """
    Main entry point for processing.
    """
    # Remove H1 header from the body to avoid duplication with Starlight title
    # First, separate existing frontmatter if any
    fm_match = re.match(r'^---\n([\s\S]*?)\n---\n', content)
    if fm_match:
        frontmatter = fm_match.group(0)
        body = content[fm_match.end():]
    else:
        frontmatter = ""
        body = content

    # Remove the first H1 header found in the body
    # This matches a line starting with one '#' and space, possibly preceded by whitespace/newlines
    body = re.sub(r'^\s*#\s+.*$', '', body, count=1, flags=re.MULTILINE).lstrip()
    
    # Recombine for further processing
    content = frontmatter + body

    content = transform_hints(content)
    content = add_frontmatter(content, title, order)
    return content
