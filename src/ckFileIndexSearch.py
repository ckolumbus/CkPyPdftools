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

import os, os.path
from shutil import rmtree
from whoosh import index
from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import StemmingAnalyzer

class AttachmentSearchSchema(SchemaClass):
    path     = ID  (stored=True)
    checksum = ID  (stored=True)
    content  = TEXT(analyzer=StemmingAnalyzer())
    author   = TEXT(stored=True)
    atype    = TEXT(stored=True)
    asubtype = TEXT(stored=True)
    tags     = KEYWORD


class AttachmentSearchIndex:

    def __init__(self, idxPath, idxName=None, idxSchema=AttachmentSearchSchema):
        # avoid wrong relative adressing if cwd changes during operations
        self.idxPath   = os.path.realpath(idxPath)
        self.idxName   = idxName
        self.idxSchema = idxSchema
        self.idx       = None


    def _openIndex(self):
        self.ix = index.open_dir(self.idxPath)

    def _createIndex(self):
        try:
            os.mkdir(self.idxPath)
        except:
            pass
        self.ix = index.create_in(self.idxPath, self.idxSchema)

    def openIndex(self, create=True):
        # close before reopening
        self.closeIndex()

        # is the index  NOT valid...
        if not index.exists_in(self.idxPath):
            # if no creation requested = return
            if not create:
                return False

            # .. create the index... 
            self._createIndex()
        else:
            # ... otherwise just open it.
            self._openIndex()

        return self.ix is not None

    def purgeIndexDir(self, doIt=False):
        self.closeIndex()
        if doIt:
            rmtree(self.idxPath)

    def closeIndex(self):
        if self.idx:
            self.idx.close()
            self.idx = None

    def isValid(self):
        return index.exists_in(self.idxPath)

    def search(self, ):
        pass

    def addFileToIndex(self, path):
        pass

    def addDirToIndex(self, path, recursive=False):
        pass


def test():
    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
    ix = create_in("indexdir", schema)
    writer = ix.writer()
    writer.add_document(title=u"First document", path=u"/ac",
                        content=u"This is the first document2 we've added!")
    writer.add_document(title=u"First xxxxwdocument", path=u"/ac",
                        content=u"This is the first document2 we've added!")
    writer.add_document(title=u"Second document", path=u"/b",
                        content=u"The second one is even more interesting!")
    writer.commit()
    from whoosh.qparser import QueryParser
    results = None
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse("first")
        results = searcher.search(query, terms=True)
        for i in results:
            print i, i.matched_terms()

    return results

def main(argv=None):
    # not using argparser to support Python<2.7
    from optparse import OptionParser

    usage = "usage: %prog [options] <cmd> [{dir|files} ...]"
    parser = OptionParser(usage)
    parser.set_defaults(verbose=False)
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                      help="verbose output")
    parser.add_option("-q", "--quite", dest="verbose", action="store_false",
                      help="supress all output (quite)")
    (options, args) = parser.parse_args(argv[1:])

    if len(args) == 0:
        parser.print_help()
        return 2

    test()
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))


