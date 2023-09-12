from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
from werkzeug.security import check_password_hash, generate_password_hash
app = Flask(__name__)

#add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = "key"

db = SQLAlchemy(app)

print('created db?')
#db model
class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(100), nullable=False)
	password = db.Column(db.String(200), nullable=False)
	date_added = db.Column(db.DateTime, default=datetime.utcnow)

	#Create String	
	'''
	def __repr__(self):
		return '<Name %r>', % self.name
	'''
@app.route('/', methods = ['GET', 'POST'])
def login():
	if (request.method == 'POST'):
		email = request.form['email']
		password = request.form['password']

		user = Users.query.filter_by(email=email).first()
		
		if user and check_password_hash(user.password, password):
			return redirect('/home')
		else:
			print('incorrect')
			flash('Your email or password was incorrect. Please enter your information again')

	return render_template('login.html')

@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		password = request.form['password']
		'''
		exists = Users.query.filter_by(email=email).first()
		if exists:
			flash('This email has already been registered. Please sign-in')
			return redirect(url_for(''))
		'''

		user = Users(name=name, email=email, password=generate_password_hash(password))
		db.session.add(user)
		db.session.commit()
		flash('registration successful!')
		return redirect('/')
	
	return render_template('temp.html')

@app.route('/passing', methods=['GET', 'POST'])
def display():
	if request.method == 'POST':
		result = request.form
		
		
		# Send the form result data to a file
		return render_template('result_data.html', result=result)

with app.app_context():
	db.create_all()

if __name__ == '__main__':
	
	app.run(debug=True)


