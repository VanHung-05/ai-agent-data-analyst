import os
import requests

from databricks import sql

HOST = "dbc-8e02bd60-745e.cloud.databricks.com"
HTTP_PATH = "/sql/1.0/warehouses/c4b9846edf9d97af"
CLIENT_ID = os.getenv("DATABRICKS_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("DATABRICKS_CLIENT_SECRET", "")


def validate_credentials(client_id: str, client_secret: str) -> None:
    if not client_id or not client_secret:
        raise RuntimeError(
            "Missing env vars DATABRICKS_CLIENT_ID / DATABRICKS_CLIENT_SECRET"
        )
    if client_id.startswith("Application_ID") or client_id.startswith("<"):
        raise RuntimeError(
            "DATABRICKS_CLIENT_ID is still a placeholder. Paste real Application ID."
        )
    if client_secret.startswith("SECRET_") or client_secret.startswith("<"):
        raise RuntimeError(
            "DATABRICKS_CLIENT_SECRET is still a placeholder. Paste real OAuth secret."
        )


def fetch_access_token(host: str, client_id: str, client_secret: str) -> str:
    token_url = f"https://{host}/oidc/v1/token"
    payload = {
        "grant_type": "client_credentials",
        "scope": "all-apis",
    }
    response = requests.post(token_url, data=payload, auth=(client_id, client_secret), timeout=30)
    if response.status_code != 200:
        raise RuntimeError(f"Token request failed ({response.status_code}): {response.text}")
    data = response.json()
    token = data.get("access_token")
    if not token:
        raise RuntimeError("Token response missing access_token")
    return token

def run_query(cursor, q):
    print(f"\nSQL> {q}")
    try:
        cursor.execute(q)
        # fetch if query returns rows
        if cursor.description:
            rows = cursor.fetchall()
            print("OK - rows:", rows[:5])
        else:
            print("OK - no result set")
    except Exception as e:
        print("ERROR:", str(e))

validate_credentials(CLIENT_ID, CLIENT_SECRET)
ACCESS_TOKEN = fetch_access_token(HOST, CLIENT_ID, CLIENT_SECRET)

with sql.connect(
    server_hostname=HOST,
    http_path=HTTP_PATH,
    access_token=ACCESS_TOKEN,
) as conn:
    with conn.cursor() as cur:
        # 1) baseline read should pass
        run_query(cur, "SELECT current_user()")
        run_query(cur, "SELECT COUNT(*) FROM ai_analyst.ecommerce.orders")

        # 2) write tests should fail
        run_query(cur, "INSERT INTO ai_analyst.ecommerce.orders VALUES ('Z998','U001','P001',1,1.00,DATE '2026-04-02','pending')")
        run_query(cur, "UPDATE ai_analyst.ecommerce.orders SET quantity = 99 WHERE order_id = 'O001'")
        run_query(cur, "DELETE FROM ai_analyst.ecommerce.orders WHERE order_id = 'O001'")