import requests
from bs4 import BeautifulSoup as bs
from urls_consts import (URL_LIGHT_VERSION, URL_LIGHT_VERSION_OVER, URL_LIGHT_VERSION_LIVE)


__all__ = {"get_matches", "get_upcoming_matches", "get_links_form"}


def get_matches(html) -> list[str]:
    """Get list of match's ids"""
    soup = bs(html.text, "html.parser")
    all_tags_a = soup.find("div", id="score-data").find_all("a")
    matches = [unique_href.get("href")[:-4]
                     if unique_href.get("href").endswith("?s=3")
                     or unique_href.get("href").endswith("?s=2")
                     else unique_href.get("href") for unique_href in all_tags_a]
    return matches


def get_upcoming_matches():
    """Get list of upcoming match's ids"""
    html = lambda url: requests.get(url)
    all_match_ids = get_matches(html(URL_LIGHT_VERSION))
    all_match_over_ids = get_matches(html(URL_LIGHT_VERSION_OVER))
    all_match_live_ids = get_matches(html(URL_LIGHT_VERSION_LIVE))
    result = [match for match in all_match_ids if
              match not in all_match_live_ids + all_match_over_ids]
    return result


def get_links_form() -> list[str]:
    """ Formation upcoming matches links list"""
    all_upcoming_match_id = get_upcoming_matches()
    url = lambda id: "https://www.flashscore.com.ua" + id + "#/standings/form/overall/5"
    all_links_table = [url(match_id) for match_id in all_upcoming_match_id]
    return all_links_table
