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
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usage_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feature_name TEXT,
            user_id TEXT,
            usage_count INTEGER,
            session_duration REAL,
            date_recorded DATE,
            user_segment TEXT,
            conversion_impact REAL,
            retention_impact REAL
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def generate_sample_data(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Clear existing data
        cursor.execute("DELETE FROM customer_feedback")
        cursor.execute("DELETE FROM usage_metrics")
        
        features = [
            "Dark mode support", "Advanced search filters", "Mobile app improvements",
            "API rate limiting", "Real-time notifications", "Export functionality",
            "User role management", "Dashboard customization", "Integration with Slack",
            "Performance optimization", "Multi-language support", "Advanced analytics",
            "Two-factor authentication", "Bulk data import", "Custom reporting"
        ]
        
        customers = [f"CUST_{i:04d}" for i in range(1, 101)]
        segments = ["Enterprise", "SMB", "Startup", "Individual"]
        
        # Generate feedback data
        for _ in range(150):
            cursor.execute('''
                INSERT INTO customer_feedback 
                (customer_id, feature_request, feedback_type, priority_level, source, 
                 customer_segment, revenue_impact, effort_estimate, business_value_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                random.choice(customers),
                random.choice(features),
                random.choice(['feature_request', 'enhancement', 'bug_report']),
                random.choice(['low', 'medium', 'high', 'critical']),
                random.choice(['support_ticket', 'survey', 'user_interview', 'sales']),
                random.choice(segments),
                round(random.uniform(1000, 50000), 2),
                random.randint(1, 21),
                random.randint(1, 10)
            ))
        
        # Generate usage data
        for _ in range(300):
            cursor.execute('''
                INSERT INTO usage_metrics 
                (feature_name, user_id, usage_count, session_duration, date_recorded,
                 user_segment, conversion_impact, retention_impact)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                random.choice(features),
                f"USER_{random.randint(1, 200):04d}",
                random.randint(1, 50),
                round(random.uniform(1, 120), 2),
                (datetime.now() - timedelta(days=random.randint(0, 90))).date(),
                random.choice(segments),
                round(random.uniform(0.01, 0.15), 4),
                round(random.uniform(0.02, 0.20), 4)
            ))
        
        conn.commit()
        conn.close()
        return True
    
    def get_feedback_summary(self):
        try:
            conn = sqlite3.connect(self.db_path)
            query = '''
            SELECT 
                feature_request,
                COUNT(*) as request_count,
                AVG(business_value_score) as avg_business_value,
                AVG(revenue_impact) as avg_revenue_impact,
                AVG(effort_estimate) as avg_effort,
                customer_segment,
                priority_level,
                feedback_type
            FROM customer_feedback 
            GROUP BY feature_request, customer_segment, priority_level, feedback_type
            ORDER BY request_count DESC
            '''
            df = pd.read_sql(query, conn)
            conn.close()
            return df
        except Exception as e:
            print(f"Error in get_feedback_summary: {e}")
            return pd.DataFrame()
    
    def get_usage_analytics(self):
        try:
            conn = sqlite3.connect(self.db_path)
            query = '''
            SELECT 
                feature_name,
                COUNT(DISTINCT user_id) as unique_users,
                AVG(usage_count) as avg_usage,
                AVG(session_duration) as avg_session_duration,
                AVG(conversion_impact) as avg_conversion_impact,
                AVG(retention_impact) as avg_retention_impact,
                user_segment,
                date_recorded
            FROM usage_metrics 
            GROUP BY feature_name, user_segment, date_recorded
            ORDER BY unique_users DESC
            '''
            df = pd.read_sql(query, conn)
            conn.close()
            return df
        except Exception as e:
            print(f"Error in get_usage_analytics: {e}")
            return pd.DataFrame()
    
    def get_feature_analytics_summary(self):
        """Get feature analytics - SQLite compatible (no FULL OUTER JOIN)"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Get feedback data
            feedback_query = '''
            SELECT 
                feature_request as feature_name,
                COUNT(*) as request_count,
                AVG(business_value_score) as avg_business_value,
                AVG(revenue_impact) as avg_revenue_impact,
                AVG(effort_estimate) as avg_effort,
                SUM(CASE WHEN priority_level = 'critical' THEN 1 ELSE 0 END) as critical_requests,
                SUM(CASE WHEN priority_level = 'high' THEN 1 ELSE 0 END) as high_requests
            FROM customer_feedback 
            GROUP BY feature_request
            '''
            feedback_df = pd.read_sql(feedback_query, conn)
            
            # Get usage data
            usage_query = '''
            SELECT 
                feature_name,
                COUNT(DISTINCT user_id) as unique_users,
                AVG(usage_count) as avg_usage,
                AVG(session_duration) as avg_session_duration,
                AVG(conversion_impact) as avg_conversion_impact,
                AVG(retention_impact) as avg_retention_impact
            FROM usage_metrics 
            GROUP BY feature_name
            '''
            usage_df = pd.read_sql(usage_query, conn)
            conn.close()
            
            # Use pandas merge instead of SQL FULL OUTER JOIN
            merged_df = pd.merge(feedback_df, usage_df, on='feature_name', how='outer')
            
            # Fill missing values with defaults
            merged_df = merged_df.fillna({
                'request_count': 0,
                'avg_business_value': 5,
                'avg_revenue_impact': 10000,
                'avg_effort': 8,
                'critical_requests': 0,
                'high_requests': 0,
                'unique_users': 0,
                'avg_usage': 0,
                'avg_session_duration': 30,
                'avg_conversion_impact': 0.05,
                'avg_retention_impact': 0.08
            })
            
            return merged_df
            
        except Exception as e:
            print(f"Error in get_feature_analytics_summary: {e}")
            # Return empty DataFrame with correct columns
            return pd.DataFrame(columns=[
                'feature_name', 'request_count', 'avg_business_value', 
                'avg_revenue_impact', 'avg_effort', 'critical_requests', 
                'high_requests', 'unique_users', 'avg_usage', 
                'avg_session_duration', 'avg_conversion_impact', 'avg_retention_impact'
            ])
    
    def add_feedback(self, feedback_data):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO customer_feedback 
                (customer_id, feature_request, feedback_type, priority_level, source, 
                 customer_segment, revenue_impact, effort_estimate, business_value_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', feedback_data)
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding feedback: {e}")
            return False
    
    def log_ai_query(self, query_text, role, response):
        """Log AI queries - simplified implementation"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ai_queries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query_text TEXT,
                    role TEXT,
                    response TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                INSERT INTO ai_queries (query_text, role, response)
                VALUES (?, ?, ?)
            ''', (query_text, role, str(response)))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error logging AI query: {e}")
            return False

