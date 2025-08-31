import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import random
import os

class DatabaseManager:
    def __init__(self, db_path="data/product_roadmap.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.setup_database()
        
    def setup_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS customer_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT,
            feature_request TEXT,
            feedback_type TEXT,
            priority_level TEXT,
            source TEXT,
            customer_segment TEXT,
            revenue_impact REAL,
            effort_estimate INTEGER,
            business_value_score INTEGER,
            created_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def generate_sample_data(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Clear existing data
        cursor.execute("DELETE FROM customer_feedback")
        
        features = [
            "Dark mode support", "Advanced search filters", "Mobile app improvements",
            "API rate limiting", "Real-time notifications", "Export functionality",
            "User role management", "Dashboard customization", "Integration with Slack"
        ]
        
        for _ in range(50):
            cursor.execute('''
                INSERT INTO customer_feedback 
                (customer_id, feature_request, feedback_type, priority_level, source, 
                 customer_segment, revenue_impact, effort_estimate, business_value_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                f"CUST_{random.randint(1, 100):04d}",
                random.choice(features),
                random.choice(['feature_request', 'enhancement']),
                random.choice(['low', 'medium', 'high']),
                random.choice(['support_ticket', 'survey']),
                random.choice(['Enterprise', 'SMB']),
                random.uniform(1000, 50000),
                random.randint(1, 20),
                random.randint(1, 10)
            ))
        
        conn.commit()
        conn.close()
    
    def get_feedback_summary(self):
        try:
            conn = sqlite3.connect(self.db_path)
            query = '''
            SELECT 
                feature_request,
                COUNT(*) as request_count,
                AVG(business_value_score) as avg_business_value,
                AVG(revenue_impact) as avg_revenue_impact,
                AVG(effort_estimate) as avg_effort
            FROM customer_feedback 
            GROUP BY feature_request 
            ORDER BY request_count DESC
            '''
            df = pd.read_sql(query, conn)
            conn.close()
            return df
        except:
            return pd.DataFrame()

