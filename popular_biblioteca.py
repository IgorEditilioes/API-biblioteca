from biblioteca.models import Autor, Livro
from datetime import datetime

# Lista de autores e livros
dados = [
    {"autor": "Machado de Assis", "titulo": "Dom Casmurro", "genero": "Romance", "ano_publicacao": 1899},
    {"autor": "Paulo Coelho", "titulo": "O Alquimista", "genero": "Ficção filosófica", "ano_publicacao": 1988},
    {"autor": "Gabriel García Márquez", "titulo": "Cem Anos de Solidão", "genero": "Realismo mágico", "ano_publicacao": 1967},
    {"autor": "George Orwell", "titulo": "A Revolução dos Bichos", "genero": "Sátira política", "ano_publicacao": 1945},
    {"autor": "Antoine de Saint-Exupéry", "titulo": "O Pequeno Príncipe", "genero": "Fábula", "ano_publicacao": 1943},
    {"autor": "J.R.R. Tolkien", "titulo": "O Senhor dos Anéis: A Sociedade do Anel", "genero": "Fantasia", "ano_publicacao": 1954},
    {"autor": "Jane Austen", "titulo": "Orgulho e Preconceito", "genero": "Romance", "ano_publicacao": 1813},
    {"autor": "Dan Brown", "titulo": "O Código Da Vinci", "genero": "Suspense", "ano_publicacao": 2003},
]

for item in dados:
    autor, created = Autor.objects.get_or_create(nome=item["autor"])
    Livro.objects.get_or_create(
        titulo=item["titulo"],
        autor=autor,
        genero=item["genero"],
        ano_publicacao=datetime(item["ano_publicacao"], 1, 1),
        disponivel=True
    )

print("✅ Autores e livros adicionados com sucesso!")