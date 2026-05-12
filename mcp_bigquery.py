from google.cloud import bigquery

client = bigquery.Client()

def query_transactions(sql_query: str):
    """Executes a read-only SQL query against the BigQuery transactions table."""
    if any(keyword in sql_query.upper() for keyword in ["DROP", "DELETE", "UPDATE", "INSERT"]):
        return "Error: Only SELECT queries are allowed via this tool."

    results = client.query(sql_query).result()
    return [dict(row) for row in results]

def log_anomaly(tx_id: str, timestamp: str, source: str, target: str, amount: float, anomaly_type: str, score: float):
    """Logs a detected suspicious transaction into the flagged_anomalies table."""
    query = f"""
        INSERT INTO `fintrac_prod.flagged_anomalies`
        (tx_id, timestamp, source, target, amount, anomaly_type, score)
        VALUES ('{tx_id}', '{timestamp}', '{source}', '{target}', {amount}, '{anomaly_type}', {score})"""
    client.query(query).result()
    return f"Successfully logged anomaly for transaction {tx_id}"
