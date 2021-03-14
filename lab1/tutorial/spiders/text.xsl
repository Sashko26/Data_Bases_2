<?xml version="1.0" encoding="windows-1251"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:output method="xml"
  encoding="windows-1251"
  omit-xml-declaration="no"
  indent="yes"
  media-type="text/xml"
  doctype-public="-//W3C//DTD XHTML 1.1//EN"
  doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"
/>

<xsl:template match="items">
    <html>
    <body>
        <table border="1">
            <tr>
                <th>title</th>
                <th>year</th>
                <th>genre</th>
            </tr>
        <xsl:for-each select="item">
            <tr>
              <td><xsl:value-of select="title"/></td>
              <td><img src=""/> <xsl:value-of select="image"/></td>
              <td><xsl:value-of select="price"/></td>
            </tr>
        </xsl:for-each>
        </table>
    </body>
</html>
</xsl:template>
</xsl:stylesheet>