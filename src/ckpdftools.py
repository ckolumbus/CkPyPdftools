#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 CKolumbus
# All rights reserved.
#
# This file is part of CkPyPdftools
#
# CkPyPdftools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CkPyPdftools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CkPyPdftools.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Author   : Chris <ckolumbus@ac-drexler.de>
# Date     : 2014-04-09

__version__ = "0.1"


from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import PDFObjectNotFound
from pdfminer.converter import TextConverter

def extractText(fp, caching=False, codec='utf-8', laparams=None):
    import StringIO
    outfp = StringIO.StringIO()

    rsrcmgr = PDFResourceManager(caching=caching)
    device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams,
                               imagewriter=None)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(fp, pagenos,
                                  maxpages=maxpages, password=password,
                                  caching=caching, check_extractable=True):
        page.rotate = (page.rotate+rotation) % 360
        interpreter.process_page(page)
    device.close()
    result = outfp.getvalue()
    outfp.close()
    return result


def extractComments(fp):
    parser = PDFParser(fp)
    doc = PDFDocument(parser, "")

    visited = set()
    pages = []
    resultList = []

    def extract(objid, obj):
        result = None
        if isinstance(obj, dict):
            # 'Type' is PDFObjRef type
            if obj.has_key('Type') and obj['Type'].name == 'Page':
                pages.append(objid)
            elif obj.has_key('C'):
                pr = obj['P']
                try:
                    pi = pages.index(pr.objid)+1
                except:
                    pi = -1
                try:
                    result = (objid, pi, obj['Subtype'].name, obj['Subj'],obj['T'],obj['Contents'])
                except:
                    # if any of the listed entries do not exist, ignore 
                    #print(objid, pi, obj['Subtype'].name)
                    result = ()

        return result

    for xref in doc.xrefs:
        for objid in xref.get_objids():
            if objid in visited: continue
            visited.add(objid)
            try:
                obj = doc.getobj(objid)
                if obj is None: continue
                r= extract(objid,obj)
                if r:
                    resultList.append(r)
            except PDFObjectNotFound, e:
                print >>sys.stderr, 'not found: %r' % e

    return resultList

def main(argv=None):
    # not using argparser to support Python<2.7
    from optparse import OptionParser

    usage = "usage: %prog [options] pdf"
    parser = OptionParser(usage)
    parser.set_defaults(verbose=False)
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                      help="verbose output")
    parser.add_option("-q", "--quite", dest="verbose", action="store_false",
                      help="supress all output (quite)")
    (options, args) = parser.parse_args(argv[1:])

    if len(args) != 1:
        parser.print_help()
        return 2

    with file(args[0], 'rb') as fp:
        for i in extractComments(fp):
            print i

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))

