#!/usr/bin/env python

# Python bindings to the Google search engine
# Copyright (c) 2009-2016, Geovany Rodrigues
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice,this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

__all__ = [
    # Main search function.
    'search',
]

# Default user agent, unless instructed by the user to change it.
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'


def get_page(url):
    request = Request(url)
    request.add_header('User-Agent', USER_AGENT)
    response = urlopen(request)
    return response


def search(url=''):
    products = []
    last_page = False
    page = 1

    while not last_page:
        print(f'Processing page {page}')
        page_url = url
        if page > 1:
            page_url += f'/pagina-{page}'

        html = get_page(page_url)
        soup = BeautifulSoup(html, 'html.parser')

        products_cards = soup.find_all(attrs={"class": "product-grid-item"})
        if len(products_cards) == 0:
            last_page = True

        for product_card in products_cards:
            product_url = product_card.find('a')
            product_url = product_url.attrs['href']

            product = {
                'Nome': product_card.find('h2').text
            }

            product_html = get_page('https://www.americanas.com.br' + product_url)
            product_soup = BeautifulSoup(product_html, 'html.parser')

            about = product_soup.find('table')
            rows = about.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                product[cols[0].text.strip()] = cols[1].text.strip()

            products.append(product)

        page += 1

    return products
