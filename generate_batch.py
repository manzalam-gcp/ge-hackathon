import csv
import uuid
from datetime import datetime, timedelta
import random
FILENAME = 'fintrac_batch.csv'
BASE_TIME = datetime(2026, 5, 9, 8, 0, 0)
LOCAL = ["K1A 0G9", "K2P 2N2", "K1S 5B6"]
OFFSHORE = ["KY1-1104", "BS-N481"]
transactions = []
# Generate Normal Noise
for i in range(50):
 transactions.append({
 "tx_id": f"TXN-{uuid.uuid4().hex[:8].upper()}",
 "timestamp": (BASE_TIME + timedelta(minutes=random.randint(1, 1400))).isoformat(),
 "sender": f"ACCT-{random.randint(10000, 99999)}",
 "receiver": f"ACCT-{random.randint(10000, 99999)}",
 "amount": round(random.uniform(50.0, 4500.0), 2),
 "sender_postal": random.choice(LOCAL),
 "receiver_postal": random.choice(LOCAL)
 })
# Inject Structuring Anomaly (Smurfing to dodge $10k limit)
smurf_time = BASE_TIME + timedelta(hours=2)
for i in range(3):
 transactions.append({
 "tx_id": f"TXN-{uuid.uuid4().hex[:8].upper()}",
 "timestamp": (smurf_time + timedelta(minutes=i*45)).isoformat(),
 "sender": "ACCT-SMURF01",
 "receiver": "ACCT-TARGET99",
 "amount": round(random.uniform(9500.0, 9950.0), 2),
 "sender_postal": "K1S 5B6",
 "receiver_postal": "K2P 2N2"
 })
transactions.sort(key=lambda x: x["timestamp"])
with open(FILENAME, mode='w', newline='') as f:
 writer = csv.DictWriter(f, fieldnames=transactions[0].keys())
 writer.writeheader()
 writer.writerows(transactions)
print(f"Generated {FILENAME}")
