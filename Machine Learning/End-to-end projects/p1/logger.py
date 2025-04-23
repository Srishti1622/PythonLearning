import logging
import os
from datetime import datetime

# if want to have each new log in separate file and folder
# LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
# logs_path=os.path.join(os.getcwd(),"logs")
# os.makedirs(logs_path,exist_ok=True)

# LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

# logging all the logs in single file
LOGS_DIR=os.path.join(os.getcwd(),'logs')
os.makedirs(LOGS_DIR,exist_ok=True)

LOG_FILE_PATH=os.path.join(LOGS_DIR,'app.log')

logging.basicConfig(
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filemode='a',   # append mode (default)

    # if want to log only in file
    filename=LOG_FILE_PATH,  
    # if want to log in both file and console
    # handlers=[
    #     logging.FileHandler(LOG_FILE_PATH),
    #     logging.StreamHandler()
    # ]
)

# create a logger object that other modules can import
logger=logging.getLogger('P1-Project')