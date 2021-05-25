from time import sleep
from selenium import webdriver
import values


def infinite_run():
    chrome_path = "chromedriver"
    op = webdriver.ChromeOptions()
    op.add_argument('--headless')
    driver = webdriver.Chrome(chrome_path, options=op)

    while True:
        check_stand(driver, values.stands['dev'])
        sleep(3)
        check_stand(driver, values.stands['qa'])
        sleep(3)
        check_stand(driver, values.stands['uat'])
        sleep(3)
        check_stand(driver, values.stands['sync'])
        sleep(10)


def type_on_input(input_element, text: str):
    for c in text:
        input_element.send_keys(c)
        sleep(0.1)


def check_stand(driver, stand_obj):
    driver.get(stand_obj['login_url'])
    sleep(2)
    type_on_input(driver.find_element_by_css_selector('input[formcontrolname="login"]'), values.login)
    type_on_input(driver.find_element_by_css_selector('input[formcontrolname="password"]'), values.password)
    driver.find_element_by_css_selector('button[type="submit"]').click()
    sleep(1.5)
    driver.get(stand_obj['map_url'])
    sleep(3)
    if driver.find_element_by_css_selector('#wrapper'):
        if not stand_obj['running']:
            print(f'Стэнд {stand_obj["name"]} поднялся')
            stand_obj['running'] = True
    else:
        if stand_obj['running']:
            print(f'Стэнд {stand_obj["name"]} упал')
            stand_obj['running'] = False


if __name__ == '__main__':
    infinite_run()