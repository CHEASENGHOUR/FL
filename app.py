from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'test'
app.config['MYSQL_PORT'] = 3308
mysql = MySQL(app)


# Configuration for file upload
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET'])
def index():
    curcor = mysql.connection.cursor()
    curcor.execute("SELECT * FROM data")
    data = curcor.fetchall()
    curcor.close()
    return render_template('index.html', data=data)


@app.route('/upload', methods=['POST'])
def upload():
    cursor = mysql.connection.cursor()
    name = request.form['name']
    password = request.form['password']
    file = request.files['file']

    # convert file name
    filename = file.filename
    # save file to uploads folder
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    quary = """
        INSERT INTO data(name, password, img) VALUES (%s, %s, %s)
    """
    cursor.execute(quary, (name, password, filename))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('index'))


@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        id_data = request.form['ID']
        name = request.form['name']
        password = request.form['password']
        file = request.files['file']
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        quary = """
        UPDATE data SET name = %s, password = %s, img = %s WHERE id = %s
        """
        cursor.execute(quary, (name, password, filename, id_data))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('index'))


@app.route('/delete/<int:Data_ID>', methods=['GET'])
def delete(Data_ID):
    cursor = mysql.connection.cursor()
    quary = """
        DELETE FROM data WHERE id = %s
    """
    cursor.execute(quary, (Data_ID,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
