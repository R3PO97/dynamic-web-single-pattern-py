# FastAPI TensorFlow Model Serving API

Dynamic model serving API built with FastAPI and TensorFlow that automatically creates prediction endpoints for each model loaded from a specified directory. It provides a flexible solution for serving machine learning models with minimal configuration, primarily intended for the initial stages of testing, though not highly scalable. Originally conceived as a component for a trading bot, this API separates the inference logic from the trading bot itself, enabling models to be hosted independently and accessed over a network.

## Project Overview

- **Dynamic Model Management**: Models are loaded dynamically from a specified directory on startup, allowing for easy updates and management without redeploying the API.

- **Concurrency**: Leveraging FastAPI’s asynchronous capabilities, the API can handle multiple prediction requests concurrently, providing low-latency responses.

## Purpose

While developing a trading bot, I recognized the need for a flexible and scalable inference service. Traditional monolithic designs where the bot and model inference are tightly coupled do not scale well, especially when experimenting with different models or strategies.

- **Testing and Experimentation**: Quickly test different models and configurations by simply dropping new model files into the designated directory.

## Key Features

- **Dynamic Model Loading**: Models are loaded from a specified directory at startup, allowing for easy updates and experimentation.
- **RESTful API Endpoints**: 
  - `/predict/{model_name}`: Make predictions using the specified model.
  - `/models`: List all currently loaded models.
  - `/health`: Check the health of the API service.
- **Logging and Monitoring**: Detailed logging for monitoring model loading and inference processes.
- **Asynchronous Handling**: Built with FastAPI to handle concurrent requests efficiently.

## Current Status

This project is still a work in progress and is primarily intended for testing and experimentation. It is not yet optimized for production deployment, and there are several areas where improvements can be made:

- **Improved Error Handling**: More robust mechanisms to handle errors during model loading and prediction.
- **Security**: Implementing authentication and authorization to secure the API endpoints.
- **Scalability**: Exploring ways to scale the service, such as containerization and orchestration.
- **Advanced Features**: Adding support for more complex model management tasks, such as model versioning or A/B testing.
