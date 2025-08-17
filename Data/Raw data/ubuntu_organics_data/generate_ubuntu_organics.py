import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta
import os
import zipfile

# Setup
fake = Faker()
Faker.seed(42)
random.seed(42)
np.random.seed(42)

# Parameters
NUM_PRODUCTS = 30
NUM_CUSTOMERS = 1200
NUM_ORDERS = 8500
NUM_CAMPAIGNS = 8
RETURN_RATE = 0.03
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 12, 31)
DATE_RANGE = pd.date_range(START_DATE, END_DATE)

# Reference Data
provinces = [
    "Gauteng", "Western Cape", "KwaZulu-Natal", "Eastern Cape",
    "Free State", "Limpopo", "Mpumalanga", "Northern Cape", "North West"
]
channels = ["Meta", "Google", "Influencer", "Newsletter", "Referral"]
categories = ["Supplements", "Skincare", "Fitness Gear", "Apparel", "Haircare"]

# Generate products
products = []
for i in range(NUM_PRODUCTS):
    category = random.choice(categories)
    selling_price = round(random.uniform(100, 2000), 2)
    product_cost = round(selling_price * random.uniform(0.5, 0.7), 2)
    launch_date = fake.date_between(START_DATE, END_DATE)
    products.append({
        "product_id": f"P{i+1:03}",
        "product_name": fake.catch_phrase(),
        "category": category,
        "selling_price": selling_price,
        "product_cost": product_cost,
        "launch_date": launch_date
    })
products_df = pd.DataFrame(products)

# Generate customers
customers = []
for i in range(NUM_CUSTOMERS):
    signup_date = fake.date_between(START_DATE, END_DATE)
    customers.append({
        "customer_id": f"C{i+1:04}",
        "name": fake.name(),
        "signup_date": signup_date,
        "region": random.choice(provinces),
        "acquisition_channel": random.choice(channels)
    })
customers_df = pd.DataFrame(customers)

# Generate campaigns
campaigns = []
for i in range(NUM_CAMPAIGNS):
    start = fake.date_between(START_DATE, END_DATE - timedelta(days=30))
    end = start + timedelta(days=random.randint(7, 30))
    campaigns.append({
        "campaign_id": f"M{i+1:02}",
        "campaign_name": fake.bs().title(),
        "start_date": start,
        "end_date": end,
        "channel": random.choice(channels),
        "budget": round(random.uniform(5000, 50000), 2)
    })
campaigns_df = pd.DataFrame(campaigns)

# Generate orders
orders = []
for i in range(NUM_ORDERS):
    order_date = random.choice(DATE_RANGE)
    product = random.choice(products)
    customer = random.choice(customers)
    quantity = random.randint(1, 5)
    campaign_id = random.choice([c["campaign_id"] for c in campaigns]) if random.random() < 0.6 else None
    orders.append({
        "order_id": f"O{i+1:05}",
        "order_date": order_date,
        "customer_id": customer["customer_id"],
        "product_id": product["product_id"],
        "quantity": quantity,
        "unit_price": product["selling_price"],
        "campaign_id": campaign_id
    })
orders_df = pd.DataFrame(orders)

# Generate returns
num_returns = int(NUM_ORDERS * RETURN_RATE)
reasons = ["Damaged item", "Incorrect item", "Changed mind", "Late delivery", "Other"]
returned_orders = random.sample(orders, num_returns)
returns = []
for i, order in enumerate(returned_orders):
    returns.append({
        "return_id": f"R{i+1:04}",
        "order_id": order["order_id"],
        "product_id": order["product_id"],
        "return_date": order["order_date"] + timedelta(days=random.randint(1, 14)),
        "quantity_returned": min(order["quantity"], random.randint(1, 2)),
        "reason": random.choice(reasons)
    })
returns_df = pd.DataFrame(returns)

# Output directory
os.makedirs("ubuntu_organics_data", exist_ok=True)

# Export to CSV
products_df.to_csv("ubuntu_organics_data/products.csv", index=False)
customers_df.to_csv("ubuntu_organics_data/customers.csv", index=False)
orders_df.to_csv("ubuntu_organics_data/orders.csv", index=False)
campaigns_df.to_csv("ubuntu_organics_data/campaigns.csv", index=False)
returns_df.to_csv("ubuntu_organics_data/returns.csv", index=False)

# Zip the files
with zipfile.ZipFile("ubuntu_organics_dataset.zip", 'w') as zipf:
    for filename in os.listdir("ubuntu_organics_data"):
        zipf.write(f"ubuntu_organics_data/{filename}", arcname=filename)

print("✅ Dataset generated and saved as 'ubuntu_organics_dataset.zip'")
