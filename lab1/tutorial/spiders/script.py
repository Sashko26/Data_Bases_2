import scrapy
import xml.etree.ElementTree as ET
global listOfTextSnippetsPerPage
def createRootElement():
    root = ET.Element('data')
    ET.indent(root, "  ", 0)
    return root
root = createRootElement()

def getLinks(response):
    listOfLinks = []
    for link in response.xpath('//a'):
        listOfLinks.append(link)
    return listOfLinks

def createXmlTagOfImage(src):
    src = str(src)
    image = ET.Element('fragment', type='image')
    image.text = src
    return image

def createXmlTagOfText(text):
    text = str(text)
    fragmentText = ET.Element('fragment', type='text')
    fragmentText.text = text
    return fragmentText

def createPage(url):
    page = ET.Element('page', url=url)
    return page

global amountOfEnteringIn

def createXMLpageFullContent(url, listOfXmlElements):
    page = createPage(str(url))
    for el in listOfXmlElements:
        page.append(el)
    return page

def clean_price(text):
    digits = [symbol for symbol in text if symbol.isdigit()]
    cleaned_text = ''.join(digits)
    if not cleaned_text:
        return None
    return int(cleaned_text)

class BlogSpider(scrapy.Spider):
    globalIteratot =0
    name = 'blogSpider'
    start_urls = ['https://golos.ua/']
    amountOfPages = 0
    listOfTextSnippetsPerPage = []

    def createListOfXmlElements(self, response):
        amountOfImages = 0
        amountOfTextElements = 0
        listOfElement = [];
        for link in response.xpath('//*'):
            imageElement = ""
            textElement = ""
            if link.xpath('name()')[0].get() == "script" or link.xpath('name()')[0].get() == "style":
                script = 0
            elif link.xpath('name()')[0].get() == "img":
                imageElement = createXmlTagOfImage(str(link.xpath('@src')[0].get()))
                listOfElement.append(imageElement)
                amountOfImages = amountOfImages + 1
            else:
                text = str(link.xpath('text()').get())
                text = text.strip()
                href = link.xpath('@href').get()
                if (text != "None" and text != ""):
                    amountOfTextElements = amountOfTextElements + 1
                    textElement = createXmlTagOfText(text)
                    listOfElement.append(textElement)
        buf = amountOfTextElements
        self.listOfTextSnippetsPerPage.append(buf)
        if self.amountOfPages==19:
            averageNumberOfTextFragments =0
            for el in  self.listOfTextSnippetsPerPage:
                averageNumberOfTextFragments=averageNumberOfTextFragments+el
            averageNumberOfTextFragments=averageNumberOfTextFragments/20
            print('list of text snippets per page:')
            print(self.listOfTextSnippetsPerPage)
            print('Average number of text fragments per page:')
            print(averageNumberOfTextFragments)
        return listOfElement

    def parse_dir_contents(self, response):
            listOfXmlElements = self.createListOfXmlElements(response)
            page = createXMLpageFullContent(str(response.url), listOfXmlElements)
            root.append(page)
            rootStr = ET.tostring(root, encoding="unicode", method='xml',
                                  xml_declaration="<?xml version = '1.0' encoding = 'iso-8859-1' standalone = 'no' ?>")
            self.amountOfPages=self.amountOfPages+1
            if self.amountOfPages == 19:
                ET.indent(root, "  ", 0)
                rootStr = ET.tostring(root, encoding="unicode", method='xml',
                          xml_declaration="<?xml version = '1.0' encoding = 'iso-8859-1' standalone = 'no' ?>")
                with open('golos.xml', "w", encoding="utf-8") as f:
                    f.write(rootStr)

    def parse(self, response):
        urlNew = 'https://golos.ua/'
        listOfXmlElements = self.createListOfXmlElements(response)
        firstpage = createXMLpageFullContent(urlNew, listOfXmlElements)
        self.amountOfPages=self.amountOfPages+1
        root.append(firstpage)
        links = getLinks(response)
        links = links[:20]
        ExtractedLinks =[]
        for link in links:
            ExtractedLinks.append(link.xpath('@href').extract()[0])
        i =0
        b= 0
        for href in ExtractedLinks:
            if href[0]=='/':
                href = href[1:len(href)]
                urlNew = str(response.url) + href
                yield response.follow(url=urlNew, callback=self.parse_dir_contents)
            elif href[0] == 'h':
                urlNew = href
                yield response.follow(url=urlNew, callback=self.parse_dir_contents)



