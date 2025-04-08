from langchain_core.tools import tool
from agent_logs.supabase_client import supabase


@tool
def get_transaction(transaction_id: str):
    """Get transaction details for a given transaction id"""
    try:
        res = supabase.table("Transaction") \
            .select("id, amount, content, date") \
            .eq("id", transaction_id) \
            .single() \
            .execute()
        
        if res.data:
            return res.data
        else:
            return {"error": "Transaction not found"}
    except Exception as e:
        return {"error": str(e)}


@tool
def get_transactions(org_id:str):
    """Get latest transactions for a given organization id and user id"""
    try:
        res = supabase.table("TransactionHistory") \
            .select("id, amount, content, date") \
            .eq("organizationId", org_id) \
            .order("dateTime", desc=True) \
            .limit(8) \
            .execute()
        
        if res.data:
            return res.data
        else:
            return {"error": "No transactions found"}
        
    except Exception as e:
        return {"error": str(e)}
