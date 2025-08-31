import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os

class FeaturePrioritizationEngine:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.scaler = StandardScaler()
        self.ml_model = None
        self.model_path = "models/"
        
        # Create models directory
        os.makedirs(self.model_path, exist_ok=True)
        
    def calculate_rice_scores(self):
        """Calculate RICE scores for all features"""
        features_df = self.db_manager.get_feature_analytics_summary()
        
        rice_scores = []
        
        for _, row in features_df.iterrows():
            # RICE Components
            reach = self._calculate_reach_score(row)
            impact = self._calculate_impact_score(row)
            confidence = self._calculate_confidence_score(row)
            effort = max(row['avg_effort'], 1)  # Avoid division by zero
            
            rice_score = (reach * impact * confidence) / effort
            
            rice_scores.append({
                'feature_name': row['feature_name'],
                'reach_score': reach,
                'impact_score': impact,
                'confidence_score': confidence,
                'effort_estimate': effort,
                'rice_score': rice_score,
                'request_count': row['request_count'],
                'avg_business_value': row['avg_business_value'],
                'avg_revenue_impact': row['avg_revenue_impact'],
                'unique_users': row['unique_users'],
                'avg_conversion_impact': row['avg_conversion_impact'],
                'avg_retention_impact': row['avg_retention_impact'],
                'critical_requests': row['critical_requests'],
                'high_requests': row['high_requests']
            })
        
        df = pd.DataFrame(rice_scores)
        df = df.sort_values('rice_score', ascending=False)
        df['priority_rank'] = range(1, len(df) + 1)
        
        return df
    
    def _calculate_reach_score(self, row):
        """Calculate reach score based on users and requests"""
        user_reach = row['unique_users']
        request_reach = row['request_count'] * 2  # Weight requests
        priority_multiplier = 1 + (row['critical_requests'] * 0.5) + (row['high_requests'] * 0.3)
        
        return max(user_reach, request_reach) * priority_multiplier
    
    def _calculate_impact_score(self, row):
        """Calculate impact score based on business value and usage metrics"""
        # Normalize business value (0-1 scale)
        business_value = min(row['avg_business_value'] / 10, 1)
        
        # Normalize revenue impact (scaled to reasonable range)
        revenue_impact = min(row['avg_revenue_impact'] / 50000, 1)
        
        # Usage impact
        conversion_impact = row['avg_conversion_impact'] * 20
        retention_impact = row['avg_retention_impact'] * 15
        
        # Weighted combination
        impact = (business_value * 0.3 + revenue_impact * 0.3 + 
                 conversion_impact * 0.2 + retention_impact * 0.2)
        
        # Convert to RICE impact scale (0.25, 0.5, 1, 2, 3)
        if impact <= 0.1:
            return 0.25
        elif impact <= 0.3:
            return 0.5
        elif impact <= 0.6:
            return 1
        elif impact <= 0.8:
            return 2
        else:
            return 3
    
    def _calculate_confidence_score(self, row):
        """Calculate confidence score based on data quality"""
        base_confidence = 0.4
        
        # More data points = higher confidence
        if row['request_count'] > 15:
            base_confidence += 0.2
        elif row['request_count'] > 5:
            base_confidence += 0.1
        
        if row['unique_users'] > 30:
            base_confidence += 0.2
        elif row['unique_users'] > 10:
            base_confidence += 0.1
        
        # High business value = higher confidence
        if row['avg_business_value'] > 8:
            base_confidence += 0.15
        elif row['avg_business_value'] > 6:
            base_confidence += 0.1
        
        # Critical/high priority requests = higher confidence
        if row['critical_requests'] > 0 or row['high_requests'] > 2:
            base_confidence += 0.05
        
        return min(base_confidence, 1.0)
    
    def train_ml_prioritization_model(self):
        """Train ML model for advanced feature prioritization"""
        rice_df = self.calculate_rice_scores()
        
        if len(rice_df) < 10:
            # Not enough data for training
            return rice_df
        
        # Prepare features for ML model
        feature_cols = [
            'reach_score', 'impact_score', 'confidence_score', 'effort_estimate',
            'request_count', 'avg_business_value', 'avg_revenue_impact',
            'unique_users', 'avg_conversion_impact', 'avg_retention_impact'
        ]
        
        X = rice_df[feature_cols].fillna(0)
        y = rice_df['rice_score']
        
        # Add synthetic variations for better training
        X_synthetic, y_synthetic = self._generate_synthetic_training_data(X, y)
        X_combined = pd.concat([X, X_synthetic], ignore_index=True)
        y_combined = pd.concat([y, y_synthetic], ignore_index=True)
        
        # Train model
        X_train, X_test, y_train, y_test = train_test_split(
            X_combined, y_combined, test_size=0.2, random_state=42
        )
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Use Gradient Boosting for better performance
        self.ml_model = GradientBoostingRegressor(
            n_estimators=100, 
            learning_rate=0.1,
            max_depth=4,
            random_state=42
        )
        self.ml_model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        train_score = self.ml_model.score(X_train_scaled, y_train)
        test_score = self.ml_model.score(X_test_scaled, y_test)
        
        # Save model and scaler
        joblib.dump(self.ml_model, f'{self.model_path}feature_prioritization_model.pkl')
        joblib.dump(self.scaler, f'{self.model_path}feature_scaler.pkl')
        
        # Add ML scores to the dataframe
        X_original_scaled = self.scaler.transform(X)
        ml_predictions = self.ml_model.predict(X_original_scaled)
        rice_df['ml_priority_score'] = ml_predictions
        
        # Calculate composite score
        rice_df['composite_score'] = (rice_df['rice_score'] * 0.7 + 
                                    rice_df['ml_priority_score'] * 0.3)
        
        # Re-rank based on composite score
        rice_df = rice_df.sort_values('composite_score', ascending=False)
        rice_df['priority_rank'] = range(1, len(rice_df) + 1)
        
        return rice_df, {'train_score': train_score, 'test_score': test_score}
    
    def _generate_synthetic_training_data(self, X, y, num_samples=100):
        """Generate synthetic training data for better ML model performance"""
        synthetic_X = []
        synthetic_y = []
        
        for _ in range(num_samples):
            # Create variations of existing data points
            base_idx = np.random.randint(0, len(X))
            base_row = X.iloc[base_idx].copy()
            
            # Add controlled noise
            for col in base_row.index:
                if col in ['reach_score', 'request_count', 'unique_users']:
                    base_row[col] *= np.random.uniform(0.7, 1.3)
                elif col in ['impact_score', 'confidence_score']:
                    base_row[col] *= np.random.uniform(0.9, 1.1)
                elif col == 'effort_estimate':
                    base_row[col] *= np.random.uniform(0.6, 1.4)
                else:
                    base_row[col] *= np.random.uniform(0.8, 1.2)
            
            # Ensure positive values
            base_row = base_row.abs()
            
            # Recalculate target
            synthetic_rice = (base_row['reach_score'] * base_row['impact_score'] * 
                            base_row['confidence_score']) / max(base_row['effort_estimate'], 1)
            
            synthetic_X.append(base_row)
            synthetic_y.append(synthetic_rice)
        
        return pd.DataFrame(synthetic_X), pd.Series(synthetic_y)
    
    def get_feature_importance(self):
        """Get feature importance from the ML model"""
        if self.ml_model is None:
            return None
        
        feature_names = [
            'reach_score', 'impact_score', 'confidence_score', 'effort_estimate',
            'request_count', 'avg_business_value', 'avg_revenue_impact',
            'unique_users', 'avg_conversion_impact', 'avg_retention_impact'
        ]
        
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': self.ml_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        return importance_df
    
    def assign_quarters(self, df):
        """Assign features to quarters based on priority and capacity"""
        df_copy = df.copy()
        
        # Calculate quartiles for assignment
        q1_threshold = df_copy['composite_score'].quantile(0.75)
        q2_threshold = df_copy['composite_score'].quantile(0.50)
        q3_threshold = df_copy['composite_score'].quantile(0.25)
        
        def assign_quarter(score):
            if score >= q1_threshold:
                return "Q1 2026"
            elif score >= q2_threshold:
                return "Q2 2026"
            elif score >= q3_threshold:
                return "Q3 2026"
            else:
                return "Q4 2026"
        
        df_copy['recommended_quarter'] = df_copy['composite_score'].apply(assign_quarter)
        
        return df_copy

