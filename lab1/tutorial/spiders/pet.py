import scrapy
import xml.etree.ElementTree as ET

def createRootItemsElement():
    root = ET.Element('items')
    ET.indent(root, "  ", 0)
    return root
root = createRootItemsElement()

def createXmlTagOfPrice(price):
    price = str(price)
    image = ET.Element('price')
    image.text = price
    return image
def createXmlTagOfTitle(text):
    text = str(text)
    fragmentText = ET.Element('title')
    fragmentText.text = text
    return fragmentText
def createXmlTagOfImage(src):
    text = str(src)
    fragmentText = ET.Element('image')
    fragmentText.text = text
    return fragmentText
def createItem():
    item = ET.Element('item')
    return item
def createXMLitemFullContent(imageTag,titleTag,priceTag):
    page = createItem()
    page.append(titleTag)
    page.append(imageTag)
    page.append(priceTag)
    return page
class shopSpider(scrapy.Spider):
    amountItems =0
    name = 'shopSpider'
    start_urls = ['https://petmarket.ua/']
    amountOfPages = 0
    listOfTextSnippetsPerPage = []

    def parse(self, response):
        self.parse_dir_contents(response)
        yield response.follow(url="https://petmarket.ua/zootovary-dlja-sobak/suhoj-korm-dlja-sobak/royal-canin-korm-dlja-sobak/", callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):

        for cart in response.xpath('.//div[@class="catalogCard-box j-product-container"]'):
            if self.amountItems<20:
                price = cart.xpath('.//div[@class="catalogCard-price"]/text()').extract_first().strip()
                title = cart.xpath('.//div[@class="catalogCard-title"]/a/text()').extract_first().strip()
                image = cart.xpath('.//img[@class="catalogCard-img"]/@src').extract_first().strip()
                image = image[1:len(image)]
                image = str(response.url) + image
                imageTag = createXmlTagOfImage(image)
                titleTag = createXmlTagOfTitle(title)
                priceTag = createXmlTagOfPrice(price)
                newItem  = createXMLitemFullContent(imageTag,titleTag,priceTag)
                print(newItem)
                root.append(newItem)
                self.amountItems=self.amountItems+1

            ET.indent(root, "  ", 0)
            rootStr = ET.tostring(root, encoding="unicode", method='xml',
                                  xml_declaration="<?xml version = '1.0' encoding = 'UTF-8' standalone = 'no' ?>")
            with open('text.xml', "w") as f:
                f.write(rootStr)










