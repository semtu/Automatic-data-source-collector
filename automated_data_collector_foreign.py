# imports
import os
import pandas as pd
import re
import requests
import string
from bs4 import BeautifulSoup
from pathlib import Path

class Error(Exception):
    pass

class crawler:
    """
    This is a class for the pubmed crawler function for articles published in foreign language

    Attributes:
        search (str): You must specify a search parameter
        languages (arr): You must specify an array of language(s)
    """

    def __init__(self, search, languages):
        """
        The constructor for the class.
        Initialize variables to objects that can be inherited later on.
        """
        self.search = search
        self.languages = languages
        self.base_url = "https://pubmed.ncbi.nlm.nih.gov/"
        (
            self.article_url,
            self.article_language,
            self.article_title,
            self.article_abstract,
        ) = (list(), list(), list(), list())
        self.BASE_DIR = Path(__file__).resolve().parent

    def url_params(self):
        """
        This function processes the input parameters needed to customize the url

        Returns: A valid pubmed url
        """
        entry = re.sub(
            "\s+", "+", self.search.strip()
        )  # Replaces whitspace with + sign to make the url valid
        if self.search == "":
            raise Error(f"Search parameter must have a value")
        elif len(self.languages) == 0:
            raise Error(f"Atleast one language must be specified")
        elif isinstance(self.languages, (list, tuple)) is False:
            raise Error(f"Languages parameter must be an array")
        url = f"{self.base_url}?term={entry}"
        for language in self.languages:
            url += f"&filter=lang.{language}"
        url = url + "&page="
        return url

    def remove_punctuation(self, text):
        """
        This function removes punctuations from a string data

        Parameters:
            text:

        Returns: text without punctuation
        """
        return text.translate(str.maketrans("", "", string.punctuation))

    def pubmed_crawler(self, start_page, end_page):
        """
        This function crawls the pubmed website between specified page boundaries and appends data to list objects
        """
        url = self.url_params()
        next_page = url + str(start_page)
        try:
            response = requests.get(str(next_page))  # get request to present page
            soup = BeautifulSoup(response.content, "html.parser")
            main_page = soup.findAll("div", {"class": "search-results"})
            num_of_pages = int(
                "".join(
                    n
                    for n in f"{main_page[0].findAll('label', 'of-total-pages')[0].text}"
                    if n.isdigit()
                )
            )  # Number of pages available
            if start_page > num_of_pages or end_page > num_of_pages:
                raise Error(
                    f"Start Page or End page value cannot be more than the total number of pages {num_of_pages}"
                )
            main_contents = main_page[0].findAll(
                "article", {"class": "full-docsum"}
            )  # Main content section with articles information
            for i in range(0, len(main_contents)):
                # article url
                header = main_contents[i].findAll("a", {"class": "docsum-title"})
                self.article_url.append(
                    self.base_url + header[0]["data-article-id"]
                )  # append url to list object

                # article language
                language = (
                    main_contents[i]
                    .findAll(
                        "span", {"class": "language spaced-citation-item citation-part"}
                    )[0]
                    .text
                )
                self.article_language.append(
                    self.remove_punctuation(language)
                )  # append language to list object

                # article title
                title = " ".join(header[0].text.split())
                self.article_title.append(
                    self.remove_punctuation(title)
                )  # append article title to list object

                # article abstract snippet
                abstract = (
                    main_contents[i]
                    .findAll("div", {"class": "full-view-snippet"})[0]
                    .text
                )
                self.article_abstract.append(
                    " ".join(abstract.split())
                )  # append abstract snippet to list object

            print(f"page {start_page}/{end_page}: done")  # visualize runtime

            if start_page < end_page:
                start_page += 1
                self.pubmed_crawler(
                    start_page, end_page
                )  # recursively iterate through the web pages

        except (IndexError, ValueError):
            print("You have entered an invalid search or language parameter")
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return

    def generate_csv(self, start_page=1, end_page=10):
        """
        This function writes the data to a csv file

        Parameters:
            start_page: start page for the crawler (defaults to 1)
            end_page: end page for the crawler (defaults to 10)

        Returns: ''
        """
        self.pubmed_crawler(start_page, end_page)

        data_dict = {
            "Url": self.article_url,
            "Language": self.article_language,
            "Title": self.article_title,
            "Abstract": self.article_abstract,
        }
        df = pd.DataFrame(data_dict)
        df.to_csv(os.path.join(self.BASE_DIR, "data.csv"), index=None)
        return


if __name__ == "__main__":
    crawler_obj = crawler("arthritis", ["chinese"])
    crawler_obj.generate_csv(1,4) #get results from page 1 to 4

"""
Pubmed already handles translation from foreign languages to English
"""
