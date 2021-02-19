from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import numpy as np

my_data = np.genfromtxt('addresses.csv', dtype=str, delimiter=',', skip_header=1)
print("First Five Rows of the Data:\n", my_data[:3, :])

new_data = [['Constituent ID', 'Street #', 'Street Name', 'Real Estate Number']]

with open('properties.csv', 'w') as my_file:
    my_file.writelines('Constituent ID, Street #, Street Name, Real Estate Number \n')

for i, row in enumerate(my_data):
    rowValue = [row[0]]            # add Constituent ID
    csvValue = row[0] + ', '
    if row[1] == '' or len(row[1]) == 1 or row[1] == 'Box':    # if no address provided
        rowValue.append('')
        rowValue.append('')
        rowValue.append('')
        new_data.append(rowValue)
        csvValue += ' , , '
        with open('properties.csv', 'a') as my_file:
            my_file.writelines(csvValue)
            my_file.writelines('\n')
        continue
    else:                           # if address is provided
        rowValue.append(row[1])     # add street number
        rowValue.append(row[2])     # add street name
        csvValue += row[1] + ', '
        csvValue += row[2] + ', '
        browser = webdriver.Chrome('C:/WebDriver/bin/chromedriver')
        browser.get("https://paopropertysearch.coj.net/Basic/Search.aspx")

        number_search_input = browser.find_element_by_id('ctl00_cphBody_tbStreetNumber')
        number_search_input.send_keys(row[1])    # row[1] = street number
        street_search_input = browser.find_element_by_id('ctl00_cphBody_tbStreetName')
        street_search_input.send_keys(row[2])    # row[2] = street name

        search_button = browser.find_element_by_id('ctl00_cphBody_bSearch')
        search_button.click()

        try:
            text = "Detail.aspx"
            property_link = browser.find_element_by_xpath('//a[contains(@href, "%s")]' % text)
            property_link.click()
        except NoSuchElementException:
            rowValue.append('')
            new_data.append(rowValue)
            csvValue += ' ,'
            browser.close()
            with open('properties.csv', 'a') as my_file:
                my_file.writelines(csvValue)
                my_file.writelines('\n')
            continue

        real_estate_number = browser.find_element_by_id('ctl00_cphBody_lblRealEstateNumber')
        rowValue.append(real_estate_number.text)
        csvValue += real_estate_number.text + ', '

        new_data.append(rowValue)
        browser.close()
        with open('properties.csv', 'a') as my_file:
            my_file.writelines(csvValue)
            my_file.writelines('\n')

my_new_data = np.array(new_data)
print("First 10 Rows of the new Data:\n", my_new_data[:10, :])

np.savetxt("newAddresses.csv", my_new_data, delimiter=",")
