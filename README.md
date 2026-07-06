# 📝 Todo App - CI/CD Demo

A simple Todo application built with Flask (backend) and React (frontend) for demonstrating CI/CD pipelines with Jenkins.

## 🏗️ Architecture

├── backend/
│ └── Flask REST API (Python 3.9)
│ ├── SQLite database
│ └── Pytest for testing
├── frontend/
│ └── React with Vite
│ ├── Axios for API calls
│ └── Dockerized with nginx
└── docker-compose.yml

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 20+ (for local development)
- Python 3.9+ (for local development)

### Run with Docker Compose

```bash
docker compose up --build

Access:

    Frontend: http://localhost:3000

    Backend API: http://localhost:5000/api/todos

    Health Check: http://localhost:5000/api/health

    Local Development

Backend:
bash

cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py

Frontend:
bash

cd frontend
npm install
npm run dev

🧪 Testing

Backend:
bash

cd backend
pytest -v --cov=.

Frontend:
bash

cd frontend
npm test

🔄 CI/CD Pipeline (Jenkins)

This repository is configured for Jenkins CI/CD pipeline with:

    Automated testing

    Docker image building

    Multi-environment deployment

📦 Docker Images

Build individual images:
bash

# Backend
docker build -t todo-backend:latest ./backend

# Frontend
docker build -t todo-frontend:latest ./frontend

🛠️ Tech Stack
Component	Technology
Backend	Flask, Python 3.9
Database	SQLite
Frontend	React, Vite
Container	Docker
CI/CD	Jenkins
📝 License

MIT
🤝 Contributing

    Fork the repository

    Create a feature branch (git checkout -b feature/amazing-feature)

    Commit changes (git commit -m 'Add amazing feature')

    Push to branch (git push origin feature/amazing-feature)

    Open a Pull Request