from IPython.display import HTML, display
from typing import Any, Optional
import json
import uuid

def get_theme_colors(is_dark: bool) -> dict:
    """Returns color scheme based on dark/light mode preference."""
    return {
        'background': '#1e1e1e' if is_dark else '#f8f9fa',
        'text': '#d4d4d4' if is_dark else '#2c3e50',
        'string': '#6A9955' if is_dark else '#28a745',
        'number': '#569CD6' if is_dark else '#0066cc',
        'boolean': '#C586C0' if is_dark else '#e83e8c',
        'null': '#808080' if is_dark else '#6c757d',
        'key': '#4EC9B0' if is_dark else '#2c3e50',
        'line': '#404040' if is_dark else '#dee2e6',
        'collapsible_bg': '#2d2d2d' if is_dark else '#e9ecef',
        'collapsible_hover': '#383838' if is_dark else '#dee2e6',
        'collapsible_border': '#404040' if is_dark else '#ced4da',
        'property_hover': 'rgba(255,255,255,0.02)' if is_dark else 'rgba(0,0,0,0.02)',
        'shadow': 'rgba(0,0,0,0.2)' if is_dark else 'rgba(0,0,0,0.05)'
    }

def get_marker(index: int, length: int) -> str:
    """Returns the marker for the current property based on its position."""
    if index == 0:
        return "┐"  # Top corner
    elif index == length - 1:
        return "┘"  # Bottom corner
    else:
        return "├"  # Middle connector

def format_value(v: Any, depth: int = 0, path: str = '', max_depth: Optional[int] = None) -> str:
    """
    Formats a value into HTML with proper styling and structure.
    """
    if max_depth is not None and depth >= max_depth:
        return '<span class="json-string">"..."</span>'

    if isinstance(v, dict):
        return format_dict(v, depth, path, max_depth)
    elif isinstance(v, list):
        return format_list(v, depth, path, max_depth)
    elif isinstance(v, str):
        return f'<span class="json-string">"{v}"</span>'
    elif isinstance(v, bool):
        return f'<span class="json-boolean">{str(v).lower()}</span>'
    elif v is None:
        return '<span class="json-null">null</span>'
    else:
        return f'<span class="json-number">{v}</span>'

def format_dict(d: dict, depth: int, path: str, max_depth: Optional[int]) -> str:
    """Formats dictionary values with proper indentation and styling."""
    if not d:
        return '<span class="json-bracket">{}</span>'

    result = [
        '<div class="json-collapsible-container">',
        '<span class="collapsible">▼</span>',
        '<div class="content"><div class="json-container">'
    ]

    items = list(d.items())
    for i, (k, v) in enumerate(items):
        marker = get_marker(i, len(items))
        current_path = f"{path}.{k}" if path else k
        
        result.append(
            f'<div class="property">'
            f'<span class="depth-marker">{marker}</span>'
            f'<span class="json-key">"{k}"</span>'
            f'<span class="key-value-separator">:</span>'
            f'{format_value(v, depth + 1, current_path, max_depth)}'
            f'{"," if i < len(items) - 1 else ""}</div>'
        )

    result.append('</div></div></div>')
    return '\n'.join(result)

def format_list(lst: list, depth: int, path: str, max_depth: Optional[int]) -> str:
    """Formats list values with proper indentation and styling."""
    if not lst:
        return '<span class="json-bracket">[]</span>'

    result = [
        '<div class="json-collapsible-container">',
        '<span class="collapsible">▼</span>',
        '<div class="content"><div class="json-container">'
    ]

    for i, item in enumerate(lst):
        marker = get_marker(i, len(lst))
        current_path = f"{path}[{i}]"
        
        result.append(
            f'<div class="property">'
            f'<span class="depth-marker">{marker}</span>'
            f'{format_value(item, depth + 1, current_path, max_depth)}'
            f'{"," if i < len(lst) - 1 else ""}</div>'
        )

    result.append('</div></div></div>')
    return '\n'.join(result)

