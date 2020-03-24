#!/usr/bin/env python

import importlib
import unittest

bookstore = importlib.import_module('bookstore')
FILE = 'basket.csv'


class BookstoreTestCase(unittest.TestCase):

    def test_read_file(self):
        basket = bookstore.read_file(FILE)
        self.assertTrue(isinstance(basket, bookstore.Basket))
        self.assertEqual(len(basket.books), 6)
        self.assertEqual(basket.total, 320.5)

    def test_show_file(self):
        basket = bookstore.Basket([])
        self.assertEqual(bookstore.show_file(basket), None)

    def test_write_file(self):
        basket = bookstore.Basket([])
        self.assertEqual(bookstore.write_file(basket, 'output.txt'), None)

    def test_show_aggregate(self):
        self.assertEqual(bookstore.show_aggregate([]), None)


if __name__ == '__main__':
    unittest.main()
