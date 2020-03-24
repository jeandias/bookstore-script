#!/usr/bin/env python

from optparse import OptionParser
import csv
from operator import attrgetter
from itertools import groupby


class Author:
    def __init__(self, name):
        self.name = name


class Book:
    def __init__(self, title, isbn, price, authors):
        self.title = title
        self.isbn = isbn
        self.price = price
        self.authors = authors

    @property
    def list_authors(self):
        return ", ".join(map(lambda a: a.name, self.authors))


class ExclusiveBook(Book):
    @property
    def type(self):
        return 'Exclusivo'

    @property
    def discount(self):
        return self.price


class NewBook(Book):
    @property
    def type(self):
        return 'Novo'

    @property
    def discount(self):
        return self.price - self.price * 10 / 100


class UsedBook(Book):
    @property
    def type(self):
        return 'Usado'

    @property
    def discount(self):
        return self.price - self.price * 25 / 100


class Basket:
    def __init__(self, books):
        self.books = books

    @property
    def total(self):
        return sum(map(lambda b: float(b.discount), self.books))


switcher = {
    'ExclusiveBook': ExclusiveBook,
    'NewBook': NewBook,
    'UsedBook': UsedBook
}


def read_file(filename):
    with open(filename, 'r') as basket:
        reader = csv.reader(basket, delimiter=',')
        next(reader)

        books = []
        for row in reader:
            authors = [Author(author) for author in row[4].split("|")]

            book = switcher[row[0]](row[1], row[2], float(row[3]), authors)
            books.append(book)

        return Basket(books)


def show_file(basket):
    for book in basket.books:
        print(
            f"{'€{:7,.2f}'.format(book.price)}/{'{0:.2f}'.format(book.discount)}: {book.title} - {book.list_authors}"
        )


def write_file(basket, outfile):
    f = open(outfile, 'w')
    for book in basket.books:
        f.write(
            f"{'€{:7,.2f}'.format(book.discount)} [{book.type}] {book.isbn}: {book.title} - {book.list_authors}\n"
        )
    f.write('€{:7,.2f} - Total'.format(basket.total))
    f.close()


def show_aggregate(books):
    list_books = [attrgetter('isbn', 'discount', 'title', 'list_authors')(obj) for obj in books]
    data = sorted(list_books)

    for key, group in groupby(data, lambda x: x[0]):
        g = list(group)
        print(
            f"{'€{:7,.2f}'.format(sum(map(lambda b: float(b[1]), g)))} ({len(g)}) {key}: {g[0][2]} - {g[0][3]}"
        )


if __name__ == '__main__':
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)

    parser.add_option('--version', dest="version", default=1.0, type="float")
    parser.add_option('-f', '--file', dest="filename", help="file to read", metavar="FILE")
    parser.add_option('-o', '--output', dest="outfile", default="output.txt")
    parser.add_option('-d', '--displayauthors', dest="display", action="store_true", help="show only")
    parser.add_option('-a', '--aggregate', dest="aggregate", action="store_true", help="show only")

    (options, args) = parser.parse_args()

    basket = read_file(options.filename)
    show_file(basket) if options.display else write_file(basket, options.outfile)
    options.aggregate and show_aggregate(basket.books)
