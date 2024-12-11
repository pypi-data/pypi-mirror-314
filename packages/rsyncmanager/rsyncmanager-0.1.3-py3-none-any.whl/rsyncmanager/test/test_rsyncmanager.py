# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "04/05/2020"


import logging
import os
import shutil
import tempfile
import unittest
from ..rsyncmanager import RSyncManager
from silx.gui.utils.testutils import SignalListener
from silx.gui.utils.testutils import TestCaseQt
import time

logging.disable(logging.INFO)


class _BaseTest(TestCaseQt):
    def setUp(self):
        super(_BaseTest, self).setUp()
        self.input_dir = tempfile.mkdtemp()
        self.output_dir = tempfile.mkdtemp()

        # create some files
        self.folder_1 = os.path.join(self.input_dir, 'folder1')
        self.folder_2 = os.path.join(self.input_dir, 'folder2')
        self.file_1 = os.path.join(self.folder_1, 'f1.txt')
        self.file_2 = os.path.join(self.folder_2, 'f2.txt')

        for folder in (self.folder_1, self.folder_2):
            os.mkdir(folder)

        for my_file in (self.file_1, self.file_2):
            with open(my_file, "w") as txt_file:
                txt_file.write('toto')

    def tearDown(self):
        shutil.rmtree(self.input_dir)
        shutil.rmtree(self.output_dir)
        super(_BaseTest, self).tearDown()


@unittest.skipIf(RSyncManager().has_rsync() is False, "Rsync is missing")
class TestSync(_BaseTest):
    """Check that the RSyncManager is correctly synchronizing files.
    """
    def testSyncFolder(self):
        """Test synchronization of a folder"""
        RSyncManager().sync_file(source=self.folder_1, target=self.output_dir,
                                 wait=True)
        target_folder = os.path.join(self.output_dir, 'folder1')
        target_file = os.path.join(self.output_dir, 'folder1', 'f1.txt')

        self.assertTrue(os.path.exists(target_folder))
        self.assertTrue(os.path.exists(target_file))
        self.assertTrue(os.path.exists(self.folder_1))

    def testSyncFile(self):
        """Test synchronization of a file"""
        target = os.path.join(self.output_dir, 'f1.txt')
        RSyncManager().sync_file(source=self.file_1, target=target,
                                 wait=True)
        target_file = os.path.join(self.output_dir, 'f1.txt')
        self.assertTrue(os.path.exists(target_file))
        self.assertTrue(os.path.exists(self.file_1))

    def testSyncSetFiles(self):
        """Test synchronization of a file and a folder"""
        target_file_2 = os.path.join(self.output_dir, 'f2.txt')
        RSyncManager().sync_files(sources=(self.folder_1, self.file_2),
                                  targets=(self.output_dir, target_file_2),
                                  wait=True)
        target_folder = os.path.join(self.output_dir, 'folder1')
        self.assertTrue(os.path.exists(target_folder))
        target_file_1 = os.path.join(self.output_dir, 'folder1', 'f1.txt')
        self.assertTrue(os.path.exists(target_file_1))
        self.assertTrue(os.path.exists(target_file_2))
        self.assertTrue(os.path.exists(self.folder_1))
        self.assertTrue(os.path.exists(self.file_2))


@unittest.skipIf(RSyncManager().has_rsync() is False, "Rsync is missing")
class TestCallbacks(_BaseTest):
    """Check that the RSyncManager is calling callbacks after synchronization
    """

    def setUp(self):
        super(TestCallbacks, self).setUp()
        self.timeout = 2
        self.callback_listener = SignalListener()

    def tearDown(self):
        super(TestCallbacks, self).tearDown()

    def testCallbackSyncFile(self):
        RSyncManager().sync_file(source=self.file_1, target=self.output_dir,
                                 wait=False, callback=self.callback_listener)
        while self.callback_listener.callCount() < 1 and self.timeout > 0:
            self.qapp.processEvents()
            time.sleep(0.2)
            self.timeout -= 0.2

        if self.timeout <= 0:
            raise TimeoutError('callback never called')

    def testCallbackSyncFiles(self):
        RSyncManager().sync_files(sources=(self.folder_1, self.file_2),
                                  targets=(self.output_dir, self.output_dir),
                                  callback=self.callback_listener,
                                  wait=False)
        while self.callback_listener.callCount() < 1 and self.timeout > 0:
            self.qapp.processEvents()
            time.sleep(0.2)
            self.timeout -= 0.2

        if self.timeout <= 0:
            raise TimeoutError('callback never called')


class TestSyncAndDelete(_BaseTest):
    """Check that the RSyncManager is correctly synchronizing files and then
    can delete the source files.
    """

    def testSyncFolder(self):
        """Test synchronization of a folder"""
        RSyncManager().sync_file(source=self.folder_1,
                                 target=self.output_dir,
                                 wait=True,
                                 delete=True)
        target_folder = os.path.join(self.output_dir, 'folder1')
        target_file = os.path.join(self.output_dir, 'folder1', 'f1.txt')

        self.assertTrue(os.path.exists(target_folder))
        self.assertTrue(os.path.exists(target_file))
        self.assertFalse(os.path.exists(self.folder_1))

    def testSyncFile(self):
        """Test synchronization of a file"""
        target = os.path.join(self.output_dir, 'f1.txt')
        RSyncManager().sync_file(source=self.file_1,
                                 target=target,
                                 wait=True,
                                 delete=True)
        target_file = os.path.join(self.output_dir, 'f1.txt')
        self.assertTrue(os.path.exists(target_file))
        self.assertFalse(os.path.exists(self.file_1))

    def testSyncSetFiles(self):
        """Test synchronization of a file and a folder"""
        target_file_2 = os.path.join(self.output_dir, 'f2.txt')
        RSyncManager().sync_files(sources=(self.folder_1, self.file_2),
                                  targets=(self.output_dir, target_file_2),
                                  wait=True,
                                  delete=True)
        target_folder = os.path.join(self.output_dir, 'folder1')
        self.assertTrue(os.path.exists(target_folder))
        target_file_1 = os.path.join(self.output_dir, 'folder1', 'f1.txt')
        self.assertTrue(os.path.exists(target_file_1))
        self.assertTrue(os.path.exists(target_file_2))
        self.assertFalse(os.path.exists(self.folder_1))
        self.assertFalse(os.path.exists(self.file_2))


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestSync, TestCallbacks, TestSyncAndDelete):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest="suite")
