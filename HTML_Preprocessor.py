"""
HTML Preprocessor Module
=========================
A standalone module to fetch, analyze, clean, and restructure HTML before passing to BeautifulSoup.

Author: Custom HTML Preprocessor
Version: 1.0.1 (Fixed)
Dependencies: requests, re, collections

DOCUMENTATION
=============

CLASS: HTMLPreprocessor
-----------------------
Main class for HTML preprocessing operations.

INITIALIZATION:
    HTMLPreprocessor(html_string=None, url=None)
    
    Parameters:
        html_string (str, optional): Raw HTML string
        url (str, optional): URL to fetch HTML from
        
    Note: Provide either html_string OR url (not both)
    
    Examples:
        # From HTML string
        preprocessor = HTMLPreprocessor(html_string="<html>...</html>")
        
        # From URL
        preprocessor = HTMLPreprocessor(url="https://example.com")


METHODS:
--------

1. fetch(url=None, headers=None)
   Fetch HTML from a URL
   
   Parameters:
       url (str, optional): URL to fetch. Uses initialized URL if None.
       headers (dict, optional): Custom HTTP headers
   
   Returns:
       self (for chaining)
   
   Example:
       preprocessor.fetch("https://example.com")
       preprocessor.fetch(url="https://example.com", 
                         headers={'User-Agent': 'CustomBot'})


2. analyze(show_output=True)
   Analyze HTML structure using regex patterns
   
   Parameters:
       show_output (bool): Print analysis results (default: True)
   
   Returns:
       dict: Analysis results with keys:
           - tags: Counter of all HTML tags
           - classes: Counter of CSS classes
           - ids: Counter of element IDs
           - headings: List of (tag, content) tuples
           - paragraphs: List of paragraph contents
           - total_tags: Total tag count
           - unique_tags: Unique tag count
   
   Example:
       analysis = preprocessor.analyze()
       print(analysis['tags'].most_common(5))


3. get_summary()
   Get analysis summary without printing
   
   Returns:
       dict: Same as analyze() but with show_output=False
   
   Example:
       summary = preprocessor.get_summary()


4. remove_scripts_and_styles()
   Remove <script> and <style> tags and their content
   
   Returns:
       self (for chaining)
   
   Example:
       preprocessor.remove_scripts_and_styles()


5. remove_unwanted_tags(tags=None)
   Remove specific tags and their content
   
   Parameters:
       tags (list, optional): Tag names to remove. 
                             Uses config default if None.
                             Default: ['script', 'style', 'nav', 'footer', 
                                      'header', 'noscript', 'svg']
   
   Returns:
       self (for chaining)
   
   Example:
       preprocessor.remove_unwanted_tags(['aside', 'iframe'])


6. remove_inline_styles()
   Remove style attributes from all tags
   
   Returns:
       self (for chaining)
   
   Example:
       preprocessor.remove_inline_styles()


7. remove_comments()
   Remove HTML comments
   
   Returns:
       self (for chaining)
   
   Example:
       preprocessor.remove_comments()


8. remove_by_class(class_names)
   Remove elements containing specific CSS classes
   
   Parameters:
       class_names (list): List of class names to remove
   
   Returns:
       self (for chaining)
   
   Example:
       preprocessor.remove_by_class(['advertisement', 'popup', 'ad'])


9. remove_by_id(id_names)
   Remove elements with specific IDs
   
   Parameters:
       id_names (list): List of ID names to remove
   
   Returns:
       self (for chaining)
   
   Example:
       preprocessor.remove_by_id(['header', 'footer', 'sidebar'])


10. fix_html_entities()
    Decode HTML entities to proper characters
    Examples: &#39; → ', &#x27; → ', &nbsp; → space
    
    Returns:
        self (for chaining)
    
    Example:
        preprocessor.fix_html_entities()


11. clean_whitespace()
    Clean excessive whitespace and formatting
    
    Returns:
        self (for chaining)
    
    Example:
        preprocessor.clean_whitespace()


12. clean(analyze_first=False, interactive=False)
    Main cleaning pipeline - runs all cleaning operations
    
    Parameters:
        analyze_first (bool): Run analysis before cleaning (default: False)
        interactive (bool): Ask user for cleaning preferences (default: False)
    
    Returns:
        str: Cleaned HTML string ready for BeautifulSoup
    
    Example:
        cleaned_html = preprocessor.clean()
        cleaned_html = preprocessor.clean(analyze_first=True)
        cleaned_html = preprocessor.clean(interactive=True)


13. reset()
    Reset to original raw HTML
    
    Returns:
        self (for chaining)
    
    Example:
        preprocessor.reset()


14. get_raw()
    Get original raw HTML
    
    Returns:
        str: Original HTML
    
    Example:
        raw = preprocessor.get_raw()


15. get_cleaned()
    Get current cleaned HTML
    
    Returns:
        str: Current state of HTML
    
    Example:
        cleaned = preprocessor.get_cleaned()


ATTRIBUTES:
-----------
    raw_html (str): Original HTML
    html (str): Current HTML (cleaned or raw)
    url (str): URL if fetched
    analysis (dict): Analysis results
    config (dict): Configuration settings


USAGE EXAMPLES:
===============

Example 1: Basic Usage with URL
--------------------------------
from html_preprocessor import HTMLPreprocessor
from bs4 import BeautifulSoup

# Initialize with URL
preprocessor = HTMLPreprocessor(url="https://example.com")

# Analyze and clean
preprocessor.analyze()
cleaned_html = preprocessor.clean()

# Use with BeautifulSoup
soup = BeautifulSoup(cleaned_html, 'html.parser')


Example 2: From HTML String
----------------------------
import requests
from html_preprocessor import HTMLPreprocessor

response = requests.get("https://example.com")
preprocessor = HTMLPreprocessor(html_string=response.text)
cleaned_html = preprocessor.clean()


Example 3: Custom Pipeline (Chainable)
---------------------------------------
preprocessor = HTMLPreprocessor(url="https://example.com")
cleaned_html = (preprocessor
    .remove_scripts_and_styles()
    .remove_by_class(['ad', 'popup', 'banner'])
    .remove_by_id(['header', 'footer'])
    .fix_html_entities()
    .clean_whitespace()
    .get_cleaned())


Example 4: Interactive Mode
----------------------------
preprocessor = HTMLPreprocessor(url="https://example.com")
cleaned_html = preprocessor.clean(analyze_first=True, interactive=True)


Example 5: Multiple URLs
-------------------------
urls = ["https://site1.com", "https://site2.com"]
for url in urls:
    preprocessor = HTMLPreprocessor(url=url)
    cleaned = preprocessor.clean()
    # Process with BeautifulSoup...


Example 6: Save Cleaned HTML
-----------------------------
preprocessor = HTMLPreprocessor(url="https://example.com")
cleaned_html = preprocessor.clean()

with open('cleaned.html', 'w', encoding='utf-8') as f:
    f.write(cleaned_html)
"""

