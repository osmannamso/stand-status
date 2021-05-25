# encoding=utf8 
import sys 
reload(sys)
sys.setdefaultencoding('utf8')
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
import urllib
import unicodecsv as csv
from selenium.webdriver.common.action_chains import ActionChains
import math



# kaspi_brands = []
# with open('kaspi_brands.csv', 'rb') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         kaspi_brands.append(row[0])

# for kaspi_brand in kaspi_brands:
# 	print(kaspi_brand)

chrome_path = "/home/osmn/chromedriver"
driver = webdriver.Chrome(chrome_path)
driver.get('https://www.kabinka.kz/production/dushevye-kabiny/')

sections_elems = driver.find_elements_by_css_selector('a.catalog_section_list__item')
sections = []
category_names = []
for section_elem in sections_elems:
	sections.append({'link': section_elem.get_attribute('href'), 'name': section_elem.get_attribute('textContent')})

i = 0
for section in sections:
	i += 1
	if i == 1:
		continue
	driver.get(section['link'])
	while(len(driver.find_elements_by_css_selector('button.catalog_section_more')) > 0):
		driver.find_elements_by_css_selector('button.catalog_section_more')[0].click()
		time.sleep(5)

	products_links_elems = driver.find_elements_by_css_selector('a.catalog_section__item_link')

	for product_link_elem in products_links_elems:
		link = product_link_elem.get_attribute('href')
		driver.execute_script("window.open('');")
		driver.switch_to_window(driver.window_handles[len(driver.window_handles) - 1])
		driver.get(link)
		time.sleep(3)

		pr_name = driver.find_element_by_css_selector('h1.catalog_element__name').get_attribute('textContent')
		print(pr_name)

		pr_description = driver.find_elements_by_css_selector('div.catalog_element__tabs_panel')[0].get_attribute('textContent')
		print(pr_description)

		pr_images_elems = driver.find_elements_by_css_selector('span.catalog_element__images_item')
		pr_images = {}
		pr_images['images'] = []
		for pr_image_elem in pr_images_elems:
			pr_image_elem.click()
			time.sleep(0.5)
			pr_images['images'].append('https://www.kabinka.kz' + driver.find_element_by_css_selector('div.catalog_element__image img').get_attribute('src'))
		pr_images_json = json.dumps(pr_images, ensure_ascii=False).encode('utf-8')
		print(pr_images_json)

		pr_price = driver.find_element_by_css_selector('span.catalog_element__price_value').get_attribute('textContent')
		print(pr_price)

		pr_category_remote = section['name']
		print(pr_category_remote)

		characters = {}
		characters['fields'] = []
		lis_elems = driver.find_elements_by_css_selector('li.catalog_element__property')
		terms = []
		for li_elem in lis_elems:
			term = {}
			li_name = li_elem.find_element_by_css_selector('span.catalog_element__property_name').get_attribute('textContent')
			li_value = li_elem.find_element_by_css_selector('span.catalog_element__property_value').get_attribute('textContent')
			term['specification_name'] = li_name
			term['specification_value'] = li_value
			terms.append(term)
		characters['fields'].append({'terms': terms, 'specification_group_name': 'Характеристики'})
		pr_spec_json = json.dumps(characters, ensure_ascii=False).encode('utf-8')
		print(pr_spec_json)
		
		fields = [pr_name, pr_description, pr_images_json, pr_price[:-2].replace(' ', ''), pr_category_remote, pr_spec_json]
		with open('kabinka.csv', 'a') as f:
			writer = csv.writer(f)
			writer.writerow(fields)
			print(fields)

		driver.close()
		driver.switch_to_window(driver.window_handles[len(driver.window_handles) - 1])

# links = driver.find_elements_by_css_selector('a.nav__sub-list-el-link')
# id = 0
# for link in links:
# 	id += 1
# 	print(id)
# 	category_link = link.get_attribute('href')

# 	category_name = link.get_attribute('textContent')
# 	if 'Все' in category_name:
# 		continue
	
