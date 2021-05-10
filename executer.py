import logging
from cowin_helper import CowinWorker
import notification
import sys
import schedule
import time
from dotenv import load_dotenv
import os

load_dotenv()
frequency = os.getenv("FREQUENCY")

class Executer:
    def __init__(self):          
        self.cowin_worker = CowinWorker()
                
    def execute_by_district(self,state, district, age):
        msg =self.cowin_worker.get_slot_by_district(state, district, age)        
        center_names = []
        if msg is not None:
            if msg.get("status code")==200:
                for center in msg["details"]:
                    center_names.append(center["name"] for center in msg["details"])
                result = notification.send_notification(title = msg["message"], message = f"Available centers are {center_names}", timeout = 10)
                logging.info(result)
                logging.info(msg["details"])
            else:
                logging.error(msg)
        else:
            logging.info(f"No slots are available in the centers found in {district} area")
            
    def execute_by_pin(self,pin, age):
        msg =self.cowin_worker.get_slot_by_pin(pin,age)        
        center_names = []
        if msg is not None:
            if msg.get("status code")==200:
                for center in msg["details"]:
                    center_names.append(center["name"])                
                result = notification.send_notification(title = msg["message"], message = f"Available centers are {center_names}", timeout = 10)
                logging.info(result)
            else:
                logging.error(msg)
        else:
            logging.info(f"No slots are available in the centers found in {pin} code")
               
def main():   
    if len(sys.argv)==1 or sys.argv[1] not in ["pin", "district"]:
        logging.warning("Either you missed to give the choice or invalid choice given, please choose between 'pin' or 'district'")
        

    elif sys.argv[1]=="district":
        if len(sys.argv)<5:
            logging.warning("Please enter all the parameters for getting slots by district")
        else:        
            state = sys.argv[2]
            district = sys.argv[3]
            age = sys.argv[4]
            logging.info(f"{district} selected")
            ex = Executer()
            ex.execute_by_district(state, district, int(age))   
        
    elif sys.argv[1]=="pin":
        if len(sys.argv)!=4:
            logging.warning("Please enter all the parameters for getting slots by PIN")
        else:
            pin = sys.argv[2]
            age = sys.argv[3] 
            logging.info(f"{pin} selected")        
            ex = Executer()
            ex.execute_by_pin(pin, int(age))   
    
if __name__ == "__main__":    
    logging.basicConfig(
        filename="exec.log",
        filemode= "w",
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S"   
    )

    schedule.every(int(frequency)).seconds.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)


