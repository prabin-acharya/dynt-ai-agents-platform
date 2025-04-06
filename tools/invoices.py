from langchain_core.tools import tool
from agent_logs.supabase_client import supabase

@tool
def get_invoices(org_id: str):
    """Get latest invoices for a given organization id"""
    try:
        res = (
            supabase
            .table("Invoice")
            .select("id", "totalAmount", "status", "dueDate", "invoice_number", "approvalStatus", "createdAt")
            .eq("organizationId", org_id)
            .order("createdAt", desc=True)
            .limit(8) \
            .execute()
        )

        if res.data:
            return res.data
        else:
            return {"error": "No invoices found"}

    except Exception as e:
        return {"error": str(e)}
