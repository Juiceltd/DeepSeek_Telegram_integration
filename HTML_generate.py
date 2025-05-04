from markdown import markdown
import aiofiles
import aiofiles.os as aios
import uuid
import re
import os


html_template = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Chat Bot</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        body {{
        margin: 0;
        padding: 20px;
        font-family: 'Roboto', sans-serif;
        background-color: #f9f9f9;
        color: #333;
        }}
        .container {{
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        }}
        .content {{
        display: flex;
        flex-direction: column;
        width: 100%;
        max-width: 450px;
        background-color: #fff;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }}
        p {{
        line-height: 1.6;
        margin: 10px 0;
        }}
        a {{
        color: #007bff;
        text-decoration: none;
        }}
        a:hover {{
        text-decoration: underline;
        }}
        code {{
        font-family: 'Courier New', Courier, monospace;
        background-color: #f1f1f1;
        padding: 2px 4px;
        border-radius: 4px;
        }}
        pre {{
        background-color: #f1f1f1;
        padding: 15px;
        border-radius: 8px;
        overflow-x: auto;
        margin: 10px 0;
        }}
        ul, ol {{
        margin: 10px 0 10px 20px;
        }}
        @media (max-width: 450px) {{
        .content {{
        margin: 0 10px;
        }}
        }}
    </style>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script>
        MathJax = {{
                    tex: {{
                    inlineMath: [['$', '$'], ['\\(', '\\)']],
                    displayMath: [['$$','$$'], ['\\[','\\]']]
                        }}
                }};
    </script>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
</head>
<body>
<div class="container">
    <div class="content">
        {content}
    </div>
</div>
</body>
</html>
"""

async def update_html_page(user_id, content: str):
    allowed_chars = "_*~`?>#+-=|{}.!:,—"
    pattern = re.compile(r'\\([' + re.escape(allowed_chars) + r'])')
    unescaped_content = pattern.sub(r'\1', content)
    unescaped_content = unescaped_content.replace('***', '**')
    new_content = markdown(unescaped_content, extensions=["fenced_code", "codehilite"])
    html_content = html_template.format(user_id=user_id, content=new_content)
    token = str(uuid.uuid4().hex)
    try:
        await aios.makedirs(f'pages/{token}')
    except Exception:
        pass
    async with aiofiles.open(f'pages/{token}/index.html', 'w', encoding='utf8') as f:
        await f.write(html_content)
    return token
