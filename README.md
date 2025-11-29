API biblioteca — Documentação Oficial
Descrição do projeto

A Library API é uma aplicação desenvolvida para gerenciar o fluxo de dados de uma biblioteca.
Ela oferece funcionalidades para cadastro, listagem, atualização e remoção de livros, autores e usuários.

O sistema foi criado seguindo boas práticas de arquitetura, design de API REST, autenticação segura e documentação clara.
O objetivo principal é fornecer uma API simples, organizada e fácil de integrar com aplicações externas ou front-ends.

Tecnologias Utilizadas

Python

Django Rest Framework (DRF)

SQLite ou PostgreSQL

Django ORM

JWT Authentication

Como executar o projeto
1. Clone o repositório
git clone https://github.com/SeuUsuario/library-api.git
cd library-api

2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate     # Linux/MacOS
venv\Scripts\activate        # Windows

3. Instale as dependências
pip install -r requirements.txt

4. Execute as migrações
python manage.py migrate

5. Inicie o servidor
python manage.py runserver


A API ficará acessível em:

http://127.0.0.1:8000/

Autenticação (JWT)

Para acessar rotas protegidas, é necessário obter um token.

Requisição:

POST /api/token/

Body:

{
  "username": "seu_usuario",
  "password": "sua_senha"
}


O token retornado deve ser enviado no cabeçalho:

Authorization: Bearer seu_token

1. Endpoints de Autores
Método	Endpoint	Descrição
GET	/autores/	Lista todos os autores
POST	/autores/	Cadastra um novo autor
GET	/autores/{id}/	Detalha um autor específico
PUT	/autores/{id}/	Atualiza um autor
PATCH	/autores/{id}/	Atualização parcial
DELETE	/autores/{id}/	Remove autor

2. Endpoints de Livros
Método	Endpoint	Descrição
GET	/livros/	Lista todos os livros
POST	/livros/	Cadastra um novo livro
GET	/livros/{id}/	Detalha um livro específico
PUT	/livros/{id}/	Atualiza um livro
PATCH	/livros/{id}/	Atualização parcial
DELETE	/livros/{id}/	Remove livro

3. Endpoints de Usuários
Método	Endpoint	Descrição
GET	/usuarios/	Lista usuários cadastrados
POST	/usuarios/	Cadastra um novo usuário
GET	/usuarios/{id}/	Detalha usuário
PUT	/usuarios/{id}/	Atualiza usuário
DELETE	/usuarios/{id}/	Remove usuário

4. Endpoints de Empréstimos
Método	Endpoint	Descrição
GET	/emprestimos/	Lista todos os empréstimos
POST	/emprestimos/	Cria um novo empréstimo
GET	/emprestimos/{id}/	Detalhes de um empréstimo
PUT	/emprestimos/{id}/	Atualiza empréstimo
DELETE	/emprestimos/{id}/	Remove empréstimo
