import json
from typing import Dict, List

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

BANKS = (
    "https://www.banktrack.org/article/new_report_world_s_60_largest_banks_have_poured"
    "_3_8_trillion_into_fossil_fuels_since_paris_agreement_climate_groups_sound_alarm"
    "_as_financing_for_fossil_fuel_expansion_continues_to_rise"
)
BANKTRACK = "https://www.banktrack.org"


def get_html_from_url(url: str) -> BeautifulSoup:
    """Get the html parsed data structure from an url.

    Args:
        url (str): a valid url

    Returns:
        BeautifulSoup: a data structure representing a parsed HTML document.

    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def get_outside_banktrack_urls(soup: Tag) -> List[str]:
    """Get all urls that link to outside banktrack.

    Args:
        soup (Tag): A data structure that represtents a HTML tag from a parsed HTML
        document.

    Returns:
        List[str]: a list of urls.

    """
    url_list = []
    for link in soup.find_all("a", href=True):
        if BANKTRACK not in link.get("href"):
            url_list.append(link.get("href"))
    return url_list


def get_urls_for_bank(url: Tag) -> Dict[str, List[str]]:
    """Get all urls for the bank on the policy tab on banktrack.

    Args:
        url (Tag): A HTML tag that contains a url (href)

    Returns:
        Dict[str, List[str]]: A dictionary with the bank name as key and a list
        of urls for that bank as value.

    """
    soup = get_html_from_url(url.get("href"))
    bank_name = soup.find("span", id="maintitle").text
    policy_files = soup.find("div", class_="policyfiles")
    url_list = get_outside_banktrack_urls(policy_files)
    return {bank_name: url_list}


def get_all_urls_for_banks() -> Dict[str, List[str]]:
    """Get all the outside urls for the 60 banks on banktrack.

    Returns:
        Dict[str, List[str]]: A dictionary containing all the banks as key and a
        list of urls (outside of banktrack) as value.

    """
    urls = {}
    soup = get_html_from_url(BANKS)
    banks = soup.find("div", class_="rowed banks downlist image-left")
    for bank_link in banks.find_all("a", href=True):
        urls.update(get_urls_for_bank(bank_link))
    return urls


if __name__ == "__main__":
    with open("bank_urls.json", "w") as outfile:
        json.dump(get_all_urls_for_banks(), outfile)
