# Automatic data source collector (foreign articles)

A web crawler for Pubmed:
-take a disease name as input
-find articles on the disease name in a foreign language (preferably from Pubmed) 
-translate their title and body paragraphs to English.

To run:
- Install dependencies
- Run from terminal using the command
```
pip install requirements.txt
python3 remove.py
python3 restore.py
```

## Future improvement
When scraping for very large data, it is best to make request calls asynchronously. This can be done easily in Python using the grequest module

## Discussion
Pubmed website already handles translations inhouse. For websites not automatically translated to English, the Google translation Api cn easily be set up
