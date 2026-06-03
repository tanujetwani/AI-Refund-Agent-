Project: AI Customer Support Refund Agent

This project processes or denies e-commerce refunds.




Architecture Overview Of Project:

An order id is given in the chat window and on pressing "Enter",the agent decides whether the Refund for the order id given in chat window will be "APPROVED", "DENIED" or "ESCALATED".




Flow of the Application:

The streamlit UI requests the FASTAPI endpoint("/chat") and sends the order id in the HTTPrequest .
The FastAPI endpoint calls the agent .
The agent has 3 tools binded to the llm.The 3 tools are:

a.get_order_details: This tool retrieves the order details given an order id.

b.get_customer_details: This tool retrieves the customer details given a customer id.

c.search_policy: This tool reads the entire Refund Policy document.

The agent is invoked with the user prompt "I need refund for order id {any eg order id} ".

A system prompt is also provided to the agent which asks the agent to retrieve the information from 3 tools and then decide whether to process or deny the refund request.

On invoking the agent  the above user prompt, it decides which tools to call and the arguments to give to those tools.
The agent then calls the tools  and retrieves the information. 

It retrieves the order details from get_order_details tool.

It retrives the customer information from get_customer_tools.

It reads the Refund Policy text document.

After retrieving the information from tools, a Business rule logic is applied which decides whether the refund request has to be "APPROVED", "DENIED" or "ESCALATED".

Although the agent replies whether to process or deny the refund, but a business rule logic is applied to decide whether the refund request should be denied or processed. This is because so that the refunds are handled safely and legally.It may happen that the llm might give a wrong decision on refund request.So to avoid any problems ,business rule logic is applied for deciding on the refund request.

The final decision and the agents internal reasoning behind the refund request is returned to the fastapi endpoint which then returns it to the streamlit UI.
The streamlit UI finally dispalys the  result.



Tech Stack:
Database: SQLITE3 ,
Ai Framework: Langchain ,
Backend: FastAPI ,
Frontend: Streamlit


NO need to insert OPEN_API_KEY. I've already hard coded it in agent.py



