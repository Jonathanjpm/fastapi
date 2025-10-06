# Practical Exercise with FastApi

## Project Setup

### Virtual Environment Configuration

- python3 -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt



### Run Project
```
cd src
uvicorn main:app --reload
```

### Unit Tests
```
cd src
pytest
```

### Docker run
```
docker build -t fastapi-app .
docker run -p 8000:8000 --name fastapi-container fastapi-app
```