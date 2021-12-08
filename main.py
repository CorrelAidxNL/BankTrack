import argparse

from scraper.banktrack_scraper import BankTrackScraper
from scraper.logger import logger

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


def main(args: argparse.Namespace):
    logger.setLevel("DEBUG" if args.debug else "INFO")
    if args.command == "banktrack":
        logger.info("Scraping banktrack webpage for links to banks")
        links = BankTrackScraper.get_all_urls_for_banks()
        BankTrackScraper.save_as_json(links, args.filename)


if __name__ == "__main__":

    main(parser.parse_args())
