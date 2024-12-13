import os
import re
import requests
import codecs
from pypers.steps.base.extract import ExtractBase
from pypers.utils import utils

from lxml import etree

class Trademarks(ExtractBase):
    """
    Extract CHTM marks information from the API response
    """
    spec = {
        "version": "2.0",
        "descr": [
            "Returns the directory with the extraction"
        ]
    }

    # a file with trademarks in XML
    def unpack_archive(self, archive, dest):
        self.logger.debug('processing file %s' % archive)

        parser = etree.XMLParser(ns_clean=True, dtd_validation=False, load_dtd=False, no_network=True, recover=True, encoding='utf-8')
        xml_root = None
        try:
            xml_root = etree.parse(archive, parser=parser)
        except Exception as e: 
            self.logger.error("XML parsing failed for %s: %s" % (archive, e))

        nss = { "com": "http://www.wipo.int/standards/XMLSchema/ST96/Common", "tmk": "http://www.wipo.int/standards/XMLSchema/ST96/Trademark" }
        trademark_nodes = xml_root.xpath("//tmk:Trademark", namespaces=nss)
        appnum_nodes = xml_root.xpath("//tmk:Trademark/com:ApplicationNumber/com:ApplicationNumberText/text()", namespaces=nss)
        for index, trademark_node in enumerate(trademark_nodes):
            if appnum_nodes != None and len(appnum_nodes)>index:
                appnum = appnum_nodes[index]

                # sanitize
                appnum = appnum.replace('/', '')
                appxml_file = os.path.join(dest, appnum+".xml")
                with open(appxml_file, 'w') as fh:
                    fh.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
                    fh.write(etree.tostring(trademark_node, pretty_print=True).decode("utf-8"))
                self.add_xml_file(appnum, appxml_file)

                results = trademark_node.xpath("./tmk:MarkRepresentation/tmk:MarkReproduction/tmk:MarkImageBag/tmk:MarkImage/com:FileName/text()", namespaces=nss)
                if results != None and len(results)>0:
                    self.add_img_url(appnum, results[0])


    def collect_files(self, dest):
        pass

    def process(self):
        pass
        #raise Exception("HERE")
