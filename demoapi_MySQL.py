# MySQL database connection
# demo project to pull info from csv file
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_restful import Resource, Api, reqparse
from flask_mysqldb import MySQL

app = Flask(__name__)
api = Api(app)

# Connect to the MySQL database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_user' #this database must exist #'user_db'
db = MySQL(app)

# /users endpoint
users_table = 'users'


class Users(Resource):
    def get(self):
        # Get all users

        # Method 1:   
        # cur = db.connection.cursor()
        # cur.execute("SELECT * FROM users")
        # users = cur.fetchall()
        # cur.close()
        # return jsonify(users)

        # Method 2:
        # users = pd.read_sql("SELECT * FROM users", db.connection)
        # return jsonify(users.to_dict()), 200

        # Method 3:
        users = db.query(f'SELECT * FROM {users_table}')
        # Convert the query to a list of dictionaries
        users_list = [{
            'userId': user['userId'],
            'name': user['name'],
            'city': user['city'],
            'locations': user[3]
        } for user in users]
        return {'data': users_list}, 200

    def post(self):    
        # Add a new user
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True, type=int, location='args')
        parser.add_argument('name', required=True, type=str, location='args')
        parser.add_argument('city', required=True, type=str, location='args')
        args = parser.parse_args()

        # Check if the user already exists
        user_exists = db.query(f'SELECT * FROM {users_table} WHERE userId = {args["userId"]}')
        if len(user_exists) > 0:
            return {
                'message': f"'{args['userId']}' already exists."
            }, 409
        else:
            # Add the new user
            db.query(f'INSERT INTO {users_table} (userId, name, city) VALUES ({args["userId"]}, "{args["name"]}", "{args["city"]}")')
            return {'message': 'User created successfully'}, 201


# api.com/users
api.add_resource(Users, '/users')

if __name__ == '__main__':
    app.run(debug=True)