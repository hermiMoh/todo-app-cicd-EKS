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