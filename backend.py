from fastapi import FastAPI
from pydantic import BaseModel ,Field 
from typing import Annotated 
from agent import run_the_agent,order_exists
from fastapi import HTTPException
from dotenv import load_dotenv



app=FastAPI()


#validation of data using pydantic
class UserInput(BaseModel):
      order_id: Annotated[int, Field(..., gt=0, lt=100, description='Order ID for which the refund has to be processed')]


@app.post("/chat")
def  process_refund(data: UserInput):
     
     load_dotenv()
     #check if the order_id exists
     valid_order=order_exists(data.order_id)

     if valid_order == 1:
         
         result=run_the_agent(data.order_id)

         if result is None:
              print(f"Inside backend to print result{result}")
              return{
                   "final_decision": "not approved",
                   "reason": "No reason"
                   
                  }
         
        # decision, decision_reason=run_the_agent(data.order_id)
         print("when result to backend.py is not None")
         print(f"Decision : {result["decision"]}")
         print(f"Reason: {result["reasoning_logs"]}")
         return {
              "status_code": 200,
               "final_decision":result["decision"],
               "reasoning_logs":result["reasoning_logs"]
               }

     else:
          
          raise  HTTPException(status_code=400 , detail='Order does not exist')