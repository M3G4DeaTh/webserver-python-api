import os
import flask
import flask_login
from datetime import datetime, timedelta
from flask import request
from datetime import datetime

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
def load_user(userid):
    #Check if user id exists and returns its object
    
    user = User()
    user.id = '1'
    user.name = 'Synvia'
    user.privileges = '3'
    return user
    

######################################################## CRUD RESOURCES ####################################################


######################################################################################################################


@app.route('/api/Machines/Receive', methods=['post'])
def api():
    global databaseOBJ
    userid = flask_login.current_user.get_id()
    dt = datetime.now()
    now = datetime.now()
    tm = datetime.timestamp(now)
    dtstring = dt.strftime ('%Y/%m/%d %H:%M:%S')   
    if flask.request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        
        if (content_type == 'application/json'):
            pct = str(request.data)
            print(pct)
            # pct = pct.strip("b'[]")
            # pct = pct.split(",")
            
            # parada1 = 0
            # parada2 = int(pct[1])
            # parada3 = 0
            # pc1 = int(pct[2])
            # pc2 = int(pct[3])
            # pc3 = int(pct[0])
            # tempo1= tm - int(2)
            # tempo2= tm - int(2)
            # print(pc1)

            # dt_fim = datetime.fromtimestamp(tm)
            # dt_inicio1 = datetime.fromtimestamp(tempo1)
            # dt_inicio2 = datetime.fromtimestamp(tempo2)

           
            # parada_1= databaseOBJ.readRaw("select id from parada where estado=true and id_maquina=1")
            # parada_2= databaseOBJ.readRaw("select id from parada where estado=true and id_maquina=2")
            # parada_3= databaseOBJ.readRaw("select id from parada where estado=true and id_maquina=3")

            # producao_1= databaseOBJ.readRaw("select id from producao where estado=true and id_maquina=1")
            # producao_2= databaseOBJ.readRaw("select id from producao where estado=true and id_maquina=2")
            # producao_3= databaseOBJ.readRaw("select id from producao where estado=true and id_maquina=3")
            # if (parada_1 == []):
            #     print(pc1)
            # print(parada_1)
            # #Producao Máquina 1
            # if(producao_1 == []):
            #     print("Máquina 1 sem OF aberta")
            # else:
            #     if(parada_1 == []):
            #         if(parada1==1):
            #             databaseOBJ.writeRaw("insert into parada(id_producao, id_motivo, id_usuario, id_maquina, inicio_parada, estado) \
            #                                 select id, 99, 1, 1,  '"+ dtstring +"', TRUE from producao \
            #                                 where estado=TRUE and id_maquina =1;")
            #             print('Adicionada parada Automatica 1')
            #     elif(parada_1[0][0] > 0):
            #         if(parada1==0):
            #             databaseOBJ.writeRaw("update parada SET (estado, fim_parada, justificativa, tempo) = \
            #                                 (FALSE, '" + dtstring +"','Parada Automatica', ('" + dtstring +"' - inicio_parada)) from \
            #                                 (select id from parada where id_maquina= 1 order by id DESC limit 1) as subquery\
            #                                 where parada.id=subquery.id and estado=TRUE")
            #             print('Retomada Produção 1 ')
            #     if(pc1==1 and parada_1 == []):
            #         print('ola')
            #         databaseOBJ.writeRaw("insert into pecas(data_inicio, data_fim, id_maquina) VALUES('"+ str(dt_inicio1) +"','"+ str(dt_fim) +"', 1)")
            #         print('Adicionado maquina 1')
            
            # if(producao_2 == []):
            #     print("Máquina 2 sem OF aberta")
            # else:
            #     if(parada_2 == []):
            #         if(parada2==1):
            #             databaseOBJ.writeRaw("insert into parada(id_producao, id_motivo, id_usuario, id_maquina, inicio_parada, estado) \
            #                                 select id, 99, 1, 2,  '"+ dtstring +"', TRUE from producao \
            #                                 where estado=TRUE and id_maquina =2;")
            #             print('Adicionada parada Automatica 2')
            #     elif(parada_2[0][0] > 0):
            #         if(parada2==0):
            #             databaseOBJ.writeRaw("update parada SET (estado, fim_parada, justificativa, tempo) = \
            #                                 (FALSE, '" + dtstring +"','Parada Automatica', ('" + dtstring +"' - inicio_parada)) from \
            #                                 (select id from parada where id_maquina= 2 order by id DESC limit 1) as subquery\
            #                                 where parada.id=subquery.id and estado=TRUE")
            #             print('Retomada Produção 2 ')
            #     if(pc2==1 and parada_2 == []):
            #         databaseOBJ.writeRaw("insert into pecas(data_inicio, data_fim, id_maquina) VALUES('"+ str(dt_inicio2) +"','"+ str(dt_fim) +"', 2)")
            #         print('Adicionado maquina 2')
            # if(producao_3 == []):
            #     print("Máquina 3 sem OF aberta")
            # else:
            #     if(parada_3 == []):
            #         if(parada3==1):
            #             databaseOBJ.writeRaw("insert into parada(id_producao, id_motivo, id_usuario, id_maquina, inicio_parada, estado) \
            #                                 select id, 99, 1, 2,  '"+ dtstring +"', TRUE from producao \
            #                                 where estado=TRUE and id_maquina =3;")
            #             print('Adicionada parada Automatica 3')
            #     elif(parada_3[0][0] > 0):
            #         if(parada3==0):
            #             databaseOBJ.writeRaw("update parada SET (estado, fim_parada, justificativa, tempo) = \
            #                                 (FALSE, '" + dtstring +"','Parada Automatica', ('" + dtstring +"' - inicio_parada)) from \
            #                                 (select id from parada where id_maquina= 3 order by id DESC limit 1) as subquery\
            #                                 where parada.id=subquery.id and estado=TRUE")
            #             print('Retomada Produção 3 ')
            #     if(pc3==1 and parada_3 == []):
            #         databaseOBJ.writeRaw("insert into pecas(data_inicio, data_fim, id_maquina) VALUES('"+ str(dt_inicio2) +"','"+ str(dt_fim) +"', 3)")
            #         print('Adicionado maquina 3')
            return '123'
            
        else:
            return 'Content-Type not supported!'
    else:
        flask.abort(405)

######################################################## VIEWS ########################################################


@app.route('/')
@app.route('/inicio')
def inicio():
    global databaseOBJ
    

    return flask.render_template('inicio.html')


app.run(debug=True)
