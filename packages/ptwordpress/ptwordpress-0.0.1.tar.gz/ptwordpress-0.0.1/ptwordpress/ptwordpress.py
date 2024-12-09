#!/usr/bin/python3
"""
    Copyright (c) 2024 Penterep Security s.r.o.

    ptwordpress - Wordpress API tester

    ptwordpress is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    ptwordpress is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with ptwordpress.  If not, see <https://www.gnu.org/licenses/>.
"""

import argparse
import re
import csv
import os
import sys; sys.path.append(__file__.rsplit("/", 1)[0])
import urllib
import socket
import json

import requests

from _version import __version__
from ptlibs import ptjsonlib, ptprinthelper, ptmisclib, ptnethelper, ptnethelper
from ptlibs.threads import ptthreads

from copy import deepcopy
from collections import OrderedDict

from modules.user_enumeration import UserEnumeration
from modules.source_enumeration import SourceEnumeration

import defusedxml.ElementTree as ET

from bs4 import BeautifulSoup

class PtWordpress:
    def __init__(self, args):
        self.ptjsonlib = ptjsonlib.PtJsonLib()
        self.ptthreads   = ptthreads.PtThreads()
        self.args = args
        self.routes_and_status_codes = []
        self.hide_bloat = True
        self.REST_URL = self.get_wp_json_url(args.url)
        self.BASE_URL = self.REST_URL.split("/wp-json")[0]

    def run(self, args) -> None:
        """Main method"""
        ptprinthelper.ptprint(f"Target: {args.url}", "TITLE", condition=not self.args.json, colortext=True)
        response = self._check_if_site_running_wordpress(args.url)

        ptprinthelper.ptprint(f"Target Headers:", "TITLE", condition=not self.args.json, colortext=True, newline_above=True)
        for header, value in response.raw.headers.items():
            ptprinthelper.ptprint(f"{header}: {value}", "TEXT", condition=not self.args.json, colortext=False, indent=4)

        self._process_meta_tags()
        self._scrape_themes()
        self.parse_info_from_wp_json(response.json())

        SourceEnumeration(self.REST_URL, args, self.ptjsonlib).run()
        self._scrape_feed()
        UserEnumeration(self.REST_URL, args, self.ptjsonlib).enumerate_users()

        # TODO: Scan all routes, check for routes that are not auth protected (not 401)

        self.ptjsonlib.set_status("finished")
        ptprinthelper.ptprint(self.ptjsonlib.get_result_json(), "", self.args.json)

    def _scrape_themes(self):
        ptprinthelper.ptprint(f"Theme discovery: ", "TITLE", condition=not self.args.json, colortext=True, newline_above=True)
        html_content = requests.get(f"{self.BASE_URL}").text
        soup = BeautifulSoup(html_content, 'lxml')
        theme_pattern = re.compile(r'(https?://[^/]+/wp-content/themes/[^/]+)')
        themes = set()
        # Iterate over all tags
        for tag in soup.find_all(True):  # True finds all tags
            # Iterate over all attributes of the tag
            for attr, value in tag.attrs.items():
                if value and 'themes/' in value:
                    #print(f"Full URL: {value}")
                    match = theme_pattern.search(value)
                    if match:
                        full_url_until_segment = match.group(1)  # URL up to the segment
                        remaining_part = value[len(full_url_until_segment):]  # Part after the segment
                        theme_name = full_url_until_segment.rsplit("/", 1)[-1]
                        if theme_name not in themes:
                            themes.add(theme_name)
                            ptprinthelper.ptprint(f"{theme_name}", "TEXT", condition=not self.args.json, indent=4)


    def _scrape_feed(self):
        ptprinthelper.ptprint(f"RSS feed users:", "TITLE", condition=not self.args.json, colortext=True, newline_above=True)

        rss_authors = set()
        response = requests.get(f"{self.BASE_URL}/feed")
        if response.status_code == 200:
            root = ET.fromstring(response.text.strip())
            # Define the namespace dictionary
            namespaces = {'dc': 'http://purl.org/dc/elements/1.1/'}
            # Find all dc:creator elements and print their text
            creators = root.findall('.//dc:creator', namespaces)
            for creator in creators:
                creator = creator.text.strip()
                if creator not in rss_authors:
                    rss_authors.add(creator)
                    ptprinthelper.ptprint(f"{creator}", "TEXT", condition=not self.args.json, colortext=False, indent=4)
        else:
            ptprinthelper.ptprint(f"Feed not found", "TEXT", condition=not self.args.json, indent=4)


    def _process_meta_tags(self):
        ptprinthelper.ptprint(f"Meta tags:", "TITLE", condition=not self.args.json, colortext=True, newline_above=True)
        html_content = requests.get(self.BASE_URL).text
        soup = BeautifulSoup(html_content, 'lxml')
        # Find all meta tags with name="generator"
        tags = soup.find_all('meta', attrs={'name': 'generator'})
        if tags:
            for tag in tags:
                ptprinthelper.ptprint(f"{tag.get('content')}", "TEXT", condition=not self.args.json, colortext=False, indent=4)
        else:
            ptprinthelper.ptprint(f"Found none", "TEXT", condition=not self.args.json, colortext=False, indent=4)


    def parse_routes_into_nodes(self, url: str) -> list:
        rest_url = self.get_wp_json_url(url)
        routes_to_test = []

        json_response = self.get_wp_json_response(url)
        for route in json_response["routes"].keys():
            nodes_to_add = []
            main = self.ptjsonlib.create_node_object(node_type="endpoint", properties={"url": url + route})
            routes_to_test.append({"id": main["key"], "url": url + route})

            nodes_to_add.append(main)
            for endpoint in json_response["routes"][route]["endpoints"]:
                endpoint_method = self.ptjsonlib.create_node_object(parent=main["key"], parent_type="endpoint", node_type="method", properties={"name": endpoint["methods"]})
                nodes_to_add.append(endpoint_method)

                if endpoint.get("args"):
                    for parameter in endpoint["args"].keys():
                        nodes_to_add.append(self.ptjsonlib.create_node_object(parent=endpoint_method["key"], parent_type="method", node_type="parameter", properties={"name": parameter, "type": endpoint["args"][parameter].get("type"), "description": endpoint["args"][parameter].get("description"), "required": endpoint["args"][parameter].get("required")}))

            self.ptjsonlib.add_nodes(nodes_to_add)

        return routes_to_test

    def update_status_code_in_nodes(self):
        if self.use_json:
            for dict_ in self.routes_and_status_codes:
                for node in self.ptjsonlib.json_object["results"]["nodes"]:
                    if node["key"] == dict_["id"]:
                        node["properties"].update({"status_code": dict_["status_code"]})

    def parse_info_from_wp_json(self, wp_json: dict):
        """
        Collects and stores basic information about the target from wp-json
        """

        ptprinthelper.ptprint(f"Site info:", "TITLE", condition=not self.args.json, colortext=True, newline_above=True)

        site_description = wp_json.get("description", "")
        site_name = wp_json.get("name", "")
        site_home = wp_json.get("home", "")
        site_gmt = wp_json.get("gmt_offset", "")
        site_timezone = wp_json.get("timezone_string", "")
        _timezone =  f"{str(site_timezone)} (GMT{'+' if not '-' in str(site_gmt) else '-'}{str(site_gmt)})" if site_timezone else ""

        ptprinthelper.ptprint(f"Name: {site_name}", "TEXT", condition=not self.args.json, indent=4)
        ptprinthelper.ptprint(f"Description: {site_description}", "TEXT", condition=not self.args.json, indent=4)
        ptprinthelper.ptprint(f"Home: {site_home}", "TEXT", condition=not self.args.json, indent=4)
        ptprinthelper.ptprint(f"Timezone: {_timezone}", "TEXT", condition=not self.args.json, indent=4)

        authentication = wp_json.get("authentication", [])
        if authentication:
            ptprinthelper.ptprint(f"Authentication:", "TITLE", condition=not self.args.json, colortext=True)
            for auth in authentication:
                ptprinthelper.ptprint(f"{auth}", "TEXT", condition=not self.args.json, indent=4)


        namespaces = wp_json.get("namespaces", [])
        with open(os.path.join("modules", "plugin_list.csv"), mode='r') as file:
            csv_reader = csv.reader(file)
            csv_data = list(csv_reader)

        if "wp/v2" in namespaces: # wp/v2 is prerequirement
            #has_v2 = True
            ptprinthelper.ptprint(f"Namespaces (API provided by addons):", "TITLE", condition=not self.args.json, colortext=True, newline_above=True)
            for namespace in namespaces:
                namespace_description = self.find_description_in_csv(csv_data, namespace)
                ptprinthelper.ptprint(f"{namespace} {namespace_description}", "TEXT", condition=not self.args.json, indent=4)
        return

    def get_wp_json_url(self, url: str) -> None:
        parsed_url = urllib.parse.urlparse(url)
        return urllib.parse.urlunparse((parsed_url.scheme, parsed_url.netloc, 'wp-json', '', '', ''))

    def _check_if_site_running_wordpress(self, url):
        """Try to retrieve content of /wp-json"""
        parsed_url = urllib.parse.urlparse(url)
        parsed_url = parsed_url._replace(path="/wp-json")
        url = urllib.parse.urlunparse(parsed_url)
        response = ptmisclib.load_url_from_web_or_temp(url, "GET", headers=self.args.headers, proxies=self.args.proxy, data=None, timeout=None, redirects=True, verify=False, cache=self.args.cache)
        try:
            _response_json = response.json()
            return response
        except Exception as e:
            self.ptjsonlib.end_error(f"Not a wordpress site", self.args.json)

    def find_description_in_csv(self, csv_data, text: str):
        # Iterate over the rows in the CSV file
        for row in csv_data:
            if row[0] == text:
                if row[2]:
                    return f"- {row[1]} ({row[2]})"
                else:
                    return f"- {row[1]}"
        return ""

