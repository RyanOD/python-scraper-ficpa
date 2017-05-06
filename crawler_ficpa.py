from lxml import html
import requests
from sys import argv
from random import randint
from time import sleep

script = argv
target = open('cpa_list_raw_data.txt', 'w')

companyUrl = 'http://www.ficpa.org/Public/Referral/FindCPADetails.aspx?FirmID='

xpath = '//*[@id="ctl00_PanelContent_ProfileID_lblFirmName"]/text()'
xpath_address_1 = '//*[@id="ctl00_PanelContent_ProfileID_firmProfile_ctl00_rowfaddr1"]/td[2]/text()'
xpath_address_2 = '//*[@id="ctl00_PanelContent_ProfileID_firmProfile_ctl00_rowfaddr3"]/td[2]/text()'
xpath_phone = '//*[@id="ctl00_PanelContent_ProfileID_firmProfile_ctl00_rowfphone"]/td[2]/text()'
xpath_business = '//*[@id="ctl00_PanelContent_ProfileID_firmProfile_ctl00_rowGeneralBusiness"]/td[2]/text()'
xpath_email = '//*[@id="ctl00_PanelContent_ProfileID_firmProfile_ctl00_rowContact2"]/td[2]/a/text()'
xpath_url = '//*[@id="ctl00_PanelContent_ProfileID_firmProfile_ctl00_FirmLink"]/text()'
xpath_contact = '//*[@id="ctl00_PanelContent_ProfileID_firmProfile_ctl00_rowContact1"]/td[2]/text()'

# Scrape company list
def capture( start, end, companyUrl, xpath ):
  temp = '"company","address 1","address 2","contact","email","phone","url","business type"'+'\n'
  for i in range( start, end ):
    #sleep(randint(1,2))
    page = requests.get(companyUrl + str(i))
    tree = html.fromstring(page.content)
    tree_path = []

    temp += '"'
    temp += clean(tree, xpath)
    temp += '","'
    temp += clean(tree, xpath_address_1)
    temp += '","'
    temp += clean(tree, xpath_address_2)
    temp += '","'
    temp += clean(tree, xpath_contact)
    temp += '","'
    temp += clean(tree, xpath_email)
    temp += '","'
    temp += clean(tree, xpath_phone)
    temp += '","'
    temp += clean(tree, xpath_url)
    temp += '","'
    temp += clean(tree, xpath_business)
    temp += '"'+'\n'
  return temp

def clean( url, path ):
  return str(url.xpath(path)).replace('[\'','').replace('\']','').replace('\\r\\n','').replace('                                \', \'                                ',', ').strip()

def check( tree_path ):
  if(tree_path != '[]'):
    print tree_path

start = 15000
end = 20000
tree = capture( start, end, companyUrl, xpath )
target = open('raw_cpa_data_' + str(start) + '_' + str(end) + '.csv', 'w')
target.write(tree)
