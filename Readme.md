# HTML Preprocessor - Complete Understanding Guide

## What Does This Script Do?

This script **cleans messy HTML** before you parse it with BeautifulSoup. Think of it as a "pre-wash" for dirty HTML that removes ads, scripts, styling, and other junk.

---

## 🔑 Core Concept

```
Raw HTML (messy) → HTMLPreprocessor → Clean HTML → BeautifulSoup → Data
```

**Why?** Web pages have tons of noise: ads, JavaScript, CSS, navigation menus. This script strips all that away so BeautifulSoup can focus on the actual content.

---

## 📝 Basic Usage Pattern

### **Pattern 1: From URL (Most Common)**
```python
from html_preprocessor import HTMLPreprocessor
from bs4 import BeautifulSoup

# Step 1: Create preprocessor with URL
pp = HTMLPreprocessor(url="https://example.com")

# Step 2: Clean the HTML
cleaned = pp.clean()

# Step 3: Parse with BeautifulSoup
soup = BeautifulSoup(cleaned, 'html.parser')

# Step 4: Extract what you need
titles = soup.find_all('h1')
```

### **Pattern 2: From HTML String**
```python
import requests

# Get HTML yourself
response = requests.get("https://example.com")
html_string = response.text

# Pass it to preprocessor
pp = HTMLPreprocessor(html_string=html_string)
cleaned = pp.clean()
```

---

## 🛠️ What Gets Cleaned?

When you call `.clean()`, it automatically:

1. **Removes `<script>` tags** - All JavaScript code
2. **Removes `<style>` tags** - All CSS styling  
3. **Removes navigation** - `<nav>`, `<header>`, `<footer>` elements
4. **Removes inline styles** - `style="color: red"` attributes
5. **Removes HTML comments** - `<!-- comment -->`
6. **Fixes entities** - Converts `&#39;` to `'`, `&nbsp;` to space
7. **Cleans whitespace** - Removes extra spaces/newlines

---

## Custom Cleaning (Advanced)

You can chain methods to customize what gets removed:

```python
pp = HTMLPreprocessor(url="https://news-site.com")

cleaned = (pp
    .remove_scripts_and_styles()           # Remove JS/CSS
    .remove_by_class(['ad', 'popup'])      # Remove ads
    .remove_by_id(['sidebar', 'footer'])   # Remove specific sections
    .fix_html_entities()                   # Fix &#39; → '
    .clean_whitespace()                    # Clean spaces
    .get_cleaned())                        # Get result
```

**The magic:** Each method returns `self`, so you can chain them!

---

## Analyzing Before Cleaning

Want to see what's in the HTML first?

```python
pp = HTMLPreprocessor(url="https://example.com")

# Analyze structure
analysis = pp.analyze()

# See what you found
print(analysis['total_tags'])      # Total number of tags
print(analysis['tags'])            # Counter of tag types
print(analysis['classes'])         # All CSS classes found
print(analysis['headings'])        # All h1, h2, etc.
```

**Output example:**
```
Total tags: 1,234
Unique tag types: 45

  Most common tags:
   <div>: 456
   <span>: 234
   <p>: 123
```

---

##  Real-World Examples

### **Example 1: Scraping News Article**
```python
# Goal: Get article text without ads/navigation
pp = HTMLPreprocessor(url="https://news-site.com/article")
cleaned = pp.clean()
soup = BeautifulSoup(cleaned, 'html.parser')

# Now soup only has article content
article_text = soup.get_text()
```

### **Example 2: Remove Specific Ads**
```python
pp = HTMLPreprocessor(url="https://blog.com")

# First, analyze to see what classes exist
pp.analyze()  # Shows: "advertisement", "sidebar-ad", "popup"

# Then remove those specific classes
cleaned = (pp
    .remove_by_class(['advertisement', 'sidebar-ad', 'popup'])
    .get_cleaned())
```

### **Example 3: Interactive Mode**
```python
# Let the script ask you what to remove
pp = HTMLPreprocessor(url="https://example.com")
cleaned = pp.clean(analyze_first=True, interactive=True)

# It will prompt:
# "Remove <script> and <style> tags? (y/n)"
# "Remove <nav>, <footer>, <header>? (y/n)"
# etc.
```

---

##  Method Chaining Explained

