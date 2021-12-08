from typing import List

from bs4.element import Tag

from scraper.scraper import BankLinks, Scraper

from .logger import logger


class BankTrackScraper(Scraper):

    START_URL = (
        "https://www.banktrack.org/article/new_report_world_s_60_largest_banks_have"
        "_poured_3_8_trillion_into_fossil_fuels_since_paris_agreement_climate_groups"
        "_sound_alarm_as_financing_for_fossil_fuel_expansion_continues_to_rise"
    )
    SKIP_URL = "https://www.banktrack.org"

    @classmethod
    def get_outside_banktrack_urls(cls, soup: Tag) -> List[str]:
        """Get all urls that link to outside banktrack.

        Args:
            soup (Tag): A data structure that represtents a HTML tag from a parsed HTML
            document.

        Returns:
            List[str]: a list of urls.

        """
        logger.debug(f"Filtering links that do not link to {cls.SKIP_URL}")
        url_list = []
        for link in cls.find_all_urls_on_webpage(soup):
            if cls.SKIP_URL not in link.get("href"):
                url_list.append(link.get("href"))
        return url_list

    @classmethod
    def get_urls_for_bank(cls, link: Tag) -> BankLinks:
        """Get all urls for the bank on the policy tab on banktrack.

        Args:
            link (Tag): A HTML tag that contains a url (href)

        Returns:
            Dict[str, List[str]]: A dictionary with the bank name as key and a list
            of urls for that bank as value.

        """
        soup = cls.get_html_from_url(link.get("href"))
        bank_name = soup.find("span", id="maintitle").text
        logger.debug(f"Looking for links to {bank_name}")
        policy_files = soup.find("div", class_="policyfiles")
        url_list = cls.get_outside_banktrack_urls(policy_files)
        url_list = list(filter(cls.url_is_valid, url_list))
        return BankLinks(
            bank_name=bank_name,
            pdfs=list(filter(cls.url_is_pdf, url_list)),
            urls=list(filter(cls.url_is_not_pdf, url_list)),
        )

    @classmethod
    def get_all_urls_for_banks(cls) -> List[BankLinks]:
        """Get all the outside urls for the 60 banks on banktrack.

        Returns:
            Dict[str, List[str]]: A dictionary containing all the banks as key and a
            list of urls (outside of banktrack) as value.

        """
        logger.debug(f"Scraping {cls.START_URL} for list of banks")
        urls = []
        soup = cls.get_html_from_url(cls.START_URL)
        banks = soup.find("div", class_="rowed banks downlist image-left")
        for bank_link in cls.find_all_urls_on_webpage(banks):
            urls.append(cls.get_urls_for_bank(bank_link))
        return urls
