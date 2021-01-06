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


p = getPE10()
y = bondYield()
swr = mainFactor - peFactor * math.log(p) + bondFactor * y
brandonSWR = 3.5 + (30 - p) / 25 * 2

print("Bond yield: {:0.2f}%".format(y))
print("PE10: {:0.2f}".format(p))
print("Safe withdrawl rate: {:0.2f}%".format(swr))
print("Brandon's safe withdrawl rate: {:0.2f}%".format(brandonSWR))
