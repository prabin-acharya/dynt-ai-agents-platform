# DYNT AI Agents Platform

## Tools:

Tools for performing various tasks are defined at `/tools`. Here is a list of currently available tools:

- get_transactions(org_id): Get latest transactions for a given organization.
- get_transaction(transaction_id): Get a specific transaction details by its ID.
- get_invoices(org_id): Get latest invoices for a given organization.
- get_categories(org_id): Get all defined categories for a given organization.

Similarly, new tools can be added to update, add data by defining a new function wrapping the supabase call and adding it to the tools list.

## Agents

The `/agents` folder contains the code for the agents. The agents are designed to perform specific tasks like categorizing transactions, inferring merchants. (Built with Langchain)

## Chat:

`/chat` serves as the foundation for a financial advisor agent or in-app assistant. It uses all available tools to respond to user queries about transactions, invoices, and more. Additional capabilities can be added by defining and registering new tools. Right now, you can only read data with these tools but you can add new tools to update, add data.

Right now, you have to pass the organization id or the necessary parameters in the chat itself. But, once it is integrated in the dynt-app, users can simply chat and the app will manage the identification details itself. (Built with Langgraph)

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
