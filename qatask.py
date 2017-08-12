#!/usr/bin/python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import unittest


class AmazonQA(unittest.TestCase):

    def setUp(self):
        global driver
        driver=webdriver.Firefox()
        driver.get("http://www.amazon.com")

        if "Amazon" in driver.title:
            print ("'Connection to amazon.com' verified")
        else:
            print ("'Connection to amazon.com' could't verified.")
            driver.close()

    def test_Amazon(self):

        #Locators
        amazonSigninLinkID          = "nav-link-accountList"
        amazonEmailFieldID          = "ap_email"
        amazonPasswordFieldID       = "ap_password"
        amazonSearchBoxID           = "twotabsearchtextbox"
        amazonSecondPageXpath       = ".//*[@id='pagn']/span[3]/a"
        amazonThirdProductXpath     = ".//*[@id='s-results-list-atf']/li[3]/div/div/div/div[2]/div[1]/div[1]/a/h2"
        amazonAddToListButtonID     = "add-to-wishlist-button-submit"
        amazonWishListXpath         = ".//*[@id='nav-flyout-wl-items']/div/a[3]/span"
        amazonDeleteButtonName      = "submit.deleteItem"
        amazonSearchResultCSS       = ".a-color-state.a-text-bold"

        #Amazon credentials
        amazonEmail                 = "YOUR_EMAIL_HERE"
        amazonPassword              = "YOUR_PASSWORD_HERE"
        amazonSearchText            = "YOUR_TEXT_HERE"
 
        # Signin to amazon.com.
        amazonSigninLinkElement     = WebDriverWait(driver,10).until(
            EC.visibility_of_element_located((By.ID, amazonSigninLinkID)))
        amazonSigninLinkElement.click()

        amazonEmailFieldElement     = WebDriverWait(driver,10).until(
            EC.visibility_of_element_located((By.ID, amazonEmailFieldID)))
        amazonEmailFieldElement.send_keys(amazonEmail)

        amazonPasswordFieldElement  = WebDriverWait (driver,10).until(
            EC.visibility_of_element_located((By.ID, amazonPasswordFieldID)))
        amazonPasswordFieldElement.send_keys(amazonPassword)
        amazonPasswordFieldElement.submit()

        # Send search text to search box and submit.
        amazonSearchBoxElement = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, amazonSearchBoxID)))
        amazonSearchBoxElement.clear()
        amazonSearchBoxElement.send_keys(amazonSearchText)
        amazonSearchBoxElement.submit()

        # Verify the results for search text.
        amazonSearchResultElement = WebDriverWait(driver,10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,amazonSearchResultCSS)))
        text=amazonSearchResultElement.get_attribute("innerHTML")
        if amazonSearchText in text:
            print ("'Results for "+amazonSearchText+"' verified")
        else:
            print ("'Results for " + amazonSearchText + "' couldn't verified")
            driver.close()

        # Switch the second page of search results.
        amazonSecondPageElement= WebDriverWait(driver,10).until(
            EC.visibility_of_element_located((By.XPATH, amazonSecondPageXpath)))

        amazonSecondPageElement.click()

        # Verify second page is shown.
        if "page=2" in driver.current_url:
            print ("'Second  page of results is shown' verified ")
        else:
            print ("'Second page of results is shown' could't verified")
            driver.close()

        # Get the product's unique id from the element and select the product.
        amazonProductElem = WebDriverWait(driver,10).until(
            EC.visibility_of_element_located((By.XPATH,".//*[@id='s-results-list-atf']/li[3]")))
        amazonProductID= amazonProductElem.get_attribute("data-asin")
        amazonProductElem.find_element_by_xpath(".//a").click()

        # Add product to list.
        amazonAddToListButtonElement = WebDriverWait(driver,10).until(
            EC.visibility_of_element_located((By.ID ,amazonAddToListButtonID)))
        amazonAddToListButtonElement.click()

        #Hover on list link and select the WishList.
        amazonListhover= WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, ".//*[@id='nav-link-accountList']")))
        ActionChains(driver).move_to_element(amazonListhover).perform()
        amazonWishListElement = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH ,amazonWishListXpath)))
        amazonWishListElement.click()

        #Verify the product  added to list.
        amazonlistElements = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID ,"g-items"))).find_elements_by_xpath(".//div")
        for div in amazonlistElements:
            if amazonProductID in div.get_attribute("data-reposition-action-params"):
                print("'The product  added to list' verified")
                productDiv = div
                break

        # Delete the product from the list.
        productDiv.find_element_by_xpath(".//input[@type='submit']").click()

        driver.refresh()
        amazonlistElements2 = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "g-items"))).find_elements_by_xpath(".//div")
        for division in amazonlistElements2:
            if amazonProductID in division.get_attribute("data-reposition-action-params"):
                print ("'The product deleted from the list' verified")
                break


if __name__ == "__main__":
    unittest.main()