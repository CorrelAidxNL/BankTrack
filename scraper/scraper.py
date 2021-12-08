# - * - Coding: UTF-8 - * -
import json
import re
import ssl
import time
import urllib.request
from typing import Dict, List

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from pydantic import BaseModel

from .logger import logger


class BankLinks(BaseModel):
    bank_name: str
    urls: List[str]
    pdfs: List[str]


class Scraper:
    PDF = ".pdf"
    BASE_URL_PATTERN = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+"
    PAUSE = 1.0

    @classmethod
    def get_html_from_url(cls, url: str) -> BeautifulSoup:
        """Get the html parsed data structure from an url.

        Args:
            url (str): a valid url

        Returns:
            BeautifulSoup: a data structure representing a parsed HTML document.

        """
        logger.debug(f"Scraping {url}")
        time.sleep(cls.PAUSE)  # prevent over requesting
        headers = {"user-agent": "my-app/0.0.1"}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        return soup

    @staticmethod
    def url_is_valid(url: str) -> bool:
        """Check if url is reachable without actually downloading the page or pdf.

        Args:
            url (str): a url to html or pdf

        Returns:
            bool
        """
        logger.debug(f"Validating {url}")
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        try:
            code = urllib.request.urlopen(
                urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}),
                context=ctx,
            ).getcode()
            if code != 200:
                logger.info(f"Url {url} is not valid, code = {code}")
                return False
            return True
        except urllib.error.HTTPError:
            logger.info(f"Url {url} is not valid, HTTPError")
            return False
        except urllib.error.URLError:
            logger.info(f"Url {url} is not valid, URLError")
            return False
        except Exception as e:
            logger.info(f"Url {url} is not valid, unknown exception: {e}")
            return False

    @classmethod
    def url_is_pdf(cls, url: str) -> bool:
        """Check if url links to pdf.

        Args:
            url (str): a url

        Returns:
            bool
        """
        return cls.PDF in url

    @classmethod
    def url_is_not_pdf(cls, url: str) -> bool:
        """Check if url does not link to pdf.

        Args:
            url (str): a url

        Returns:
            bool
        """
        return cls.PDF not in url

    @classmethod
    def save_as_json(cls, links: List[BankLinks], filename: str):
        """Save the links as json.

        Args:
            links (List[BankLinks]): List of banklinks
            filename (str): a json file
        """
        logger.info(f"Saving links to {filename}")
        json_dict = cls.convert_banklinks_to_dict(links)
        with open(filename, "w") as outfile:
            json.dump(json_dict, outfile)

    @staticmethod
    def read_from_json(filename: str):
        """Read links from a json file.

        Args:
            filename (str): a json file

        Returns:
            Dict: A dictionary with links
        """
        logger.info(f"Reading files from {filename}")
        with open(filename, "r") as file:
            links = json.load(file)
        return links

    @classmethod
    def get_base_url(cls, url: str):
        """Get base url from webpage url.

        Args:
            url (str): a url

        Returns:
            [type]: a base url in the form of http(s)://www.[bank].[domain name]
        """
        return re.findall(cls.BASE_URL_PATTERN, url)[0]

    @staticmethod
    def find_all_urls_on_webpage(soup: BeautifulSoup) -> List[Tag]:
        """Find all urls on in a beautifulsoup data structure.

        Args:
            soup (BeautifulSoup): a beautifulsoup data structure from a html webpage

        Returns:
            List[Tag]: a list of beautiful soup tags containing the urls
        """
        return soup.find_all("a", href=True)

    @staticmethod
    def convert_banklinks_to_dict(
        links: List[BankLinks],
    ) -> List[Dict]:
        """Convert the datastructure BankLinks to a dictionary.

        Args:
            links (Dict[str,BankLinks]): a dictionary with
                the bankname and BankLinks datastructure for each bank

        Returns:
            Dict[str,Dict[str,List]]: a nested dictionary
        """
        return [dict(item) for item in links]
