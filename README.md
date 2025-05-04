# Know Your Fan 🎮

**Know Your Fan** é uma plataforma interativa voltada para a comunidade de e-sports, que permite o engajamento entre fãs e eventos. A aplicação oferece funcionalidades tanto para usuários comuns quanto para equipes que buscam entender melhor seu publico, com dashboards personalizados, autenticação segura por cookies, verificação de identidade com IA e análise de dados.

---

## 🚀 Funcionalidades

### 👤 Usuário
- Registro com upload de documentos e validação facial (OCR + AWS Rekognition)
- Login via cookies (HTTP-only)
- Participação em eventos e sorteios
- Seguir jogos e visualizar ranking de usuários
- Feed de notícias personalizadas com curadoria da IA (Gemini API)

### 🛠️ Administrador
- Login seguro para administradores
- Dashboard com:
  - Total de usuários registrados
  - Usuários por estado
  - Jogos mais seguidos
  - Engajamento por evento
  - Crescimento de usuários por mês
  - Distribuição de idade
  - Quantidade de usuários verificados
  - Eventos e sorteios ativos
  - Ranking geral de usuários

---

## 🧰 Tecnologias Utilizadas

### Backend
- FastAPI
- Tortoise ORM + PostgreSQL
- JWT + Autenticação via cookies HTTP-only
- OCR + Verificação facial (AWS Rekognition)
- Google Gemini API para classificação de notícias

### Frontend
- React + TypeScript
- Bootstrap 5
- Consumo de API com cookies para autenticação
- Dashboards interativos

---

## 📂 Estrutura do Projeto

```
KnowYourFan/
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   ├── .env
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.tsx
│   └── package.json
└── README.md
```

---

## 🔐 Autenticação

A autenticação é realizada com tokens JWT armazenados em cookies HTTP-only, protegidos contra acesso por JavaScript. Sessões duram 2 horas por padrão.

---

## 📊 Rotas Administrativas

- `GET /admin/total_users`
- `GET /admin/users_by_state`
- `GET /admin/most_followed_games`
- `GET /admin/event_engagement`
- `GET /admin/verified-users`
- `GET /admin/age-distribution`
- `GET /admin/user-ranking`
- `GET /admin/sorteios-ativos`
- `GET /admin/eventos-ativos`
- `GET /admin/crescimento-usuarios`

---

## 🧪 Executando o Projeto

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 📘 Documentação da API

- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---
