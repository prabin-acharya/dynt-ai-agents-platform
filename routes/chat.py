from flask import Blueprint, request, jsonify, render_template
from tools.transactions import get_transactions, get_transaction
from tools.invoices import get_invoices
from tools.categories import get_users_transactions_categories
from langgraph.prebuilt import create_react_agent
from prompts.chat_agent import agent_system_prompt_template
from langchain.schema import HumanMessage, AIMessage
from tools.organization import get_organization_details

bp = Blueprint("chat", __name__, url_prefix="/chat")

@bp.route("/", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")
    history = data.get("history", [])
    
    tools = [
        get_transaction,
        get_transactions,
        get_invoices,
        get_users_transactions_categories,
        get_organization_details
    ]
    
    agent = create_react_agent(
        "openai:gpt-4o-mini",
        tools=tools,
        prompt=agent_system_prompt_template
    )
    
    # Convert history to proper format
    messages = []
    for msg in history:
        if msg["type"] == "human":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["type"] == "ai":
            messages.append(AIMessage(content=msg["content"]))
    
    # Add the latest message
    messages.append(HumanMessage(content=user_message))
    
    response = agent.invoke({"messages": messages})
    
    # Extract just the latest AI message
    latest_ai_message = response["messages"][-1]
    
    # Return only the latest AI response, not the entire conversation history
    return jsonify({
        "aiResponse": latest_ai_message.content
    }), 200
    
@bp.route("/", methods=["GET"])
def chat_ui():
    return render_template("chat.html")



def serialize_message(msg):
    if isinstance(msg, HumanMessage):
        return {"type": "human", "content": msg.content}
    elif isinstance(msg, AIMessage):
        return {"type": "ai", "content": msg.content}
    else:
        return {"type": "unknown", "content": str(msg)}
    



# def create_prompt(state):
#     return [
#         {
#             "role": "system", 
#             "content": agent_system_prompt_template.format(
#                 instructions=prompt_instructions["agent_instructions"],
#                 **profile
#                 )
#         }
#     ] + state['messages']