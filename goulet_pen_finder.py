#!/usr/env/bin python3

import urllib.request
import ssl
from bs4 import BeautifulSoup
import csv
import time

class PenFinderMethods:
    global html_parser
    html_parser = 'html.parser'
    global context
    context = ssl._create_unverified_context()

    def get_web_page(self, url):
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(url, context=context) as raw_page:
            results = raw_page
            return results

    def find_all_pens(self, start_page, end_page):
        pen_links = []
        fountain_pen_pages = "https://www.gouletpens.com/collections/all-fountain-pens?page="
        all_fountain_pens_products = "all-fountain-pens/products"
        gouletpens_url_base = 'https://www.gouletpens.com'
        for x in range(start_page,end_page + 1):
            url = fountain_pen_pages + str(x)
            raw_page = urllib.request.urlopen(url, context=context)
            parsed_page = BeautifulSoup(raw_page, html_parser)
            links = parsed_page.find_all('a', href=True)
            for x in links:
                if all_fountain_pens_products in str(x['href']):
                    pen_links.append(gouletpens_url_base + str(x['href']))
        return set(pen_links)

    def get_pen_name(self, parsed_soup):
        pen_name = parsed_soup.find('meta', property="og:title")['content']
        return pen_name

    def get_pen_price(self, parsed_soup):
        price = float(parsed_soup.find('meta', property="og:price:amount")['content'].replace(',',''))
        return price

    def get_technical_specs(self, parsed_soup):
        technical_specs = {}
        dt_tags = parsed_soup.find('dl').find_all('dt')
        dd_tags = parsed_soup.find('dl').find_all('dd')
        for index, key in enumerate(dt_tags):
            technical_specs[key.contents[0].strip()] = dd_tags[index].contents[0]
        return technical_specs

    def get_pen_grip_diameter(self, parsed_soup):
        technical_specs = self.get_technical_specs(parsed_soup)
        technical_specs_keys = technical_specs.keys()
        if 'Diameter - Grip' in technical_specs_keys:
            grip_diameter_raw = self.get_technical_specs(parsed_soup)['Diameter - Grip']
            grip_diameter_mm = float(grip_diameter_raw.split("mm")[0])
            return grip_diameter_mm
        else:
            return None


    def format_row(self, parsed_soup, pen_url):
        technical_specs = self.get_technical_specs(parsed_soup)

        pen_technical_specs_keys = technical_specs.keys()

        pen_name = self.get_pen_name(parsed_soup)
        pen_price = self.get_pen_price(parsed_soup)
        pen_grip_diameter = self.get_pen_grip_diameter(parsed_soup)

        if 'Body Material' in pen_technical_specs_keys:
            body_material = technical_specs['Body Material']
        else:
            body_material = None

        if 'Cap Type' in pen_technical_specs_keys:
            cap_type = technical_specs['Cap Type']
        else:
            cap_type = None

        if 'Grip Material' in pen_technical_specs_keys:
            grip_material = technical_specs['Grip Material']
        else:
            grip_material = None

        if pen_url == 'https://www.gouletpens.com/collections/all-fountain-pens/products/platinum-century-the-prime-fountain-pen-silver-limited-edition':
            pass
        else:
            new_row = [pen_name, pen_price, body_material, cap_type, grip_material, pen_grip_diameter, pen_url]

            return new_row

    def main(self):

        header = ['Pen Name', 'Price', 'Body Material', 'Cap Type', 'Grip Material', 'Grip Diameter', 'Url']

        pens = self.find_all_pens(1,52)

        output_file_name = 'all_goulet_pens.tsv'
        with open(output_file_name, 'w') as csv_file:
            file_writer = csv.writer(csv_file, delimiter='\t')
            file_writer.writerow(header)
            for pen in pens:
                time.sleep(1)
                with urllib.request.urlopen(pen, context=context) as raw_page:
                    parsed_page = BeautifulSoup(raw_page, html_parser)
                row = self.format_row(parsed_page, pen)
                file_writer.writerow(row)
#                try:
#                    file_writer.writerow(row)
#                except:
#                    print('this pen is missing data ' + pen)

if __name__ == "__main__":
    c = PenFinderMethods()
    c.main()
