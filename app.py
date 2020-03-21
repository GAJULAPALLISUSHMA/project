from flask import Flask,render_template,request,flash,session,redirect,url_for
from sqlalchemy import create_engine,asc,desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from createdatabase import Customers,State,StateSchemes
from flask_uploads import IMAGES,UploadSet,configure_uploads,DOCUMENTS
from flask_login import UserMixin, login_user, current_user, logout_user, login_required, LoginManager
from flask_mail import Mail,Message
from createdatabase import *
import random
import string
app=Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='governmentschemes123@gmail.com'
app.config['MAIL_PASSWORD']='schemes@123'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)

photos=UploadSet('photos',IMAGES)
app.config['UPLOADED_PHOTOS_DEST']='static/upload_files'
configure_uploads(app,photos)
Base=declarative_base()
engine=create_engine('sqlite:///Government schemes.db',connect_args={'check_same_thread':False},echo=True)
Base.metadata.bind=engine
DBsession= sessionmaker(bind=engine)
session= DBsession()

app.debug=True
app.config['SECRET_KEY'] = 'e7a9804ba98684deefd88d6a6c8cd0db'
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/upload_files'
configure_uploads(app, photos)

Base=declarative_base()
#connect to database
engine=create_engine('sqlite:///SCHEMES.db',connect_args={'check_same_thread':False},echo=True)
Base.metadata.bind=engine
#create session
DBsession=sessionmaker(bind=engine)
session=DBsession()




@app.route('/')
def index():
	a=session.query(Customers).all()
	return render_template("index.html",a=a)


@app.route('/Home') 
def Home():
     return render_template("index.html")

@app.route('/pension') 
def pension():
     return render_template("pension.html")  

@app.route('/central_registration') 
def central_registration():
     return render_template("central_registration.html")          

@app.route('/Contact') 
def Contact():
     return render_template("Contact.html")
@app.route('/Contact_info',methods=["GET","POST"])
def Contact_info():
	if request.method=="POST":
		data=Suggestions(Name=request.form['name'],Emailaddress=request.form['email'],Mobileno=request.form['contact'],suggestions=request.form['suggestion'])
		session.add(data)
		session.commit()
		m=request.form['email']
		m1=request.form['suggestion']
		msg=Message('successfully Registerd',sender='governmentschemes123@gmail.com',recipients=['t.vani594@gmail.com',m])
		html_content=m+"\n"+m1
		msg.body=html_content
		msg.html=msg.body
		mail.send(msg)
		return redirect(url_for('index'))
	else:
		return render_template('/')


@app.route('/About') 
def About():
     return render_template("About.html")

@app.route('/vidyadeevena') 
def vidyadeevena():
     return render_template("vidyadeevena.html")

@app.route('/users')
def users():
    data=session.query(Customers).all()
    return render_template('/users.html',udata=data)

@app.route('/status')
def status():
    data=session.query(Details).all()
    return render_template('/status.html',udata=data)

@app.route('/followus') 
def followus():
     return render_template("followus.html") 

@app.route('/Aadhar') 
def Aadhar():
     return render_template("Aadhar.html") 

@app.route('/registration') 
def registration():
     return render_template("registration.html") 


@app.route('/Add_User',methods=['GET','POST'])
def Add_User():
 	if(request.method=="POST"):
 		data=Customers(Name=request.form['name'],Mobileno=request.form['phoneno'],AdharNo=request.form['adhar'],Emailaddress=request.form['email'],Password=request.form['pswd'])
 		session.add(data)
 		session.commit()

 		msg=Message('Alert',sender='governmentschemes123@gmail.com',recipients=[request.form['email']])
 		# mail.body("successfully Registerd Gov't SCHEMES wait for updates..!!!")
 		html_content='new user Registerd'
 		html_content='Registration completed'
 		msg.body=html_content
 		msg.html=msg.body
 		mail.send(msg)
 		return redirect('/signin')
 	else:
 		return render_template('signup.html')


@app.route('/signup',methods=['POST','GET']) 
def signup():
	 if request.method=='POST':
	 	 a=Customers(Name=request.form['name'],Mobileno=request.form['phoneno'],AdharNo=request.form['adhar'],Emailaddress=request.form['email'],Password=request.form['pswd'])
	 	 session.add(a)
	 	 session.commit()
	 	 flash("data added successfully")
	 	 return render_template("signup.html")
	 else:
	 	 flash('data not inserted')
	 	 return render_template("signup.html")
@app.route('/schemesall')
def schemesall():
	data=session.query(State).all()
	a=session.query(Central).all()
	return render_template('/home_two.html',data=data,a=a)

@app.route('/signin' ,methods=["GET","POST"]) 
def signin():
	if current_user.is_authenticated:
		print("hi*******************************************")
		data=session.query(State).all()
		a=session.query(Central).all()
		print(data)
		print(a)
		return redirect('/schemesall')


	try:
		if request.method=="POST":
			a=session.query(Customers).filter_by(Emailaddress=request.form["email"],Password=request.form["pswd"]).one()
			if a:
				login_user(a)
				next_page=request.args.get('next')
				return redirect(next_page) if next_page else redirect('/schemesall')
			else:
				flash("login failed","danger")
				return render_template("signin.html")
		else:
			return render_template("signin.html",title="Login")
	except Exception as e:
		flash("login failed","danger")
		return render_template("signin.html")
	return render_template("signin.html")

