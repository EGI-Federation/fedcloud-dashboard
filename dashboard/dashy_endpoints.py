#!/usr/bin/env python

"""
This code has been copied from https://github.com/tdviet/fedcloudclient
"""

from urllib import parse

import defusedxml.ElementTree as ElementTree
import requests
import yaml

DEFAULT_ICON = (
    "https://github.com/openstack/openstackdocstheme/blob/master"
    "/openstackdocstheme/theme/openstackdocs/static/favicon.ico?raw=true"
)
GOCDB_PUBLICURL = "https://goc.egi.eu/gocdbpi/public/"
DOCS_URL = "https://docs.egi.eu/users/compute/cloud-compute/openstack/"
TIMEOUT = 10


def get_sites():
    """
    Get list of sites (using GOCDB instead of site configuration)
    :return: list of site IDs
    """
    q = {"method": "get_site_list", "certification_status": "Certified"}
    url = "?".join([GOCDB_PUBLICURL, parse.urlencode(q)])
    r = requests.get(url)
    sites = {}
    if r.status_code == 200:
        root = ElementTree.fromstring(r.text)
        for s in root:
            name = s.attrib.get("NAME")
            country = s.attrib.get("COUNTRY")
            country_code = s.attrib.get("COUNTRY_CODE")
            sites[name] = {"country": country, "country_code": country_code}
    else:
        print("Something went wrong...")
        print(r.status_code)
        print(r.text)
    return sites


def find_endpoints(service_type, production=True, monitored=True):
    """
    Searching GOCDB for endpoints according to service types and status
    :param service_type:
    :param production:
    :param monitored:
    :param site: list of sites, None for searching all sites
    :return: list of endpoints
    """
    q = {"method": "get_service_endpoint", "service_type": service_type}
    if monitored:
        q["monitored"] = "Y"
    sites = get_sites()
    url = "?".join([GOCDB_PUBLICURL, parse.urlencode(q)])
    r = requests.get(url)
    endpoints = []
    if r.status_code == 200:
        root = ElementTree.fromstring(r.text)
        for sp in root:
            if production:
                prod = sp.find("IN_PRODUCTION").text.upper()
                if prod != "Y":
                    continue
            os_url = sp.find("URL").text
            ep_site = sp.find("SITENAME").text
            if ep_site not in sites:
                continue
            # os_url = urlparse.urlparse(sp.find('URL').text)
            # sites[sp.find('SITENAME').text] = urlparse.urlunparse(
            #    (os_url[0], os_url[1], os_url[2], '', '', ''))
            endpoints.append(
                [
                    ep_site,
                    service_type,
                    os_url,
                    sites[ep_site]["country"],
                    sites[ep_site]["country_code"],
                ]
            )
    else:
        print("Something went wrong...")
        print(r.status_code)
        print(r.text)
    return endpoints


def main():
    dashy_conf = {
        "pageInfo": {
            "title": "EGI Cloud Compute",
            "description": "FedCloud providers dashboards",
            "navLinks": [
                {
                    "title": "Documentation",
                    "path": DOCS_URL,
                }
            ],
            "logo": "https://egi-api.nois3.net/app/uploads/2021/11/egi-logo.svg",
        },
        "appConfig": {
            "theme": "material",
            "layout": "horizontal",
            "iconSize": "medium",
            "language": "en",
            "disableConfiguration": True,
        },
        "sections": [
            {"name": "OpenStack Dashboards", "icon": "fas fa-clouds", "items": []}
        ],
        "displayData": {
            "sortBy": "alphabetical",
            "rows": 1,
            "cols": 1,
            "collapsed": False,
            "hideForGuests": False,
        },
    }
    endpoints = find_endpoints("org.openstack.horizon")
    items = dashy_conf["sections"][0]["items"]
    for s in endpoints:
        items.append(
            {
                "title": s[0],
                "description": "%s (%s)" % (s[3], s[4]),
                "icon": DEFAULT_ICON,
                "url": s[2],
                "target": "newtab",
            }
        )
    print(yaml.dump(dashy_conf))


if __name__ == "__main__":
    main()