def get_help():
    return [
        {"description": ["Wordpress Security Testing Tool"]},
        {"usage": ["ptwordpress <options>"]},
        {"usage_example": [
            "ptwordpress -u https://www.example.com",
        ]},
        {"options": [
            ["-u",  "--url",                    "<url>",            "Connect to URL"],
            ["-p",  "--proxy",                  "<proxy>",          "Set Proxy"],
            ["-T",  "--timeout",                "",                 "Set Timeout"],
            ["-c",  "--cookie",                 "<cookie>",         "Set Cookie"],
            ["-a", "--user-agent",              "<a>",              "Set User-Agent"],
            ["-H",  "--headers",                "<header:value>",   "Set Header(s)"],
            ["-r",  "--redirects",              "",                 "Follow redirects (default False)"],
            ["-C",  "--cache",                  "",                 "Cache HTTP communication"],
            ["-v",  "--version",                "",                 "Show script version and exit"],
            ["-h",  "--help",                   "",                 "Show this help message and exit"],
            ["-j",  "--json",                   "",                 "Output in JSON format"],
        ]
        }]


def parse_args():
    parser = argparse.ArgumentParser(add_help="False", description=f"{SCRIPTNAME} <options>")
    parser.add_argument("-u",  "--url",              type=str, required=True)
    parser.add_argument("-p",  "--proxy",            type=str)
    parser.add_argument("-T",  "--timeout",          type=int, default=10)
    parser.add_argument("-t",  "--threads",          type=int, default=100)
    parser.add_argument("-a",  "--user-agent",       type=str, default="Penterep Tools")
    parser.add_argument("-c",  "--cookie",           type=str)
    parser.add_argument("-H",  "--headers",          type=ptmisclib.pairs, nargs="+")
    parser.add_argument("-r",  "--redirects",        action="store_true")
    parser.add_argument("-C",  "--cache",            action="store_true")
    parser.add_argument("-j",  "--json",             action="store_true")
    parser.add_argument("-v",  "--version",          action='version', version=f'{SCRIPTNAME} {__version__}')

    parser.add_argument("--socket-address",          type=str, default=None)
    parser.add_argument("--socket-port",             type=str, default=None)
    parser.add_argument("--process-ident",           type=str, default=None)


    if len(sys.argv) == 1 or "-h" in sys.argv or "--help" in sys.argv:
        ptprinthelper.help_print(get_help(), SCRIPTNAME, __version__)
        sys.exit(0)

    args = parser.parse_args()
    args.timeout = args.timeout if not args.proxy else None
    args.proxy = {"http": args.proxy, "https": args.proxy} if args.proxy else None
    args.user_agent  = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36"
    args.headers = ptnethelper.get_request_headers(args)

    ptprinthelper.print_banner(SCRIPTNAME, __version__, args.json)
    return args


def main():
    global SCRIPTNAME
    SCRIPTNAME = "ptwordpress"
    requests.packages.urllib3.disable_warnings()
    args = parse_args()
    script = PtWordpress(args)
    script.run(args)


if __name__ == "__main__":
    main()
