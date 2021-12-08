import re
import urllib.parse
from typing import List

from scraper.scraper import Scraper

from .logger import logger


class WebScraper(Scraper):
    @classmethod
    def get_all_links_to_pdfs_on_page(cls, url: str) -> List[str]:
        """Get all links to pdfs on a webpage.

        Args:
            url (str): a valid url

        Returns:
            List[str]: a list of urls to pdfs
        """
        logger.debug(f"Scraping {url} for links to pdfs")
        soup = cls.get_html_from_url(url)
        url_list = []
        for link in cls.find_all_urls_on_webpage(soup):
            if cls.PDF in link.get("href"):
                pdf_url = cls.parse_pdf_url(link.get("href"), url)
                if cls.url_is_valid(pdf_url):
                    url_list.append(pdf_url)
        return list(set(url_list))

    @classmethod
    def parse_pdf_url(cls, url: str, start_url: str) -> str:
        """Parse the partial pdf url and return a complete url to a pdf.

        Args:
            url (str): partial or full url to a pdf
            base_url (str): base url of the webpage

        Returns:
            str: a valid url to a pdf
        """
        base_url = cls.get_base_url(start_url)
        logger.debug(f"found url {url}, base-url:{base_url}")
        if re.match(cls.BASE_URL_PATTERN, url):
            pdf_url = url
        elif re.match("^/-/", url):
            pdf_url = base_url + url
        elif re.match("^./", url):
            pdf_url = start_url.rsplit("/", 1)[0] + url.lstrip(".")
        elif re.match("^../", url):
            pdf_url = start_url.rsplit("/", 2)[0] + url.lstrip(".")
        else:
            pdf_url = base_url + url
        pdf_url = pdf_url.partition(cls.PDF)[0] + cls.PDF
        if not pdf_url.isascii() or " " in pdf_url:
            pdf_url = urllib.parse.quote(pdf_url, safe=":/")
        logger.debug(pdf_url)
        return pdf_url
