#!/usr/bin/env python3
"""
Format ChatGPT Deep Research markdown output for clean PDF conversion.

Cleans up:
- entity["type","name","description"] → **name** (description)
- citeturnXXsearchXX markers → removes or formats as footnote references
- image_group{...} blocks → removes or converts to placeholder text

ChatGPT Deep Research uses special Unicode markers (Private Use Area):
- U+E200 (\ue200): Start of annotated element
- U+E201 (\ue201): End of annotated element  
- U+E202 (\ue202): Content separator within element
"""

import re
import sys
import argparse
from pathlib import Path


# Unicode Private Use Area markers used by ChatGPT Deep Research
MARKER_START = '\ue200'   # Start of annotated element
MARKER_END = '\ue201'     # End of annotated element
MARKER_SEP = '\ue202'     # Content separator


def format_entities(text: str) -> str:
    """Find and replace all entity markers with formatted text."""
    # Pattern: \ue200entity\ue202["type","name","desc"]\ue201
    pattern = re.escape(MARKER_START) + r'entity' + re.escape(MARKER_SEP) + r'\[([^\]]+)\]' + re.escape(MARKER_END)
    
    def replace_entity(match):
        content = match.group(1)
        parts = re.findall(r'"([^"]*)"', content)
        if len(parts) >= 2:
            name = parts[1]
            description = parts[2] if len(parts) > 2 else ""
            if description:
                return f"**{name}** ({description})"
            return f"**{name}**"
        return match.group(0)
    
    return re.sub(pattern, replace_entity, text)


def format_citations(text: str, style: str = "remove") -> str:
    """
    Handle citation markers with Unicode delimiters.
    Format: \ue200cite\ue202turn19search6\ue202turn19search5\ue201
    
    Styles:
    - 'remove': Delete citation markers entirely
    - 'footnote': Convert to numbered footnote style [1]
    - 'bracket': Convert to bracketed reference [cite]
    """
    # Pattern matches the full citation block including Unicode markers
    pattern = re.escape(MARKER_START) + r'cite(?:' + re.escape(MARKER_SEP) + r'turn\d+(?:search|view)\d+)+' + re.escape(MARKER_END)
    
    if style == "remove":
        return re.sub(pattern, '', text)
    elif style == "footnote":
        counter = [0]
        def replace_with_number(m):
            counter[0] += 1
            return f"[{counter[0]}]"
        return re.sub(pattern, replace_with_number, text)
    elif style == "bracket":
        return re.sub(pattern, '[cite]', text)
    return text


def remove_image_groups(text: str, replacement: str = "") -> str:
    """Remove or replace image_group{...} blocks."""
    # Pattern matches image_group with possible Unicode markers and JSON content
    # First try with Unicode markers
    pattern_with_markers = re.escape(MARKER_START) + r'image_group' + re.escape(MARKER_SEP) + r'\{[^}]+\}' + re.escape(MARKER_END)
    text = re.sub(pattern_with_markers, replacement, text)
    
    # Also try plain image_group (without markers)
    pattern_plain = r'image_group\{[^}]+\}'
    text = re.sub(pattern_plain, replacement, text)
    
    return text


def clean_extra_whitespace(text: str) -> str:
    """Clean up extra whitespace left after removals."""
    # Remove multiple consecutive blank lines (keep max 2)
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Remove trailing spaces on lines
    text = re.sub(r' +$', '', text, flags=re.MULTILINE)
    # Remove spaces before punctuation (from removed citations)
    text = re.sub(r' +([.,;:!?])', r'\1', text)
    return text


def format_deep_research(content: str, citation_style: str = "remove") -> str:
    """Apply all formatting transformations."""
    # Format entity markers
    content = format_entities(content)
    
    # Handle citations
    content = format_citations(content, citation_style)
    
    # Remove image groups
    content = remove_image_groups(content)
    
    # Clean up whitespace
    content = clean_extra_whitespace(content)
    
    return content


def main():
    parser = argparse.ArgumentParser(
        description="Format ChatGPT Deep Research markdown for PDF conversion"
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Input markdown file"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output file (default: input-formatted.md)"
    )
    parser.add_argument(
        "--citations",
        choices=["remove", "footnote", "bracket"],
        default="remove",
        help="How to handle citations (default: remove)"
    )
    parser.add_argument(
        "--inplace",
        action="store_true",
        help="Modify the input file in place"
    )
    
    args = parser.parse_args()
    
    if not args.input.exists():
        print(f"Error: File '{args.input}' not found", file=sys.stderr)
        sys.exit(1)
    
    content = args.input.read_text(encoding="utf-8")
    formatted = format_deep_research(content, args.citations)
    
    if args.inplace:
        output_path = args.input
    elif args.output:
        output_path = args.output
    else:
        output_path = args.input.with_stem(args.input.stem + "-formatted")
    
    output_path.write_text(formatted, encoding="utf-8")
    print(f"Formatted output written to: {output_path}")


if __name__ == "__main__":
    main()
