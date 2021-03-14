import lxml.etree as ET
dom = ET.parse("./spiders/text.xml")
xslt = ET.parse("./spiders/text.xsl")
transform = ET.XSLT(xslt)
newdom = transform(dom)
newdom.write('some.html', pretty_print=True,method="xml")

