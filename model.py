import pandas as pd
from functools import lru_cache
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from time import sleep

from data import get_links_form


__all__ = {"TableFormParser", "parser"}


class TableFormParser:

    @staticmethod
    def launch_driver(url_form):
        """ Open page of match """
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url=url_form)
        sleep(1.5)
        return driver

    @lru_cache(maxsize=None)
    def get_form_goals_dict(self, scored_goals: str, missed_goals: str):
        """ Get excel matches """
        # all_links = ['https://www.flashscore.com.ua/match/G4dGbP8J/#/standings/form/overall/5',
        #              'https://www.flashscore.com.ua/match/jJbkHL6i/#/standings/form/overall/5',
        #              'https://www.flashscore.com.ua/match/ngpsIfBO/#/standings/form/overall/5']
        all_links = get_links_form()
        names_matches, names_teams = [], []
        for link in all_links:
            teams = []
            page = TableFormParser.launch_driver(link)
            name_match = page.find_element(By.CLASS_NAME, "tournamentHeader__country")
            command_row_participant = page.find_elements(By.CLASS_NAME, "table__row--selected ")
            for tag in command_row_participant:
                span_tag = tag.find_element(By.CLASS_NAME, "table__cell--score ")
                command = tag.find_element(By.CLASS_NAME, "tableCellParticipant__block")
                goals = span_tag.text.split(":")
                if goals[0] >= scored_goals and goals[1] >= missed_goals:
                    teams.append(command.text)
                    if len(teams) == 2:
                        names_matches.append(name_match.text)
                        names_teams.append(teams)
        df = pd.DataFrame({"match": [*names_matches], "teams": [*names_teams]})
        df.to_excel("./matches.xlsx")
        return df


parser = TableFormParser()
