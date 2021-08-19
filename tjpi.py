import scrapy
from bs4 import BeautifulSoup
import search_tjpi


class TJPI_Spider(scrapy.Spider):

    name = "tjpi"
    allowed_domains = "tjpi.pje.jus.br"

    def _init_(self, process=None, *args, **kwargs):
        super(TJPI_Spider, self)._init_(*args, **kwargs)

    def start_requests(self):

        url = f'https://tjpi.pje.jus.br/1g/ConsultaPublica/DetalheProcessoConsultaPublica/listView.seam?ca=7128a142e82dac3e6379a516790c20c2880c63c23fbb9757'

        yield scrapy.Request(url=url, callback=search_tjpi.crawler, headers=search_tjpi.build_headers)