def generate_css(theme_id: str) -> str:
    """Generates CSS styles for the JSON viewer with scoped variables."""
    return f"""
    <style id="json-viewer-styles-{theme_id}">
    #json-viewer-{theme_id} {{
        font-family: 'JetBrains Mono', 'Fira Code', Consolas, monospace;
        font-size: 10px;
        background-color: var(--theme-{theme_id}-background);
        color: var(--theme-{theme_id}-text);
        border-radius: 8px;
        padding: 1.5em;
        line-height: 1.6;
        box-shadow: 0 2px 8px var(--theme-{theme_id}-shadow);
    }}
    
    #json-viewer-{theme_id} .json-title {{
        font-size: 12px;
        font-weight: bold;
        margin-bottom: 15px;
        color: var(--theme-{theme_id}-text);
        border-bottom: 2px solid var(--theme-{theme_id}-line);
        padding-bottom: 8px;
    }}
    
    #json-viewer-{theme_id} .json-string {{ color: var(--theme-{theme_id}-string); word-break: break-word; }}
    #json-viewer-{theme_id} .json-number {{ color: var(--theme-{theme_id}-number); }}
    #json-viewer-{theme_id} .json-boolean {{ color: var(--theme-{theme_id}-boolean); }}
    #json-viewer-{theme_id} .json-null {{ color: var(--theme-{theme_id}-null); }}
    #json-viewer-{theme_id} .json-key {{
        color: var(--theme-{theme_id}-key);
        font-weight: 600;
        margin-right: 8px;
    }}
    
    #json-viewer-{theme_id} .json-bracket {{ color: var(--theme-{theme_id}-text); opacity: 0.7; }}
    #json-viewer-{theme_id} .json-container {{ position: relative; padding-left: 24px; }}
    
    #json-viewer-{theme_id} .json-collapsible-container {{
        position: relative;
        display: inline-block;
        width: 100%;
    }}

    #json-viewer-{theme_id} .collapsible {{
        cursor: pointer;
        padding: 2px 8px;
        background-color: var(--theme-{theme_id}-collapsible-bg);
        border-radius: 4px;
        display: inline-block;
        margin: 2px;
        transition: all 0.2s;
        border: 1px solid transparent;
    }}
    
    #json-viewer-{theme_id} .collapsible:hover {{
        background-color: var(--theme-{theme_id}-collapsible-hover);
        border-color: var(--theme-{theme_id}-collapsible-border);
    }}
    
    #json-viewer-{theme_id} .content {{ display: block; position: relative; }}
    #json-viewer-{theme_id} .collapsed {{ display: none !important; }}
    
    #json-viewer-{theme_id} .property {{
        display: flex;
        align-items: flex-start;
        padding: 2px 0;
        border-radius: 4px;
    }}
    
    #json-viewer-{theme_id} .property:hover {{
        background-color: var(--theme-{theme_id}-property-hover);
    }}
    
    #json-viewer-{theme_id} .key-value-separator {{
        margin: 0 8px;
        color: var(--theme-{theme_id}-null);
    }}
    
    #json-viewer-{theme_id} .depth-marker {{
        color: var(--theme-{theme_id}-null);
        margin-right: 8px;
        font-size: 10px;
        opacity: 0.5;
    }}
    </style>
    """

def display_json(
    data: Any,
    title: Optional[str] = None,
    max_depth: Optional[int] = None,
    collapsed: bool = False,
    indent_size: int = 24,
    dark_mode: bool = False
) -> None:
    """
    Displays JSON data in Jupyter Notebooks with enhanced visual hierarchy and dynamic theme support.
    """
    try:
        viewer_id = str(uuid.uuid4())
        light_theme = json.dumps(get_theme_colors(False))
        dark_theme = json.dumps(get_theme_colors(True))
        
        script = f"""
        <script>
        (function() {{
            const viewerId = "{viewer_id}";
            const lightTheme = {light_theme};
            const darkTheme = {dark_theme};
            
            function setThemeColors(isDark) {{
                const theme = isDark ? darkTheme : lightTheme;
                const root = document.querySelector(`#json-viewer-${{viewerId}}`);
                if (!root) return;
                
                Object.entries(theme).forEach(([key, value]) => {{
                    root.style.setProperty(`--theme-${{viewerId}}-${{key}}`, value);
                }});
            }}
            
            function setupCollapsible(viewerElement) {{
                const collapsibles = viewerElement.querySelectorAll('.collapsible');
                collapsibles.forEach(button => {{
                    button.addEventListener('click', function(e) {{
                        e.stopPropagation();
                        const content = this.nextElementSibling;
                        const isCollapsed = content.classList.contains('collapsed');
                        
                        if (isCollapsed) {{
                            content.classList.remove('collapsed');
                            this.textContent = '▼';
                        }} else {{
                            content.classList.add('collapsed');
                            this.textContent = '▶';
                        }}
                    }});
                }});
                
                if ({str(collapsed).lower()}) {{
                    collapsibles.forEach(button => {{
                        const content = button.nextElementSibling;
                        content.classList.add('collapsed');
                        button.textContent = '▶';
                    }});
                }}
            }}
            
            // Initialize
            setThemeColors({str(dark_mode).lower()});
            
            // Setup after a short delay to ensure DOM is ready
            setTimeout(() => {{
                const viewer = document.getElementById(`json-viewer-${{viewerId}}`);
                if (viewer) {{
                    setupCollapsible(viewer);
                }}
            }}, 100);
        }})();
        </script>
        """
        
        # Combine all components
        html_content = [generate_css(viewer_id)]
        html_content.append(f'<div id="json-viewer-{viewer_id}">')
        
        if title:
            escaped_title = title.replace('<', '&lt;').replace('>', '&gt;')
            html_content.append(f'<div class="json-title">{escaped_title}</div>')
        
        json_content = format_value(data, max_depth=max_depth)
        html_content.append(f'<div class="json-content">{json_content}</div>')
        
        html_content.append('</div>')
        html_content.append(script)
        
        display(HTML('\n'.join(html_content)))
        
    except Exception as e:
        raise ValueError(f"Failed to process JSON data: {str(e)}") from e