import time
import json

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from additions import add_lead_to_db, check_lead


def main():
    opts = Options()
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 Mobile Safari/537.36")
    opts.add_argument("user-data-dir=D:\\projects\\Личные проекты\\tilda_telegram_bot\\UserDataDir")

    driver = webdriver.Chrome(
        executable_path='D:\\projects\\Личные проекты\\tilda_telegram_bot\\ChromeDriver\\chromedriver.exe',
        chrome_options=opts)

    login = 'akorchuganoff@yandex.ru'
    password = '2004Efiop'

    url = 'https://tilda.cc'
    url_logged = 'https://tilda.cc/projects/'

    have_cookies = True

    if not have_cookies:
        driver.get(url=url)
        time.sleep(5)

        enter_button = driver.find_element(by=By.CLASS_NAME, value='t934__enter')
        print(enter_button)
        enter_button.click()
        time.sleep(5)

        email_field = driver.find_element(by=By.ID, value='email')
        email_field.clear()
        email_field.send_keys(login)
        time.sleep(2)

        password_field = driver.find_element(by=By.ID, value='password')
        password_field.clear()
        password_field.send_keys(password)
        time.sleep(20)

        enter_button = driver.find_element(by=By.CLASS_NAME, value='ts-btn')
        enter_button.click()
        # time.sleep(10)

        cookies = driver.get_cookies()

        with open('cookies.json', 'w') as jsonfile:
            json.dump(cookies, jsonfile)

        for cookie in cookies:
            print(cookie)
    else:
        driver.get(url_logged)
        time.sleep(3)

        project_link = driver.find_element(by=By.CLASS_NAME, value='td-site__section-one')
        project_link.click()
        time.sleep(3)

        leads_link = driver.find_element(by=By.XPATH, value='/html/body/div[7]/div[2]/div/div[1]/div[1]/div/a')
        leads_link.click()
        time.sleep(3)

        i = 1
        lead = driver.find_element(by=By.XPATH, value=f'/html/body/div[3]/div[3]/div/table[2]/tbody/tr[{i}]')
        print(lead)
        flag = True
        date = None
        while flag:
            i += 1
            try:
                xpath = f'/html/body/div[3]/div[3]/div/table[2]/tbody/tr[{i}]'
                lead = driver.find_element(by=By.XPATH, value=xpath)
                print(lead)
                new_date = driver.find_element(by=By.XPATH, value=xpath + '/td[1]').text
                if new_date != '':
                    date = new_date
                    date = "'" + date + "'"

                time = driver.find_element(by=By.XPATH, value=xpath + '/td[2]').text
                error = driver.find_element(by=By.XPATH, value=xpath + '/td[3]').text
                phone = driver.find_element(by=By.XPATH, value=xpath + '/td[4]').text
                name = driver.find_element(by=By.XPATH, value=xpath + '/td[5]').text
                guest_data = driver.find_element(by=By.XPATH, value=xpath + '/td[6]').text

                time = "'" + time.replace(':', '/') + "'"
                error = "'" + error + "'"
                phone = "'" + phone.replace(' ', '') + "'"
                name = "'" + name + "'"

                guest_data = guest_data.replace('\n', '|')
                guest_data = "'" + guest_data.replace(':', ' -') + "'"

                if check_lead(phone, date, time):
                    lead_to_db = (date, time, error, phone, name, guest_data)
                    add_lead_to_db(*lead_to_db)

            except NoSuchElementException as e:
                flag = False
                print(e.msg)

if __name__ == '__main__':
    main()