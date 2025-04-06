from flask import Blueprint, request, jsonify
from tools.transactions import get_transactions, get_transaction
from tools.invoices import get_invoices
from tools.organization import get_organization_details


bp = Blueprint("tools", __name__, url_prefix="/tools")

@bp.route("/hello", methods=["GET"])
def hello_tool():
    return {"message": "Hello from the /tools route!"}, 


@bp.route("/organization", methods=["GET"])
def organization():
    org_id = request.args.get("org_id") 

    if not org_id:
        return jsonify({"error": "Missing org_id parameter"}), 400

    result = get_organization_details(org_id)
    return jsonify(result)

@bp.route("/transactions", methods=["GET"])
def transactions():
    org_id = request.args.get("org_id") 

    if not org_id:
        return jsonify({"error": "Missing org_id parameter"}), 400
        
    result = get_transactions(org_id)
    return jsonify(result)

@bp.route("/transaction", methods=["GET"])
def transactions():
    transaction_id = request.args.get("txn_id") 

    if not transaction_id:
        return jsonify({"error": "Missing org_id parameter"}), 400
        
    result = get_transaction(transaction_id)
    return jsonify(result)

@bp.route("/invoices", methods=["GET"])
def invoices():
    org_id = request.args.get("org_id") 

    if not org_id:
        return jsonify({"error": "Missing org_id parameter"}), 400

    result = get_invoices(org_id)
    return jsonify(result)
