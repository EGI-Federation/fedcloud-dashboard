#!/usr/bin/env python

"""
This code has been copied from https://github.com/tdviet/fedcloudclient
"""

from pathlib import Path
from urllib import parse

import requests
import yaml
from defusedxml import ElementTree

GOCDB_PUBLICURL = "https://goc.egi.eu/gocdbpi/public/"
DOCS_URL = "https://docs.egi.eu/users/compute/cloud-compute/openstack/"
CONFIG_OUTPUT = "config.output"
CONFIG_TEMPLATE = {
    "title": "EGI Cloud Compute",
    "subtitle": "FedCloud Dashboards",
    "theme": "classic",
    "columns": "3",
    "defaults": {
        "layout": "list",
        "colorTheme": "auto",
    },
    "stylesheet": ["assets/egi.css"],
    "colors": {
        "light": {"highlight-hover": "#ef8200", "highlight-secondary": "#005faa"}
    },
    "links": [
        {
            "icon": "fas fa-book",
            "name": "User documentation",
            "target": "_blank",
            "url": "https://docs.egi.eu/users/compute/cloud-compute/openstack/",
        },
        {
            "icon": "fas fa-book",
            "name": "Provider documentation",
            "target": "_blank",
            "url": "https://docs.egi.eu/providers/cloud-compute/",
        },
    ],
    "logo": "assets/egi-logo.svg",
    "message": {
        "content": "You can find here link to the OpenStack dashboards of "
        "the EGI FedCloud providers",
        "icon": "fa fa-table-columns",
        "style": "is-dark",
        "title": "Provider dashboards",
    },
    "services": [{"icon": "fas fa-cloud", "items": [], "name": "OpenStack Dashboards"}],
    "footer": '<p><a href="https://www.egi.eu/service/cloud-compute/">Cloud '
    "Compute</a> is a service delivered by the <a "
    'href="https://www.egi.eu/egi-infrastructure/">EGI '
    "Infrastructure</a> | This dashboard uses <a "
    'href="https://github.com/bastienwirtz/homer">Homer</a>\n'
    "</p>\n",
}


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
    """
    Main function, generates config
    """
    config = CONFIG_TEMPLATE
    try:
        endpoints = find_endpoints("org.openstack.horizon")
        items = config["services"][0]["items"]
        for s in endpoints:
            items.append(
                {
                    "name": s[0],
                    "logo": "assets/icons/openstack.png",
                    "subtitle": f"{s[3]} ({s[4]})",
                    "tag": s[4],
                    "target": "_blank",
                    "url": s[2],
                }
            )
        print(yaml.dump(config))
        with open(CONFIG_OUTPUT, "w", encoding="utf-8") as f:
            yaml.dump(config, f)
    # catching anything, we don't need to be specific
    except Exception:  # pylint: disable=broad-exception-caught
        if Path(CONFIG_OUTPUT).is_file():
            with open(CONFIG_OUTPUT, "r", encoding="utf-8") as f:
                print(yaml.dump(yaml.safe_load(f)))
        else:
            # to-do: write in config: "site not available at the moment"
            print(yaml.dump(config))


if __name__ == "__main__":
    main()
