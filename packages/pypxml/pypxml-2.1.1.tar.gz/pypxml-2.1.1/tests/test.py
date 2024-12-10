from pypxml import PageXML, PageType


pxml = PageXML.from_xml('/home/janik/Documents/d2_0001-0100/173736378X_00000051.xml')
res = pxml.find_all(PageType.Coords, recursive=True)
for r in res:
    print(r['points'])