@app.route('/details',methods=["GET","POST"])
def Detailss():
	print("hi")
	if (request.method=="POST"):
		print("hi*********************")
		filename=photos.save(request.files['file1'])
		filename2=photos.save(request.files['file2'])
		data=Details(Name=request.form['name'],AdharNo=request.form['adhar'],Emailaddress=request.form['email'],Mobileno=request.form['phone'],AccountNO=request.form['accno'],Age=request.form['age'],image=filename,Category=request.form['a'],img=filename2)
		session.add(data)
		session.commit()
		a=request.form['email']
		content=Message('successfully Registerd',sender='governmentschemes123@gmail.com',recipients=[a])
		mail.send(content)
		return render_template('index.html')
	else:
		return render_template('vidyadeevena.html')



@app.route('/info',methods=["GET","POST"])
def Infos():
	print("hi")
	if (request.method=="POST"):
		print("hi*********************")
		filename=photos.save(request.files['file3'])
		data=Info(Name=request.form['name'],AdharNo=request.form['adhar'],Mobileno=request.form['phone'],AccountNO=request.form['accno'],Age=request.form['age'],image=filename,Category=request.form['b'])
		session.add(data)
		session.commit()
		#b=request.form['email']
		#content=Message('successfully Registerd',sender='governmentschemes123@gmail.com',recipients=[b])
		#mail.send(content)
		return render_template('index.html')
	else:
		return render_template('pension.html')

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))


# @app.route('/States') 
# def States():
#      return render_template("State.html")	

@app.route('/states',methods=['GET','POST'])
def Add_State():
	if(request.method=="POST"):
		# filename=photos.save(request.files['file1'])
		filename=photos.save(request.files['file1'])
		data=State(statename=request.form['statename'],image=filename)
		session.add(data)     
		session.commit()
		flash("data added successfully")
		return render_template("index.html")
	else:
		states=session.query(State).all()
		#flash('data not inserted')
		return render_template("State.html",states=states)
@app.route('/schemes/<state>',methods=["GET"])
def schemes(state):
	state=session.query(State).filter_by(statename=state.replace(" ","")).first()
	schemes=session.query(StateSchemes).filter_by(state_id=state.id).all()
	print(schemes)
	return render_template("ap.html",schemes=schemes)

@app.route('/centralschemes/<central>',methods=["GET"])
def centralschemes(central):
	print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
	state=session.query(Central).filter_by(central_scheme_name=central.replace(" ","")).first()
	print("%%%%%%%%%%%%%%@@@@@@@@@@@@@@@@@@@@@@@@@")
	Schemes=session.query(CentralSchemes).filter_by(central_id=state.id).all()
	print(schemes)
	return render_template("pension.html",schemes=Schemes)


@app.route('/add_schemes',methods=['POST','GET'])
def Add_StateSchemes1():
	if(request.method=="POST"):
		filename=photos.save(request.files['file1'])
		data=StateSchemes(name=request.form['schemename'],description=request.form['description'],link=request.form['link'],image=filename,state_id=request.form['stateid'])
		session.add(data)
		session.commit()
		a=session.query(Customers).all()
		l=[]
		for i in a:
			l.append(i.Emailaddress)
		print(l)
		a=l
		msg=Message('Alert',sender='governmentschemes123@gmail.com',recipients=a)
		# html_content='new scheme added'
		# html_content="new scheme added                 "   + "scheme name is :" + <b>request.form['schemename']</b>
		# msg.body=html_content
		msg.html="new scheme added                 "+" <br>"  + "scheme name is :" + "<b>"+request.form['schemename']+"</b>"+"<br>"+"Apply for scheme"+"<br>"+"To know more visit website"
		mail.send(msg)
		flash("data added successfully")
		return render_template('StateSchemes.html')
	else:
		return render_template('StateSchemes.html')
@app.route('/Aadhar' ,methods=['GET','POST'])
def Aadhars():
	if request.method=="POST":
		print("1")
		print("******************")
		a=session.query(Details).filter_by(AdharNo=request.form["adhar"]).first()
		if a:
			b=session.query(Details).filter_by(id=a.id).all()
			return  render_template('Aadhar.html',aa=b)
		else:
			flash("no adhar no found")
			return render_template('Aadhar.html')
	else:
		flash("No Data found")
		return render_template("index.html")
	

		
