from urllib.request import urlopen
import re

# ************************************************************************************************************************************************************************* #
# The following urls are able to be scraped
# Please feel free to play around with them!
# Just paste them as such html = urlopen("URLHERE")
# https://www.bestbuy.ca/en-ca/collection/laptops-on-sale/46082?icmp=computing_evergreen_laptops_and_macbooks_category_detail_category_icon_shopby_laptops_on_sale
# https://www.bestbuy.ca/en-ca/category/laptops-macbooks/20352
# ************************************************************************************************************************************************************************* #

def main():
	html = urlopen("https://www.bestbuy.ca/en-ca/category/laptops-macbooks/20352")
	count = 0
	html = str(html.read())

	# Matches with products from the hardcoded url
	values = re.findall(r'<div class="col-xs-12_1GBy8 col-sm-4_NwItf col-lg-3_2V2hX x-productListItem productLine_2N9kG">(.*?)</div></div></div></div></a></div></div>', html)
	for val in values:
		count += 1

	file_out = open("bb_product_list.txt", "w")

	print(str(count) + ": products scraped from BB")
	print("Entries ==> bb_product_list.txt")
	for val in values:
		file_out.write(val)
		file_out.write("\n\n\n")
	file_out.close()

	file = open("bb_product_list.txt", "r")
	file = file.read()
	first_bb_extract(file)

def extract_price(file):
	prices = re.findall(r'(?<!SAVE )([$]+[0-9.,]*)', file)
	sales = re.findall(r'(?<=SAVE )([$]+[0-9.,]*)|$', file)
	return prices, sales

def first_bb_extract(file):
	product_extracted_data = re.findall(r'href="/en-ca/product/(.*?)/', file)
	file_out = open("bb_extracted_data.txt", "w")
	prices, sales = extract_price(file)

	# Grabs the producers and groups them
	producers = {}
	for product in product_extracted_data:
		# Matches with the first two characters in a line
		brand = re.search(r'^(.{2})', product)
		if brand.group(0) in producers:
			producers[brand.group(0)].append(product)
		else:
			producers[brand.group(0)] = []


	count = 0
	for key in producers.keys():
		for product in producers[key]:
			file_out.write("Producer: " + key + " Price: " + prices[2*count] + "	")
			file_out.write(product)
			file_out.write("\n")
			count += 1


if __name__ == "__main__":
	main()
