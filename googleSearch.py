import asyncio
from random import randrange

from pyppeteer import launch
from time import sleep
from googlesearch import search
from bs4 import BeautifulSoup
from robobrowser import RoboBrowser
import datetime
import csv
import useragent;

from requests import Session

#"packers and movers in powai"
#"packers and movers in colaba",
# ["packers and movers in thane",
#     "packers and movers in dadar",
#     "packers and movers in mumbai",
#     "packers and movers in worli",
#                 "packers and movers in kharghar"]
# ["packers and movers in chembur",
#     "packers and movers in mulund east",
#     "packers and movers in mulund west",
#     "packers and movers in gorai",
#     "packers and movers in dongari",
#     "packers and movers in borivali"]
# ["packers and movers in kandivali west",
#     "packers and movers in kandivali east",
#     "packers and movers in goregaon",
#     "packers and movers in andheri west",
#     "packers and movers in andheri east"]

# "packers and movers in navi mumbai",
#     "packers and movers in vashi",
#     "packers and movers in kopar khairane",
#     "packers and movers in malad",
#     "packers and movers in jogeshwari",
#     "packers and movers in bhandup",
#     "packers and movers in powai"]
async def main():
    keywords =["packers and movers in vashi"]

    sitename = "tbpackersmovers"

    # Boiler plate code
    parser = 'html.parser'

    # Output dictionary
    rankResult = {}
    topSitesFile = 'topsites' + datetime.date.today().strftime("%d-%m-%Y") + '.csv'



    for keyword in keywords:

        #sleep(randrange(60, 120))

        browser = await launch({'headless': True})
        page = await browser.newPage()
        await page.setViewport({"width": 828, "height": 1792, "isMobile" : True})
        await page.setUserAgent(useragent.useragent())
        page.setDefaultNavigationTimeout(0);

        await page.goto("https://www.google.com?num=100")

        # await page.waitForXPath("input[contains(@class, 'gLFyf')]")
        await page.keyboard.type(keyword)

        await page.keyboard.press('Enter');

        await page.waitForNavigation()


        searchQueryUrl = await page.evaluate('() => location.href');

        #await page.waitFor(600000)

        body = await page.content()

        await browser.close()


        bodyParsed = BeautifulSoup(str(body), "html.parser");
        #
        links = bodyParsed.find_all("div", {"class": "r"});
        #

        counter = 0
        ourSiteRank = -1
        #
        d = []
        sites = []
        #
        for link in links:
            counter = counter + 1
            fetchSiteLink = link.find('a').get_attribute_list("href")[0]

            print(str(counter) + " " + fetchSiteLink)
            sites.append(fetchSiteLink)

            if (sitename in str(link)) and ourSiteRank == -1:
                ourSiteRank = "%d" % (counter)

        rankResult[keyword] = ourSiteRank

        with open(topSitesFile, 'a+') as topsites:
            writer = csv.writer(topsites)
            writer.writerow([keyword])

            for site in sites:
              writer.writerow([site])

    file = 'stats.csv'
    with open(file, 'a+') as f:
      writer = csv.writer(f)
      writer.writerow(['Keyword', 'Rank'])

      for k, v in rankResult.items():
        writer.writerow([str(k), str(v)])


asyncio.get_event_loop().run_until_complete(main())
