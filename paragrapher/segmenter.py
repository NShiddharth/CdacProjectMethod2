from typing import List, Dict
import re
from utils.validators import is_valid_paragraph
from config import MIN_WORDS_PER_PARAGRAPH

def detect_heading(line: str) -> bool:
    """
    Detects if a given block or line is likely a heading.
    Heading detection logic is based on:
    - Short length (<80 characters)
    - Mostly Title Case or ALL CAPS
    - Ends without punctuation
    - Contains numbering patterns like "1.", "1.1", "Chapter", "Section", "Topic"
    """
    line = line.strip()
    if not line:
        return False
        
    # Focus on the first line if it's a multi-line block
    first_line = line.split('\n')[0].strip()
    if not first_line:
        return False
        
    # Rule 1: Line length is short (<80 characters)
    is_short = len(first_line) < 80
    
    # Rule 2: Ends without punctuation
    ends_without_punct = first_line[-1] not in ".?!"
    
    # Rule 3: Mostly Title Case or ALL CAPS
    words = first_line.split()
    mostly_caps = False
    if words:
        cap_counts = sum(1 for w in words if w.istitle() or w.isupper())
        mostly_caps = (cap_counts / len(words)) > 0.5
        
    # Rule 4: Contains numbering patterns like "1.", "1.1", "Chapter", "Section", etc.
    pattern = re.compile(r'^(\d+(\.\d+)*\.?)\s+|^(Chapter|Section|Topic)\b', re.IGNORECASE)
    has_pattern = bool(pattern.search(first_line))
    
    # A heading is likely if it is short, ends without punctuation, and has heading-like text
    if is_short and ends_without_punct and (mostly_caps or has_pattern):
        return True
        
    return False

def detect_paragraphs(pages_text: List[str]) -> List[Dict[str, str]]:
    """
    Parses a list of text pages into individual, valid paragraphs.
    Implements cross-page continuation logic so sentences are properly merged.
    Returns a list of dictionaries, each containing:
    {
       "paragraph_id": int,
       "text": str
    }
    """
    paragraphs = []
    paragraph_id = 1
    
    pending_paragraph = ""
    
    # Extract text page by page using a loop over pages_text
    for page_num, page in enumerate(pages_text):
        # Split text by two or more consecutive newlines to get basic blocks
        raw_blocks = re.split(r'\n\s*\n+', page)
        
        first_block_on_page = True
        
        for block in raw_blocks:
            block = block.strip()
            if not block:
                continue
                
            cleaned_block = re.sub(r'\n+', ' ', block).strip()
            
            should_merge = False
            
            # Check cross-page merging rules if transitioning to a new page
            if first_block_on_page and pending_paragraph:
                is_heading = detect_heading(block)
                
                first_line = block.split('\n')[0].strip()
                starts_with_lower = first_line[0].islower() if first_line else False
                first_line_long = len(first_line) > 80
                prev_ends_without_punct = pending_paragraph[-1] not in ".?!" if pending_paragraph else False
                
                # Cross-page continuation rules
                if not is_heading:
                    if prev_ends_without_punct or starts_with_lower or first_line_long:
                        should_merge = True
                        
            # Mark that we've processed the first valid block on this page
            first_block_on_page = False
            
            if should_merge:
                # APPEND to the previous paragraph
                pending_paragraph += " " + cleaned_block
            else:
                # Save previous pending paragraph
                if pending_paragraph:
                    if is_valid_paragraph(pending_paragraph, MIN_WORDS_PER_PARAGRAPH):
                        paragraphs.append({
                            "paragraph_id": paragraph_id,
                            "text": pending_paragraph
                        })
                        paragraph_id += 1
                
                # Start a new paragraph block
                pending_paragraph = cleaned_block
                
    # Append the last remaining paragraph after loop finishes
    if pending_paragraph:
        if is_valid_paragraph(pending_paragraph, MIN_WORDS_PER_PARAGRAPH):
            paragraphs.append({
                "paragraph_id": paragraph_id,
                "text": pending_paragraph
            })
            
    return paragraphs
