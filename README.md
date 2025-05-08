# Fortune Cookie Backend

A repository-agnostic Flask backend API that generates fortune cookie wisdom based on user input using AWS Bedrock's Claude 3 Sonnet model. This project serves as a demonstration for implementing CI/CD pipelines using AWS Amplify and CodeBuild across different Git providers.

## Overview

This backend API is part of a demo application showcasing how to build repository-agnostic CI/CD pipelines. It works alongside a Next.js frontend (in a separate repository) to provide AI-generated fortune cookie wisdom.

### Features

- Flask REST API with CORS support
- Integration with AWS Bedrock (Claude 3 Sonnet) for AI-generated responses
- Dockerized application for easy deployment
- AWS CodeBuild configuration for CI/CD pipeline
- Designed for deployment on AWS ECS Fargate

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check endpoint for AWS services |
| `/fortune` | POST | Accepts a JSON payload with `input` field and returns fortune cookie wisdom |

### Example Request

```bash
curl -X POST http://localhost:8080/fortune \
  -H "Content-Type: application/json" \
  -d '{"input": "starting a new job"}'
```

### Example Response

```json
{
  "fortune": "New paths reveal talents undiscovered; your greatest strength often emerges from unfamiliar terrain."
}
```

## Local Development

### Prerequisites

- Python 3.11+
- Docker (for containerized testing)
- AWS CLI configured with appropriate permissions for Bedrock

### Setup

1. Clone this repository:
   ```bash
   git clone [repository-url]
   cd fortune_cookie_backend
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set environment variables:
   ```bash
   export AWS_REGION=us-west-2  # Or your preferred AWS region
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   ```

4. Run the application:
   ```bash
   python app/app.py
   ```

### Quick Local Hosting Options

#### Option 1: Direct Flask Development Server

For quick testing with the built-in Flask development server:

```bash
# Make sure you're in the project root
cd /path/to/fortune_cookie_backend
flask --app app/app.py run --host=0.0.0.0 --port=8080
```

#### Option 2: Using Gunicorn (Recommended for Better Performance)

```bash
# Install gunicorn if not already installed
pip install gunicorn

# Run with gunicorn
gunicorn --bind 0.0.0.0:8000 "app.app:app"
```

#### Option 3: Using Docker

Build and run the container locally:

```bash
docker build -t fortune-cookie-backend .
docker run -p 8000:8000 -e AWS_REGION=us-west-2 -e AWS_ACCESS_KEY_ID=your_key -e AWS_SECRET_ACCESS_KEY=your_secret fortune-cookie-backend
```

### Testing Your Local Deployment

Once running, test that your API is working:

```bash
# Health check
curl http://localhost:8000/health

# Test fortune endpoint
curl -X POST http://localhost:8000/fortune \
  -H "Content-Type: application/json" \
  -d '{"input": "learning new technology"}'
```

### Troubleshooting

- **AWS Credentials**: Make sure your AWS credentials have permission to access Bedrock service
- **CORS Issues**: When testing with a frontend, ensure your frontend origin is allowed in the CORS configuration
- **Port Conflicts**: If port 8080 is already in use, change the port number in your run command

## Deployment with AWS

This application is designed to be deployed using AWS CodeBuild and ECS Fargate as part of a repository-agnostic CI/CD pipeline.

### AWS Services Used

- **AWS CodeBuild**: Builds the Docker image from this repository
- **Amazon ECR**: Stores the Docker image
- **Amazon ECS Fargate**: Runs the containerized application
- **AWS Bedrock**: Provides AI model access for generating responses

### CI/CD Pipeline

The included `buildspec.yml` file configures AWS CodeBuild to:

1. Build the Docker image
2. Push the image to Amazon ECR
3. Update the ECS service to deploy the new container

### Required Environment Variables for CodeBuild

- `AWS_DEFAULT_REGION`: The AWS region for deployment
- `ECR_REPOSITORY_URI`: URI of your ECR repository
- `ECS_CLUSTER`: Name of your ECS cluster
- `ECS_SERVICE`: Name of your ECS service

## Session Demo Information

This backend is part of a demonstration on building repository-agnostic CI/CD pipelines using AWS services. The complete demonstration includes:

- This Flask backend that integrates with AWS Bedrock
- A Next.js frontend deployed with AWS Amplify
- CI/CD pipelines that work across different Git providers (GitHub, GitLab, etc.)

For more information about the session, please refer to the session description and accompanying materials.

## License

[MIT License](LICENSE)