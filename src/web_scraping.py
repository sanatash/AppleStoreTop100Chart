"""
Web Scraping by BeautifulSoup and lxml.etree
"""
import os
from bs4 import BeautifulSoup
from lxml import etree
import json
from web_request import *

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

top_100_appl_list = []

def update_app_type(dict):
    """
    Updates new field appType. It sets if its Tv App or Music App or Game App or Other.
    And sets Other type. First set default value to new field.
    :param dict: application dictionary of attributes
    :type dict: dict
    :return:
    :rtype:
    """
    tv_app_value = {"TV App": "No", "Music App": "No", "Game App": "No",
                    "Other": {"Other App": "No", "type": ""}}

    dict["appType"] = tv_app_value

    if "TV" in dict["description"] and dict["category"] == "Entertainment":
        dict["appType"]["TV App"] = "Yes"
    elif dict["category"] == "Music":
        dict["appType"]["Music App"] = "Yes"
    elif dict["category"] == "Games":
        dict["appType"]["Game App"] = "Yes"
    else:
        dict["appType"]["Other"]["Other App"] = "Yes"
        dict["appType"]["Other"]["type"] = dict["category"]

def app_json_dict_update(dict, name, rank, id, category, age_limit):
    """
    Adds the missing fields to dictionary received from json file of application
    :param dict: application dictionary of attributes
    :type dict: dict
    :param name: application name
    :type name: str
    :param rank: application rank
    :type rank: int
    :param id: application id
    :type id: int
    :param category: application category
    :type category: str
    :param agg_limit: application agg limit
    :type agg_limit: str
    :return:
    :rtype:
    """
    dict[" ApplicationName"] = name
    dict["rank"] = rank
    dict["applicationId"] = id
    dict["category"] = category
    dict["ageLimit"] = age_limit
    if dict["ageLimit"] == "4+":
        dict["kidsFriendly"] = "Yes"
    else:
        dict["kidsFriendly"] = "No"

    update_app_type(dict)

def get_app_age_limit(dom):
    """
    Scraps age_limit of the application
    :param dom: HTML tree
    :type dom: lxml.etree._Element
    :return: application age_limit data
    :rtype: str
    """
    app_age_limit_element = dom.xpath('//span[@class="badge badge--product-title"]/text()')
    app_age_limit = app_age_limit_element[0].strip()
    return app_age_limit


def get_app_category(dom):
    """
    Scraps category of the application
    :param dom: HTML tree
    :type dom: lxml.etree._Element
    :return: application category
    :rtype: str
    """
    app_category_element = dom.xpath('//dd[@class="information-list__item__definition"]/a/text()')
    app_category = app_category_element[0].strip()
    return app_category


def get_app_id(dom):
    """
    Scraps application id.
    :param dom: HTML tree
    :type dom: lxml.etree._Element
    :return: application id
    :rtype: str
    """
    app_id_element = dom.xpath('//meta[@name = "apple:content_id"]/@content')
    app_id = app_id_element[0]
    return app_id


def get_app_json(dom):
    """
    Scraps application json file and returns its in the form of dictionary
    :param dom: HTML tree
    :type dom: lxml.etree._Element
    :return: application json file in form of dictionary
    :rtype: dict
    """
    app_json_element = dom.xpath('//script[@name = "schema:software-application"]/text()')
    app_json_dict = json.loads(app_json_element[0].strip())
    return app_json_dict


def app_json_dict_clean(dict):
    """
    Cleans unnecessary field from the application dict json data
    :param dict: dictionary of json application data
    :type dict: dict
    :return:
    :rtype:
    """
    dict.pop("screenshot", None)
    dict.pop("offers", None)
    dict.pop("image", None)
    dict.pop("@type", None)
    dict.pop("@context", None)
    dict["aggregateRating"].pop("@type", None)
    dict["author"].pop("@type", None)
    dict["author"].pop("url", None)

def get_app_name(dom):
    """
     Scraps application name.
     :param dom: HTML tree
     :type dom: lxml.etree._Element
     :return: application name
     :rtype: str
     """
    app_name_element = dom.xpath('//h1[@class="product-header__title app-header__title"]/text()')
    app_name = app_name_element[0].strip()
    return app_name

