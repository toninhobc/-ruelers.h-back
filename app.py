import base64
from flask import Flask,jsonify,request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os 
from datetime import datetime, timedelta 
import requests

app = Flask(__name__)
load_dotenv("./.env")
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DB')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Forms(db.Model):
    id = db.Column(db.Integer,primary_key = True, autoincrement = True)
    Genero = db.Column(db.String(100))
    ClassificacaoAlerta = db.Column(db.String(100))
    TipoOcorrencia = db.Column(db.String(100))
    HoraOcorrencia = db.Column(db.DateTime)
    Descricao = db.Column(db.String(1000))
    Localizacao = db.Column(db.String(200))

class Images(db.Model):
    id = db.Column(db.Integer,primary_key = True, autoincrement = True)
    fotoOcorrencia = db.Column(db.LargeBinary)
    Categoria = db.Column(db.String(100))
    Localizacao = db.Column(db.String(1000))
    Descricao = db.Column(db.String(1000))

@app.route('/alertas',methods=['POST'])
def adicionarNovoAlerta():
    Alerta = request.get_json()

    if 'Genero' not in Alerta or 'TipoOcorrencia' not in Alerta or 'ClassificaoAlerta' not in Alerta or 'HoraOcorrencia' not in Alerta or 'Descricao' not in Alerta or 'Localizacao' not in Alerta:
        return jsonify({"message": "Dados incompletos"}), 400

    novo_alerta = Forms(
        Genero=Alerta['Genero'],
        ClassificacaoAlerta=Alerta['ClassificacaoAlerta'],
        TipoOcorrencia=Alerta['TipoOcorrencia'],
        HoraOcorrencia=datetime.strptime(Alerta['HoraOcorrencia'], '%Y-%m-%d %H:%M:%S'),
        Descricao=Alerta['Descricao'],
        Localizacao=Alerta['Localizacao']
    )

    db.session.add(novo_alerta)
    db.session.commit()

    return jsonify({"message": "Alerta adicionado com sucesso"}), 201

@app.route('/alertas',methods=['GET'])
def listarAlertasUltimas24hrs():
    tempo_limite = datetime.now() - timedelta(hours=24)
    alertas = Forms.query.filter(Forms.HoraOcorrencia >= tempo_limite).all()

    lista_alertas = []
    for alerta in alertas:
        lista_alertas.append({
            "id": alerta.id,
            "Genero": alerta.Genero,
            "ClassificacaoAlerta": alerta.ClassificacaoAlerta,
            "TipoOcorrencia": alerta.TipoOcorrencia,
            "HoraOcorrencia": alerta.HoraOcorrencia.isoformat() if alerta.HoraOcorrencia else None,
               "Descricao": alerta.Descricao,
            "Localizacao": alerta.Localizacao
        })

    lista_alertas.sort(key=lambda x: x['HoraOcorrencia'], reverse=True)

    return jsonify(lista_alertas), 200


@app.route("/alertas-temporeal", methods=['GET'])
def alertaTemporeal():
    regiao_administrativa = request.args.get('regiao_administrativa')
    hora_ocorencia = request.args.get('hora_ocorencia')
    if not regiao_administrativa or not hora_ocorencia:
        return jsonify({"message": "Dados incompletos"}), 400

    url = "https://hook.us2.make.com/9izgak8bgq6twkuxm5fgl12kxxqxtb59"
    headers = {
        "x-make-apikey": "0000"
    }
    params = {
        "regiao_administrativa": regiao_administrativa,
        "hora_ocorencia": hora_ocorencia
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        try:
            valor = float(response.text)
            return jsonify({"risco": valor}), 200
        except ValueError:
            return jsonify({"risco": ""}), 400

    except requests.exceptions.RequestException as e:
        print("Erro na requisição:", e)
        return jsonify({"message": "Erro na API"}), 500

@app.route('/images', methods=['POST'])
def adicionarNovaImagem():
    imagem = request.files.get('fotoOcorrencia')
    categoria = request.form.get('Categoria')
    localizacao = request.form.get('Localizacao')
    descricao = request.form.get('Descricao')

    if not imagem or not categoria or not localizacao or not descricao:
        return jsonify({"message": "Dados incompletos"}), 400

    nova_imagem = Images(
        fotoOcorrencia=imagem.read(),
        Categoria=categoria,
        Localizacao=localizacao,
        Descricao=descricao
    )

    db.session.add(nova_imagem)
    db.session.commit()

    return jsonify({"message": "Imagem adicionada com sucesso"}), 201

@app.route('/images', methods=['GET'])
def listarImagens():
    imagens = Images.query.all()

    lista_imagens = []
    for imagem in imagens:
        foto_base64 = None
        if imagem.fotoOcorrencia:
            foto_base64 = base64.b64encode(imagem.fotoOcorrencia).decode('utf-8')
        lista_imagens.append({
            "id": imagem.id,
            "fotoOcorrencia": foto_base64,
            "Categoria": imagem.Categoria,
            "Localizacao": imagem.Localizacao,
            "Descricao": imagem.Descricao
        })

    return jsonify(lista_imagens), 200

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(port=5002,host='0.0.0.0',debug=True)
