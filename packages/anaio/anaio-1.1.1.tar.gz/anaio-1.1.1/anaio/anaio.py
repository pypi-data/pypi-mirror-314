#!/usr/bin/env python
# encoding: utf-8
"""
anaio.py

A C extension for Python to read ana f0 files. Based on Michiel van Noort's
IDL DLM library 'f0' which contains a cleaned up version of the original
anarw routines.

To read a file:
> anadata = anaio.fzread(<filename>, [debug=0])
which will return a dict with the data in anadata['data'] and some meta info in anadata['header'].
To return only the data or header, use anaio.getdata() and anaio.getheader() respectively.
The letter will also not read the data and therefore speed up the process if you are interested in the header only.

To write a file:
> anaio.fzwrite(<filename>, <data>, [compress=1, [comments=False, [debug=0]]]):
or use anaio.writeto(), which is an alias to fzwrite().

Created by Tim van Werkhoven (t.i.m.vanwerkhoven@gmail.com) on 2009-02-11.
Copyright (c) 2009--2011 Tim van Werkhoven.
Since 2020 maintained and extended by Johannes Hoelken (hoelken@mps.mpg.de).

Published under MIT license.
"""

import os
import unittest

from ._anaio import fzread as _fzread, fzwrite as _fzwrite, fzhead as _fzhead


def fzread(filename, debug=0):
    """
    Load an ANA file and return the data, size, dimensions and comments in a
    dict.

    data = pyana.load(filename)
    """
    if not os.path.isfile(filename):
        raise IOError("File does not exist!")

    return _fzread(filename, debug)


def fzhead(filename: str) -> str:
    """
    Load only the header (comment) of an ANA file.

    header = pyana.getheader(filename)
    """
    if not os.path.isfile(filename):
        raise IOError("File does not exist!")

    return _fzhead(filename)


def getdata(filename, debug=0):
    """
    Load an ANA file and only return the data as a numpy array.

    data = pyana.getdata(filename)
    """
    return (fzread(filename, debug))['data']


def getheader(filename) -> str:
    """
    Load only the header (comment) of an ANA file.

    header = pyana.getheader(filename)
    """
    return fzhead(filename)


def fzwrite(filename, data, compress=1, comments=False, debug=0):
    """
    Save a 2d numpy array as an ANA file and return the bytes written, or NULL

    written = pyana.fzwrite(filename, data, compress=1, comments=False)
    """
    if comments:
        return _fzwrite(filename, data, compress, comments, debug)
    else:
        return _fzwrite(filename, data, compress, '', debug)


def writeto(filename, data, compress=1, comments=False, debug=0):
    """
    Similar as pyana.fzwrite().
    """
    return fzwrite(filename, data, compress, comments, debug)


# --- Selftesting using unittest starts below this line ---
class PyanaTests(unittest.TestCase):
    def setUp(self):
        # Create a test image, store it, reread it and compare
        import numpy as N
        self.numpy = N
        self.img_size = (456, 345)
        self.img_src = N.arange(N.product(self.img_size))
        self.img_src.shape = self.img_size
        self.img_i8 = self.img_src * 2 ** 8 / self.img_src.max()
        self.img_i8 = self.img_i8.astype(N.int8)
        self.img_i16 = self.img_src * 2 ** 16 / self.img_src.max()
        self.img_i16 = self.img_i16.astype(N.int16)
        self.img_f32 = self.img_src * 1.0 / self.img_src.max()
        self.img_f32 = self.img_f32.astype(N.float32)

    def runTests(self):
        unittest.TextTestRunner(verbosity=2).run(self.suite())

    def suite(self):
        return unittest.TestLoader().loadTestsFromTestCase(PyanaTests)

    def test_read_header(self):
        file = os.path.join(os.path.dirname(__file__), '..', 'testdata', 'testfile.f0')
        header = fzhead(file)
        self.assertEqual(header, 'Time=1234567890')

    def test_read(self):
        file = os.path.join(os.path.dirname(__file__), '..', 'testdata', 'testfile.f0')
        data = fzread(file)
        self.assertEqual(data['header']['header'], 'Time=1234567890')
        self.assertEqual(data['header']['size'], 1200000)
        self.assertEqual(data['data'].shape, (600, 1000))

    def testi8c(self):
        # Test int 8 compressed functions
        fzwrite('/tmp/pyana-testi8c', self.img_i8, 1, 'testcase', 1)
        self.img_i8c_rec = fzread('/tmp/pyana-testi8c', 1)
        self.assertTrue(self.numpy.sum(self.img_i8c_rec['data'] - self.img_i8) == 0,
                        msg="Storing 8 bits integer data with compression failed (diff: %d)" % (
                            self.numpy.sum(self.img_i8c_rec['data'] - self.img_i8)))

    def testi8u(self):
        # Test int 8 uncompressed functions
        fzwrite('/tmp/pyana-testi8u', self.img_i8, 0, 'testcase', 1)
        self.img_i8u_rec = fzread('/tmp/pyana-testi8u', 1)
        self.assertTrue(self.numpy.sum(self.img_i8u_rec['data'] - self.img_i8) == 0,
                        msg="Storing 8 bits integer data without compression failed (diff: %d)" % (
                            self.numpy.sum(self.img_i8u_rec['data'] - self.img_i8)))

    def testi16c(self):
        # Test int 16 compressed functions
        fzwrite('/tmp/pyana-testi16c', self.img_i16, 1, 'testcase', 1)
        self.img_i16c_rec = fzread('/tmp/pyana-testi16c', 1)
        self.assertTrue(self.numpy.allclose(self.img_i16c_rec['data'], self.img_i16),
                        msg="Storing 16 bits integer data with compression failed (diff: %d)" % (
                            self.numpy.sum(self.img_i16c_rec['data'] - self.img_i16)))

    def testi16u(self):
        # Test int 16 uncompressed functions
        fzwrite('/tmp/pyana-testi16u', self.img_i16, 0, 'testcase', 1)
        self.img_i16u_rec = fzread('/tmp/pyana-testi16u', 1)
        self.assertTrue(self.numpy.allclose(self.img_i16u_rec['data'], self.img_i16),
                        msg="Storing 16 bits integer data without compression failed (diff: %d)" % (
                            self.numpy.sum(self.img_i16u_rec['data'] - self.img_i16)))

    def testf32u(self):
        # Test float 32 uncompressed functions
        fzwrite('/tmp/pyana-testf32', self.img_f32, 0, 'testcase', 1)
        self.img_f32_rec = fzread('/tmp/pyana-testf32', 1)
        self.assertTrue(self.numpy.allclose(self.img_f32_rec['data'], self.img_f32),
                        msg="Storing 32 bits float data without compression failed (diff: %g)" % (
                                1.0 * self.numpy.sum(self.img_f32_rec['data'] - self.img_f32)))

    def testf32c(self):
        # Test if float 32 compressed fails
        self.assertRaises(RuntimeError, fzwrite, '/tmp/pyana-testf32', self.img_f32, 1, 'testcase', 1)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(PyanaTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
