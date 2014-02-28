#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
#= Imports ====================================================================
import isbn
import convertors
from marcxml import MARCXMLRecord


def testJSONConvertor():
    data = open(
        "tests/resources/aleph_data_examples/aleph_sources/example.xml"
    ).read()

    epub = convertors.toEPublication(data)
    epub2 = convertors.fromJSON(convertors.toJSON(epub))

    assert(epub == epub2)


def testMARCXML():
    xml = """<record xmlns="http://www.loc.gov/MARC21/slim/"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.loc.gov/MARC21/slim
http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd">
<leader>-----cam-a22------a-4500</leader>
<controlfield tag="001">cpk20051492461</controlfield>
<controlfield tag="003">CZ-PrNK</controlfield>
<controlfield tag="005">20120509091037.0</controlfield>
<controlfield tag="007">ta</controlfield>
<controlfield tag="008">041216s2004----xr-a---e-f----001-0-cze--</controlfield>
<datafield tag="015" ind1=" " ind2=" ">
<subfield code="a">cnb001492461</subfield>
</datafield>
<datafield tag="020" ind1=" " ind2=" ">
<subfield code="a">80-251-0225-4 (brož.) :</subfield>
<subfield code="c">Kč 590,00</subfield>
</datafield>
<datafield tag="035" ind1=" " ind2=" ">
<subfield code="a">(OCoLC)85131856</subfield>
</datafield>
<datafield tag="040" ind1=" " ind2=" ">
<subfield code="a">BOA001</subfield>
<subfield code="b">cze</subfield>
<subfield code="d">ABA001</subfield>
</datafield>
<datafield tag="041" ind1="1" ind2=" ">
<subfield code="a">cze</subfield>
<subfield code="h">eng</subfield>
</datafield>
<datafield tag="072" ind1=" " ind2="7">
<subfield code="a">004.4/.6</subfield>
<subfield code="x">Programování. Software</subfield>
<subfield code="2">Konspekt</subfield>
<subfield code="9">23</subfield>
</datafield>
<datafield tag="080" ind1=" " ind2=" ">
<subfield code="a">004.451.9Unix</subfield>
<subfield code="2">MRF</subfield>
</datafield>
<datafield tag="080" ind1=" " ind2=" ">
<subfield code="a">004.451</subfield>
<subfield code="2">MRF</subfield>
</datafield>
<datafield tag="080" ind1=" " ind2=" ">
<subfield code="a">004.42</subfield>
<subfield code="2">MRF</subfield>
</datafield>
<datafield tag="080" ind1=" " ind2=" ">
<subfield code="a">(035)</subfield>
<subfield code="2">MRF</subfield>
</datafield>
<datafield tag="100" ind1="1" ind2=" ">
<subfield code="a">Raymond, Eric S.</subfield>
<subfield code="7">jn20020721375</subfield>
<subfield code="4">aut</subfield>
</datafield>
<datafield tag="245" ind1="1" ind2="0">
<subfield code="a">Umění programování v UNIXu /</subfield>
<subfield code="c">Eric S. Raymond</subfield>
</datafield>
<datafield tag="250" ind1=" " ind2=" ">
<subfield code="a">Vyd. 1.</subfield>
</datafield>
<datafield tag="260" ind1=" " ind2=" ">
<subfield code="a">Brno :</subfield>
<subfield code="b">Computer Press,</subfield>
<subfield code="c">2004</subfield>
</datafield>
<datafield tag="300" ind1=" " ind2=" ">
<subfield code="a">509 s. :</subfield>
<subfield code="b">il. ;</subfield>
<subfield code="c">23 cm</subfield>
</datafield>
<datafield tag="500" ind1=" " ind2=" ">
<subfield code="a">Glosář</subfield>
</datafield>
<datafield tag="504" ind1=" " ind2=" ">
<subfield code="a">Obsahuje bibliografii, bibliografické odkazy a rejstřík</subfield>
</datafield>
<datafield tag="546" ind1=" " ind2=" ">
<subfield code="a">Přeloženo z angličtiny</subfield>
</datafield>
<datafield tag="650" ind1="0" ind2="7">
<subfield code="a">UNIX</subfield>
<subfield code="7">ph117153</subfield>
<subfield code="2">czenas</subfield>
</datafield>
<datafield tag="650" ind1="0" ind2="7">
<subfield code="a">operační systémy</subfield>
<subfield code="7">ph115593</subfield>
<subfield code="2">czenas</subfield>
</datafield>
<datafield tag="650" ind1="0" ind2="7">
<subfield code="a">programování</subfield>
<subfield code="7">ph115891</subfield>
<subfield code="2">czenas</subfield>
</datafield>
<datafield tag="650" ind1="0" ind2="9">
<subfield code="a">UNIX</subfield>
<subfield code="2">eczenas</subfield>
</datafield>
<datafield tag="650" ind1="0" ind2="9">
<subfield code="a">operating systems</subfield>
<subfield code="2">eczenas</subfield>
</datafield>
<datafield tag="650" ind1="0" ind2="9">
<subfield code="a">programming</subfield>
<subfield code="2">eczenas</subfield>
</datafield>
<datafield tag="655" ind1=" " ind2="7">
<subfield code="a">příručky</subfield>
<subfield code="7">fd133209</subfield>
<subfield code="2">czenas</subfield>
</datafield>
<datafield tag="655" ind1=" " ind2="9">
<subfield code="a">handbooks, manuals, etc.</subfield>
<subfield code="2">eczenas</subfield>
</datafield>
<datafield tag="765" ind1="0" ind2=" ">
<subfield code="t">Art of UNIX programming</subfield>
<subfield code="9">Česky</subfield>
</datafield>
<datafield tag="901" ind1=" " ind2=" ">
<subfield code="b">9788025102251</subfield>
<subfield code="f">1. vyd.</subfield>
<subfield code="o">20050217</subfield>
</datafield>
<datafield tag="910" ind1="1" ind2=" ">
<subfield code="a">ABA001</subfield>
</datafield>
</record>"""

    m = MARCXMLRecord(xml)

    # test getters
    assert m.getAuthors()[0].name == "Eric S."
    assert m.getAuthors()[0].surname == "Raymond"
    assert m.getISBNs()[0] == "80-251-0225-4"
    assert "brož." in m.getBinding()[0]
    assert len(m.getCorporations()) == 0
    assert len(m.getDistributors()) == 0
    assert m.getFormat() == "23 cm"
    assert m.getName() == "Umění programování v UNIXu /"
    assert m.getSubname() == ""
    assert m.getPrice() == "Kč 590,00"
    assert m.getPart() == ""
    assert m.getPartName() == ""
    assert m.getPart() == ""
    assert m.getPublisher() == "Computer Press,"
    assert m.getPubDate() == "2004"
    assert m.getPubOrder() == "1. vyd."
    assert m.getOriginals()[0] == "Art of UNIX programming"

    # test m.__str__() equality with original XML
    assert set(xml.splitlines()) == set(str(m).splitlines())

def testISBN():
    assert isbn.is_valid_isbn("0-306-40615-2")
    assert isbn.is_valid_isbn("0-9752298-0-X")
    assert not isbn.is_valid_isbn("0-9752298-0-1")

    assert isbn.is_valid_isbn("978-0-306-40615-7")
    assert not isbn.is_valid_isbn("978-0-306-40115-7")

    assert not isbn.is_valid_isbn("978-80-7302-134-x")


#= Main program ===============================================================
if __name__ == '__main__':
    testJSONConvertor()
    testMARCXML()
    testISBN()

    print "Everything is ok."