def app_page_scraping(page, rank):
    """
    Scraps application page by help of BeautifulSoup and lxml.etree libraries
    :param page: html page of application
    :type page: str
    :param rank: rank of application as received from main page
    :type rank: int
    :return:
    :rtype:
    """
    app_soup = BeautifulSoup(page, "lxml")
    app_dom = etree.HTML(str(app_soup))
    app_name = get_app_name(app_dom)
    app_age_limit = get_app_age_limit(app_dom)
    app_category = get_app_category(app_dom)
    app_id = get_app_id(app_dom)
    app_json_dict = get_app_json(app_dom)
    print(f"{rank}.{app_name}")
    app_json_dict_clean(app_json_dict)
    app_json_dict_update(app_json_dict, app_name, rank, int(app_id), app_category, app_age_limit)
    top_100_appl_list.append(app_json_dict)


def get_chart_list_name(soup):
    """
    Extracts chart list name by help of BeautifulSoup library
    :param soup: object of BeautifulSoup library used for scraping of html pages
    :type soup: BeautifulSoup object
    :return: chart list name
    :rtype: str
    """
    return soup.find('h2').get_text().strip()


def get_appl_rank(list_item):
    """
    Scraps application rank from list item (in html file)
    :param list_item: list item li (in html applications list)
    :type list_item: bs4.element.Tag
    :return: rank of application
    :rtype: int
    """
    return list_item.find('p').get_text()


def get_app_url(list_item):
    """
    Scraps url of application
    :param list_item: list item li (in html applications list)
    :type list_item: bs4.element.Tag
    :return: url of application
    :rtype: str
    """
    a = list_item.find('a', href=True)
    app_url = a['href']
    return app_url


def list_of_applications_scraping(soup):
    """
    Goes over all links to all application found in this list
    and scraps data from everyone of it.
    :param soup: object of BeautifulSoup library used for scraping of html pages
    :type soup: BeautifulSoup object
    :return:
    :rtype:
    """
    app_list = soup.find('ol')

    # finding all li (list item)  tags in ol (ordered list) tag
    for li in app_list.find_all("li"):
        app_rank = get_appl_rank(li)
        app_url = get_app_url(li)
        response = web_get_url(app_url)
        app_page = response.text
        app_page_scraping(app_page, app_rank)

def main_chart_list_scraping(html_page):
    """
    Scraps data from the main application chart html page.
    Scraps chart list name. Scraps list of all applications.
    :param html_page: html page of main chart list of applications
    :type page: str
    :return:
    :rtype:
    """
    soup = BeautifulSoup(html_page, 'html.parser')

    chart_list_name = get_chart_list_name(soup)
    list_of_applications_scraping(soup)

    return chart_list_name


def read_input_file():
    """
    Read url string from input file found in /input/chart_url.txt file in project directory
    :return: url of page which should be scraped for top chart list of applications
    :rtype: str
    """
    with open(f"{project_root}/input/chart_url.txt", "r") as infile:
        url = infile.read().strip()
        return url


def write_output_file(file_name):
    """
    Write to top_100_appl_list global variable of type list into the json file
    with name given as input parameter to the function. The json file will be found
    in output directory of the project
    :param file_name: file name of json file to write
    :type file_name: str
    :return:
    :rtype:
    """
    with open(f"{project_root}/output/{file_name}.json", "w") as outfile:
        json.dump(top_100_appl_list, outfile)


def get_json_output_file_name(chart_list_name):
    """
    Construct the json file name from chart list name string
    :param chart_list_name: chart list name scraped from the url
    :type chart_list_name: str
    :return: json file name
    :rtype: str
    """
    json_file_name = '_'.join(chart_list_name.lower().split())
    return json_file_name


def web_get_chart_list():
    """
    Main function that takes url to top free applications chart list and returns
    info about these application in format of json file.
    It reads url from /input/chart_url.txt file found in project directory.
    It writes data about applications scraped from input url into the json file
    into the directory output found in project directory. Name of output json file is similar to name of chart list.
    :return:
    :rtype:
    """
    global top_100_appl_list
    url = read_input_file()
    if "apps.apple.com/us/charts" not in url:
        raise Exception("Not valid input url! Should be one of 'apps.apple.com/us/charts' urls.")

    response = web_get_url(url)
    page = response.text
    chart_list_name = main_chart_list_scraping(page)
    json_file_name = get_json_output_file_name(chart_list_name)
    write_output_file(json_file_name)


if __name__ == '__main__':
    web_get_chart_list()
