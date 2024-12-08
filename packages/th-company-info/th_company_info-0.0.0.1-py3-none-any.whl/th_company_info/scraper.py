import cloudscraper
from bs4 import BeautifulSoup
import json
from .exception import ScraperException, ParseException

def safe_find_text(soup, search, next_tag="td", default="null"):
    """
    Safely extracts text from a BeautifulSoup object.
    :param soup: BeautifulSoup object
    :param search: String to search for in the HTML
    :param next_tag: Tag to look for next
    :param default: Default value if extraction fails
    :return: Extracted text or default value
    """
    try:
        element = soup.find(string=search)
        if element:
            return element.find_next(next_tag).text.strip()
    except AttributeError:
        return default
    return default

def th_company_info(tax_id: str):
    """
    Scrapes company data from dataforthai.com based on tax ID.
    :param tax_id: Tax ID to query (must be a 13-digit string)
    :return: Dictionary containing scraped data
    :raises: ScraperException, ParseException
    """

    # Enforce string input
    if not isinstance(tax_id, str):
        raise ValueError("Tax ID must be provided as a string.")

    # Validate the length of the tax_id
    if len(tax_id) != 13 or not tax_id.isdigit():
        raise ValueError("Tax ID must be a 13-digit numeric value (string type).")

    url = f"https://www.dataforthai.com/company/{tax_id}"
    scraper = cloudscraper.create_scraper()

    try:
        response = scraper.get(url)
        response.raise_for_status()
    except Exception as e:
        raise ScraperException(f"Error fetching URL: {e}")

    try:
        soup = BeautifulSoup(response.text, "html.parser")

        data = {
            "tax_id": safe_find_text(soup, "เลขทะเบียน"),
            "name_th": soup.find("h1", class_="noselect").text.strip() if soup.find("h1", class_="noselect") else "null",
            "name_en": soup.find("h3", class_="noselect").text.strip() if soup.find("h3", class_="noselect") else "null",
            "description": safe_find_text(soup, "ธุรกิจ"),
            "status": safe_find_text(soup, "สถานะ"),
            "registered_date": safe_find_text(soup, "จดทะเบียน"),
            "registered_capital": safe_find_text(soup, "ทุนจดทะเบียน"),
            "address": safe_find_text(soup, "ที่ตั้ง"),
            "website": (
                soup.find(string="เว็บไซต์").find_next("a").text.strip()
                if soup.find(string="เว็บไซต์") else "null"
            ),
            "stock_symbol": safe_find_text(soup, "หลักทรัพย์"),
        }
        return data_to_json(data)

    except Exception as e:
        raise ParseException(f"Error parsing HTML: {e}")

def data_to_json(data):
    """
    Converts data dictionary to a formatted JSON string.
    :param data: Dictionary containing the data
    :return: JSON string
    """
    return json.dumps(data, ensure_ascii=False, indent=4)
