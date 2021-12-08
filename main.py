import argparse

from scraper.banktrack_scraper import BankTrackScraper
from scraper.logger import logger
from scraper.web_scraper import WebScraper

parser = argparse.ArgumentParser(description="Scraping banks.")
parser_flags = argparse.ArgumentParser()
parser_flags.add_argument(
    "--filename",
    type=str,
    help="file name for the json save file",
    default="bank_urls.json",
)
parser_flags.add_argument(
    "--debug", action="store_true", help="set logger to debug", default=False
)


group = parser.add_subparsers(title="actions", dest="command")
group.add_parser(
    "banktrack",
    help="scrape banktrack webpage for 60 banks",
    parents=[parser_flags],
    add_help=False,
)
group.add_parser(
    "pdf",
    help="scrape a bunch of pages for links to pdfs",
    parents=[parser_flags],
    add_help=False,
)


def main(args: argparse.Namespace):
    logger.setLevel("DEBUG" if args.debug else "INFO")
    if args.command == "banktrack":
        logger.info("Scraping banktrack webpage for links to banks")
        links = BankTrackScraper.get_all_urls_for_banks()
        BankTrackScraper.save_as_json(links, args.filename)

    if args.command == "pdf":
        logger.info("Scraping webpages for pdfs")
        links = WebScraper.read_from_json(args.filename)
        for bank in links:
            logger.debug(f"Scraping {bank.bank_name}")
            for url in bank.urls:
                pdf_links = WebScraper.get_all_links_to_pdfs_on_page(url)
                bank.pdfs.extend(pdf_links)
            WebScraper.save_as_json(links, args.filename)


if __name__ == "__main__":

    main(parser.parse_args())