# 	time.sleep(3)
# 	driver.execute_script("window.open('');")
# 	driver.switch_to_window(driver.window_handles[len(driver.window_handles) - 1])
# 	driver.get(category_link)
# 	time.sleep(3)
# 	count_elem = driver.find_elements_by_css_selector('span.filters__count')[0]
# 	count = int(count_elem.get_attribute('textContent')[2:-1])
# 	page_count = int(math.ceil(float(count)/12))

# 	for i in range(1, page_count + 1):
# 		driver.execute_script("window.open('');")
# 		driver.switch_to_window(driver.window_handles[len(driver.window_handles) - 1])
# 		driver.get(category_link + '?page=' + str(i))
		
# 		products_elems = driver.find_elements_by_css_selector('div.item-card')
# 		for product_elem in products_elems:
# 			link_prod = product_elem.find_element_by_css_selector('a.item-card__name-link.ddl_product.ddl_product_link').get_attribute('href')
			
# 			pr_name = product_elem.find_element_by_css_selector('a.item-card__name-link.ddl_product.ddl_product_link').get_attribute('textContent')
# 			print(pr_name)

# 			pr_names = []
# 			with open('products.csv', 'rb') as f:
# 				reader = csv.reader(f)
# 				for row in reader:
# 					pr_names.append(row[0])
			
# 			if pr_name in pr_names:
# 				continue

# 			driver.execute_script("window.open('');")
# 			driver.switch_to_window(driver.window_handles[len(driver.window_handles) - 1])
# 			driver.get(link_prod)

# 			description_elem = driver.find_element_by_css_selector('div.item__description-text')
# 			pr_description = description_elem.get_attribute('textContent')
# 			print(pr_description)

# 			brand_name = ''
# 			for kaspi_brand in kaspi_brands:
# 				if kaspi_brand in pr_name:
# 					brand_name = kaspi_brand
# 			if brand_name:
# 				print(brand_name)

# 			images = {}
# 			images_elems = driver.find_elements_by_css_selector('img.item__slider-pic')
# 			for image_elem in images_elems:
# 				images['images'] = []
# 				images['images'].append(image_elem.get_attribute('src'))
# 			data_images = json.dumps(images, ensure_ascii=False).encode('utf-8')
# 			print(data_images)

# 			offers = {}
# 			offer_table = driver.find_element_by_css_selector('table.sellers-table__self')
# 			trs_offers = offer_table.find_elements_by_css_selector('tbody tr')
# 			offers['fields'] = []
# 			for tr_offer in trs_offers:
# 				td_name_elem = tr_offer.find_elements_by_css_selector('td.sellers-table__cell')[0]
# 				partner_name = td_name_elem.find_elements_by_css_selector('a')[0].get_attribute('textContent')
				
# 				results = []

# 				with open('partners.csv', 'rb') as f:
# 					reader = csv.reader(f)
# 					for row in reader:
# 						results.append(row[0])

# 				gangsta = any(partner_name in t for t in results)
# 				if gangsta == True:
# 					continue

# 				linka = td_name_elem.find_elements_by_css_selector('a')[0].get_attribute('href')
# 				driver.execute_script("window.open('');")
# 				driver.switch_to_window(driver.window_handles[len(driver.window_handles) - 1])
# 				driver.get(linka)
# 				time.sleep(3)
# 				partner_gain_name = driver.find_element_by_css_selector('h1.merchant-profile__name').get_attribute('textContent')
# 				partner_gain_phone = ''
# 				for number in driver.find_elements_by_css_selector('span.merchant-profile__contact-text'):
# 					partner_gain_phone += number.get_attribute('textContent')
# 				partner_gain_shit = ''
# 				partner_gain_shit += driver.find_element_by_css_selector('div.merchant-profile__data-create').get_attribute('textContent').strip()
# 				partner_gain_shit += driver.find_element_by_css_selector("meta[itemprop='ratingValue']").get_attribute('content')
# 				partner_gain_trs_elems = driver.find_elements_by_css_selector('tr.merchant-address__list-content-items ')
# 				partner_gain_adresses = {}
# 				partner_gain_adresses['nodnag'] = []
# 				for partner_tr_elem in partner_gain_trs_elems:
# 					partner_gain_address_name = partner_tr_elem.find_element_by_css_selector('td.merchant-address__list-content-item._address').get_attribute('textContent')
# 					partner_gain_address_mode = partner_tr_elem.find_element_by_css_selector('td.merchant-address__list-content-item._mode').get_attribute('textContent')
# 					partner_gain_adresses['nodnag'].append({'address': partner_gain_address_name, 'mode': partner_gain_address_mode})
# 				partner_gain_address_json = json.dumps(partner_gain_adresses, ensure_ascii=False).encode('utf-8')
# 				print(partner_gain_name)
# 				print(partner_gain_phone)
# 				print(partner_gain_shit)
# 				print(partner_gain_address_json)
				