import requests
import re
from collections import Counter


class HTMLPreprocessor:
    """Analyze and clean HTML using only regex - prepares HTML for BeautifulSoup"""
    
    def __init__(self, html_string=None, url=None):
        """
        Initialize HTMLPreprocessor with either HTML string or URL
        
        Args:
            html_string (str, optional): Raw HTML string
            url (str, optional): URL to fetch HTML from
        
        Raises:
            ValueError: If neither html_string nor url is provided
        """
        if html_string is None and url is None:
            raise ValueError("Must provide either html_string or url")
        
        if html_string and url:
            raise ValueError("Provide only one: html_string OR url")
        
        # Validate html_string is not empty
        if html_string is not None and not html_string.strip():
            raise ValueError("html_string cannot be empty")
        
        self.url = url
        self.raw_html = html_string
        self.html = html_string
        self.analysis = {}
        
        # Configuration
        self.config = {
            'remove_tags': ['script', 'style', 'nav', 'footer', 'header', 'noscript', 'svg'],
            'remove_inline_styles': True,
            'remove_comments': True,
            'clean_whitespace': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # If URL provided, fetch immediately
        if url:
            self.fetch(url)
    
    # ========================================
    # UTILITY METHODS
    # ========================================
    
    def _ensure_html(self):
        """Ensure self.html is not None before operations"""
        if self.html is None:
            raise ValueError("No HTML content available. Use fetch() or provide html_string.")
    
    def _strip_tags(self, text):
        """Remove HTML tags from text"""
        return re.sub(r'<[^>]+>', '', text).strip()
    
    # ========================================
    # FETCHING METHOD
    # ========================================
    
    def fetch(self, url=None, headers=None):
        """
        Fetch HTML from URL
        
        Args:
            url (str, optional): URL to fetch. Uses self.url if None.
            headers (dict, optional): Custom HTTP headers
        
        Returns:
            self: For method chaining
        
        Raises:
            requests.RequestException: If fetch fails
        """
        fetch_url = url or self.url
        if not fetch_url:
            raise ValueError("No URL provided")
        
        self.url = fetch_url
        
        # Default headers
        if headers is None:
            headers = {'User-Agent': self.config['user_agent']}
        
        print(f"🌐 Fetching: {fetch_url}")
        
        try:
            response = requests.get(fetch_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Check if response is actually HTML
            content_type = response.headers.get('content-type', '')
            if 'text/html' not in content_type and 'application/xhtml' not in content_type:
                print(f"⚠️  Warning: Content-Type is '{content_type}', not HTML")
            
            self.raw_html = response.text
            self.html = response.text
            
            if not self.html.strip():
                raise ValueError("Fetched content is empty")
            
            print(f"✅ Fetched {len(self.raw_html):,} characters")
            
        except requests.Timeout:
            print(f"❌ Timeout: Server took too long to respond")
            raise
        except requests.ConnectionError:
            print(f"❌ Connection Error: Could not reach server")
            raise
        except requests.HTTPError as e:
            print(f"❌ HTTP Error {e.response.status_code}: {e}")
            raise
        except requests.RequestException as e:
            print(f"❌ Error fetching URL: {e}")
            raise
        
        return self
    
    # ========================================
    # ANALYSIS METHODS
    # ========================================
    
    def analyze(self, show_output=True):
        """
        Analyze HTML structure using regex patterns
        
        Args:
            show_output (bool): Print analysis results (default: True)
            
        Returns:
            dict: Analysis results containing tags, classes, ids, headings, paragraphs
        """
        self._ensure_html()
        
        if show_output:
            print("\n" + "="*60)
            print("ANALYZING HTML STRUCTURE")
            print("="*60)
            if self.url:
                print(f"URL: {self.url}")
        
        # 1. Find all opening tags
        tag_pattern = r'<(\w+)(?:\s+[^>]*)?>'
        all_tags = re.findall(tag_pattern, self.html, re.IGNORECASE)
        tag_counts = Counter(all_tags)
        
        if show_output:
            print(f"\n📊 Total tags: {len(all_tags)}")
            print(f"📊 Unique tag types: {len(tag_counts)}")
            print("\n🏷️  Most common tags:")
            for tag, count in tag_counts.most_common(10):
                print(f"   <{tag}>: {count}")
        
        # 2. Find all classes
        class_pattern = r'class=["\']([^"\']+)["\']'
        all_classes = re.findall(class_pattern, self.html, re.IGNORECASE)
        individual_classes = []
        for cls in all_classes:
            individual_classes.extend(cls.split())
        class_counts = Counter(individual_classes)
        
        if show_output:
            print(f"\n🎨 Total class attributes: {len(all_classes)}")
            print(f"🎨 Unique classes: {len(class_counts)}")
            if class_counts:
                print("🎨 Top 10 classes:", ', '.join([c for c, _ in class_counts.most_common(10)]))
        
        # 3. Find all IDs
        id_pattern = r'id=["\']([^"\']+)["\']'
        all_ids = re.findall(id_pattern, self.html, re.IGNORECASE)
        id_counts = Counter(all_ids)
        
        if show_output:
            print(f"\n🆔 Total IDs: {len(all_ids)}")
            if all_ids:
                print(f"🆔 IDs: {', '.join(list(id_counts.keys())[:10])}")
        
        # 4. Find headings
        heading_pattern = r'<(h[1-6])[^>]*>(.*?)</\1>'
        headings = re.findall(heading_pattern, self.html, re.IGNORECASE | re.DOTALL)
        
        if show_output:
            print(f"\n📰 Headings found: {len(headings)}")
            for tag, content in headings[:5]:
                clean = self._strip_tags(content)[:60]
                print(f"   <{tag}>: {clean}...")
        
        # 5. Find paragraphs
        p_pattern = r'<p[^>]*>(.*?)</p>'
        paragraphs = re.findall(p_pattern, self.html, re.IGNORECASE | re.DOTALL)
        
        if show_output:
            print(f"\n📄 Paragraphs: {len(paragraphs)}")
        
        # Store analysis
        self.analysis = {
            'tags': tag_counts,
            'classes': class_counts,
            'ids': id_counts,
            'headings': headings,
            'paragraphs': paragraphs,
            'total_tags': len(all_tags),
            'unique_tags': len(tag_counts)
        }
        
        return self.analysis
    
    def get_summary(self):
        """
        Get analysis summary without printing
        
        Returns:
            dict: Analysis results
        """
        if not self.analysis:
            self.analyze(show_output=False)
        return self.analysis
    
    # ========================================
    # CLEANING METHODS
    # ========================================
    
    def remove_scripts_and_styles(self):
        """
        Remove <script> and <style> tags and their content
        
        Returns:
            self: For method chaining
        """
        self._ensure_html()
        self.html = re.sub(r'<script[^>]*>.*?</script>', '', self.html, flags=re.DOTALL | re.IGNORECASE)
        self.html = re.sub(r'<style[^>]*>.*?</style>', '', self.html, flags=re.DOTALL | re.IGNORECASE)
        return self
    
    def remove_unwanted_tags(self, tags=None):
        """
        Remove specific tags and their content
        
        Args:
            tags (list, optional): List of tag names to remove. Uses config default if None.
        
        Returns:
            self: For method chaining
        """
        self._ensure_html()
        tags = tags or self.config['remove_tags']
        for tag in tags:
            pattern = f'<{tag}[^>]*>.*?</{tag}>'
            self.html = re.sub(pattern, '', self.html, flags=re.DOTALL | re.IGNORECASE)
        return self
    
    def remove_inline_styles(self):
        """
        Remove style attributes from tags
        
        Returns:
            self: For method chaining
        """
        self._ensure_html()
        self.html = re.sub(r'\s+style=["\'][^"\']*["\']', '', self.html, flags=re.IGNORECASE)
        return self
    
    def remove_comments(self):
        """
        Remove HTML comments
        
        Returns:
            self: For method chaining
        """
        self._ensure_html()
        self.html = re.sub(r'<!--.*?-->', '', self.html, flags=re.DOTALL)
        return self
    
    def remove_by_class(self, class_names):
        """
        Remove elements containing specific class names
        
        Args:
            class_names (list): List of class names to remove
        
        Returns:
            self: For method chaining
        """
        self._ensure_html()
        for cls in class_names:
            # Use word boundaries to avoid partial matches
            escaped_cls = re.escape(cls)
            
            # Pattern for elements with closing tags (capture tag name for matching close)
            pattern1 = rf'<(\w+)[^>]*\bclass=["\'][^"\']*\b{escaped_cls}\b[^"\']*["\'][^>]*>.*?</\1>'
            self.html = re.sub(pattern1, '', self.html, flags=re.DOTALL | re.IGNORECASE)
            
            # Pattern for self-closing tags
            pattern2 = rf'<\w+[^>]*\bclass=["\'][^"\']*\b{escaped_cls}\b[^"\']*["\'][^>]*/>'
            self.html = re.sub(pattern2, '', self.html, flags=re.IGNORECASE)
        
        return self
    
    def remove_by_id(self, id_names):
        """
        Remove elements with specific IDs
        
        Args:
            id_names (list): List of ID names to remove
        
        Returns:
            self: For method chaining
        """
        self._ensure_html()
        for id_name in id_names:
            escaped_id = re.escape(id_name)
            
            # Pattern for elements with closing tags (capture tag name for matching close)
            pattern1 = rf'<(\w+)[^>]*\bid=["\']({escaped_id})["\'][^>]*>.*?</\1>'
            self.html = re.sub(pattern1, '', self.html, flags=re.DOTALL | re.IGNORECASE)
            
            # Pattern for self-closing tags
            pattern2 = rf'<\w+[^>]*\bid=["\']({escaped_id})["\'][^>]*/>'
            self.html = re.sub(pattern2, '', self.html, flags=re.IGNORECASE)
        
        return self
    
    def fix_html_entities(self):
        """
        Decode HTML entities to proper characters
        Examples: &#39; → ', &#x27; → ', &nbsp; → space
        
        Returns:
            self: For method chaining
        """
        self._ensure_html()
        
        # Numeric entities (&#39;)
        def decode_numeric(match):
            return chr(int(match.group(1)))
        self.html = re.sub(r'&#(\d+);', decode_numeric, self.html)
        
        # Hex entities (&#x27;)
        def decode_hex(match):
            return chr(int(match.group(1), 16))
        self.html = re.sub(r'&#x([0-9a-fA-F]+);', decode_hex, self.html)
        
        # Named entities
        entities = {
            '&nbsp;': ' ', '&amp;': '&', '&lt;': '<', '&gt;': '>',
            '&quot;': '"', '&apos;': "'", '&mdash;': '—', '&ndash;': '–',
            '&rsquo;': ''', '&lsquo;': ''', '&rdquo;': '"', '&ldquo;': '"',
            '&hellip;': '...', '&copy;': '©', '&reg;': '®'
        }
        for entity, char in entities.items():
            self.html = self.html.replace(entity, char)
        
        return self
    
    def clean_whitespace(self):
        """
        Clean excessive whitespace while preserving inline spacing
        
        Returns:
            self: For method chaining
        """
        self._ensure_html()
        
        # Collapse multiple spaces/tabs/newlines into single space
        self.html = re.sub(r'[ \t]+', ' ', self.html)
        self.html = re.sub(r'\n\s*\n', '\n', self.html)
        
        # Only remove whitespace between block-level elements
        block_elements = r'(div|p|h[1-6]|section|article|header|footer|nav|ul|ol|li|table|tr|td|th)'
        self.html = re.sub(rf'</{block_elements}>\s+<', r'</\1><', self.html, flags=re.IGNORECASE)
        self.html = re.sub(rf'<{block_elements}[^>]*>\s+', r'<\1>', self.html, flags=re.IGNORECASE)
        
        return self
    
    # ========================================
    # MAIN CLEANING PIPELINE
    # ========================================
    
    def clean(self, analyze_first=False, interactive=False):
        """
        Main cleaning pipeline - returns cleaned HTML ready for BeautifulSoup
        
        Args:
            analyze_first (bool): Run analysis before cleaning (default: False)
            interactive (bool): Ask user for cleaning preferences (default: False)
            
        Returns:
            str: Cleaned HTML string
        """ 
        self._ensure_html()
        
        if analyze_first:
            self.analyze(show_output=True)
        
        if interactive:
            self._interactive_cleaning()
        else:
            # Default cleaning pipeline
            print("\n🧹 Cleaning HTML...")
            self.remove_scripts_and_styles()
            self.remove_unwanted_tags()
            self.remove_inline_styles()
            self.remove_comments()
            self.fix_html_entities()
            self.clean_whitespace()
            print(f"✅ Cleaned: {len(self.raw_html):,} → {len(self.html):,} characters")
        
        return self.html
    
    def _interactive_cleaning(self):
        """Interactive mode - ask user what to clean"""
        print("\n" + "="*60)
        print("INTERACTIVE CLEANING MODE")
        print("="*60)
        
        if input("\nRemove <script> and <style> tags? (y/n, default: y): ").strip().lower() != 'n':
            self.remove_scripts_and_styles()
        
        if input("Remove <nav>, <footer>, <header>? (y/n, default: y): ").strip().lower() != 'n':
            self.remove_unwanted_tags()
        
        if input("Remove inline style attributes? (y/n, default: y): ").strip().lower() != 'n':
            self.remove_inline_styles()
        
        if input("Remove HTML comments? (y/n, default: y): ").strip().lower() != 'n':
            self.remove_comments()
        
        # Ask about specific classes
        if self.analysis and self.analysis['classes']:
            print(f"\nAvailable classes: {', '.join(list(self.analysis['classes'].keys())[:10])}")
            remove_classes = input("Remove elements by class? (comma-separated, or Enter to skip): ").strip()
            if remove_classes:
                self.remove_by_class([c.strip() for c in remove_classes.split(',')])
        
        if input("Fix HTML entities (&#x27; → ')? (y/n, default: y): ").strip().lower() != 'n':
            self.fix_html_entities()
        
        if input("Clean excessive whitespace? (y/n, default: y): ").strip().lower() != 'n':
            self.clean_whitespace()
        
        print(f"\n✅ Cleaned: {len(self.raw_html):,} → {len(self.html):,} characters")
    
    # ========================================
    # STATE MANAGEMENT METHODS
    # ========================================
    
    def reset(self):
        """
        Reset to original raw HTML
        
        Returns:
            self: For method chaining
        """
        self.html = self.raw_html
        return self
    
    def get_raw(self):
        """
        Get original raw HTML
        
        Returns:
            str: Original HTML
        """
        return self.raw_html
    
    def get_cleaned(self):
        """
        Get current cleaned HTML
        
        Returns:
            str: Current state of HTML
        """
        return self.html


# ============================================
# QUICK REFERENCE
# ============================================
def print_documentation():
    """Print quick reference guide"""
    doc = """
    ╔════════════════════════════════════════════════════════════╗
    ║           HTML PREPROCESSOR - QUICK REFERENCE              ║
    ╚════════════════════════════════════════════════════════════╝
    
    INITIALIZATION:
        HTMLPreprocessor(html_string="<html>...")
        HTMLPreprocessor(url="https://example.com")
    
    MAIN METHODS:
        .fetch(url)              - Fetch HTML from URL
        .analyze()               - Analyze HTML structure
        .clean()                 - Clean HTML (default pipeline)
        .get_cleaned()           - Get cleaned HTML
        .get_raw()               - Get original HTML
        .reset()                 - Reset to raw HTML
    
    CLEANING METHODS (Chainable):
        .remove_scripts_and_styles()
        .remove_unwanted_tags(['aside', 'iframe'])
        .remove_inline_styles()
        .remove_comments()
        .remove_by_class(['ad', 'popup'])
        .remove_by_id(['header', 'footer'])
        .fix_html_entities()
        .clean_whitespace()
    
    USAGE:
        from html_preprocessor import HTMLPreprocessor
        from bs4 import BeautifulSoup
        
        # From URL
        pp = HTMLPreprocessor(url="https://example.com")
        cleaned = pp.clean()
        soup = BeautifulSoup(cleaned, 'html.parser')
        
        # Custom pipeline
        cleaned = (pp
            .remove_scripts_and_styles()
            .remove_by_class(['ad'])
            .fix_html_entities()
            .get_cleaned())
    """
    print(doc)


# ============================================
# EXAMPLE USAGE
# ============================================

if __name__ == "__main__":
    from bs4 import BeautifulSoup
    
    # Print documentation
    print_documentation()
    
    print("\n\n" + "="*60)
    print("RUNNING EXAMPLES")
    print("="*60)
    
    # Example 1: Basic usage with URL
    print("\n Example 1: Basic Usage")
    print("-" * 60)
    
    url = "https://www.anthropic.com/research/building-ai-cyber-defenders"
    preprocessor = HTMLPreprocessor(url=url)
    preprocessor.analyze()
    cleaned_html = preprocessor.clean()
    
    # Use with BeautifulSoup
    soup = BeautifulSoup(cleaned_html, 'html.parser')
    print(f"\n BeautifulSoup: Found {len(soup.find_all('p'))} paragraphs")
    
    # Example 2: Custom pipeline
    print("\n\n Example 2: Custom Pipeline")
    print("-" * 60)
    
    preprocessor.reset()
    cleaned = (preprocessor
        .remove_scripts_and_styles()
        .remove_by_class(['advertisement'])
        .fix_html_entities()
        .clean_whitespace()
        .get_cleaned())
    
    print(f" Custom pipeline: {len(cleaned):,} characters")
    
    # Example 3: Save cleaned HTML
    print("\n\n Example 3: Save Cleaned HTML")
    print("-" * 60)
    
    choice = input("Save cleaned HTML? (y/n): ").strip().lower()
    if choice == 'y':
        filename = input("Filename (default: cleaned.html): ").strip() or "cleaned.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(cleaned_html)
        print(f" Saved to {filename}")
