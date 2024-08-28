import os
import yaml
import logging
from typing import Dict
from datetime import datetime

from tensorflow import keras
from fastapi import FastAPI, HTTPException

# Load config
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

model_dir = config.get("model_dir", "WSPAPI/models")
log_dir = config.get("log_dir", "WSPAPI/logs")

# Setup
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = f"{log_dir}/{current_time}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)

app = FastAPI()

models: Dict[str, keras.Model] = {}

@app.on_event("startup")
async def load_models():
    """
    Load models dynamically from the specified directory on startup.
    """
    if not os.path.exists(model_dir):
        logging.error(f"Model directory '{model_dir}' does not exist.")
        return

    logging.info(f"Loading models from directory: {model_dir}")
    for filename in os.listdir(model_dir):
        logging.info(f"Checking file: {filename}")
        if filename.endswith(".hdf5"):
            model_path = os.path.join(model_dir, filename)
            try:
                model = keras.models.load_model(model_path)
                model_name = filename[:-3]
                models[model_name] = model
                logging.info(f"Loaded model: {model_name} from {model_path}")
            except Exception as e:
                logging.error(f"Error loading model '{filename}': {e}")

@app.post("/predict/{model_name}")
async def predict(model_name: str, input_data):
    """
    Generates a prediction using the specified model.
    """
    if model_name not in models:
        raise HTTPException(status_code=404, detail=f"Model '{model_name}' not found.")

    try:
        model_input = input_data.features
        prediction = models[model_name].predict([model_input])
        return {"prediction": prediction.tolist()}
    except Exception as e:
        logging.error(f"Error predicting with model '{model_name}': {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")
    
@app.get("/models")
async def list_models():
    """
    Endpoint to list all available models.
    """
    return {"available_models": list(models.keys())}

@app.get("/health")
async def health_check():
    """
    Endpoint for health checks.
    """
    return {"status": "ok"}
