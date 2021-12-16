import scrapy
from scrapy.selector import Selector
import lxml
from lxml.html.clean import Cleaner
import re
from urllib.parse import urlparse



class DSSpider(scrapy.Spider):


    name = "ds_spider"

    allowed_domains = ('toscrape.com')

    start_urls = ['https://quotes.toscrape.com/page/1/']
       

    def parse(self, response):
        selector = Selector(response)
        # get page title
        page_title = selector.xpath('//title/text()').extract()[0]
        # get page content
        cleaner = Cleaner()
        cleaner.javascript = True
        cleaner.style = True
        page_html = selector.xpath('//body').extract()[0]
        # remove js and css code
        page_html = cleaner.clean_html(page_html)
        # extract text
        html_doc = lxml.html.document_fromstring(page_html)
        page_content = ' '.join(lxml.etree.XPath("//text()")(html_doc))
        page_content += ' ' + page_title
        # remove line breaks, tabs and extra spaces
        page_content = re.sub('\n', ' ', page_content)
        page_content = re.sub('\r', ' ', page_content)
        page_content = re.sub('\t', ' ', page_content)
        page_content = re.sub(' +', ' ', page_content)
        page_content = page_content.strip()
        # get page links
        page_hrefs = response.xpath('//a/@href').extract()
        # page_urls = []
        # filter out links with unallowed domains
        # for link in page_hrefs:
        #     # convert relative links to absolute urls
        #     url = response.urljoin(link)
        #     # extract domain from url
        #     parsed_url = urlparse(url)
        #     url_domain = parsed_url.netloc
        #     if url_domain in self.allowed_domains:
        #         page_urls.append(url)
        # # log out some info
        # e = self.log('Page: %s (%s)' % (response.url, page_title))
        print(page_title)

test = DSSpider('ds_spider')
print(test)