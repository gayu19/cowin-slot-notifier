import requests
from pprint import pprint
import json
from datetime import date
from dotenv import load_dotenv
import os
import logging

load_dotenv()
useragent = os.getenv("USERAGENT")
headers = {"Accept-Language":"hi_IN","User-Agent":useragent}

class CowinWorker: 
    def __init__(self):        
        logging.basicConfig(
        filename="cowin.log",
        filemode= "w",
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S"   
    )        
                
    def get_state_list(self):
        """To get the state list of India
        each state has state_id and state_name in it
        """
        try:         
            url = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
            response = requests.request("GET", url, headers=headers)
        except Exception as e:            
            logging.exception(str(e))
        
        if response.status_code==200:
            state_list = json.loads(response.text)["states"]
            return state_list
        else:
            msg = {"status code": response.status_code, 
                   "message":"Currently State API is not responding, try after sometime or check if headers are present while sending request",
                   "response text": response.text}            
            logging.exception(msg)    
            raise Exception(msg)     
             
        
        
    def get_district_list(self,state_name):
        """Returns district list 

        Args:
            state_name (string): [description]

        Returns:
            [type]: [description]
        """
        
        states = self.get_state_list()                    
        for state in states:
            if state["state_name"]==state_name:
                id = state["state_id"]
        
        try:
            url = f"https://cdn-api.co-vin.in/api/v2/admin/location/districts/{id}"
            response = requests.request("GET", url, headers=headers)
        except Exception as e:
            logging.exception(str(e))            
        
        if response.status_code==200:            
            district_list = json.loads(response.text)["districts"]            
            return district_list
        else:
            msg = {"status code": response.status_code, 
                   "message":"Currently districts API is not responding, try after sometime or check if headers are present while sending request",
                   "response text": response.text}            
            logging.exception(msg) 


    def get_slot_by_district(self,state_name,district_name,age):
        """Gives us the slots by district name

        Args:
            state_name (string): Name of the state to which the district belongs
            district_name (string): Name of the district 
            age (integer): min age for which you want to check the slot 18 or 45

        Returns:
            dict: returns customized message
        """
        today = date.today().strftime("%d-%m-%Y") 
        available_centers= []        
        districts = self.get_district_list(state_name)
        for district in districts:
            if district["district_name"]==district_name:
                id = district["district_id"]
        try:        
            url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={id}&date={today}"
            response = requests.request("GET", url, headers=headers)
        except Exception as e:
            logging.exception(str(e))
        
        if response.status_code==200:
            centers = json.loads(response.text)["centers"]
        
            for center in centers:        
                if len(center["sessions"])== 1:
                    if center["sessions"][0]["available_capacity"]>0 and center["sessions"][0]["min_age_limit"] == age:
                        available_centers.append(center)                        
                        msg = {"status code":response.status_code,
                                "message":"Hurry up! slots available in your area",
                                "details":available_centers}
                        logging.info(msg)
                        return msg
                    else:
                        msg = {"message":"No slots available","center_name":center["name"]}
                        logging.info(msg)
                        
                else:
                    sessions_list = center["sessions"]
                    for session in sessions_list:
                        if session["available_capacity"]>0 and session["min_age_limit"]==age:
                            available_centers.append(center)
                            msg = {"status code":response.status_code,
                                "message":"Hurry up! slots available in your area",
                                "details":available_centers}
                            logging.info(msg)
                            return msg
                        else:
                            msg = {"message":"No slots available","center_name":center["name"]}                            
                            logging.info(msg)
                            
        else:
            msg = {"status code": response.status_code, 
                   "message":"Currently slot by district API is not responding, try after sometime or check if headers are present while sending request",
                   "response text": response.text}            
            logging.exception(msg)
                    
    def get_slot_by_pin(self,pin,age):
        """Gives us slots by PIN code

        Args:
            pin (integer): [description]
            age (integer): min age for which you want to check the slot 18 or 45

        Returns:
            dict: returns customized message
        """
        today = date.today().strftime("%d-%m-%Y") 
        available_centers= []    
        try:                
            url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pin}&date={today}"
            response = requests.request("GET", url, headers=headers)
        except Exception as e:            
            logging.exception(str(e))
        
        if response.status_code==200:
            centers = json.loads(response.text)["centers"]        
            for center in centers:        
                if len(center["sessions"])== 1:
                    if center["sessions"][0]["available_capacity"]>0 and center["sessions"][0]["min_age_limit"] == age:
                        available_centers.append(center)
                        msg = {"status code":response.status_code,
                                "message":"Hurry up! slots available in your area",
                                "details":available_centers}
                        logging.info(msg)
                        return msg                    
                else:
                    sessions_list = center["sessions"]
                    for session in sessions_list:
                        if session["available_capacity"]>0 and session["min_age_limit"]==age:
                            available_centers.append(center)
                            msg = {"status code":response.status_code,
                                "message":"Hurry up! slots available in your area",
                                "details":available_centers}
                            logging.info(msg)
                            return msg                                               
                        
        else:
            msg = {"status code": response.status_code, 
                   "message":"Currently slot by PIN API is not responding, try after sometime or check if headers are present while sending request",
                   "response text": response.text} 
            return msg           
            logging.exception(msg)     

 
            