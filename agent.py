from langchain_core.tools import tool
import sqlite3
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from datetime import datetime
from langchain_core.messages import ToolMessage
import json
from datetime import date




def run_the_agent(order_id:int) -> dict[str, str]:

    print("Inside run_the_agent")


    @tool
    def get_customer_details(customer_id):

         """This function returns the customer details given a customer id"""
         conn=sqlite3.connect("crm.db")

         conn.row_factory=sqlite3.Row
         cursor=conn.cursor()
         row = cursor.execute(
                         """
                          SELECT *
                          FROM customers
                          WHERE cust_id = ?
                        """,
                        (customer_id,)
                        ).fetchone()
         conn.close()
         if row is None:
              print(f"No cust found with {customer_id} ")
              return[]
         
         result=[dict(row)]
         print(f"Cust1-{result}")
         return result


    @tool
    def get_order_details(order_id):
         """This function returns the order details given an order_id"""
         conn=sqlite3.connect("crm.db")

         conn.row_factory=sqlite3.Row
         cursor=conn.cursor()
         row = cursor.execute(
                     """
                       SELECT *
                       FROM orders
                       WHERE order_id = ?
                      """,
                     (order_id,)
                     ).fetchone()
         conn.close()
         result=[dict(row)]
         print(result)
         return result


    @tool
    def search_policy():

         """"This tools reads the 'Refund Policy' Document and retrieves the sections of refund policy"""
    
         with open("refund_policy.txt") as f:
            return f.read()



    

    OPENAI_API_KEY=""

    llm = ChatOpenAI(api_key = OPENAI_API_KEY, model = 'gpt-4.1-nano', temperature=0.0)

     #Creating the agent with the help of tools and llm

    today = datetime.now().strftime("%d-%m-%Y")

    agent = create_agent(
               model=llm,  # or ChatOpenAI(model="gpt-4o-mini")
               tools=[get_customer_details,get_order_details,search_policy],
               system_prompt=f"""
             You are an e-commerce refund agent.

             Your job is to determine whether
             a refund should be:

             - APPROVED
             - DENIED
             - ESCALATED

     
             You must always:
            1.You must extract the customer ID and order ID accurately.
            CRITICAL RULE: Do not mix up the Order ID and Customer ID.
            Example 1 (Correct):
            User: "Can I cancel order 4452? My ID is 8871."
            JSON Output:("order_id": "4452", "customer_id": "8871")
           "CRITICAL OPERATIONS WORKFLOW:
          
           2.You must strictly follow this two-step verification process before making any refund decisions:

            STEP 1: Call the 'get_order_details' tool using the order reference provided by the user. This tool will return the order information along with the 'customer_id'.

            STEP 2: Extract the 'customer_id' from the order details response, and immediately call the 'get_customer_details' tool to verify their customer history and lifetime value.

           3. You MUST call the 'get_customer_details' tool immediately if a order context is given to verify their history 
           4. Retrieve order information.
           5. Read refund policy.
           6. Explain reasoning.In the reasoning also include the order id details for which the refund is processed and the customer details of the customer. 
           7. Today's date is {today}. Use this to calculate the days elapsed since delivery date.Display the days elapsed since delivery date.
           8. final_sale:1 means the product is for selling finally.It cannot be refunded.
           9. final_sale:0 means the product is eligible for refund as it is not for final sale.
          10.Check properly if the refund amount is greater than $500, then it needs human approval. 


           Available tools:

           - get_customer_details
           - get_order_details
           - search_policy

           Never make assumptions.
           """
           )
    
    #invoking the agent
    result = agent.invoke(
                  {
                     "messages": [
                        {"role": "user", "content": f"I need refund for order id {order_id}"}
                       ]
                  }
          )

     
    print(f"Reasoning logs:{result['messages'][-1].content}")

    today = date.today()
        #print(today)
    today_date_str=today.strftime("%d-%m-%Y")
    today_date=datetime.strptime(today_date_str, "%d-%m-%Y")

#print(today_date)

    def evaluate_refund(order, customer)-> str :
         
         print("Inside evaluate_refund" )

         delivered_date_str= order["delivered_date"]
         order["delivered_date"]=datetime.strptime(delivered_date_str, "%d-%m-%Y")


         days_since_delivery = (today_date-order["delivered_date"]).days

         if order["final_sale"]:
                print("Inside final_sale if")
                #result_dict={"decision":"DENIED","reasoning_logs": result['messages'][-1].content}
                #return { "decision":"DENIED", "reasoning_logs": result['messages'][-1].content}
                #print(result_dict)
                #decision="DENIED"
                #reasoning_logs=result['messages'][-1].content
                #return decision,reasoning_logs
                
                return "DENIED"
         
         if order["price"] > 500:
                print("Inside price if block")

                #return { "decision":"ESCALATED", "reasoning_logs":result['messages'][-1].content}

                #decision="ESCALATED"
                #reasoning_logs=result['messages'][-1].content
                #return decision,reasoning_logs
                return "ESCALATED"

         if customer["tier"] == "Gold":
               limit = 45
         else:
               limit = 30  

         if days_since_delivery > limit:
               print("Inside days_since_delivery if block")
               #return { "decision": "DENIED" , "reasoning_logs":result['messages'][-1].content}
               #decision="DENIED"
               #reasoning_logs=result['messages'][-1].content
               #return decision,reasoning_logs
               return "DENIED"


         #return {"decision":"APPROVED" , "reasoning_logs": result['messages'][-1].content}
         return "APPROVED"



    for message in result.get("messages", []):
       #print(message)

    # Check for information fetched by the agent's tools
       
       
          if message.name == "get_order_details":
              
              print("Inside message.name=get_order_details")
              result2=message.content
              result3=(json.loads(result2)) #order details
              print(result3)
              order=result3[0]
          if message.name == "get_customer_details":
              print("Inside message.name==get_customer_details")

              result4=message.content
              result5=(json.loads(result4)) #customer details
              print(result5)
              customer=result5[0]
              #print(customer)


    final_decision=evaluate_refund(order,customer)

    result_dict={"decision":final_decision, "reasoning_logs":result['messages'][-1].content}
     
    return result_dict 
    


def order_exists(order_id:int):
     
     print("Inside order_exists")
     conn=sqlite3.connect("crm.db")
     cursor=conn.cursor()
     row = cursor.execute(
                         """
                          SELECT *
                          FROM orders
                          WHERE order_id = ?
                        """,
                          (order_id,)
                          ).fetchone()
     conn.close()
     #result=[dict(row)]
     result=row
     print(f"Result inside order_exists:{result}")
     if result is None:
           print( f"There is no order with order id {order_id}")
           return 0
     else:
          return 1