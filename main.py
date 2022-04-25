from selenium import webdriver
from imotbg_search import ImotBgSearch

DRIVER = webdriver.Chrome(executable_path="/Users/aleksandarm/Desktop/selenium_dev/chromedriver")
GOOGLE_FORM_URL = 'https://forms.gle/u8Ej9kG7wfsDAFDr9'
URL = 'https://imot.bg'

imot_bot = ImotBgSearch(DRIVER, URL, GOOGLE_FORM_URL)
properties_dictionary = imot_bot.create_properties_dictionary()
imot_bot.login_to_google()

for n in range(1):
    imot_bot.fill_google_form(properties_dictionary[f"Property {n + 1}"]["address"],
                              properties_dictionary[f"Property {n + 1}"]["price"],
                              properties_dictionary[f"Property {n + 1}"]["url"])
imot_bot.create_the_table()


