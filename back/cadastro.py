import bcrypt
import pg8000  # Substituímos psycopg2 por pg8000
import redis
import json

# Configuração PostgreSQL com pg8000
conn_pg = pg8000.connect(
    user="postgres",
    password="*",
    database="users",
    host="rdsendpoint"
)

# Configuração Redis
r = redis.StrictRedis(host='redisendpoint, port=6379, db=0, socket_timeout=5)

# Função de cadastro
def cadastrar_usuario(nome, email, senha):
    senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
    cursor = conn_pg.cursor()
    cursor.execute("INSERT INTO usuarios (nome, email, senha_hash) VALUES (%s, %s, %s) RETURNING id",
                   (nome, email, senha_hash))
    usuario_id = cursor.fetchone()[0]
    conn_pg.commit()
    cursor.close()
    return usuario_id

# Função para buscar usuário com cache Redis
def buscar_usuario(email):
    # Verificar cache
    dados = r.get(f"usuario:{email}")
    if dados:
        return json.loads(dados)  # Converte de volta para um dicionário

    # Consultar no PostgreSQL
    cursor = conn_pg.cursor()
    cursor.execute("SELECT id, nome, email, criado_em, senha_hash FROM usuarios WHERE email = %s", (email,))
    usuario = cursor.fetchone()
    cursor.close()

    if usuario:
        # Converte o resultado para um dicionário
        usuario_dict = {
            "id": usuario[0],
            "nome": usuario[1],
            "email": usuario[2],
            "criado_em": usuario[3].isoformat(),
            "senha_hash": usuario[4].decode()  # Converte o hash de bytes para string
        }
        # Armazena no cache Redis como JSON
        r.setex(f"usuario:{email}", 86400, json.dumps(usuario_dict))  #  Expira após 24 horas
        return usuario_dict

    return None
