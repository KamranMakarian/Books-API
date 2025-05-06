from sqlalchemy.orm import registry, relationship, Session
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey, select

engine = create_engine(
    'mysql+pymysql://root:YourPassword@localhost:3306/books',
    echo=True)


mapper_registry = registry()

Base = mapper_registry.generate_base()

class Author(Base):
       __tablename__ = 'authors'
       author_id = Column(Integer, primary_key=True)
       first_name = Column(String(length=50))
       last_name = Column(String(length=50))

       def __repr__(self):
            return "<Author(author_id='{0}', first_name='{1}', last_name='{2}')>" \
                  .format(self.author_id, self.first_name, self.last_name)

class Book(Base):
       __tablename__ = 'books'
       
       book_id = Column(Integer, primary_key=True)
       title = Column(String(length=255))
       number_of_pages = Column(Integer)

       def __repr__(self):
            return "<Book(book_id='{0}', title='{1}', number_of_pages='{2}')>" \
                  .format(self.book_id, self.title, self.number_of_pages)

class BookAuthor(Base):
       __tablename__ = 'bookauthors'

       bookauthor_id = Column(Integer, primary_key=True)
       author_id = Column(Integer, ForeignKey('authors.author_id'))
       book_id = Column(Integer, ForeignKey('books.book_id'))

       author = relationship("Author")
       book = relationship("Book")

       def __repr__(self):
            return "<BookAuthor (bookauthor_id='{0}', author_id='{1}', book_id='{2}', first_name='{3}', last_name='{4}', title='{5}')>" \
                  .format(self.bookauthor_id, self.author_id, self.book_id, self.author.first_name, self.author.last_name, self.book.title)

Base.metadata.create_all(engine)

def add_book(book: Book, author: Author):
    with Session(engine) as session:
        # Check if the book already exists
        existing_book = session.execute(
            select(Book).filter(
                Book.title == book.title,
                Book.number_of_pages == book.number_of_pages
            )
        ).scalar_one_or_none()

        if existing_book is not None:
            raise ValueError("Book already exists.")

        # Add new book
        session.add(book)
        session.flush()  # Ensure book.book_id is available

        # Check if the author already exists
        existing_author = session.execute(
            select(Author).filter(
                Author.first_name == author.first_name,
                Author.last_name == author.last_name
            )
        ).scalar_one_or_none()

        if existing_author is not None:
            author_id = existing_author.author_id
        else:
            session.add(author)
            session.flush()  # Ensure author.author_id is available
            author_id = author.author_id

        # Check if the book-author pairing already exists
        existing_pairing = session.execute(
            select(BookAuthor).filter(
                BookAuthor.book_id == book.book_id,
                BookAuthor.author_id == author_id
            )
        ).scalar_one_or_none()

        if existing_pairing is not None:
            raise ValueError("This book-author pair already exists.")

        # Add the new pairing
        pairing = BookAuthor(author_id=author_id, book_id=book.book_id)
        session.add(pairing)
        session.commit()
        print("New pairing added " + str(pairing))


def get_book(book_id: int):
    with Session(engine) as session:
        pairing = session.execute(
            select(BookAuthor).filter(BookAuthor.book_id == book_id)
        ).scalar_one_or_none()

        if pairing is None:
            return None

        book = pairing.book
        author = pairing.author

        return {
            "book": {
                "title": book.title,
                "number_of_pages": book.number_of_pages
            },
            "author": {
                "first_name": author.first_name,
                "last_name": author.last_name
            }
        }

def get_all_books():
    with Session(engine) as session:
        pairings = session.execute(select(BookAuthor)).scalars().all()

        result = []
        for pairing in pairings:
            result.append({
                "book": {
                    "title": pairing.book.title,
                    "number_of_pages": pairing.book.number_of_pages
                },
                "author": {
                    "first_name": pairing.author.first_name,
                    "last_name": pairing.author.last_name
                }
            })

        return result
    
def update_book(book_id: int, new_title: str, new_pages: int):
    with Session(engine) as session:
        book = session.execute(
            select(Book).filter(Book.book_id == book_id)
        ).scalar_one_or_none()

        if book is None:
            return None  # let FastAPI return 404

        book.title = new_title
        book.number_of_pages = new_pages
        session.commit()

        # Get related author from pairing
        pairing = session.execute(
            select(BookAuthor).filter(BookAuthor.book_id == book_id)
        ).scalar_one_or_none()

        if pairing:
            author = pairing.author
        else:
            author = None

        return {
            "book": {
                "title": book.title,
                "number_of_pages": book.number_of_pages
            },
            "author": {
                "first_name": author.first_name,
                "last_name": author.last_name
            } if author else None
        }

def delete_book(book_id: int):
    with Session(engine) as session:
        # Check if book exists
        book = session.execute(
            select(Book).filter(Book.book_id == book_id)
        ).scalar_one_or_none()

        if book is None:
            return False  # Let FastAPI return 404

        # Delete any pairings
        session.execute(
            select(BookAuthor).filter(BookAuthor.book_id == book_id)
        ).scalars().all()
        session.query(BookAuthor).filter(BookAuthor.book_id == book_id).delete()

        # Delete the book
        session.delete(book)
        session.commit()
        return True
    
def search_books_by_title(keyword: str):
    with Session(engine) as session:
        # Use LIKE operator with wildcards and case-insensitive matching
        keyword_pattern = f"%{keyword}%"

        pairings = session.execute(
            select(BookAuthor).join(Book).filter(Book.title.ilike(keyword_pattern))
        ).scalars().all()

        result = []
        for pairing in pairings:
            result.append({
                "book": {
                    "title": pairing.book.title,
                    "number_of_pages": pairing.book.number_of_pages
                },
                "author": {
                    "first_name": pairing.author.first_name,
                    "last_name": pairing.author.last_name
                }
            })

        return result

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Tables created successfully!")
