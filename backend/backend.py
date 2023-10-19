from flask import Flask, jsonify, request
from flask_cors import CORS
import MySQLdb
from datetime import datetime

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r"/*": {'origins': "*"}})

# connect db
myhost = 'localhost'
username = 'root'
password = 'yujian233'
db_name = 'books_db'
db = MySQLdb.connect(host=myhost, user=username,
                     passwd=password, database=db_name, charset='utf8')
cursor = db.cursor()

# execute sql to create table 'books'
sql = '''CREATE TABLE IF NOT EXISTS `books` (
    `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(255) NOT NULL,
    `genre` VARCHAR(255) NOT NULL,
    `is_read` bool default 1,
    `date_created` DATETIME(6) DEFAULT NULL,
    `last_updated` DATETIME(6) DEFAULT NULL,
    `actions` TEXT DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB AUTO_INCREMENT = 1'''
cursor.execute(sql)

# execute sql to get books
sql = 'SELECT * FROM books ORDER BY id'
cursor.execute(sql)
field = cursor.description
data = cursor.fetchall()
cursor.close()

# initial data
BOOKS = []
if not data:
    t_list = [
        {'id': 1,
         'title': 'FOURTH WING',
         'genre': 'Fiction',
         'is_read': False,
         'date_created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
         'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
         'actions': ''
         },
        {'id': 2,
         'title': 'John Adams',
         'genre': 'History',
         'is_read': True,
         'date_created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
         'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
         'actions': ''
         },
        {'id': 3,
         'title': 'The Pole',
         'genre': 'Music',
         'is_read': False,
         'date_created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
         'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
         'actions': ''
         },
        {'id': 4,
         'title': 'Trail of the Lost',
         'genre': 'Travel',
         'is_read': False,
         'date_created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
         'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
         'actions': ''
         },
        {'id': 5,
         'title': 'The Long Game',
         'genre': 'Sport',
         'is_read': True,
         'date_created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
         'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
         'actions': ''
         },
        {'id': 6,
         'title': 'Of Time and Turtles',
         'genre': 'Science',
         'is_read': False,
         'date_created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
         'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
         'actions': ''
         }
    ]
    for t in t_list:
        cursor = db.cursor()
        x = [t[i] for i in t]
        sql = f'INSERT INTO books values {tuple(x)}'
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
            BOOKS.append(t)
        except Exception as e:
            db.rollback()
            print(e)

# get column name
column_list = []
for i in field:
    column_list.append(i[0])

for row in data:
    t = {}
    t[column_list[0]] = int(row[0])  # id
    t[column_list[1]] = str(row[1])  # title
    t[column_list[2]] = str(row[2])  # genre
    t[column_list[3]] = bool(row[3])  # is_read
    if row[4]:
        t[column_list[4]] = row[4].strftime(
            '%Y-%m-%d %H:%M:%S')  # date_created
    else:
        t[column_list[4]] = row[4]
    if row[5]:
        t[column_list[5]] = row[5].strftime(
            '%Y-%m-%d %H:%M:%S')  # last_updated
    else:
        t[column_list[5]] = row[5]
    t['actions'] = ''  # actions for update and delete
    BOOKS.append(t)


@app.route('/', methods=['GET'])
def greetings():
    return("Hello world!")


@app.route('/library', methods=['GET', 'POST'])
# get all and add one book
def all_books():
    response_object = {'statue': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        t = {
            'id': int(post_data.get('id')),
            'title': post_data.get('title'),
            'genre': post_data.get('genre'),
            'is_read': bool(post_data.get('is_read')),
            'date_created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'actions': ''
        }
        # execute sql
        x = [t[i] for i in t]
        sql = f'INSERT INTO books values {tuple(x)}'
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
            BOOKS.append(t)
            response_object['message'] = 'Books Added!'
        except Exception as e:
            db.rollback()
            print(e)
    if request.method == 'GET':
        response_object['books'] = BOOKS
    return jsonify(response_object)


@app.route('/library/<book_id>', methods=['PUT', 'DELETE'])
# Update and Delete
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Books Removed !'
    if request.method == 'PUT':
        post_data = request.get_json()
        t = {
            'id': int(post_data.get('id')),
            'title': post_data.get('title'),
            'genre': post_data.get('genre'),
            'is_read': bool(post_data.get('is_read')),
            'date_created': post_data.get('date_created'),
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'actions': ''
        }
        # execute sql
        sql = f'UPDATE books SET '
        for i in t:
            if t[i]:
                if type(t[i]) in [int, float]:
                    sql += f'{i}={t[i]},'
                elif type(t[i]) == bool:
                    sql += f'{i}={bool(t[i])},'
                else:
                    sql += f'{i}="{t[i]}",'
        sql = sql[:-1]
        sql += f' WHERE id = {t["id"]}'
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
            book_id = int(book_id)
            for book in BOOKS:
                if book['id'] == book_id:
                    BOOKS.remove(book)
                    BOOKS.append(t)
                    break
            response_object['message'] = 'Books Updated !'
        except Exception as e:
            db.rollback()
            print(e)
    return jsonify(response_object)


def remove_book(book_id):
    # Remove
    book_id = int(book_id)
    for book in BOOKS:
        if book['id'] == book_id:
            # execute sql
            sql = f"DELETE FROM books WHERE id={book_id}"
            cursor = db.cursor()
            try:
                cursor.execute(sql)
                db.commit()
                BOOKS.remove(book)
            except Exception as e:
                db.rollback()
                print(e)
            return True
    return False


if __name__ == "__main__":
    app.run(debug=True)
