import os
import flask
import flask_login
from model import device, users
from services import bypass, register, getData, registerUser
from flask import request

######################################################## INIT ########################################################

#Flask configuration
versao=''
app = flask.Flask(__name__)
app.secret_key = 'key'
#app.secret_key = os.environ['SECRETKEY']
#Flask-Login configuration
login_manager = flask_login.LoginManager()
login_manager.init_app(app)



######################################################## AUTHENTICATION ####################################################

#Create class that extends default flask_login User Class
class User(flask_login.UserMixin):
    def __init__(self):
        super(User, self).__init__()
        self.name = ''
        self.privileges = 1

@login_manager.user_loader
def load_user(userid: User):
    #Check if user id exists and returns its object
    user = User()
    user.id = userid.id
    user.name = userid.name
    user.privileges = userid.privileges
    return user
    

######################################################## CRUD RESOURCES ####################################################
@app.route('/api/Machines/Receive', methods=['post'])
def api():
    # userid = flask_login.current_user.get_id() 
    if flask.request.method == 'POST':
        
        content_type = request.headers.get('Content-Type')
        tag = request.headers.get('tag')
        password = request.headers.get('password')
        user  = device.iotDevice('null', 'null', False, 0.0, 0.0, 0.0, 0.0, False, 0.0)
        user.set_tag(tag)
        user.set_password(password)
        bypass.login(user)
        if user.get_logged():
            userid = User()
            userid.id = 1
            userid.name = user.get_tag()
            userid.privileges = 3
        else:
            flask.abort(401)
        
        if (content_type == 'application/json'):
            response = str(request.data)
            response = response.strip("b'[]")
            response = response.split(",")
            print(response)
            if response[0] != '':
                user.set_input01(float(response[0]))
                user.set_input02(float(response[1]))
                user.set_input03(float(response[2]))
                user.set_input04(float(response[3]))
                register.statusVerify(user)
                dataRegister = register.dataRegister(user)
                if dataRegister:
                    return str(user.get_standard())
                else:
                    flask.abort(403)
            else:
                flask.abort(400)
            
        else:
            return 'Content-Type not supported!'
        
    else:
        flask.abort(405)



@app.route('/device', methods = ['GET'])
@app.route('/device/<string:id>', methods=['GET'])
def devices(id = None):
    # userid = flask_login.current_user.get_id() 
    if flask.request.method == 'GET':
        content_type = request.headers.get('Content-Type')
        tag = request.headers.get('tag')
        password = request.headers.get('password')
        user  = users.users('null', 'null', False)
        user.set_tag(tag)
        user.set_password(password)
        bypass.login(user)
        if user.get_logged():
            
            userid = User()
            userid.id = 1
            userid.name = user.get_tag()
            userid.privileges = 3
        else:
            flask.abort(401)
        
        if (content_type == 'application/json'):
            if id is not None:
                return getData.getData(user, id)
            else:
                return getData.getAllData(user)
            
        else:
            return 'Content-Type not supported!'
        
    else:
        flask.abort(405)


@app.route('/register', methods=['GET'])
@app.route('/register/passwordUpdate/<string:devicetag>/<string:newpassword>', methods= ['PUT'])
@app.route('/register/<string:tag>/<string:password>', methods= ['POST'])
@app.route('/register/<string:tag>/<string:password>/<string:standard>', methods= ['POST'])
def register(tag = None, password = None, standard = None, devicetag = None, newpassword = None):
    if flask.request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        tagUser = request.headers.get('tag')
        passwordUser = request.headers.get('password')
        user  = users.users('null', 'null', False)
        user.set_tag(tagUser)
        user.set_password(passwordUser)
        bypass.login(user)
        if user.get_logged():
            userid = User()
            userid.id = 1
            userid.name = user.get_tag()
            userid.privileges = 3
        else:
            flask.abort(401)
        if (content_type == 'application/json'):
            tag = tag
            password = password
            if standard != None:
                userSys = device.iotDevice('null', 'null', False, 0.0, 0.0, 0.0, 0.0, False, 0.0)
                userSys.set_tag(tag)
                userSys.set_password(password)
                userSys.set_standard(standard)
            else:
                userSys = users.users('null', 'null', False)
                userSys.set_tag(tag)
                userSys.set_password(password)
            if registerUser.userValid(userSys):
                return registerUser.registerDevice(userSys)
            else:
                return 'User is already used!'
        else:
            return 'Content-Type not supported!'
    elif flask.request.method == 'PUT':
        content_type = request.headers.get('Content-Type')
        tagUser = request.headers.get('tag')
        passwordUser = request.headers.get('password')
        user  = users.users('null', 'null', False)
        user.set_tag(tagUser)
        user.set_password(passwordUser)
        bypass.login(user)
        if user.get_logged():
            userid = User()
            userid.id = 1
            userid.name = user.get_tag()
            userid.privileges = 3
        else:
            flask.abort(401)
        if (content_type == 'application/json'):
            if devicetag != None and newpassword != None:
                print(newpassword)
                return registerUser.alterRegister(str(devicetag), str(newpassword))
        else:
            return 'Content-Type not supported!'

    elif flask.request.method == 'GET':
        content_type = request.headers.get('Content-Type')
        tagUser = request.headers.get('tag')
        passwordUser = request.headers.get('password')
        user  = users.users('null', 'null', False)
        user.set_tag(tagUser)
        user.set_password(passwordUser)
        bypass.login(user)
        if user.get_logged():
            userid = User()
            userid.id = 1
            userid.name = user.get_tag()
            userid.privileges = 3
        else:
            flask.abort(401)
        if (content_type == 'application/json'):
            return registerUser.getRegister()
        else:
            return 'Content-Type not supported!'


@app.route('/standardUpdate/<string:devicetag>/<string:standard>', methods= ['PUT'])
def standardUpdate( standard = None, devicetag = None):
    if flask.request.method == 'PUT':
        content_type = request.headers.get('Content-Type')
        tagUser = request.headers.get('tag')
        passwordUser = request.headers.get('password')
        user  = users.users('null', 'null', False)
        user.set_tag(tagUser)
        user.set_password(passwordUser)
        bypass.login(user)
        if user.get_logged():
            userid = User()
            userid.id = 1
            userid.name = user.get_tag()
            userid.privileges = 3
        else:
            flask.abort(401)
        if (content_type == 'application/json'):
            if devicetag != None and standard != None:
               return registerUser.alterStandard(devicetag, standard)
                    
@app.route('/statusUpdate/<string:devicetag>/<string:status>', methods= ['PUT'])
def statusUpdate( status = None, devicetag = None):
    if flask.request.method == 'PUT':
        content_type = request.headers.get('Content-Type')
        tagUser = request.headers.get('tag')
        passwordUser = request.headers.get('password')
        user  = users.users('null', 'null', False)
        user.set_tag(tagUser)
        user.set_password(passwordUser)
        bypass.login(user)
        if user.get_logged():
            userid = User()
            userid.id = 1
            userid.name = user.get_tag()
            userid.privileges = 3
        else:
            flask.abort(401)
        if (content_type == 'application/json'):
            if devicetag != None and status != None:
                return registerUser.alterStatus(devicetag, status)
                

app.run(host='10.104.2.115', port=5000, debug=True)
