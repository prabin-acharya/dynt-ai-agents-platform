# Dynt AI Agents Platform

## 🧰 Tools

Tools for performing various tasks are defined in `/tools`. Here's a list of currently available tools:

- `get_transactions(org_id)`: Get the latest transactions for a given organization.
- `get_transaction(transaction_id)`: Get details of a specific transaction by its ID.
- `get_invoices(org_id)`: Get the latest invoices for a given organization.
- `get_categories(org_id)`: Get all defined categories for a given organization.
- `get_organization_details(org_id)`: Get details of a specific organization.

To add a new tool, wrap the desired Supabase call in a Python function and add it to the tools list.

**Tools are also exposed as endpoints:**

- [/tools/organization?org_id=](https://dynt-ai-agents-platform-production.up.railway.app/tools/organization?org_id=clm9bbaq00001ol1rs8s7z9p2)
- `/tools/transaction?tsx_id=`
- `/tools/transactions?org_id=`
- `/tools/invoices?org_id=`

## 🤖 Agents

The `/agents` directory contains the code for the agents. These agents perform tasks like categorizing transactions or inferring merchants. (Built with LangChain)

## 💬 Chat

[/chat](https://dynt-ai-agents-platform-production.up.railway.app/chat) serves as the foundation for a financial advisor agent. It uses all available tools to respond to user queries about transactions, invoices, and more. Additional capabilities can be added by defining and registering new tools. Right now, you can only read data with these tools but you can add new tools to update, add data.

Right now, you have to pass the organization id or the necessary parameters in the chat itself. But, once it is integrated in the dynt-app, users can simply chat and the app will manage the identification details itself. (Built with LangGraph)

````

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


    ```
````

## 📁 Repo Structure

```bash
.
├── app.py                         # Entry point for the app
├── config.py
├── agents/
│   ├── __init__.py
│   ├── base_agent.py
│   ├── categorize_transactions.py # Agent for categorizing transactions
├── tools/
│   ├── __init__.py
│   ├── invoices.py                # Tool for fetching latest invoices(8)
│   ├── transactions.py            # Tool for fetching latest transactions, transaction details
│   ├── organization.py            # Tool for fetching organization details
│   ├── categories.py              # Tool for fetching defined categories in the organization
├── routes/
│   ├── __init__.py
│   ├── chat.py
│   ├── tools.py                   # Route to expose tool endpoints
│   └── agents.py
├── prompts/
│   ├── __init__.py
│   ├── categorize_transaction.py
│   ├── chat_agent.py
├── templates/
│   ├── chat.html
├── agetn_logs/
│   ├── __init__.py
│   ├── logger.py
│   └── supabase_client.py         # Supabase client helper
│   └── supabase_logger_mixin.py  # Logging mixin for Supabase
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```
