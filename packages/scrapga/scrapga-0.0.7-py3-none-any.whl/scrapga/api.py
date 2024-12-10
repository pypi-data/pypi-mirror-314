from __future__ import annotations

import time

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag


class GSMArena:

    def __init__(self, interval=10, ua="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0") -> None:

        self.home = "https://www.gsmarena.com"
        self.session = requests.Session()
        self.referrer = self.home
        self.interval = interval
        self.ua = ua

    def _request(self, uri=None) -> str:

        url = f"{self.home}/{uri}"

        response = self.session.get(
            url=url,
            headers={
                "Referrer": self.referrer,
                "user-agent": self.ua,
            },
        )

        self.referrer = url

        return response.text
    
    def _get_text(self, node:Tag) -> (str|None):

        if node:
            return node.get_text().replace("\n", "")
        else:
            return None

    def get_brands(self) -> list:

        html = BeautifulSoup(
            markup=self._request(uri="makers.php3"), features="html.parser"
        )
        brand_node = html.select("table td a")

        brands = []
        for el in brand_node:
            brand = self._get_text(node=el.select_one("span")).replace("\n", "")
            brands.append(
                {
                    "id": el.attrs["href"].replace(".php", ""),
                    "name": self._get_text(node=el).replace(brand, ""),
                    "num": int(brand.replace(" devices", "")),
                }
            )

        return brands

    def _get_next(self, html: BeautifulSoup) -> str:

        next = html.select_one('a.prevnextbutton[title="Next page"]')

        if next:
            return next.attrs["href"].replace(".php", "")
        else:
            return None

    def get_devices(self, brand) -> list:

        page = brand

        devices = []
        while True:

            html = BeautifulSoup(
                markup=self._request(uri=f"{page}.php"), features="html.parser"
            )

            device_node = html.select(".makers li")
            for el in device_node:
                img = el.select_one("img")
                devices.append(
                    {
                        "id": el.select_one("a").attrs["href"].replace(".php", ""),
                        "name": self._get_text(node=el.select_one("span")).replace("\n", ""),
                        "img": img.attrs["src"],
                        "desc": img.attrs["title"],
                    }
                )

            page = self._get_next(html)
            if page != None:
                time.sleep(self.interval)
                continue
            else:
                break

        return devices

    def get_details(self, device) -> dict:

        html = BeautifulSoup(
            markup=self._request(uri=f"{device}.php"), features="html.parser"
        )

        model_name = (
            self._get_text(node=html.select_one(".specs-phone-name-title")).replace("\n", "")
        )

        try:
            img = html.select_one(".specs-photo-main a img").attrs["src"]
        except Exception as e:
            img = None

        feature = {
            "released": self._get_text(html.select_one('span[data-spec="released-hl"]')),
            "body": self._get_text(html.select_one('span[data-spec="body-hl"]')),
            "os": self._get_text(html.select_one('span[data-spec="os-hl"]')),
            "storage": self._get_text(html.select_one('span[data-spec="storage-hl"]')),
            "display_size": self._get_text(html.select_one('span[data-spec="displaysize-hl"]')),
            "display_resolution": self._get_text(html.select_one('div[data-spec="displayres-hl"]')),
            "camera": self._get_text(html.select_one(".accent-camera")),
            "video": self._get_text(html.select_one('div[data-spec="videopixels-hl"]')),
            "ram": self._get_text(html.select_one(".accent-expansion")),
            "chipset": self._get_text(html.select_one('div[data-spec="chipset-hl"]')),
            "battery_size": self._get_text(html.select_one(".accent-battery")),
            "battery_type": self._get_text(html.select_one('div[data-spec="battype-hl"]')),
        }

        spec = {}
        spec_node = html.select("table")
        for els in spec_node:
            title = self._get_text(els.select_one("th"))
            values = {}
            value_node = els.select("tr")
            for elv in value_node:
                key = self._get_text(elv.select_one("td.ttl"))
                if key:
                    values[self._get_text(elv.select_one("td.ttl"))] = self._get_text(elv.select_one("td.nfo"))
            spec[title] = values

        return {"model_name": model_name, "img": img, "feature": feature, "spec": spec}
