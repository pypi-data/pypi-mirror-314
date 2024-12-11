import os
import re
import unicodedata
from bs4 import BeautifulSoup
import logging

class EdgarDSRS:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def clean_noisy_text(self, text):
        if not text:
            return ""
        
        def is_noisy(word):
            if re.match(r'^\d{10}-\d{2}-\d{6}(\.txt|\.hdr\.sgml)?$', word):
                return False
            
            return len(word) > 15 and (
                re.search(r'[A-Z].*[a-z].*\d', word) or 
                re.search(r'[^A-Za-z0-9]', word)
            )
        
        cleaned_words = [word for word in text.split() if not is_noisy(word)]
        return ' '.join(cleaned_words)

    @staticmethod
    def extract_and_format_tables(soup):
        if not soup:
            return ""
        
        def get_text_from_element(element):
            """Extract text from any table-related element"""
            return " ".join(element.get_text(separator=' ', strip=True).split())
        
        tables = []
        
        # Find all possible table-related tags
        table_elements = soup.find_all(['table', 'TABLE'])
        
        for table in table_elements:
            table_text = []
            
            # Get all possible table content elements in one go
            content_elements = table.find_all(['td', 'TD', 'th', 'TH', 
                                             'tr', 'TR',
                                             'thead', 'THEAD',
                                             'tbody', 'TBODY',
                                             'tfoot', 'TFOOT',
                                             'ix:nonnumeric', 'ix:nonfraction', 'ix:fraction'])
            
            current_row = []
            
            for element in content_elements:
                tag_name = element.name.lower()
                
                # If it's a row tag, start a new row
                if tag_name in ['tr']:
                    if current_row:
                        table_text.append('\t'.join(filter(None, current_row)))
                    current_row = []
                
                # If it's a cell tag or XBRL tag, add its content
                elif tag_name in ['td', 'th'] or tag_name.startswith('ix:'):
                    text = get_text_from_element(element)
                    if text:
                        current_row.append(text)
            
            # Add the last row if exists
            if current_row:
                table_text.append('\t'.join(filter(None, current_row)))
            
            # Add non-empty tables
            if table_text:
                tables.append('\n'.join(table_text))
        
        return '\n\n'.join(tables)

    def clean_html_content(self, html_content):
        if not html_content:
            self.logger.warning("Empty HTML content provided")
            return "", ""

        try:
            soup = BeautifulSoup(html_content, "html.parser")
            self.logger.info("Successfully parsed HTML")
        except Exception as e:
            self.logger.error(f"HTML parsing failed: {e}")
            return "", ""

        # Extract tables first
        formatted_tables = self.extract_and_format_tables(soup)

        # Remove unwanted elements
        for element in soup(['script', 'style', 'meta', 'link', 'head', 'userStyle']):
            element.decompose()

        # Get text content
        text = soup.get_text(separator=' ')
        text = unicodedata.normalize('NFKD', text)

        # Comprehensive cleaning of metadata tags
        text = re.sub(
            r'(?i)('
            r'</?[a-z][^>]*>|'  
            r'&[a-z0-9#]+;|'    
            r'new\s+normal;|'    
            r'/p\s*p\s*|'       
            r'nbsp;|'           
            r'\s*style="[^"]*"|'  
            r'\s*class="[^"]*"|'  
            r'\s*align="[^"]*"|'  
            r'\s*valign="[^"]*"|'  
            r'\s*width:"[^"]*"|'   
            r'\s*border="[^"]*"|'  
            r'\s*cellspacing="[^"]*"|'  
            r'\s*cellpadding="[^"]*"|' 
            r'[!@#$%^&*()_+={}\[\]:;"\'<>,.?/\\|`~\-]{5,}|'  
            r'^\s*[^a-zA-Z\s]*$|'  
            r'begin [0-9]{3} [^\n]+\n(.*\n)+?end|'  
            r'^[^\w\s]{10,}$|'  
            r'\s+'  
            r')',
            ' ',
            text,
            flags=re.MULTILINE
        )

        # Clean noisy text
        text = self.clean_noisy_text(text)
        
        # Additional cleaning
        text = re.sub(r'/p|/td|/tr|font|/font|/b|', '', text)  
        text = re.sub(r'\b(p|td|tr)\b', '', text)  
        text = re.sub(r'#\d+;', '', text)  
        text = re.sub(r'\s+', ' ', text)  
        text = text.strip()  


        return text, formatted_tables

    def process_html_file(self, input_path, output_dir=None):
        try:
            if not os.path.exists(input_path):
                raise FileNotFoundError(f"Input file not found: {input_path}")

            for encoding in ['utf-8', 'latin-1', 'cp1252']:
                try:
                    with open(input_path, 'r', encoding=encoding) as file:
                        content = file.read()
                        self.logger.info(f"Read file with {encoding} encoding")
                        break
                except UnicodeDecodeError:
                    continue
            else:
                raise UnicodeDecodeError("Failed to read file with any encoding")

            cleaned_text, tables = self.clean_html_content(content)

            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                base_name = os.path.basename(input_path)
                output_path = os.path.join(output_dir, f"{os.path.splitext(base_name)[0]}_cleaned.txt")
            else:
                output_path = f"{os.path.splitext(input_path)[0]}_cleaned.txt"

            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(cleaned_text)
                if tables:
                    file.write("\n\n--- Extracted Tables ---\n\n")
                    file.write(tables)

            self.logger.info(f"Cleaned text saved to: {output_path}")
            return output_path

        except Exception as e:
            self.logger.error(f"Error processing file: {str(e)}")
            return None
