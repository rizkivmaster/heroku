__author__ = 'traveloka'

import time
import pprint
import datetime
import numpy as np

import urllib2
import xml.etree.ElementTree as ET
import logging

busContext = dict()
busState = dict()


class BusWayCoordinateFetcher:
    def __init__(self):
        pass

    def __get_session_key(self):
        req = urllib2.Request('http://smartcityjakarta.com/bustrack/')
        req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        req.add_header('Accept-Encoding','gzip, deflate')
        req.add_header('Accept-Language','en-US,en;q=0.5')
        req.add_header('Cache-Control','max-age=0')
        req.add_header('Connection','keep-alive')
        req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0')
        req.add_header('Host','smartcityjakarta.com')
        test = urllib2.urlopen(req)
        try:
            for value in test.info().values():
                if 'PHPSESSID' in value:
                    return value.split(";")[0]
        except Exception, e:
            logging.error(e)
        return None

    def request_buses(self):
        req = urllib2.Request('http://smartcityjakarta.com/bustrack/stadtbus_rapperswil.php')
        req.add_header('Accept','application/xml, text/xml, */*; q=0.01')
        req.add_header('Accept-Encoding','gzip, deflate')
        req.add_header('Connection','keep-alive')
        req.add_header('Accept-Language','en-US,en;q=0.5')
        req.add_header('Cache-Control','max-age=0')
        req.add_header('Connection','keep-alive')
        req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0')
        req.add_header('Host','smartcityjakarta.com')
        req.add_header('Referer','http://smartcityjakarta.com/bustrack/')
        req.add_header('X-Requested-With','XMLHttpRequest')
        session_key = self.__get_session_key()
        if session_key is None:
            logging.error('No session key found')
            return None
        req.add_header('Cookie',session_key)
        response = urllib2.urlopen(req)
        htmlfile = response.read()
        root = ET.fromstring(htmlfile)
        dix = dict()
        for bus in root[3]:
            dixx = dict()
            for node in bus:
                dixx[node.tag] = node.text
            identifier = dixx['identifier']
            dixx.pop('identifier')
            dix[identifier] = dixx
        return dix

