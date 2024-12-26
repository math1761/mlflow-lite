# MLFlow-Lite

MLFlow-Lite is a lightweight, open-source solution for managing and deploying machine learning models. Designed for small teams and individual developers, it provides a simple, resource-efficient alternative to traditional ML management tools.

## Features

- **Model Management**: Versioning, metadata tracking, and performance evaluation.
- **Automatic Deployment**: Generate REST APIs for models with `/predict` and `/health` endpoints.
- **Monitoring**: Real-time metrics collection and visualization.
- **CI/CD Integration**: Streamlined pipelines for testing, building, and deploying models.
- **User Dashboard**: Visualize and manage deployed models and metrics.

## Installation

### Requirements

- Python 3.10+
- Docker (optional for containerized deployment)
- PostgreSQL or SQLite

### Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/mlflow-lite.git
   cd mlflow-lite
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the application:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

### Docker Setup

1. Build the Docker image:
   ```bash
   docker build -t mlflow-lite .
   ```
2. Run the container:
   ```bash
   docker run -p 8000:8000 mlflow-lite
   ```

## Usage

### REST API

#### `/models/` (POST)
Register a new model version.
```json
{
  "name": "model_A",
  "version": "1.0",
  "accuracy": 0.92
}
```

#### `/models/` (GET)
List all registered model versions.

#### `/models/{model_id}` (GET)
Retrieve details of a specific model version.

#### `/predict` (POST)
Submit data to a deployed model for predictions.
```json
{
  "model_name": "model_A",
  "version": "1.0",
  "data": [[1.0, 2.0, 3.0]]
}
```

#### `/health` (GET)
Check the status of a deployed model.

## Configuration

Set environment variables in a `.env` file:

```env
DATABASE_URL=postgresql://user:password@localhost/mlflow_lite
STORAGE_PATH=./models
PORT=8000
```

## Development

### Testing

1. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
2. Run tests:
   ```bash
   pytest --cov=app tests/
   ```

### Contributing

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit and push changes:
   ```bash
   git push origin feature-name
   ```
4. Submit a pull request.

## Roadmap

- Integration with Prometheus and Grafana.
- Command-line interface for easier usage.
- Extended monitoring features.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
