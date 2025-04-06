from langchain_core.tools import tool
from agent_logs.supabase_client import supabase

@tool
def get_organization_details(org_id: str):
    """Get organization details for a given organization id"""
    try:
        res = (
            supabase
                .table("Organization") 
                .select("id, name, address, website, phone, city, state, type, createdAt")
                .eq("id", org_id)
                .single()
                .execute()
        )

        if res.data:
            return res.data
        else:
            return {"error": "No organization found"}
    except Exception as e:
        return {"error": str(e)}