# @app.route('/states/<int:state_id>',methods=['GET','POST'])
# def Add_StateSchemes(state_id):
# 	if(request.method=="POST"):
# 		filename=photos.save(request.files['file1'])
# 		data=StateSchemes(name=request.form['schemename'],description=request.form['description'],link=request.form['link'],image=filename)
# 		session.add(data)
# 		session.commit()
# 		a=session.query(Customers).all()
# 		flash("data added successfully")
# 		return render_template("index.html",a=a)	
# 	else:
# 		flash('data not inserted')
# 		return render_template("StateSchemes.html",state_id=state_id)		
@app.route('/deletedata/<int:data_id>',methods=["GET"])
def deletedata(data_id):
    deleteRes=session.query(Customers).filter_by(id=data_id)
    deleteRes.delete()
    session.commit()
    return redirect('/users')
@app.route('/Customers_data')
def Customers_data():
	data=session.query(Customers).all()
	return render_template('users.html',udata=data)
# @app.route('/editdata/<int:data_id>',methods=["GET","POST"])
# def editdata(data_id):
#     edit_data=session.query(Customers).filter_by(id=data_id)
#     if request.method == "POST":
#         editdatas = session.query(Customers).filter_by(id=data_id).one()
#         editdatas.name = request.form['name']
#         session.commit()
#         return redirect('/users')
#     else:
#         editdata= session.query(Customers).filter_by(id=data_id).one()
#         return render_template("editdata.html", editRest=editdata)

@app.route('/editdata1/<int:data_id>',methods=['GET','POST'])
def editdata1(data_id):
	edit_data=session.query(Customers).filter_by(id=data_id)
	if request.method=="POST":
		editdata=session.query(Customers).filter_by(id=data_id).one()
		editdata.Name=request.form['name']
		editdata.Emailaddress=request.form['email']
		session.commit()
		return redirect('/users')
	else:
		editdata=session.query(Customers).filter_by(id=data_id).one()
		return render_template("editdata.html",editRest=editdata)
		
	
@app.route('/resetPsw',methods=['GET','POST'])     
def resetPsw():
	if request.method=="GET":
		return render_template('email.html')
	else:
		email=request.form['email']	 
		user=session.query(Customers).filter_by(Emailaddress=email).one_or_none()
		if not user:
			flash('email not found','success')   
			return redirect(url_for('index'))
		reply,token=sendEmail(email)
		if reply==True:
			reset_token=session.query(Reset_Token).filter_by(tourister_id=user.id).one_or_none()
			if not reset_token:
				reset_token=Reset_Token(tourister_id=user.id,token=token)
			else:
				reset_token.token=token
			session.add(reset_token)
			session.commit()
			flash('mail sent successfully',"success")
			return render_template('otp.html',email=email)
		else:
			flash('email sent failed'+str(token),'success')	
			return redirect(url_for('index'))


@app.route('/verifytoken/',methods=['POST','GET'])	
def verifyToken():
	if request.method == 'POST':
		print('/n'*5,'anil','POST in verifyToken')
		email=request.form['email']
		recieved_token=request.form['utoken']
		user=session.query(Customers).filter_by(Emailaddress=email).one_or_none()
		if not user:
			flash('email not found','success')
			return redirect(url_for('index'))
		reset_token=session.query(Reset_Token).filter_by(tourister_id=user.id).one_or_none()
		if not reset_token:
			flash('wrong request','success')
			return redirect(url_for('index'))
		user.Password=request.form['newpsw']
		session.add(user)
		session.commit()
		flash('password reset successfully','success')
		return redirect(url_for('index'))
	flash('something is wrong',"success")	
	return redirect(url_for('index'))


def sendEmail(email):
	try:
		to=email
		subject="reset your password"
		token=''.join(random.choice(string.ascii_uppercase+string.digits)
			      for x in range(32))
		flash('token '+token)
		message="reset your password by enter OTP  "+token
		print("\n\n\n\n",to,subject,message)
		msg=Message(subject,
		   sender=('welcometoschemes','governmentschemes123@gmail.com'),
		  recipients=[to])
		msg.body=message
		print('ok2') 
		print('ok3')
		mail.send(msg)
		print('\n\n\n\n\n\n','ok4')
		return True,token 
	except Exception as e:
	    return False,(str(e)) 

 
				

		




  	  



# @app.route('/Aadhar' ,methods=["GET","POST"]) 
# def Aadhar():
# 	if current_user.is_authenticated:
# 		print("hi*******************************************")
		
# 		return render_template('Aadhar.html')


# 	try:
# 		if request.method=="POST":
# 			a=session.query(Details).filter_by(AdharNo=request.form["adhar"]).one()
# 			if a:
# 				b=request.form.get('Name')
# 				c=request.form.get('Emailaddress')
# 				d=request.form.get('Mobileno')
# 				e=request.form.get('AccountNO')
# 				f=request.form.get('Age')
				
# 				return  render_template('Aadhar.html',a=a)
# 			else:
				
# 				return render_template("index.html")

# 		else:
# 			return render_template("Contact.html")

if __name__=='__main__':
     app.secret_key='APP_SECRET_KEY'
     login_manager=LoginManager(app)
     login_manager.login_view='signin'
     login_manager.login_message_category='info'

     @login_manager.user_loader
     def load_user(user_id):
     	  return session.query(Customers).get(int(user_id))
     app.debug = True
     app.run()
     