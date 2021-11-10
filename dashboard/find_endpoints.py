#!/usr/bin/env python

'''
This code has been copied from https://github.com/tdviet/fedcloudclient
'''

from urllib import parse
import defusedxml.ElementTree as ElementTree
import requests

GOCDB_PUBLICURL = "https://goc.egi.eu/gocdbpi/public/"
TIMEOUT = 10


def get_sites():
    """
    Get list of sites (using GOCDB instead of site configuration)
    :return: list of site IDs
    """
    q = {"method": "get_site_list", "certification_status": "Certified"}
    url = "?".join([GOCDB_PUBLICURL, parse.urlencode(q)])
    r = requests.get(url)
    sites = []
    if r.status_code == 200:
        root = ElementTree.fromstring(r.text)
        for s in root:
            sites.append(s.attrib.get("NAME"))
    else:
        print("Something went wrong...")
        print(r.status_code)
        print(r.text)
    return sites


def find_endpoints(service_type, production=True, monitored=True, site=None):
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
    if site:
        q["sitename"] = site
        sites = [site]
    else:
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
            endpoints.append([sp.find("SITENAME").text, service_type, os_url])
    else:
        print("Something went wrong...")
        print(r.status_code)
        print(r.text)
    return endpoints


def main():
    endpoints = find_endpoints("org.openstack.horizon")
    for site, service_type, endpoint in endpoints:
        print(site, endpoint)


if __name__ == "__main__":
    main()
