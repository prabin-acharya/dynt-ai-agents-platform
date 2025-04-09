from flask import Blueprint, request, jsonify
from agents.categorize_transactions import CategorizeTransactionsAgent
from agents.infer_merchant import InferMerchantAgent
from concurrent.futures import ThreadPoolExecutor, as_completed


bp = Blueprint("agents", __name__, url_prefix="/agents")

@bp.route("/hello", methods=["GET"])
def hello_agent():
    return {"message": "Hello from the /agents route!"}, 200


@bp.route('/categorize-transactions', methods=['POST', "GET"])
def categorize():
    # data = request.get_json()

    # if not data:
    #     return jsonify({"success": False, "error": "No data provided"}), 400
    # if 'transactions' not in data or 'categories' not in data:
    #     return jsonify({"success": False, "error": "Invalid data format"}), 400

    # transactions = data['transactions']
    # categories = data['categories']

        
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
    
    agent = CategorizeTransactionsAgent()
    results = []

    with ThreadPoolExecutor() as executor:
        future_to_tx = {
            executor.submit(agent.run, tx, categories): tx for tx in transactions
        }

        for future in as_completed(future_to_tx):
            tx = future_to_tx[future]
            try:
                result = future.result()
                result["transaction_id"] = tx["id"]  # Add original ID
                results.append(result)
            except Exception as e:
                results.append({
                    "transaction_id": tx["id"],
                    "status": "error",
                    "error": str(e)
                })

    return jsonify({
        "success": True,
        "results": results
    })

    

@bp.route('/infer-merchants', methods=['GET', 'POST'])
def infer_merchant():
    print("----------------------------")
    # data = request.get_json()
    # if not data or 'transactions' not in data:
    #     return jsonify({"success": False, "error": "Invalid input. Expected 'transactions'."}), 400

    # transactions = data['transactions']
    
    transactions = [
        {
            "id": "cm8nce0a70bpl10nmpx3crvzv",
            "amount": 191.25,
            "description": None,
            "json": {"valueDate": "2024-07-02", "bookingDate": "2024-07-02", "transactionId": "0702155941633684", "valueDateTime": "2024-07-02T16:59:52.220", "transactionAmount": {"amount": "-17.75", "currency": "EUR"}, "internalTransactionId": "130fab7296b530ba9e5c116c8ffd0edf", "balanceAfterTransaction": {"balanceType": "interimBooked", "balanceAmount": {"amount": "738.55", "currency": "EUR"}}, "proprietaryBankTransactionCode": "369", "remittanceInformationUnstructuredArray": ["BEA, Apple Pay", "KAILUA,PAS466", "NR:01143666, 02.07.24/15:59", "COSTA DA CAPA, Land: PRT"]}
        },
        {
            "id": "clzd0vxfv03ot11vmq3d2wsvn",
            "amount": -4.75,
            "description": None,
            "json": {"valueDate": "2024-08-02", "bookingDate": "2024-08-02", "transactionId": "0802184322746023", "valueDateTime": "2024-08-02T18:43:32.200", "transactionAmount": {"amount": "-4.75", "currency": "EUR"}, "internalTransactionId": "aadeb20f61a057ef89e2ba8b180481fc", "balanceAfterTransaction": {"balanceType": "interimBooked", "balanceAmount": {"amount": "404.74", "currency": "EUR"}}, "proprietaryBankTransactionCode": "426", "remittanceInformationUnstructuredArray": ["BEA, Apple Pay", "Zettle_*ijscuypje,PAS466", "NR:70105680, 02.08.24/18:43", "Amsterdam"]}
        }

    ]
    
    agent = InferMerchantAgent()
    results = []

    with ThreadPoolExecutor() as executor:
        future_to_tx = {
            executor.submit(agent.run, tx): tx for tx in transactions
        }

        for future in as_completed(future_to_tx):
            tx = future_to_tx[future]
            try:
                result = future.result()
                result["transaction_id"] = tx.get("id")
                result["status"] = "success"
                results.append(result)
            except Exception as e:
                results.append({
                    "transaction_id": tx.get("id"),
                    "status": "error",
                    "error": str(e)
                })

    return jsonify({
        "success": True,
        "results": results
    })