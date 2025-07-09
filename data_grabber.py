# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common import action_chains, keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import time, sleep


class Grabber(object):
    _driver = None

    def __init__(self):
        self.result = {}
        # self.driver = webdriver.PhantomJS('./phantomjs')
        # self.driver.set_page_load_timeout(10)

    @property
    def driver(self):
        if not self._driver:
            self._driver = webdriver.Chrome('./chromedriver')
            self.driver.set_window_size(1440, 800)
        return self._driver

    def save_cookies(self, name="cookies.pkl"):
        import pickle

        pickle.dump(self.driver.get_cookies(), open(name, "wb"))

    def load_cookies(self, name="cookies.pkl"):
        import pickle

        cookies = pickle.load(open(name, "rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)

    def not_a_match(self, name):
        if not name:
            return True
        for word in ["Matches", "(Goals)", "shots on goal", "Overtime"]:
            if word in name:
                return True

    def get_caption(self, text):
        caption = text
        return ".".join(caption.split())
        if "\n" in caption:
            caption = caption.split("\n")
            team_a, team_b = caption[0].split(), caption[1].split()
            if team_a[0] == "1." or team_a[0] == "Club":
                team_a = team_a[1:]
            if team_b[0] == "1." or team_b[0] == "Club":
                team_b = team_b[1:]
            caption = ".".join([team_a[0], team_b[0]])
        else:
            # print "ATTENTION: ", caption
            caption = ".".join(caption.split())
        return caption

    def get_koef(self, koef_item):
        try:
            return float(koef_item.text)
        except:
            return 1

    def load_page(self, category, url):
        start_time = time()
        self.driver.get(url)
        sleep(5)
        print "Page loaded", time() - start_time

    def fetch_from_category(self, category, url):
        try:
            self.load_page(category, url)
            events = self.get_events(category)
            print "Total events found on page:", len(events)

            for num, event in enumerate(events):
                name = self.get_event_name(event)
                if self.not_a_match(name):
                    continue
                caption = "{}:{}".format(self.get_caption(name), category)
                if caption and caption in self.result:
                    print "Error: {} already in results.".format(caption)
                else:
                    koefs = self.get_koefs(event)
                    print "#{} Game: {}={}".format(num, caption, koefs)
                    if koefs:
                        self.result[caption] = koefs
        except Exception, err:
            print "Some error in fetch from category:\n{}".format(err)

    def run(self):
        try:
            for category, url in self.urls.items():
                print "Start {}".format(category)
                self.fetch_from_category(category, url)
            return self.result
        finally:
            print "Quit driver"
            self.driver.quit()


class FavBetGrabber(Grabber):
    urls = {
        "Ice Hockey": "https://www.фавбет.бел/en/bets/#tours=17281,17451,18102,18091,18120,18121,18144,18148,18348,18397,18739,20530,20813,21492,62962,576892,527931,18124,792440,18125,18504,417979,332729,792221,406522,18095,17291,17427,333032,17417,112732,20815,217533,18106,17547&startingSoon=1440",
        "Football": "https://www.фавбет.бел/en/bets/#tours=17761,17573,17763,17575,17574,18316,17471,17473,20846,17294,637980,21562,18320,17818,18643,18790,23048,17847,17840,17394,166149,202727,19158,18319,19154,17396,19150,17756,244523,17798,18674,18563,17794,17791,17790,17793,17792,17649,17409,17710,17393,20280,17644,17487,20206,17482,17851,19896,17361,17369,17240,17777,20611,18175,17788,17558,19475,17783,17780,17781,17389,569930,17387,19874,19875,17494,17868,17492,17493,20193,17863,17862,19078,388052,17319,17252,22604,18995,17625,17239,17541,19197,347227,18588,17876,17428,17872,17873,17849,21051,21050,17425,21756,17877,17340,17935,57215,17668,17633,17436,17635,245501,21048,17439,17282,17803,17804,17534,17531,18368,18478,18699,160526,21049,17137,410746,17337,17336,17883,27944,17333,21640,18755,17441,17440,19531,17345,17445,17358,17604,17351,17602,63607,17812,18328,17811,17817,20414,17295,17296,19829,17754,17757,21634,19665,17329,17331,17892,17890,17891,18926,17894,17895,17456,20718,19527,20861,17343,58837,572043,17944,75768,17824,1154206,17821,17820,18326,17795,17906,19428,18655,18654,17773,17771,17770,17373,17466,19096,17869,17779,17838,23355,18022,20908,188740,22698,17667,17834,17660,17837,18949,17881,22214,17262,18435,17584,18971,19002,18283&startingSoon=1440",
    }

    def load_page(self, category, url):
        super(FavBetGrabber, self).load_page(category, url)
        sleep(10)

    def get_events(self, category):
        return self.driver.find_elements_by_class_name("event--head-block")

    def get_koefs(self, event):
        try:
            koefs = event.find_elements_by_xpath(".//ul/li/label")
            return [self.get_koef(x) for x in koefs[:3]]
            #if len(koefs) >= 3:
            #    return (float(koefs[0].text), float(koefs[1].text), float(koefs[2].text))
        except Exception, err:
            print "Error during koefs fetching: {}".format(err)
            return []

    def get_event_name(self, event):
        return event.find_element_by_class_name("event--name--info").text.encode('utf-8').strip()


class oneXBetGrabber(Grabber):
    urls = {
        "Ice Hockey": "https://1xbet.com/en/line/Ice-Hockey/",
        "Football": "https://1xbet.com/en/line/Football/",
        "Basketball": "https://1xbet.com/en/line/Basketball/",
    }

    def load_page(self, category, url):
        start_time = time()
        super(oneXBetGrabber, self).load_page(category, url)
        try:
            #close_btn = (By.ID, "help_popup")
            #WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located(close_btn))
            sleep(20)
            action_chains.ActionChains(self.driver).send_keys(keys.Keys.ESCAPE).perform()
            sleep(1)
            action_chains.ActionChains(self.driver).send_keys(keys.Keys.ESCAPE).perform()
        except:
            print "No dialogs were showed"
        sleep(2)
        show_dropdown = (By.XPATH, "//div[@class='labelFdropAct']")
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(show_dropdown)).click()
        self.driver.find_element_by_xpath("//div[@class='labelFdropList']/div[@data-type='500']").click()
        sleep(2)
        self.driver.find_element_by_xpath("//a[@title='Hourly']").click()
        self.driver.find_element_by_xpath("//li[@value='1440']").click()
        sleep(2)
        self.driver.find_element_by_xpath("//label[@title='{}']".format(category)).click()
        sleep(5)
        print "Setup page for 1x bet: ", time() - start_time

    def get_events(self, category):
        return self.driver.find_elements_by_xpath("//a[@class='c-events__name']/ancestor::div[@class='c-events__item']")

    def get_koefs(self, event):
        try:
            koefs = event.find_elements_by_xpath("./div[@class='c-bets']/div[@class='c-bets__item']/a")
            return [self.get_koef(x) for x in koefs[:3]]
        except Exception, err:
            print "Error during koefs fetching: {}".format(err)
            return []

    def get_event_name(self, event):
        try:
            return event.find_element_by_class_name("c-events__name").text.encode('utf-8').strip()
        except Exception, err:
            print "ERROR", event.find_element_by_class_name("c-events__name").text
            print err
            print


class PariMatchGrabber(Grabber):
    urls = {
        "Ice Hockey": "https://www.parimatch.com/en/bet.html?filter=24hours",
        "Football": "https://www.parimatch.com/en/bet.html?filter=24hours",
        "Basketball": "https://www.parimatch.com/en/bet.html?filter=24hours",
    }

    def get_events(self, category):
        events_locator = "//h3[contains(text(),'{}') and not(contains(text(),'Stats'))]/following-sibling::div//tbody[contains(@class,'processed') and contains(@class,'row')]".format(category)
        return self.driver.find_elements_by_xpath(events_locator)

    def get_event_name(self, event):
        try:
            return event.find_element_by_xpath(".//a[@class='om']").text.encode('utf-8', errors='ignore').strip()
        except:
            return None

    def get_koefs(self, event):
        try:
            #koefs = event.find_elements_by_xpath("./tr/td/u/a")
            #return [self.get_koef(x) for x in koefs[4:7]]
            koefs = event.find_elements_by_xpath("./tr/td")
            return [self.get_koef(x.find_element_by_xpath("./u/a")) for x in koefs[8:11]]
        except Exception, err:
            print "Error during koefs fetching: {}".format(err)
            return []

if __name__ == '__main__':
    import json
    result = {}

    bets = {
        #"favbet": FavBetGrabber(),
        #"1xbet": oneXBetGrabber(),
        "parimatch": PariMatchGrabber(),
    }

    start_time = time()
    for site, grabber in bets.items():
        result[site] = grabber.run()
        with open("{}.txt".format(site), 'w') as outfile:
            json.dump(result[site], outfile)
        print("Total event on {} site: {}".format(site, len(result[site])))
    print("Total events grabbed: {}\nTotal time: {}".format(len(result), time() - start_time))
