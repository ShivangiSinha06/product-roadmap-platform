import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class ProductAnalytics:
    def __init__(self, db_manager, prioritization_engine):
        self.db_manager = db_manager
        self.prioritization_engine = prioritization_engine
    
    def generate_comprehensive_analysis(self):
        """Generate comprehensive product analytics"""
        
        # Train ML model and get results
        try:
            rice_df, model_stats = self.prioritization_engine.train_ml_prioritization_model()
            
            # If no ML scores, use RICE scores as composite
            if 'ml_priority_score' not in rice_df.columns:
                rice_df['ml_priority_score'] = rice_df['rice_score']
                rice_df['composite_score'] = rice_df['rice_score']
        except Exception as e:
            # Fallback to RICE-only scoring
            rice_df = self.prioritization_engine.calculate_rice_scores()
            rice_df['ml_priority_score'] = rice_df['rice_score']
            rice_df['composite_score'] = rice_df['rice_score']
            model_stats = {'train_score': 0, 'test_score': 0}
        
        # Assign quarters
        rice_df = self.prioritization_engine.assign_quarters(rice_df)
        
        # Calculate additional metrics
        rice_df['business_impact_score'] = self._calculate_business_impact(rice_df)
        rice_df['technical_complexity'] = self._calculate_technical_complexity(rice_df)
        rice_df['strategic_alignment'] = self._calculate_strategic_alignment(rice_df)
        
        return rice_df, model_stats
    
    def _calculate_business_impact(self, df):
        """Calculate comprehensive business impact score"""
        # Normalize revenue impact
        max_revenue = df['avg_revenue_impact'].max()
        revenue_norm = df['avg_revenue_impact'] / max_revenue if max_revenue > 0 else 0
        
        # Combine different business metrics
        business_impact = (
            revenue_norm * 0.4 +
            (df['avg_business_value'] / 10) * 0.3 +
            (df['avg_conversion_impact'] * 20) * 0.15 +
            (df['avg_retention_impact'] * 15) * 0.15
        )
        
        return business_impact * 100  # Scale to 0-100
    
    def _calculate_technical_complexity(self, df):
        """Calculate technical complexity score"""
        # Higher effort = higher complexity
        max_effort = df['effort_estimate'].max()
        effort_norm = df['effort_estimate'] / max_effort if max_effort > 0 else 0
        
        # Add some randomization for demonstration
        complexity_variation = np.random.uniform(0.8, 1.2, len(df))
        
        return (effort_norm * complexity_variation * 100).clip(0, 100)
    
    def _calculate_strategic_alignment(self, df):
        """Calculate strategic alignment score"""
        # Higher priority requests suggest better strategic alignment
        priority_weight = (df['critical_requests'] * 2 + df['high_requests']) / (df['request_count'] + 1)
        
        # Business value alignment
        value_alignment = df['avg_business_value'] / 10
        
        # User demand alignment
        user_demand = df['unique_users'] / df['unique_users'].max() if df['unique_users'].max() > 0 else 0
        
        alignment = (priority_weight * 0.4 + value_alignment * 0.4 + user_demand * 0.2) * 100
        
        return alignment.clip(0, 100)
    
    def calculate_roi_projections(self, df):
        """Calculate ROI projections for features"""
        roi_data = []
        
        for _, row in df.head(15).iterrows():  # Top 15 features
            # Development cost estimation
            dev_cost = row['effort_estimate'] * 18000  # $18k per story point (updated rate)
            
            # Revenue benefit estimation
            annual_revenue = (
                row['avg_revenue_impact'] * 
                max(row['unique_users'], row['request_count']) * 
                (1 + row['avg_conversion_impact'] * 5) *  # Conversion multiplier
                12  # Annual
            )
            
            # Calculate ROI
            roi = ((annual_revenue - dev_cost) / dev_cost) * 100 if dev_cost > 0 else 0
            
            # Payback period
            monthly_revenue = annual_revenue / 12
            payback_months = dev_cost / monthly_revenue if monthly_revenue > 0 else float('inf')
            
            roi_data.append({
                'feature_name': row['feature_name'],
                'development_cost': dev_cost,
                'projected_annual_revenue': annual_revenue,
                'roi_percentage': roi,
                'payback_months': min(payback_months, 60),  # Cap at 5 years
                'confidence_level': row['confidence_score'],
                'risk_score': self._calculate_risk_score(row)
            })
        
        return pd.DataFrame(roi_data)
    
    def _calculate_risk_score(self, row):
        """Calculate risk score for a feature"""
        # High effort + low confidence = high risk
        effort_risk = (row['effort_estimate'] / 25) * 30  # Effort contributes 30%
        confidence_risk = (1 - row['confidence_score']) * 40  # Low confidence = high risk (40%)
        complexity_risk = (row.get('technical_complexity', 50) / 100) * 30  # Complexity contributes 30%
        
        total_risk = effort_risk + confidence_risk + complexity_risk
        return min(total_risk, 100)  # Cap at 100%
    
    def analyze_customer_segments(self):
        """Analyze feature requests by customer segment"""
        feedback_df = self.db_manager.get_feedback_summary()
        
        segment_analysis = feedback_df.groupby(['customer_segment', 'feature_request']).agg({
            'request_count': 'sum',
            'avg_revenue_impact': 'mean',
            'avg_business_value': 'mean'
        }).reset_index()
        
        # Calculate segment priorities
        segment_priorities = feedback_df.groupby('customer_segment').agg({
            'request_count': 'sum',
            'avg_revenue_impact': 'mean',
            'avg_business_value': 'mean'
        }).reset_index()
        
        segment_priorities['segment_priority_score'] = (
            segment_priorities['avg_revenue_impact'] / 1000 +
            segment_priorities['avg_business_value'] * 2 +
            segment_priorities['request_count'] * 0.1
        )
        
        return segment_analysis, segment_priorities
    
    def create_priority_matrix_data(self, df):
        """Prepare data for priority matrix visualization"""
        matrix_data = df.copy()
        
        # Add quadrant classifications
        effort_median = matrix_data['effort_estimate'].median()
        impact_median = matrix_data['impact_score'].median()
        
        def classify_quadrant(row):
            if row['effort_estimate'] <= effort_median and row['impact_score'] > impact_median:
                return "Quick Wins"
            elif row['effort_estimate'] > effort_median and row['impact_score'] > impact_median:
                return "Major Projects"
            elif row['effort_estimate'] <= effort_median and row['impact_score'] <= impact_median:
                return "Fill-ins"
            else:
                return "Questionable"
        
        matrix_data['quadrant'] = matrix_data.apply(classify_quadrant, axis=1)
        
        return matrix_data
    
    def create_timeline_data(self, df):
        """Create timeline data for Gantt charts"""
        timeline_data = []
        
        quarter_dates = {
            "Q1 2026": ("2026-01-01", "2026-03-31"),
            "Q2 2026": ("2026-04-01", "2026-06-30"),
            "Q3 2026": ("2026-07-01", "2026-09-30"),
            "Q4 2026": ("2026-10-01", "2026-12-31")
        }
        
        for _, row in df.iterrows():
            quarter = row['recommended_quarter']
            if quarter in quarter_dates:
                start_date, end_date = quarter_dates[quarter]
                
                timeline_data.append({
                    'feature_name': row['feature_name'],
                    'start_date': start_date,
                    'end_date': end_date,
                    'quarter': quarter,
                    'effort': row['effort_estimate'],
                    'priority_score': row['composite_score'],
                    'team': self._assign_team(row)
                })
        
        return pd.DataFrame(timeline_data)
    
    def _assign_team(self, row):
        """Assign team based on feature characteristics"""
        feature_name = row['feature_name'].lower()
        
        if any(word in feature_name for word in ['api', 'performance', 'backend', 'database']):
            return "Backend Team"
        elif any(word in feature_name for word in ['mobile', 'app', 'ios', 'android']):
            return "Mobile Team"
        elif any(word in feature_name for word in ['ui', 'ux', 'design', 'interface', 'dark mode']):
            return "Frontend Team"
        elif any(word in feature_name for word in ['analytics', 'reporting', 'data']):
            return "Data Team"
        else:
            return "Product Team"
    
    def create_capacity_analysis(self, df):
        """Analyze team capacity and workload"""
        quarterly_workload = df.groupby(['recommended_quarter']).agg({
            'effort_estimate': 'sum',
            'feature_name': 'count'
        }).reset_index()
        
        quarterly_workload.columns = ['quarter', 'total_effort', 'feature_count']
        
        # Add capacity recommendations
        quarterly_workload['recommended_capacity'] = quarterly_workload['total_effort'].apply(
            lambda x: "Increase Team" if x > 120 else "Current Team" if x > 60 else "Consider Optimization"
        )
        
        return quarterly_workload
    
    def generate_executive_summary(self, df, roi_df):
        """Generate executive summary metrics"""
        summary = {
            'total_features': len(df),
            'high_priority_features': len(df[df['composite_score'] > df['composite_score'].quantile(0.8)]),
            'total_effort_sp': df['effort_estimate'].sum(),
            'avg_roi': roi_df['roi_percentage'].mean() if not roi_df.empty else 0,
            'total_projected_revenue': roi_df['projected_annual_revenue'].sum() if not roi_df.empty else 0,
            'total_investment': roi_df['development_cost'].sum() if not roi_df.empty else 0,
            'high_risk_features': len(df[df.get('risk_score', 0) > 70]) if 'risk_score' in df.columns else 0,
            'quick_wins': len(df[(df['effort_estimate'] <= df['effort_estimate'].median()) & 
                               (df['impact_score'] > df['impact_score'].median())]),
            'avg_business_impact': df.get('business_impact_score', pd.Series([0])).mean(),
            'strategic_alignment_score': df.get('strategic_alignment', pd.Series([0])).mean()
        }
        
        return summary

