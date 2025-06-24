# API de Gestão de Alertas e Imagens de Ocorrências

Esta API foi desenvolvida para gerenciar alertas de ocorrências e o upload de imagens relacionadas. Ela permite o registro de novos alertas com detalhes como gênero, tipo de ocorrência e localização, além de possibilitar a listagem de alertas recentes e o armazenamento de imagens com suas respectivas categorias e descrições.

---

## Funcionalidades

* **Registro de Alertas:** Adicione novos alertas com informações detalhadas.
* **Listagem de Alertas:** Recupere alertas das últimas 24 horas, ordenados cronologicamente.
* **Consulta de Alerta em Tempo Real:** Integração com um serviço externo para obter informações de risco em tempo real.
* **Upload de Imagens:** Envie imagens de ocorrências com metadados como categoria, localização e descrição.
* **Listagem de Imagens:** Recupere todas as imagens cadastradas, com as fotos codificadas em Base64.

---

## Tecnologias Utilizadas

* **Python:** Linguagem de programação principal.
* **Flask:** Microframework web para Python.
* **Flask-CORS:** Extensão para lidar com Cross-Origin Resource Sharing.
* **Flask-SQLAlchemy:** Extensão para interagir com bancos de dados relacionais.
* **MySQL:** Banco de dados utilizado para persistência dos dados.
* **python-dotenv:** Para gerenciar variáveis de ambiente.
* **requests:** Para realizar requisições HTTP a serviços externos.

---

## Primeiros Passos

Siga estas instruções para configurar e executar a API localmente.

### Pré-requisitos

Certifique-se de ter o seguinte instalado em sua máquina:

* **Python 3.8+**
* **pip** (gerenciador de pacotes do Python)
* **MySQL Server**

### Configuração do Banco de Dados

1.  Crie um banco de dados MySQL para este projeto. Por exemplo, `ocorrencias_db`.

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do seu projeto com as seguintes variáveis:

```dotenv
MYSQL_USER=seu_usuario_mysql
MYSQL_PASSWORD=sua_senha_mysql
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=ocorrencias_db

Rode o comando 'pip install -r requirements.txt' para instalar os requirements e depois **python app.py** para rodar a aplicação
