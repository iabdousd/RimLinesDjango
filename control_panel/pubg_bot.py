from selenium import webdriver


def selectPlan(browser_, choice):
    choices = {
        "74": "amount_select.70",
        "221": "amount_select.210",
        "770": "amount_select.700",
        "2013": "amount_select.1750",
        "4200": "amount_select.3500",
        "8750": "amount_select.7000",
    }
    e = browser_.find_element_by_xpath("//li[@cr='payment_select.mol_razerzvault']")
    e.click()
    e = browser_.find_element_by_xpath("//li[@cr='" + choices[choice] + "']")
    e.click()
    # browser.quit()


if __name__ == '__main__':
    browser = webdriver.Chrome()
    url = "https://www.midasbuy.com/midasbuy/id/buy/pubgm"
    browser.get(url)
    selectPlan(browser, '770')
