from flask import Flask, request, redirect, render_template_string
import pymysql

app = Flask(__name__)

def get_db():
    return pymysql.connect(
        host="mysql", 
        user="root", 
        password="root", 
        database="devops"
    )

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>DevOps Storage Lab</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f9; }
        .container { max-width: 600px; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        input[type="text"] { width: 70%; padding: 10px; font-size: 16px; }
        button { padding: 10px 20px; font-size: 16px; background-color: #007BFF; color: white; border: none; cursor: pointer; }
        ul { margin-top: 20px; }
        li { font-size: 18px; padding: 5px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h2>DevOps Search Storage Lab</h2>
        <form action="/store" method="POST">
            <input type="text" name="word" placeholder="Type a word..." required autofocus>
            <button type="submit">Store</button>
        </form>
        <h3>Stored Words:</h3>
        <ul>
            {% for row in words %}
                <li><strong>{{ row[0] }}</strong></li>
            {% else %}
                <li>No words stored yet.</li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT word FROM storage ORDER BY id DESC;")
        words = cursor.fetchall()
        db.close()
        return render_template_string(HTML_TEMPLATE, words=words)
    except Exception as e:
        return f"<h1>Database Setup Needed!</h1><p>Error: {e}</p>"

@app.route('/store', methods=['POST'])
def store_word():
    word = request.form['word']
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO storage (word) VALUES (%s);", (word,))
    db.commit()
    db.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
"""
