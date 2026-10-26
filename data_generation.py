# data_generation.py
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def build_synthetic_database():
    conn = sqlite3.connect('revolut_ops.db')
    cursor = conn.cursor()
    
    # 1. Create tables locally using SQLite definitions
    cursor.executescript('''
    DROP TABLE IF EXISTS support_tickets;
    DROP TABLE IF EXISTS flight_bookings;
    DROP TABLE IF EXISTS transactions;
    DROP TABLE IF EXISTS users;

    CREATE TABLE users (user_id TEXT PRIMARY KEY, subscription_tier TEXT, country TEXT, preferred_currency TEXT);
    CREATE TABLE transactions (transaction_id TEXT PRIMARY KEY, user_id TEXT, amount REAL, currency TEXT, status TEXT, created_at TEXT);
    CREATE TABLE flight_bookings (booking_id TEXT PRIMARY KEY, user_id TEXT, pnr TEXT, airline TEXT, base_currency TEXT, ticket_cost REAL, flight_status TEXT, updated_at TEXT);
    CREATE TABLE support_tickets (ticket_id TEXT PRIMARY KEY, user_id TEXT, channel TEXT, initial_tag TEXT, handle_time_minutes INTEGER, status TEXT, created_at TEXT);
    ''')
    
    np.random.seed(42)
    num_users = 1000
    
    # Generate Synthetic Users
    tiers = ['Standard', 'Plus', 'Premium', 'Metal', 'Ultra']
    tier_probs = [0.60, 0.20, 0.12, 0.06, 0.02]
    currencies = {'UK': 'GBP', 'PL': 'PLN', 'PT': 'EUR', 'ES': 'EUR', 'AE': 'AED'}
    countries = list(currencies.keys())
    
    user_list = []
    for i in range(num_users):
        uid = f"USR_{100000 + i}"
        ctr = np.random.choice(countries)
        user_list.append({
            'user_id': uid,
            'subscription_tier': np.random.choice(tiers, p=tier_probs),
            'country': ctr,
            'preferred_currency': currencies[ctr]
        })
    df_users = pd.DataFrame(user_list)
    df_users.to_sql('users', conn, if_exists='append', index=False)
    
    # Generate Transactions & Flight Disruption Data across a timeline
    tx_list = []
    flight_list = []
    ticket_list = []
    base_date = datetime(2026, 10, 1)
    
    airlines = ['IndiGo', 'Akasa Air', 'British Airways', 'TAP Portugal', 'Ryanair']
    
    for i in range(5000):
        days_offset = np.random.randint(0, 25)
        timestamp = base_date + timedelta(days=days_offset, hours=np.random.randint(0, 24), minutes=np.random.randint(0, 60))
        user = df_users.sample(1).iloc[0]
        
        # Inject an Operational Disruption Anomaly: October 12th to October 16th
        is_anomaly_week = (12 <= days_offset <= 16)
        
        # Generate Booking
        pnr = "".join(np.random.choice(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"), size=6))
        status = 'cancelled' if (is_anomaly_week and np.random.rand() < 0.75) else np.random.choice(['ontime', 'delayed', 'cancelled'], p=[0.85, 0.10, 0.05])
        cost = round(float(np.random.uniform(100, 600)), 2)
        
        bid = f"BKG_{200000 + i}"
        flight_list.append({
            'booking_id': bid, 'user_id': user['user_id'], 'pnr': pnr,
            'airline': np.random.choice(airlines), 'base_currency': user['preferred_currency'],
            'ticket_cost': cost, 'flight_status': status, 'updated_at': timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
        
        # Generate Cross-Currency Transaction records linked to the action
        tx_status = 'failed' if (is_anomaly_week and status == 'cancelled' and np.random.rand() < 0.40) else 'completed'
        if status == 'cancelled' and tx_status != 'failed':
            tx_status = 'refunded'
            
        tx_list.append({
            'transaction_id': f"TX_{300000 + i}", 'user_id': user['user_id'], 'amount': cost,
            'currency': user['preferred_currency'], 'status': tx_status, 'created_at': timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
        
        # Generate Support Queue pressure
        if status == 'cancelled' or tx_status == 'failed':
            t_tag = 'Refund Failure Loop' if tx_status == 'failed' else 'Flight Cancellation Recovery'
            h_time = np.random.randint(25, 120) if is_anomaly_week else np.random.randint(10, 45)
            ticket_list.append({
                'ticket_id': f"TKT_{400000 + i}", 'user_id': user['user_id'], 'channel': 'in-app chat',
                'initial_tag': t_tag, 'handle_time_minutes': h_time, 'status': 'resolved',
                'created_at': timestamp.strftime('%Y-%m-%d %H:%M:%S')
            })
            
    pd.DataFrame(tx_list).to_sql('transactions', conn, if_exists='append', index=False)
    pd.DataFrame(flight_list).to_sql('flight_bookings', conn, if_exists='append', index=False)
    pd.DataFrame(ticket_list).to_sql('support_tickets', conn, if_exists='append', index=False)
    
    conn.commit()
    conn.close()
    print("Database built successfully containing simulated operational crisis metrics.")

if __name__ == "__main__":
    build_synthetic_database()
