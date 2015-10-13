__author__ = 'traveloka'

from bs4 import BeautifulSoup
import urllib2
import re
import logging


class BusWayFetcher:
    def __init__(self):
        pass

    def __scrap(self, link):
        html = urllib2.urlopen(link)
        scrapper = BeautifulSoup(html,'html.parser')
        return scrapper

    def __row_parser(self,text):
        innertext = re.findall('[a-zA-Z0-9 ]+[a-zA-Z0-9]', text)
        if not len(innertext) == 0:
            return re.sub('[^a-zA-Z0-9 ]+', '', innertext[0]).strip()
        else:
            return ''

    def __multi_row_parser(self, text):
        text_lines = text.split('\n')
        return_line = []
        for line in text_lines:
            inner_text = re.findall('[a-zA-Z0-9 ]+[a-zA-Z0-9]', line)
            if not len(inner_text) == 0:
                return_line.append(re.sub('[^a-zA-Z0-9 ]+', '', inner_text[0]))
            else:
                return ''
        return ','.join(return_line)

    def __multi_href_parser(self, element):
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
                        return_lists.add(a_buffer+'_'+str(item.getText()))
                        return_maps[a_buffer+'_'+str(item.getText())] = (a_buffer, str(item.getText()))
                    buffers = []
            if item.next_sibling is not None:
                if item.next_sibling.string is not None:
                    if not item.next_sibling.strip() == '':
                        for a_buffer in buffers:
                            return_lists.add(a_buffer+'_'+str(item.next_sibling).strip())
                            return_maps[a_buffer+'_'+str(item.next_sibling).strip()] = (a_buffer, str(item.next_sibling).strip())
                        buffers = []
        return return_lists,return_maps

    # return dict( corridor Names (string) -> list of Station Names (string) )
    def get_routes(self):
        routes_table = dict()
        try:
            scrapper = self.__scrap("https://en.wikipedia.org/wiki/TransJakarta_Corridors")
            main_content = scrapper.find('div', attrs={'id':'mw-content-text'})
            tables = main_content.find_all('table', {'class': 'wikitable'})
            logging.info("Fetching bus way routes")
            for table in tables:
                rows = table.find_all('tr')
                corridor_name = rows[0].find('th').find('a')['title']
                new_rows = rows[2:]
                station_list = []
                for row in new_rows:
                    station_name = self.__row_parser(row.find_all('td')[1].getText())
                    station_list.append(station_name)
                routes_table[corridor_name] = station_list
            logging.info("Finished fetching bus way routes")
        except Exception, e:
            logging.error(e.message)
        return routes_table