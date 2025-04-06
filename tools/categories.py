
from langchain_core.tools import tool
from agent_logs.supabase_client import supabase


@tool
def get_users_transactions_categories(org_id: str):
    """Get all user defined categories for a given organization"""
    try:
        res = supabase.table("Category") \
            .select("id, name, createdAt") \
            .match({"organizationId": org_id}) \
            .execute()
        
        categories = res.data

        if not categories:
            return {"error": "No categories found"}

        return categories
    except Exception as e:
        return {"error": str(e)}

