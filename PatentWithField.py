# ---------------------------------------------------------------------------
# Extends pypatent's Patent class to additionally scrape for patent fields
# ---------------------------------------------------------------------------

from pypatent import Patent
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from selenium import webdriver


class PatentWithField(Patent):
    def __init__(self, title: str, url: str):
        super().__init__(title, url)
        self.fields = None
        self.application_type = None

    # Fetches details. Need access to parsed page, so had to c/p func here
    def fetch_details(self):
        self.fetched_details = True
        r = self.web_connection.get(self.url)
        s = BeautifulSoup(r, 'html.parser')
        try:
            self.patent_num = s.find(
                string='United States Patent ').find_next().text.replace('\n', '').strip()
        except:
            pass

        try:
            self.patent_date = s.find_all(
                align='right', width='50%')[-1].text.replace('\n', '').strip()
        except:
            pass

        try:
            abstract = s.find(string='Abstract').find_next(
            ).text.replace('\n', '').strip()
            self.abstract = re.sub(' +', ' ', abstract)
        except:
            pass

        try:
            inventors = s.find(string='Inventors:').find_next(
            ).text.replace('\n', '').split('),')
            inventors = [t.split(';') for t in inventors]
            inventors = [[i.split('(') for i in j] for j in inventors]
            self.inventors = []
            for person in inventors:
                lname = person[0][0].strip()
                fname = person[1][0].strip()
                loc = person[1][1].strip().replace(')', '')
                d = [fname, lname, loc]
                self.inventors.append(d)
        except:
            pass

        try:
            self.applicant_name = s.find(string=re.compile('Applicant:')).find_next().find(
                'td').text.replace('\n', '').strip()
        except:
            pass

        try:
            rem_applicant_data = s.find(string=re.compile(
                'Applicant:')).find_next().find('td').find_next_siblings()
            try:
                self.applicant_city = rem_applicant_data[0].text.replace(
                    '\n', '').strip()
            except:
                pass
            try:
                self.applicant_state = rem_applicant_data[1].text.replace(
                    '\n', '').strip()
            except:
                pass
            try:
                self.applicant_country = rem_applicant_data[2].text.replace(
                    '\n', '').strip()
            except:
                pass
        except:
            pass

        try:
            assignee_raw = s.find(string=re.compile(
                'Assignee:')).find_next().text.replace('\n', '')
            assignee_data = assignee_raw.split('(')
            try:
                self.assignee_name = assignee_data[0].strip()
            except:
                pass
            try:
                self.assignee_loc = assignee_data[1].strip().replace(')', '')
            except:
                pass
        except:
            pass

        try:
            self.family_id = s.find(string=re.compile(
                'Family ID:')).find_next().text.replace('\n', '').strip()
        except:
            pass

        try:
            self.applicant_num = s.find(string=re.compile(
                'Appl. No.:')).find_next().text.replace('\n', '').strip()
        except:
            pass

        try:
            self.file_date = s.find(string=re.compile(
                'Filed:')).find_next().text.strip()
        except:
            pass

        try:
            claims = s.find(string=re.compile('Claims')
                            ).find_all_next(string=True)
            claims = claims[:claims.index('Description')]
            self.claims = [i.replace('\n', '').strip()
                           for i in claims if i.replace('\n', '').strip() != '']
        except:
            pass

        try:
            description = s.find(string=re.compile(
                'Description')).find_all_next(string=True)
            self.description = [i.replace('\n', '').strip() for i in description if i.replace(
                '\n', '').strip() not in ['', '* * * * *']]
        except:
            pass

        try:
            fields = s.find(string=re.compile('Current CPC Class:')).find_next().text.strip()
            self.fields = fields
        except:
            pass
