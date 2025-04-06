from flask import Blueprint, request, jsonify
from agents.categorize_transactions_agent import CategorizeTransactionsAgent

bp = Blueprint("agents", __name__, url_prefix="/agents")

@bp.route("/hello", methods=["GET"])
def hello_agent():
    return {"message": "Hello from the /agents route!"}, 200


@bp.route('/categorize', methods=['GET', 'POST'])
def categorize():
    print("----------------------------")
    # data = request.get_json()
    # if not data:
        # return jsonify({"success": False, "error": "No data provided"}), 400
    # if 'transactions' not in data or 'categories' not in data:
    #     return jsonify({"success": False, "error": "Invalid data format"}), 400
    
    transactions = [
        {
            "id": "cm8nce0a70bpl10nmpx3crvzv",
            "amount": 191.25,
            "merchant": None,
            "description": None
        },
        {
            "id": "cm8ms1bq709fv10nmecr57xte",
            "amount": -186.41,
            "description": "BEA, Apple Pay	CCV*WATERHOLE EXPLOITA,PAS466	NR:CT819216, 16.12.23/02:22	AMSTERDAM",
            "merchant": {
                "id": "cm8lcliwv077910nm3ucwjw7i",
                "name": "Lemsqzy* Macherjek"
            }
        },
        {
            "id": "cm8ms1bq709fv10nmecr57xte",
            "amount": -12.0,
            "description":"SEPA Incasso algemeen doorlopend	Incassant: NL06ZZZ412165930000	Naam: Waternet/Gem. Amsterdam	Machtiging: MD-00893924	Omschrijving: Klant: 0015879136,	 Factuur: 2022349605	IBAN: NL60RABO0110022777	Kenmerk: DBet066514715-567052704	2",
            "merchant": {
                "id": "clmhsonzg0059kg1r2zz1scr5",
                "name": "Waternet/Gem. Amsterdam"
            },
        }
    ]

    categories = [
        { "id": "clm9bbaqa0003olr1riyr0d8kl", "name": "Revenue" },
        { "id": "clm9bbaqa0005olrf60ac0kj8", "name": "Refunds" },
        { "id": "clm9bbasz0007olrb4zbksjp", "name": "Sales Marketing" },
        { "id": "clm9bbasz000bolrqeh5x8cu", "name": "Personal" },
        { "id": "clm9bbasz000eolrx72v8efn", "name": "Operating Expenses" },
        { "id": "clm9bbat7000qolrreg8jqooj", "name": "Internal Transfers" },
        { "id": "clm9bbatc000solr8zws1g3h", "name": "Vendors" },
        { "id": "clm9bbatc000volr4egj0bq9", "name": "Taxes" },
        { "id": "clm9bbatc000xol1rjzknwzwn", "name": "Financing" },
        { "id": "clqtt18d30001mi2a8m2jo7ql", "name": "Housing" },
        { "id": "clqtuu520007mi2aswldwyyw", "name": "Family" },
        { "id": "clqtuz80g0009mi2a3tl295pp", "name": "Investments" },
    ]
    
    transaction = transactions[2]

    agent = CategorizeTransactionsAgent()

    try:
        response = agent.run(
            transaction,
            categories
        )
        return jsonify({"success": True, "data": response})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500