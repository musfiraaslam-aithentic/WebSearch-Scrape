# WebSearch & Scrape 

A pipeline that: 
(1) Searches the web for a given manufacturer and model.
(2) Fetches the HTML from the top results.
(3) Uses an LLM to validate and extract the correct product details with clear provenance.


```
websearchandscrape/
  README.md 

  search/  
    __init__.py 
    google_search.py 

  scraping/  # Musfira
    __init__.py
    fetch_html.py 

  llm/  
    __init__.py
    validate_product.py  

  storage/ 
    db.py
    schema.sql
```
