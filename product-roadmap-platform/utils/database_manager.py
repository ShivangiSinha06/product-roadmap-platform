import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import random
import os

class DatabaseManager:
    def __init__(self, db_path="data/product_roadmap.db"):
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.setup_database()
        
    def setup_database(self):
        """Initialize database with schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Customer Feedback Table
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
        
        # Usage Metrics Table
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
        
        # Feature Backlog Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS feature_backlog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feature_name TEXT UNIQUE,
            description TEXT,
            category TEXT,
            status TEXT DEFAULT 'backlog',
            reach_score INTEGER,
            impact_score REAL,
            confidence_score REAL,
            effort_estimate INTEGER,
            rice_score REAL,
            ml_priority_score REAL,
            created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            target_quarter TEXT,
            assigned_team TEXT,
            stakeholder_votes INTEGER DEFAULT 0
        )
        ''')
        
        # Stakeholder Queries Log
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS stakeholder_queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_text TEXT,
            stakeholder_role TEXT,
            query_type TEXT,
            ai_response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            satisfaction_rating INTEGER
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def generate_sample_data(self):
        """Generate realistic sample data for testing"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Clear existing data
        cursor.execute("DELETE FROM customer_feedback")
        cursor.execute("DELETE FROM usage_metrics")
        
        # Sample features
        features = [
            "Dark mode support", "Advanced search filters", "Mobile app improvements",
            "API rate limiting", "Real-time notifications", "Export functionality",
            "User role management", "Dashboard customization", "Integration with Slack",
            "Performance optimization", "Multi-language support", "Advanced analytics",
            "Two-factor authentication", "Bulk data import", "Custom reporting",
            "Automated workflows", "Data visualization", "Social login integration",
            "Email templates", "Calendar integration", "File sharing", "Version control"
        ]
        
        customers = [f"CUST_{i:04d}" for i in range(1, 151)]
        segments = ["Enterprise", "SMB", "Startup", "Individual"]
        sources = ["support_ticket", "survey", "user_interview", "sales", "product_feedback"]
        
        # Generate feedback data
        feedback_data = []
        for _ in range(500):
            feedback_data.append((
                random.choice(customers),
                random.choice(features),
                random.choice(['feature_request', 'enhancement', 'bug_report']),
                random.choice(['low', 'medium', 'high', 'critical']),
                random.choice(sources),
                random.choice(segments),
                round(random.uniform(1000, 75000), 2),
                random.randint(1, 25),
                random.randint(1, 10)
            ))
        
        cursor.executemany('''
            INSERT INTO customer_feedback 
            (customer_id, feature_request, feedback_type, priority_level, source, 
             customer_segment, revenue_impact, effort_estimate, business_value_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', feedback_data)
        
        # Generate usage data
        usage_data = []
        for _ in range(800):
            usage_data.append((
                random.choice(features),
                f"USER_{random.randint(1, 300):04d}",
                random.randint(1, 75),
                round(random.uniform(0.5, 180), 2),
                (datetime.now() - timedelta(days=random.randint(0, 120))).date(),
                random.choice(segments),
                round(random.uniform(0.005, 0.20), 4),
                round(random.uniform(0.01, 0.25), 4)
            ))
        
        cursor.executemany('''
            INSERT INTO usage_metrics 
            (feature_name, user_id, usage_count, session_duration, date_recorded,
             user_segment, conversion_impact, retention_impact)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', usage_data)
        
        conn.commit()
        conn.close()
        
        return True
    
    def get_feedback_summary(self):
        """Get aggregated feedback data"""
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
    
    def get_usage_analytics(self):
        """Get usage analytics data"""
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
    
    def add_feedback(self, feedback_data):
        """Add new customer feedback"""
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
    
    def get_feature_analytics_summary(self):
        """Get comprehensive feature analytics"""
        conn = sqlite3.connect(self.db_path)
        
        # Combined query for feature analytics
        query = '''
        WITH feedback_agg AS (
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
        ),
        usage_agg AS (
            SELECT 
                feature_name,
                COUNT(DISTINCT user_id) as unique_users,
                AVG(usage_count) as avg_usage,
                AVG(session_duration) as avg_session_duration,
                AVG(conversion_impact) as avg_conversion_impact,
                AVG(retention_impact) as avg_retention_impact
            FROM usage_metrics 
            GROUP BY feature_name
        )
        SELECT 
            COALESCE(f.feature_name, u.feature_name) as feature_name,
            COALESCE(f.request_count, 0) as request_count,
            COALESCE(f.avg_business_value, 5) as avg_business_value,
            COALESCE(f.avg_revenue_impact, 10000) as avg_revenue_impact,
            COALESCE(f.avg_effort, 8) as avg_effort,
            COALESCE(f.critical_requests, 0) as critical_requests,
            COALESCE(f.high_requests, 0) as high_requests,
            COALESCE(u.unique_users, 0) as unique_users,
            COALESCE(u.avg_usage, 0) as avg_usage,
            COALESCE(u.avg_session_duration, 30) as avg_session_duration,
            COALESCE(u.avg_conversion_impact, 0.05) as avg_conversion_impact,
            COALESCE(u.avg_retention_impact, 0.08) as avg_retention_impact
        FROM feedback_agg f
        FULL OUTER JOIN usage_agg u ON f.feature_name = u.feature_name
        '''
        
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    
    def log_ai_query(self, query_text, role, response):
        """Log AI assistant queries"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO stakeholder_queries (query_text, stakeholder_role, ai_response)
            VALUES (?, ?, ?)
        ''', (query_text, role, str(response)))
        
        conn.commit()
        conn.close()
        return True