**Without chaining:**
```python
pp = HTMLPreprocessor(url="https://example.com")
pp.remove_scripts_and_styles()
pp.remove_comments()
pp.fix_html_entities()
cleaned = pp.get_cleaned()
```

**With chaining (cleaner):**
```python
pp = HTMLPreprocessor(url="https://example.com")
cleaned = (pp
    .remove_scripts_and_styles()
    .remove_comments()
    .fix_html_entities()
    .get_cleaned())
```

Both do the same thing! Chaining just looks nicer.

---

##  Common Mistakes

###  **Mistake 1: Not providing HTML or URL**
```python
pp = HTMLPreprocessor()  # ERROR: Must provide html_string or url
```

###  **Mistake 2: Providing both**
```python
pp = HTMLPreprocessor(
    html_string="<html>...",
    url="https://example.com"  # ERROR: Choose ONE
)
```

###  **Mistake 3: Forgetting to clean**
```python
pp = HTMLPreprocessor(url="https://example.com")
soup = BeautifulSoup(pp.html, 'html.parser')  # Still has junk!

# Should be:
cleaned = pp.clean()
soup = BeautifulSoup(cleaned, 'html.parser')
```

---

##  When to Use Each Method

| Method | When to Use |
|--------|-------------|
| `.clean()` | Default - removes most junk |
| `.remove_by_class(['ad'])` | You know specific class names to remove |
| `.remove_by_id(['header'])` | You know specific IDs to remove |
| `.analyze()` | You want to explore what's in the HTML first |
| `.reset()` | You cleaned too much, start over |

---

##  Pro Tips

1. **Start with `.analyze()`** to see what's in the HTML
2. **Use `.clean()` first** - it handles 90% of cases
3. **Chain methods** for custom cleaning
4. **Save cleaned HTML** if you'll reuse it:
   ```python
   with open('cleaned.html', 'w') as f:
       f.write(pp.get_cleaned())
   ```

---

##  Quick Reference Card

```python
# INITIALIZATION
pp = HTMLPreprocessor(url="https://example.com")
pp = HTMLPreprocessor(html_string="<html>...")

# ANALYSIS
pp.analyze()           # Print analysis
summary = pp.get_summary()  # Get without printing

# CLEANING (all chainable)
pp.clean()                              # Default clean
pp.remove_scripts_and_styles()          # Remove JS/CSS
pp.remove_unwanted_tags(['aside'])      # Remove specific tags
pp.remove_by_class(['ad', 'popup'])     # Remove by class
pp.remove_by_id(['header'])             # Remove by ID
pp.remove_inline_styles()               # Remove style=""
pp.remove_comments()                    # Remove <!-- -->
pp.fix_html_entities()                  # Fix &#39; etc
pp.clean_whitespace()                   # Clean spaces

# RETRIEVAL
cleaned = pp.get_cleaned()  # Get cleaned HTML
raw = pp.get_raw()          # Get original HTML
pp.reset()                  # Reset to original
```

---

##  Complete Working Example

```python
from html_preprocessor import HTMLPreprocessor
from bs4 import BeautifulSoup

# Scrape article from news site
pp = HTMLPreprocessor(url="https://example-news.com/article")

# Analyze first (optional)
pp.analyze()

# Clean with custom rules
cleaned = (pp
    .remove_scripts_and_styles()
    .remove_by_class(['ad', 'sidebar', 'comments'])
    .remove_by_id(['header', 'footer', 'navigation'])
    .fix_html_entities()
    .clean_whitespace()
    .get_cleaned())

# Parse with BeautifulSoup
soup = BeautifulSoup(cleaned, 'html.parser')

# Extract article
title = soup.find('h1').text
paragraphs = [p.text for p in soup.find_all('p')]

print(f"Title: {title}")
print(f"Paragraphs: {len(paragraphs)}")
```

---

##  The Bottom Line

**Think of it this way:**
- **Raw HTML** = Dirty laundry (full of stains, tags, lint)
- **HTMLPreprocessor** = Washing machine (removes the dirt)
- **Clean HTML** = Fresh laundry (ready to wear)
- **BeautifulSoup** = Folding the laundry (organizing it nicely)

You use the preprocessor to **clean** before BeautifulSoup **organizes**!
