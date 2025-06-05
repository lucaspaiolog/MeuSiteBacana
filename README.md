<h1 align="center">🛒 Meu Site Bacana</h1>
<p align="center">
  Sistema de vendas online desenvolvido em Django.
</p>

<p align="center">
  <img src="https://i.imgur.com/Be9FqyQ.png" alt="Screenshot do site" width="70%">
</p>

---

## 🧠 Objetivo

Este projeto foi desenvolvido para a disciplina **Desenvolvimento Web III** do curso de **Desenvolvimento de Software Multiplataforma**, com o intuito de aplicar conhecimentos em:

- Django (Python)
- Bootstrap 5
- Consumo de APIs externas (FakeStore e ViaCEP)
- Templates e herança de layout
- Controle de sessão e autenticação
- CRUD de usuários e produtos
- Gráficos com Chart.js

---

## 🚀 Como executar o projeto

1. Crie um ambiente virtual:

   python3 -m venv ambienteVirtual  <--- Em todos os comandos se atentar a qual versão do python você tem instalada na sua máquina (python, python3 e py podem funcionar)
   ambienteVirtual\Scripts\activate

2. Instale as dependências:
 
   pip install django
   pip install pillow 


3. Aplique as migrações:
  
   python manage.py makemigrations
   python manage.py migrate
 

4. Crie um superusuário (opcional, para acessar o admin):
   
   python manage.py createsuperuser
   

5. Rode o servidor:
   
   python manage.py runserver
   

6. Acesse no navegador: `http://127.0.0.1:8000/`

## Funcionalidades

- Cadastro/Login de usuários (com preenchimento automático de CEP via API ViaCEP).
- CRUD de usuários (somente usuários autenticados podem acessar).
- CRUD de produtos (com upload de imagem, lista em cards, edição e exclusão).
- Seção “Mais Vendidos” e “Produtos Internacionais” na página de produtos.
- Checkout para compra de produtos (número de cartão, validade, CVV) e registro em model `Venda`.
- Identidade visual em verde/cinza (CSS personalizado + Bootstrap 5).
- Autenticação via sessões Django (login/logout). 
