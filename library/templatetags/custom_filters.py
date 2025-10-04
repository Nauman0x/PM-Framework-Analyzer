from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter(name='format_markdown', is_safe=True)
def format_markdown(text):
    """Convert basic markdown to HTML for analysis display"""
    if not text:
        return ""
    
    # Remove excessive blank lines (more than 2 consecutive)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Convert ## headers to HTML
    text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    
    # Convert ### headers to HTML
    text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    
    # Convert **bold** to HTML
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    
    # Convert *italic* to HTML (but not already in strong tags)
    text = re.sub(r'(?<!</strong>)\*([^*]+?)\*(?!<strong>)', r'<em>\1</em>', text)
    
    # Convert bullet points
    lines = text.split('\n')
    in_list = False
    result_lines = []
    
    for line in lines:
        if line.strip().startswith('* '):
            if not in_list:
                result_lines.append('<ul>')
                in_list = True
            result_lines.append(f'<li>{line.strip()[2:]}</li>')
        else:
            if in_list:
                result_lines.append('</ul>')
                in_list = False
            result_lines.append(line)
    
    if in_list:
        result_lines.append('</ul>')
    
    text = '\n'.join(result_lines)
    
    # Convert paragraphs (lines with content that aren't HTML)
    final_lines = []
    for line in text.split('\n'):
        line = line.strip()
        if line and not line.startswith('<') and not line.endswith('>'):
            if not any(line.startswith(tag) for tag in ['<h2>', '<h3>', '<ul>', '<li>', '<p>']):
                line = f'<p>{line}</p>'
        if line:
            final_lines.append(line)
    
    return mark_safe('\n'.join(final_lines))
