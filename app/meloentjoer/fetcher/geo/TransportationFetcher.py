from app.meloentjoer.accessors.bus_routes.BusRoute import BusRoute
from app.meloentjoer.accessors.bus_routes.BusRouteAccessor import BusRouteAccessor
from app.meloentjoer.common.behavioral.Startable import Startable
from app.meloentjoer.common.executors.SchedulerExecutor import SchedulerExecutor
from app.meloentjoer.config.GeneralConfig import GeneralConfig

__author__ = 'traveloka'

import urllib2
import logging

from bs4 import BeautifulSoup
from app.meloentjoer.common.util.LinkedHash import LinkedHash
import re


class TransportationFetcher(Startable):
    def __update(self):
        route_list = self.get_busway_routes()
        for route in route_list:
            self.bus_route_accessor.upset_bus_route(route)

    def __init__(self,
                 executor,
                 bus_route_accessor,
                 general_config
                 ):
        """
        :type bus_route_accessor: BusRouteAccessor
        :type general_config: GeneralConfig
        :param bus_route_accessor:
        :return:
        """
        update_period = general_config.get_geo_refresh_period()
        self.scheduler = SchedulerExecutor(executor, update_period, self.__update)
        self.bus_route_accessor = bus_route_accessor

    def __scrap(self, link):
        html = urllib2.urlopen(link)
        scrapper = BeautifulSoup(html, 'html.parser')
        return scrapper

    def scrap(self, link):
        """
        :type link: str
        :param link: string
        :return:
        """
        html = urllib2.urlopen(link)
        scrapper = BeautifulSoup(html, 'html.parser')
        return scrapper

    def __row_parser(self, text):
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

    def get_busway_routes(self):
        """
        scrape the routes


        :rtype list[BusRoute]
        """
        routes_list = []
        try:
            scrapper = self.__scrap("https://en.wikipedia.org/wiki/TransJakarta_Corridors")
            main_content = scrapper.find('div', attrs={'id': 'mw-content-text'})
            tables = main_content.find_all('table', {'class': 'wikitable'})
            logging.info("Fetching bus way routes")
            for table in tables:
                route = BusRoute()
                rows = table.find_all('tr')
                corridor_name = rows[0].find('th').find('a')['title']
                new_rows = rows[2:]
                station_list = []
                for row in new_rows:
                    station_name = self.__row_parser(row.find_all('td')[1].getText())
                    station_list.append(station_name)
                route.stations = station_list
                route.corridor_name = corridor_name
                routes_list.append(route)
            logging.info("Finished fetching bus way routes")

        except Exception, e:
            logging.error(e.message)
        return routes_list

    def get_train_routes(self):
        train_scrapper = self.__scrap(
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

    def start(self):
        self.scheduler.start()

    def stop(self):
        self.scheduler.stop()
