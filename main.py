from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from PyDictionary import PyDictionary
from datetime import datetime, UTC, timezone, timedelta
import sqlite3

app = Flask(__name__)
# app.config['sqlalchemy_database_uri'.upper()] = 'sqlite:///test.db'
# db = SQLAlchemy(app)
dictionary = PyDictionary()
conn = sqlite3.connect('learning-list.db')

conn. execute('CREATE TABLE IF NOT EXISTS newLearningList (word TEXT, noOfSearches) ')
conn. execute('CREATE TABLE IF NOT EXISTS masteredList (word TEXT, noOfSearches) ')


# with app.app_context():
#     db.create_all()

@app.route("/",methods=['GET','POST'])
def index():
    masteredWord = request.form.get("mastered-word")
    if masteredWord:
        with sqlite3.connect('learning-list.db') as con:
            cur = con.cursor()
            query = "INSERT INTO masteredList (word, noOfSearches) VALUES (?, ?)"
            val = (masteredWord, 1)
            cur.execute(query, val)

            query = "DELETE FROM newLearningList WHERE word = ?"
            val = (masteredWord, )
            cur.execute(query, val)

            con.commit()
    learnedWord = request.form.get("learned-word")
    if learnedWord:
        with sqlite3.connect('learning-list.db') as con:
            cur = con.cursor()
            query = "INSERT INTO newLearningList (word, noOfSearches) VALUES (?, ?)"
            val = (learnedWord, 1)
            cur.execute(query, val)

            query = "DELETE FROM masteredList WHERE word = ?"
            val = (learnedWord,)
            cur.execute(query, val)

            con.commit()

    with sqlite3.connect('learning-list.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        cur.execute("select * from newLearningList")
        learnedRows = cur.fetchall()

        cur.execute("select * from masteredList")
        masteredRows = cur.fetchall()

    return render_template("index.html", learnedRows = learnedRows, masteredRows=masteredRows)

@app.route('/delete/<string:word>', methods=['GET', 'POST'])
def delete(word):
    with sqlite3.connect('learning-list.db') as con:
        cur = con.cursor()
        query = "DELETE FROM newLearningList WHERE word = ?"
        cur.execute(query, [word])
        con.commit()
    return redirect('/')

@app.route("/search", methods = ['GET', 'POST'])
def search():
    word = request. form.get("word")
    meanings = dictionary.meaning(word)
    print(meanings)
    word_types = meanings.keys()
    with sqlite3.connect('learning-list.db') as con:
        cur = con. cursor()
        query = "INSERT INTO newLearningList (word, noOfSearches) VALUES (?, ?);"
        val = (word, 1)
        cur. execute(query, val)

        con. commit()



    return render_template("result.html",
                           word=word.capitalize(),
                           word_types=word_types,
                           meanings=meanings)
conn.close()







if __name__ == "__main__":
    app.run(host = "0.0.0.0",debug=True)