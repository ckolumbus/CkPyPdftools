
# add src path
import sys
sys.path.insert(0, "../src")

import unittest, os
from shutil import rmtree
from tempfile import mkdtemp

import ckpdfsearch
class AttachmentSearchClassFixture(unittest.TestCase):
    def setUp(self):
        self.idxDir = mkdtemp(".ckdpftest")
        #print self.idxDir

    def tearDown(self):
        try:
            rmtree(self.idxDir)
        except:
            pass
        self.idxDir = None

class TestAttachmentSearchClass_CreateAndPurge(AttachmentSearchClassFixture):

    def testCreateAndPurge(self):

        idx  = ckpdfsearch.AttachmentSearchIndex(self.idxDir)
        assert idx.idxPath == self.idxDir

        idx.openIndex()
        assert idx is not None
        assert idx.isValid()

        # test Fake purge
        idx.purgeIndexDir()
        assert os.path.exists(idx.idxPath)
        assert idx.isValid()

        # test real purge
        idx.purgeIndexDir(doIt=True)
        assert not os.path.exists(idx.idxPath)
        assert idx.idx is None

class TestAttachmentSearchClass_TestIndex(AttachmentSearchClassFixture):
    def setUp(self):
        AttachmentSearchClassFixture.setUp(self)
        self.idx  = ckpdfsearch.AttachmentSearchIndex(self.idxDir)

    def test1(self):
        pass

#def main():
#    testCase = TestAttachmentSearchClass()
#
#    runner = unittest.TextTestRunner()
#    runner.run(testCase)

if __name__ == "__main__":
     unittest.main()
     #main()
