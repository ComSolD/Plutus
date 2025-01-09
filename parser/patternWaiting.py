from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProxyParsing():
    def __init__(self):
        self.service  = Service(executable_path="chromedriver.exe")
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service = self.service, options=options)

    def parser(self):
        try:
            self.driver.get("https://px6.me/")

            login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-role="login"]'))
            )
            login_button.click()

            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            password_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "login-password"))
            )


            email_input.send_keys("tzpythondemo@domconnect.ru")
            password_input.send_keys("kR092IEz")


            iframe = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "iframe"))
            )
            self.driver.switch_to.frame(iframe)

            checkbox = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "recaptcha-checkbox-border"))
            )

            checkbox.click()


            WebDriverWait(self.driver, 300).until(
                lambda d: d.find_element(By.ID, "recaptcha-anchor").get_attribute("aria-checked") == "true"
            )


            self.driver.switch_to.default_content()


            button = self.driver.find_element(By.XPATH, "//div[@class='form']//button[@class='btn btn-block btn-primary']")
            button.click()

                
            ip_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@class='right clickselect ']/b"))
            )

            date_elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//li[@class='mobile-show']/div[@class='right']"))
            )


            ips = [element.text for element in ip_elements]
            dates = [
                [line.strip() for line in element.get_attribute("textContent").split("\n") if line.strip()] for element in date_elements
            ]


            for ip, date in zip(ips, dates):
                print(f"{ip} - {date[-1]}")

        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            self.driver.quit()



if __name__ == "__main__":
    ProxyParsing().parser()