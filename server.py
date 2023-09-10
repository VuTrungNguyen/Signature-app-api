#import MySQLdb
from flask_mysqldb import MySQL
from flask import Flask, request, jsonify
import mysql.connector
import jwt


app = Flask(__name__)
# syntax for flask server
app.app_context().push()

# instace of mysql
db = MySQL(app)

# route for customer info
@app.route('/', methods=['POST'])
def getinfo():
  if request.method == 'POST':
    partyAName = request.form['partyAName']
    partyBName = request.form['partyBName']
    contractType = request.form['contractType']
    partyBPhone = request.form['partyBPhone']
    propertyAddress = request.form['propertyAddress']
    cur = db.connection.cursor()
    cur.execute("INSERT INTO users(partyAName, partyBName, propertyAddress) VALUES(%s, %s, %s, %s, %s)",(partyAName, partyBName, contractType, partyBPhone,propertyAddress))
    db.connection.commit()
    cur.close()
    return 'success'
  # replace render_template with the html file 
  #return render_template('index.html')

# route for signup
@app.route('/', methods=['POST'])
def signup():
  username = request.json['username']
  password = request.json['password']
  connection = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'flask_user'
  )
  cursor = connection.cursor()
  cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
  row = cursor.fetchone()
  if row is not None:
    return jsonify({'success': False, 'message': 'Username already exists'})
  else:


# route for login
@app.route('/', methods=['POST'])
def login():
  """
  Logs in a user.

  Parameters:
    username (str): The username of the user.
    password (str): The password of the user.

  Returns:
    A JSON object with the following fields:
      success (bool): Whether the login was successful.
      message (str): A message describing the result of the login.
  """
  username = request.json['username']
  password = request.json['password']

  # Connect to the MySQL database
  connection = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'flask_user'
  )

  # Check if the user exists in the database
  cursor = connection.cursor()
  cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
  row = cursor.fetchone()

  # If the user exists, check if the password is correct
#   if row is not None:
#     hashed_password = row[2]
#     if pwd_context.verify(password, hashed_password):
#         # Password is correct, log in the user
#         return jsonify({'success': True, 'message': 'Login successful'})
#     else:
#         # the user doesnot exist
#         return jsonify({'success': False, 'message': 'Wrong username or password'})


#   if username == 'admin' and password == 'password':
#     return {'success': True, 'message': 'Login successful'}
#   else:
#     return {'success': False, 'message': 'Wrong username or password'}

if __name__ == '__main__':
   app.run(debug=True)
