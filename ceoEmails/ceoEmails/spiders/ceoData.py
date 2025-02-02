import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.selector import Selector
from time import sleep
import undetected_chromedriver as uc

class CeodataSpider(scrapy.Spider):
    name = "ceoData"
    allowed_domains = ["growjo.com"]
    start_urls = ["https://growjo.com/industry/AI"]

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = uc.Chrome(headless=False)

    def parse(self, response):
        self.driver.get(response.url)

        # Login to the website
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div a.login-header"))
            ).click()

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            ).send_keys("wellsarison7@gmail.com")

            self.driver.find_element(By.ID, "password").send_keys("EL$g@Wfh5!k8Zst")
            self.driver.find_element(By.CSS_SELECTOR, "div button").click()
        except Exception as e:
            self.logger.error(f"Login failed: {e}")
            return
        #sleep(3)
        # Reload the page after login
        # WebDriverWait(self.driver, 10).until(
        #     lambda d: d.current_url == "https://growjo.com/industry/AI"
        # )
        self.driver.get(response.url)

        #sleep(3)        
        rows = response.css('table > tbody > tr')
        next_page = self.driver.find_element(By.CSS_SELECTOR, 'div > ul > li.next a').get_attribute("href")
        contacts = self.driver.find_elements(By.CSS_SELECTOR, 'td > button')
        if contacts:
            for contact in contacts:
                try:
                    contact.click()
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.modal-content")))
                except:
                    continue

        for row in rows:
            company_name = row.css('td > a::text').get()
            country = response.css('tr:nth-child(1) > td:nth-child(5)::text')  #row.css('td::text').getall()[2]
            ceo = row.css('tr:nth-child(1) > td:nth-child(10) > a::text').get()
            email = row.css('tr:nth-child(1) > td:nth-child(12) > a::text').get()  # Will fetch separately

            data = {
                'Company': company_name,
                'Country': country,
                'CEO_name': ceo,
                'Email': email
            }

            if 'ceo' not in ceo.lower():
                try:
                    row.find_element(By.CSS_SELECTOR, 'td > a::text').click()
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
                    )
                    #details_selector = Selector(text=self.driver.page_source)
                    ceo_infos = self.driver.find_element(By.CSS_SELECTOR, 'table')    #details_selector.css("table")[0] # table tr td::text
                    #email = details_selector.css("div a::text").get()

                    for ceo_info in ceo_infos:
                        try:
                            ceo_info.find_element(By.CSS_SELECTOR, 'tr:nth-child(1) > td:nth-child(3) > a').click()
                            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.modal-content")))
                        except:
                            continue

                    # for srow in ceo_info.css('tr'):
                        post = self.driver.find_element(By.CSS_SELECTOR, 'tr:nth-child(1) > td:nth-child(2)').text
                        if 'ceo' in post.lower():
                            data['CEO_name'] = self.driver.find_element(By.CSS_SELECTOR, 'tr:nth-child(1) > td:nth-child(1) > div:nth-child(2) > a:nth-child(2)').text
                            data['Email'] = self.driver.find_element(By.CSS_SELECTOR, 'tr:nth-child(1) > td:nth-child(12) > a').text
                except Exception:
                    pass
            print("Scraped Data:", data)
            yield data

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def close_spider(self, spider):
        self.driver.quit()