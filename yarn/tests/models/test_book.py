from yarn.models.book import Book
from yarn.tests.base import BaseTestCase


class BookTestCase(BaseTestCase):

    def test_book(self):
        """Test that we can create a book."""
        attrs = dict(
            title='Book Title',
            author='Firstname Lastname',
            description='Description',
            content='Content',
            cover_image_url='https://example.com/cover.jpg',
        )
        book = Book(**attrs)
        book.save(book)
        res = Book.get(book.id)
        for attr in attrs:
            assert getattr(res, attr) == attrs[attr]
        assert book.mobile_redirect_count == 0
        assert book.desktop_redirect_count == 0
        assert book.tablet_redirect_count == 0
