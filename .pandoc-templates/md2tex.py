#!/usr/bin/env python3
"""Convert Markdown to minimal LaTeX - no fluff."""

import re
import sys

def convert(md):
    lines = md.split('\n')
    out = []
    list_stack = []  # stack of ('ul'|'ol', indent_level)
    in_table = False
    table_rows = []
    
    def get_indent(line):
        return len(line) - len(line.lstrip())
    
    def close_lists_to_level(target_indent):
        while list_stack and list_stack[-1][1] >= target_indent:
            list_type, _ = list_stack.pop()
            if list_type == 'ul':
                out.append('\\end{itemize}')
            else:
                out.append('\\end{enumerate}')
    
    def close_all_lists():
        close_lists_to_level(0)
    
    def flush_table():
        nonlocal in_table, table_rows
        if not table_rows:
            return
        ncols = len(table_rows[0])
        out.append('')
        out.append('\\begin{table}[h]')
        out.append('\\centering')
        out.append('\\begin{tabular}{' + 'l' * ncols + '}')
        out.append('\\hline')
        for i, row in enumerate(table_rows):
            out.append(' & '.join(row) + ' \\\\')
            if i == 0:  # header
                out.append('\\hline')
        out.append('\\hline')
        out.append('\\end{tabular}')
        out.append('\\end{table}')
        table_rows = []
        in_table = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Table row
        if line.strip().startswith('|') and line.strip().endswith('|'):
            cells = [c.strip() for c in line.strip()[1:-1].split('|')]
            # Skip separator rows (|---|---|)
            if all(re.match(r'^[-:]+$', c) for c in cells):
                i += 1
                continue
            if not in_table:
                close_all_lists()
                in_table = True
            table_rows.append([convert_inline(c) for c in cells])
            i += 1
            continue
        elif in_table:
            flush_table()
        
        # Headers
        if m := re.match(r'^(#{1,4})\s+(.+)$', line):
            close_all_lists()
            level = len(m.group(1))
            title = convert_inline(m.group(2))
            cmd = ['\\section', '\\subsection', '\\subsubsection', '\\paragraph'][level-1]
            out.append('')
            out.append('')
            out.append(f'{cmd}{{{title}}}')
            i += 1
            continue
        
        # Unordered list
        if m := re.match(r'^(\s*)[-*]\s+(.+)$', line):
            indent = get_indent(line)
            # Close deeper nested lists
            while list_stack and list_stack[-1][1] > indent:
                list_type, _ = list_stack.pop()
                out.append('\\end{itemize}' if list_type == 'ul' else '\\end{enumerate}')
            # Start new list if no list or this is nested deeper
            if not list_stack or indent > list_stack[-1][1]:
                if not list_stack:  # only add blank line for top-level list
                    out.append('')
                out.append('\\begin{itemize}')
                list_stack.append(('ul', indent))
            out.append(f'\\item {convert_inline(m.group(2))}')
            i += 1
            continue
        
        # Ordered list
        if m := re.match(r'^(\s*)\d+\.\s+(.+)$', line):
            indent = get_indent(line)
            # Close deeper nested lists
            while list_stack and list_stack[-1][1] > indent:
                list_type, _ = list_stack.pop()
                out.append('\\end{itemize}' if list_type == 'ul' else '\\end{enumerate}')
            # Start new list if no list or this is nested deeper
            if not list_stack or indent > list_stack[-1][1]:
                if not list_stack:  # only add blank line for top-level list
                    out.append('')
                out.append('\\begin{enumerate}')
                list_stack.append(('ol', indent))
            out.append(f'\\item {convert_inline(m.group(2))}')
            i += 1
            continue
        
        # Image
        if m := re.match(r'^!\[.*?\]\((.+?)\)$', line.strip()):
            close_all_lists()
            out.append('')
            out.append('\\begin{figure}[h]')
            out.append('\\centering')
            out.append(f'\\includegraphics[width=\\textwidth]{{{m.group(1)}}}')
            out.append('\\end{figure}')
            i += 1
            continue
        
        # Empty line - don't close lists yet, just add blank
        if not line.strip():
            out.append('')
            i += 1
            continue
        
        # Regular paragraph - close lists before adding
        close_all_lists()
        out.append(convert_inline(line))
        i += 1
    
    close_all_lists()
    flush_table()
    return '\n'.join(out)

def convert_inline(text):
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text)
    text = re.sub(r'__(.+?)__', r'\\textbf{\1}', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'\\textit{\1}', text)
    text = re.sub(r'_(.+?)_', r'\\textit{\1}', text)
    # Code
    text = re.sub(r'`(.+?)`', r'\\texttt{\1}', text)
    # Escape %
    text = text.replace('%', '\\%')
    return text

if __name__ == '__main__':
    if len(sys.argv) < 2:
        md = sys.stdin.read()
    else:
        with open(sys.argv[1]) as f:
            md = f.read()
    
    print(convert(md))
