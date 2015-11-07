from app.meloentjoer.accessors.entity.BusRoute import BusRoute
from app.meloentjoer.fetcher.entity.BusTrackData import BusTrackData

__author__ = 'traveloka'

from app.meloentjoer.common.logging import logger as __logger
import urllib2
import xml.etree.ElementTree as Et

from bs4 import BeautifulSoup
from app.meloentjoer.common.util.LinkedHash import LinkedHash
import re


def scrap(link):
    """
    :type link: str
    :param link: string
    :return:
    """
    html = urllib2.urlopen(link)
    scrapper = BeautifulSoup(html, 'html.parser')
    return scrapper


def row_parser(text):
    innertext = re.findall('[a-zA-Z0-9 ]+[a-zA-Z0-9]', text)
    if not len(innertext) == 0:
        return re.sub('[^a-zA-Z0-9 ]+', '', innertext[0]).strip()
    else:
        return ''


def multi_row_parser(text):
    text_lines = text.split('\n')
    return_line = []
    for line in text_lines:
        inner_text = re.findall('[a-zA-Z0-9 ]+[a-zA-Z0-9]', line)
        if not len(inner_text) == 0:
            return_line.append(re.sub('[^a-zA-Z0-9 ]+', '', inner_text[0]))
        else:
            return ''
    return ','.join(return_line)


def multi_href_parser(element):
    buffers = []
    return_lists = set()
    return_maps = dict()
    items = element.find_all('a')
    for item in items:
        if item.name == 'a':
            if item.has_attr('class') and item['class'][0] == 'image':
                buffers.append(item['title'])
            else:
                for a_buffer in buffers:
                    return_lists.add(a_buffer + '_' + str(item.getText()))
                    return_maps[a_buffer + '_' + str(item.getText())] = (a_buffer, str(item.getText()))
                buffers = []
        if item.next_sibling is not None:
            if item.next_sibling.string is not None:
                if not item.next_sibling.strip() == '':
                    for a_buffer in buffers:
                        return_lists.add(a_buffer + '_' + str(item.next_sibling).strip())
                        value = (a_buffer, str(item.next_sibling).strip())
                        return_maps[a_buffer + '_' + str(item.next_sibling).strip()] = value

                    buffers = []
    return return_lists, return_maps


def get_busway_routes():
    """
    scrape the routes


    :rtype list[BusRoute]
    """
    routes_list = []
    try:
        scrapper = scrap("https://en.wikipedia.org/wiki/TransJakarta_Corridors")
        main_content = scrapper.find('div', attrs={'id': 'mw-content-text'})
        tables = main_content.find_all('table', {'class': 'wikitable'})
        for table in tables:
            route = BusRoute()
            rows = table.find_all('tr')
            corridor_name = rows[0].find('th').find('a')['title']
            new_rows = rows[2:]
            station_list = []
            for row in new_rows:
                station_name = row_parser(row.find_all('td')[1].getText())
                station_list.append(station_name)
            route.stations = station_list
            route.corridor_name = corridor_name
            routes_list.append(route)
    except Exception, e:
        __logger.error(e.message)
    return routes_list


def get_train_routes():
    train_scrapper = scrap(
        'https://en.wikipedia.org/w/index.php?title=KA_Commuter_Jabodetabek&oldid=683328854')
    raw_tables = train_scrapper.select('dl > dd > b')
    routes_table = dict()
    for table in raw_tables:
        line_name = \
            re.findall('[a-zA-Z0-9 ]+[a-zA-Z0-9]', table.parent.parent.previousSibling.previousSibling.string)[
                0].strip()
        station_list = LinkedHash(
            map(lambda x: x.strip(), re.sub(u'\u2192', ',', re.sub('\\.', '', table.parent.getText())).split(',')))
        routes_table[line_name] = station_list
    return routes_table


def get_session_key():
    req = urllib2.Request('http://smartcityjakarta.com/bustrack/')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    req.add_header('Accept-Encoding', 'gzip, deflate')
    req.add_header('Accept-Language', 'en-US,en;q=0.5')
    req.add_header('Cache-Control', 'max-age=0')
    req.add_header('Connection', 'keep-alive')
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0')
    req.add_header('Host', 'smartcityjakarta.com')
    test = urllib2.urlopen(req)
    try:
        for value in test.info().values():
            if 'PHPSESSID' in value:
                return value.split(";")[0]
    except Exception, e:
        __logger.error(e)
    return None


def request_buses():
    """
    :rtype dict[str,BusTrackData]
    :return:
    """
    req = urllib2.Request('http://smartcityjakarta.com/bustrack/stadtbus_rapperswil.php')
    req.add_header('Accept', 'application/xml, text/xml, */*; q=0.01')
    req.add_header('Accept-Encoding', 'gzip, deflate')
    req.add_header('Connection', 'keep-alive')
    req.add_header('Accept-Language', 'en-US,en;q=0.5')
    req.add_header('Cache-Control', 'max-age=0')
    req.add_header('Connection', 'keep-alive')
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0')
    req.add_header('Host', 'smartcityjakarta.com')
    req.add_header('Referer', 'http://smartcityjakarta.com/bustrack/')
    req.add_header('X-Requested-With', 'XMLHttpRequest')
    session_key = get_session_key()
    if session_key is None:
        __logger.error('No session key found')
        return None
    req.add_header('Cookie', session_key)
    response = urllib2.urlopen(req)
    htmlfile = response.read()
    root = Et.fromstring(htmlfile)
    dix = dict()
    for bus in root[3]:
        dixx = dict()
        for node in bus:
            dixx[node.tag] = node.text
        bus_track_data = BusTrackData()
        bus_track_data.name = dixx['identifier']
        bus_track_data.longitude = float(dixx['lon'])
        bus_track_data.latitude = float(dixx['lat'])
        bus_track_data.speed = float(dixx['speedKmh'])
        dix[bus_track_data.name] = bus_track_data
    return dix
