# AfyaSync

### An Offline-First Healthcare Infrastructure Platform

## Overview

AfyaSync is a learning and portfolio project exploring how healthcare information systems can remain reliable when internet connectivity is limited.

The project demonstrates practical software development and DevOps principles using a REST API.

## Problem Statement

Healthcare facilities with unreliable internet connectivity may struggle to exchange information reliably. AfyaSync explores how offline data storage and later synchronization can help address this challenge.

## Project Objectives

- Develop a REST API using Python and FastAPI.
- Store development records using SQLite.
- Explore offline data storage and synchronization queues.
- Handle retries, duplicate submissions, and synchronization failures.
- Use Docker to package and run the application.
- Automate testing and quality checks with GitHub Actions.
- Explore monitoring, logging, backups, and recovery.

## Technology Stack

- Python
- FastAPI
- SQLite
- Docker
- Git and GitHub
- GitHub Actions

## Running the Project

Ensure Docker is installed and running.

From the project directory, execute:

```bash
docker compose up --build
```

Open the API documentation in your browser:

http://127.0.0.1:8000/docs

Check the health endpoint:

http://127.0.0.1:8000/health

## Project Status

AfyaSync is under active development as a learning and portfolio project.

## Safety and Data Privacy

Use synthetic data for development and testing. Never use real patient information in this learning project.
