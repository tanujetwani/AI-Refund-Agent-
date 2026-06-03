import streamlit as st
import requests
import json

st.title("AI Customer support Agent")

col1,col2=st.columns(2)

with col1:
    st.header("Chat Window")
    
    user_prompt=st.text_input("Hi,I'm your AI Customer support Refund agent.Please mention your order id  in the chat")

    response_dict={}

    if user_prompt:
        if user_prompt.isdigit():
            user_prompt2=int(user_prompt)
            url= "http://127.0.0.1:8000/chat"
            user_input={"order_id": user_prompt2}
            response=requests.post(url, json=user_input)

            response_text=response.text

        #Converting the plain JSON text into Python dictionary

            response_dict=json.loads(response_text)



        #print(f"Response Text is:{response_text}")
       
        #print("Back to app")

        #print(f"Type of Response is :{type(response)}")

        #print(f"Response is :{response}")

            data=response.json()

        #st.write(f"Your data is {data}")
        #st.write(response.result)

            if response.status_code == 200:
                decision=response_dict["final_decision"]
                reasoning_logs=response_dict["reasoning_logs"]
                st.write(f"Your refund request for order id {user_prompt} is **{decision}**")


            else:
              st.error(f"No order exists with order ID {user_prompt} ") 
          # st.write(data) 
        else:
            st.write(f"Invalid Order ID :{user_prompt}")

    response_text2=response_dict

    
with col2:
    st.header("Admin Dashboard")   

    #if response.status_code == 200 :
    if user_prompt:
        if user_prompt.isdigit():
          if response.status_code == 200:
              st.write(f"Reasoning behind the decision:{response_text2["reasoning_logs"]}")
    
          elif response.status_code == 400:
             st.write(f"There is no order with order_id: {user_prompt}")
 
          else:
              st.write("There is some error in the application")   
        
        else:
            st.write(f"Invalid order ID: {user_prompt}")