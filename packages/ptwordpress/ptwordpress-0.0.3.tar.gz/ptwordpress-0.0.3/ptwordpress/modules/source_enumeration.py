import requests
from ptlibs import ptprinthelper

class SourceEnumeration:
    def __init__(self, rest_url, args, ptjsonlib):
        self.REST_URL = rest_url
        self.BASE_URL = rest_url.split("/wp-json")[0]
        self.args = args
        self.ptjsonlib = ptjsonlib

    def run(self):
        self.find_xmlrpc()
        self.find_robots_txt()

    def find_xmlrpc(self):
        response = requests.get(f"{self.BASE_URL}/xmlrpc.php")
        ptprinthelper.ptprint(f"XMPLRPC:", "TITLE", condition=not self.args.json, colortext=True, newline_above=True)

        if response.status_code == 200:
            ptprinthelper.ptprint(f"found: {self.BASE_URL}/xmlrpc.php", "TEXT", condition=not self.args.json, colortext=True, indent=4)
        else:
            ptprinthelper.ptprint(f"not found", "TEXT", condition=not self.args.json, colortext=False, indent=4)

    def find_robots_txt(self):
        response = requests.get(f"{self.BASE_URL}/robots.txt")
        if response.status_code == 200:
            ptprinthelper.ptprint(f"Robots.txt:", "TITLE", condition=not self.args.json, colortext=True, newline_above=True)
            for line in response.text.splitlines():
                ptprinthelper.ptprint(line, "TEXT", condition=not self.args.json, colortext=False, indent=4)
