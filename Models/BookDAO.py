class BookDAO():
    def __init__(self, DAO):
        self.db = DAO
        self.db.table = "books"

    def delete(self, id):
        q = self.db.query("DELETE FROM books where id={}".format(id))

        return q


    def reserve(self, user_id, book_id):
        # Cek apakah user sudah meminjam buku ini dulu
        check_existing = self.db.query("SELECT * FROM reserve WHERE user_id=%s AND book_id=%s", (user_id, book_id))
        already_reserved = check_existing.fetchall()
        if len(already_reserved) > 0:
            return "already_reserved"
        
        if not self.available(book_id):
            return "err_out"

        self.db.query("INSERT INTO reserve (user_id, book_id) VALUES(%s, %s);", (user_id, book_id))
        self.db.query("UPDATE books set count=count-1 where id=%s;", (book_id,))

        return "success"

    def unreserve(self, user_id, book_id):
        # Cek apakah entri reserve ada terlebih dahulu
        check_query = "SELECT * FROM reserve WHERE user_id=%s AND book_id=%s"
        check = self.db.query(check_query, (user_id, book_id))
        existing = check.fetchall()
        
        if len(existing) == 0:
            return False
            
        # Hapus satu entri peminjaman yang terkait dengan user dan buku
        self.db.query("DELETE FROM reserve WHERE user_id=%s AND book_id=%s;", (user_id, book_id))
        
        # Update stock buku
        self.db.query("UPDATE books set count=count+1 where id=%s;", (book_id,))
        
        return True

    def getBooksByUser(self, user_id):
        # Pastikan kita mengambil kolom id dari tabel books, bukan dari reserve!
        q = self.db.query("""
            select books.*, reserve.id as reserve_id 
            from books 
            left join reserve on reserve.book_id = books.id 
            where reserve.user_id=%s
        """, (user_id,))

        books = q.fetchall()
        return books

    def getBooksCountByUser(self, user_id):
        q = self.db.query("select count(reserve.book_id) as books_count from books left join reserve on reserve.book_id = books.id where reserve.user_id={}".format(user_id))

        books = q.fetchall()

        print(books)
        return books

    def getBook(self, id):
        q = self.db.query("select * from books where id={}".format(id))

        book = q.fetchone()

        print(book)
        return book

    def available(self, id):
        book = self.getById(id)
        count = book['count']

        if count < 1:
            return False

        return True

    def getById(self, id):
        q = self.db.query("select * from books where id='{}'".format(id))

        book = q.fetchone()

        return book

    def list(self, availability=1):
        query = "SELECT * FROM books"
        if availability == 1:
            query += " WHERE availability = %s"
            books = self.db.query(query, (availability,))
        else:
            books = self.db.query(query)
        
        result = books.fetchall()
        # Selalu urutkan berdasarkan id agar posisi buku tidak berubah-ubah
        result.sort(key=lambda x: x['id'])
        return result

    def getReserverdBooksByUser(self, user_id):
        query="select concat(book_id,',') as user_books from reserve WHERE user_id={}".format(user_id)
        
        books = self.db.query(query)
        
        books = books.fetchone()

        if not books or books.get('user_books') is None:
            return {'user_books': ''}

        return books

    def search_book(self, name, availability=1):
        query="select * from books where name LIKE %s"

        # Usually when no-admin user query for book
        if availability==1: 
            query= query+" AND availability=%s"
            q = self.db.query(query, (f'%{name}%', availability))
        else:
            q = self.db.query(query, (f'%{name}%',))
            
        books = q.fetchall()
        # Urutkan hasil pencarian juga berdasarkan id
        books.sort(key=lambda x: x['id'])
        return books
    
    def add(self, name, desc, author, availability, edition, count):
        query = """
            INSERT INTO books (name, "desc", author, availability, edition, count) 
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        q = self.db.query(query, (name, desc, author, availability, edition, count))
        return q