# Automatic data source collector (foreign articles)

This code is a Python script that allows the user to crawl and extract article information from the Pubmed website, and save it to a CSV file. The script is designed to crawl for articles published in foreign languages, specified by the user. The script uses BeautifulSoup for web scraping, and Pandas for writing data to a CSV file.

Installation
The script has been developed and tested in Python 3.9, and requires the following packages to be installed:

pandas
beautifulsoup4
These can be installed via pip by running the following command:

```
pip install pandas beautifulsoup4
```

Usage
1. Import the crawler class from the pubmed_crawler module:
  ```
  from pubmed_crawler import crawler
  ```
2. Initialize the crawler object with the following parameters:
search (str): The search parameter for Pubmed articles. This is a required parameter.
languages (List[str]): A list of foreign languages for articles to be extracted. This is a required parameter.
  ```
  crawler_obj = crawler(search='arthritis', languages=['german', 'french', 'spanish'])
  ```
3. Call the generate_csv method of the crawler object to crawl the Pubmed website and write the extracted article information to a CSV file. The generate_csv method has the following parameters:
start_page (int): The starting page number for crawling. Default is 1.
end_page (int): The ending page number for crawling. Default is 10.
  ```
  crawler_obj.generate_csv(start_page=1, end_page=5)
  ```
  
The output CSV file will be written to the same directory as the pubmed_crawler.py file, with the name data.csv. The output file will contain the following columns:
Url: The URL of the article on Pubmed.
Language: The language of the article.
Title: The title of the article.
Abstract: A short abstract of the article.

## Future improvement
When scraping for very large data, it is best to make request calls asynchronously. This can be done easily in Python using the grequest module

## Discussion
Pubmed website already handles translations inhouse. For websites not automatically translated to English, the Google translation Api cn easily be set up
