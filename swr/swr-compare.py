#!/usr/bin/env python3
import math
import requests
from bs4 import BeautifulSoup

bondFactor = 0.05
peFactor = 2.47
mainFactor = 12.15
bondURL = "http://www.multpl.com/10-year-treasury-rate/table/by-year"
peURL = "http://www.multpl.com/shiller-pe/table"


def getPE10():
    r = requests.get(peURL)
    soup = BeautifulSoup(r.content, "lxml")

    return float(soup.find("td").find_next_sibling("td").get_text())


def bondYield():
    r = requests.get(bondURL)
    soup = BeautifulSoup(r.content, "lxml")

    return float(soup.find("td").find_next_sibling("td").get_text().strip('% \n'))


y = bondYield()

pe10 = [22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]
print('PE swr  bswr diff')
for p in pe10:
    swr = mainFactor - peFactor * math.log(p) + bondFactor * y
    brandonSWR = 3.5 + (30 - p) / 25 * 2
    print('{} {:.2f} {:.2f} {:.2f}'.format(p, swr, brandonSWR, swr-brandonSWR))

