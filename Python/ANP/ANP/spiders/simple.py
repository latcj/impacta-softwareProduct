import scrapy

class SimpleSpider(scrapy.Spider):
    name = "simple"
    start_urls = ['https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/serie-historica-de-precos-de-combustiveis']

    def parse(self, response):
        for arquivo in response.xpath("*//div[@id='parent-fieldname-text']/ul/li/a[contains(@href, 'precos-gasolina')]"):
            title = arquivo.xpath('.//text()').get()
            link = response.urljoin(
                arquivo.xpath('.//@href').get()
            )
            yield {
                'Title':title,
                'file_urls':[link]
            }