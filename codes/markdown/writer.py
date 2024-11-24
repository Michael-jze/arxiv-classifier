from datetime import datetime, timezone, timedelta
from typing import Dict, List

class MarkdownWriter:
    def __init__(self, output_path: str):
        self.output_path = output_path
        
    def write_papers(self, categories: Dict[str, List[dict]], config: dict) -> None:
        """
        Write papers to markdown file with formatted structure
        
        Args:
            categories: Dictionary of categorized papers
            config: Configuration dictionary containing arxiv settings
        """
        markdown_output = []
        
        # Add title with search range and time info
        now = datetime.now(timezone.utc)
        start_date = now - timedelta(days=config['arxiv']['days'])
        markdown_output.append(f"# ArXiv Papers")
        markdown_output.append(f"Date range: {start_date.strftime('%Y-%m-%d')} to {now.strftime('%Y-%m-%d')}\n")
        
        # Add papers by category
        for category, papers in categories.items():
            markdown_output.append(f"\n## {category}")
            for paper in papers:
                markdown_output.append(f"- [{paper['title']}]({paper['url']})")
                self._add_abstract_lines(markdown_output, paper['abstract'])
                markdown_output.append("")  # Add blank line after abstract
        
        # Write to file
        markdown = "\n".join(markdown_output)
        with open(self.output_path, "w", encoding="utf-8") as file:
            file.write(markdown)
            
    def _add_abstract_lines(self, markdown_output: List[str], abstract: str) -> None:
        """
        Format and add abstract lines to markdown output
        
        Args:
            markdown_output: List of markdown lines
            abstract: Paper abstract text
        """
        abstract_lines = abstract.split('\n')
        for line in abstract_lines:
            if len(line) > 200:  # Handle long lines by wrapping at 200 chars
                words = line.split()
                current_line = []
                current_length = 0
                for word in words:
                    if current_length + len(word) + 1 <= 200:
                        current_line.append(word)
                        current_length += len(word) + 1
                    else:
                        markdown_output.append(f"  > {' '.join(current_line)}")
                        current_line = [word]
                        current_length = len(word)
                if current_line:
                    markdown_output.append(f"  > {' '.join(current_line)}")
            else:
                markdown_output.append(f"  > {line}")