# 				fields = [partner_gain_name, partner_gain_phone, partner_gain_shit, partner_gain_address_json]
# 				with open('partners.csv', 'a') as f:
# 					writer = csv.writer(f)
# 					writer.writerow(fields)
# 					print(fields)

# 				driver.close()
# 				driver.switch_to_window(driver.window_handles[len(driver.window_handles) - 1])

# 				td_price_elem = tr_offer.find_elements_by_css_selector('td.sellers-table__cell')[3]
# 				partner_price = td_price_elem.get_attribute('textContent')
# 				offers['fields'].append({'price': partner_price, 'partner_name': partner_name})
# 			json_offers = json.dumps(offers, ensure_ascii=False).encode('utf-8')
# 			print(json_offers)

# 			charac_elem = driver.find_element_by_css_selector("li[data-tab='specifications']")
# 			charac_elem.click()
# 			specifications = {}
# 			specifications['fields'] = []
# 			spec_elems = driver.find_elements_by_css_selector('dl.specifications-list__el')
# 			for spec_elem in spec_elems:
# 				spec_group_name = 'Основные характеристики'
# 				if len(spec_elem.find_element_by_css_selector('h4.specifications-list__header').get_attribute('textContent')) > 0:
# 					spec_group_name = spec_elem.find_element_by_css_selector('h4.specifications-list__header').get_attribute('textContent')
# 				terms_elems = spec_elem.find_elements_by_css_selector('dl.specifications-list__spec')
# 				terms = []
# 				for term_elem in terms_elems:
# 					term_name = term_elem.find_element_by_css_selector('span.specifications-list__spec-term-text').get_attribute('textContent')
# 					term_value = term_elem.find_element_by_css_selector('dd.specifications-list__spec-definition').get_attribute('textContent')
# 					terms.append({'specification_name': term_name, 'specification_value': term_value})
# 				specifications['fields'].append({'terms': terms, 'specification_group_name': spec_group_name})
# 			specifications_json = json.dumps(specifications, ensure_ascii=False).encode('utf-8')
# 			print(specifications_json)

# 			pr_category_remote = category_name
# 			print(pr_category_remote)
# 			fields = [pr_name, ' '.join(pr_description.replace(';', ' ').replace('\\n', '').split()).strip("\\n"), brand_name, data_images, ' '.join(json_offers.replace('\\n', '').split()).strip("\\n"), ' '.join(specifications_json.replace('\\n', '').replace('\\t', '').split()).strip("\\n"), pr_category_remote]
# 			with open('products.csv', 'a') as f:
# 				writer = csv.writer(f)
# 				writer.writerow(fields)
# 				print(fields)
# 			time.sleep(3)

# 			driver.close()
# 			driver.switch_to_window(driver.window_handles[len(driver.window_handles) - 1])
# 		time.sleep(3)
# 		driver.close()
# 		driver.switch_to_window(driver.window_handles[len(driver.window_handles) - 1])

# 	driver.close()
# 	driver.switch_to_window(driver.window_handles[len(driver.window_handles) - 1])