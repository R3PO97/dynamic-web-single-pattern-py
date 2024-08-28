import uvicorn
import yaml
from WSPAPI.main import app

with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

if __name__ == "__main__":
    uvicorn.run(app, 
                host=config['server']['host'],
                port=config['server']['port'])
