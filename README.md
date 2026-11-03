# Care Beyond Connectivity (CBC)

### An Offline-First Digital Healthcare Infrastructure Platform

**Reliable Healthcare, With or Without Internet.**

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-REST_API-green)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![CI/CD](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-success)
![Monitoring](https://img.shields.io/badge/Monitoring-Prometheus-orange)

## Overview

Care Beyond Connectivity (CBC) is an offline-first digital healthcare infrastructure prototype designed to explore how healthcare information systems can remain reliable when internet connectivity is limited or unavailable.

The project demonstrates backend development, containerization, automated testing, continuous integration, continuous delivery, and application monitoring.

## Problem Statement

Healthcare facilities with unreliable internet connectivity may struggle to access, manage, and exchange healthcare information reliably.

Care Beyond Connectivity explores how healthcare records can be stored locally and synchronized when internet connectivity becomes available.

## Project Objectives

- Develop a REST API using Python and FastAPI.
- Store development records using SQLite and SQLAlchemy.
- Support offline record storage and synchronization.
- Handle duplicate submissions and synchronization errors.
- Containerize the application using Docker.
- Automate testing and code-quality checks.
- Publish Docker images to GitHub Container Registry.
- Monitor application performance using Prometheus and Grafana.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Backend | FastAPI |
| Database | SQLite, SQLAlchemy |
| Containerization | Docker, Docker Compose |
| Version Control | Git, GitHub |
| CI/CD | GitHub Actions |
| Container Registry | GitHub Container Registry |
| Monitoring | Prometheus, Grafana |
| Testing | Pytest, HTTPX |
| Code Quality | Ruff, mypy |

## Application Features

- Create healthcare records.
- Retrieve stored records.
- Retrieve records awaiting synchronization.
- Synchronize pending records.
- Detect duplicate patient references.
- Validate incoming requests.
- Provide application health information.
- Expose application metrics for monitoring.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Application welcome message |
| GET | `/health` | Application health check |
| POST | `/records` | Create a clinic record |
| GET | `/records` | Retrieve clinic records |
| GET | `/records/pending` | Retrieve pending records |
| PATCH | `/records/{record_id}/sync` | Synchronize a record |
| GET | `/metrics` | Expose Prometheus metrics |

Interactive API documentation:

`http://localhost:8000/docs`

## DevOps Implementation

### 1. Containerization

Docker packages the application into a container for consistent execution across environments.

### 2. Continuous Integration

GitHub Actions automatically performs:

- Dependency installation.
- Ruff code-quality checks.
- Formatting checks.
- mypy type checks.
- Automated tests.
- Docker image builds.

### 3. Continuous Delivery

Successful pushes to the main branch trigger Docker image publishing to GitHub Container Registry.

### 4. Monitoring and Observability

Prometheus collects application metrics exposed by FastAPI.

Grafana is intended to provide dashboards for visualizing monitoring data.

## Running the Project

Clone the repository:

```bash
git clone https://github.com/noreenmusasizi/AfyaSync.git
cd AfyaSync
```

Start the application:

```bash
docker compose up --build
```

Open the API documentation:

`http://localhost:8000/docs`

Check application health:

`http://localhost:8000/health`

## Docker Image

The current Docker image is published to GitHub Container Registry:

```text
ghcr.io/noreenmusasizi/afyasync:latest
```

Pull the image:

```bash
docker pull ghcr.io/noreenmusasizi/afyasync:latest
```

## Testing

Run the automated test suite:

```bash
python3 -m pytest -v
```

Run code-quality checks:

```bash
ruff check .
ruff format --check .
mypy app
```

## Project Architecture

```text
Care Beyond Connectivity
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── schemas.py
│
├── tests/
├── monitoring/
│   └── prometheus/
│       └── prometheus.yml
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Safety and Data Privacy

Care Beyond Connectivity is an educational and portfolio project.

Only synthetic data should be used for development and testing. Never use real patient information.

## Project Status

Care Beyond Connectivity demonstrates practical experience with Python backend development, Linux, Docker, CI/CD, container registries, and monitoring infrastructure.

It is an ongoing learning and portfolio project.
