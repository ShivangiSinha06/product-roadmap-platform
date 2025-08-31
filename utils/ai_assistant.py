import pandas as pd
import numpy as np
from datetime import datetime
import re

class ProductAIAssistant:
    def __init__(self, db_manager, analytics_engine):
        self.db_manager = db_manager
        self.analytics = analytics_engine
        
    def process_query(self, query, stakeholder_role="Product Manager"):
        """Process natural language queries about the product roadmap"""
        
        # Get current data
        analysis_df, _ = self.analytics.generate_comprehensive_analysis()
        roi_df = self.analytics.calculate_roi_projections(analysis_df)
        
        # Classify and handle query
        query_type = self._classify_query(query)
        
        if query_type == 'priority':
            response = self._handle_priority_query(query, analysis_df, stakeholder_role)
        elif query_type == 'timeline':
            response = self._handle_timeline_query(query, analysis_df, stakeholder_role)
        elif query_type == 'roi':
            response = self._handle_roi_query(query, roi_df, stakeholder_role)
        elif query_type == 'comparison':
            response = self._handle_comparison_query(query, analysis_df, stakeholder_role)
        elif query_type == 'capacity':
            response = self._handle_capacity_query(query, analysis_df, stakeholder_role)
        elif query_type == 'risk':
            response = self._handle_risk_query(query, analysis_df, roi_df, stakeholder_role)
        else:
            response = self._handle_general_query(query, analysis_df, roi_df, stakeholder_role)
        
        # Log the query
        self.db_manager.log_ai_query(query, stakeholder_role, response)
        
        return response
    
    def _classify_query(self, query):
        """Classify the type of query based on keywords"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['priority', 'important', 'rank', 'top', 'highest']):
            return 'priority'
        elif any(word in query_lower for word in ['timeline', 'when', 'schedule', 'quarter', 'q1', 'q2', 'q3', 'q4']):
            return 'timeline'
        elif any(word in query_lower for word in ['roi', 'return', 'revenue', 'cost', 'profit', 'investment']):
            return 'roi'
        elif any(word in query_lower for word in ['compare', 'versus', 'vs', 'difference', 'better']):
            return 'comparison'
        elif any(word in query_lower for word in ['capacity', 'resource', 'team', 'effort', 'workload']):
            return 'capacity'
        elif any(word in query_lower for word in ['risk', 'risky', 'danger', 'problem', 'challenge']):
            return 'risk'
        else:
            return 'general'
    
    def _handle_priority_query(self, query, df, role):
        """Handle priority-related queries"""
        # Extract specific feature if mentioned
        feature_name = self._extract_feature_name(query, df['feature_name'].tolist())
        
        if feature_name:
            feature_data = df[df['feature_name'] == feature_name].iloc[0]
            
            response = f"## 🎯 Priority Analysis: {feature_name}\n\n"
            response += f"**Priority Rank:** #{int(feature_data['priority_rank'])}\n"
            response += f"**Composite Score:** {feature_data['composite_score']:.2f}\n"
            response += f"**RICE Score:** {feature_data['rice_score']:.2f}\n"
            response += f"**Recommended Quarter:** {feature_data['recommended_quarter']}\n\n"
            response += f"**Analysis:**\n"
            response += f"- **Reach:** {feature_data['reach_score']:.0f} users/requests\n"
            response += f"- **Impact:** {feature_data['impact_score']:.1f}/3\n"
            response += f"- **Confidence:** {feature_data['confidence_score']:.1f}%\n"
            response += f"- **Effort:** {feature_data['effort_estimate']:.0f} story points\n\n"
            
            # Add contextual insights
            if feature_data['priority_rank'] <= 5:
                response += "🔥 **This is a HIGH PRIORITY feature** - consider for immediate implementation."
            elif feature_data['priority_rank'] <= 10:
                response += "⚡ **This is a MEDIUM PRIORITY feature** - good candidate for next quarter."
            else:
                response += "📋 **This is a LOWER PRIORITY feature** - consider for future roadmap."
                
        else:
            # Show top priorities
            top_features = df.head(8)
            
            response = f"## 🏆 Top Priority Features\n\n"
            response += f"*Based on composite scoring (RICE + ML analysis)*\n\n"
            
            for i, (_, feature) in enumerate(top_features.iterrows(), 1):
                response += f"**{i}. {feature['feature_name']}**\n"
                response += f"   - Score: {feature['composite_score']:.2f} | Effort: {feature['effort_estimate']:.0f}SP | Quarter: {feature['recommended_quarter']}\n\n"
            
            # Add summary insights
            response += f"**Key Insights:**\n"
            response += f"- Average priority score: {top_features['composite_score'].mean():.2f}\n"
            response += f"- Total effort for top 8: {top_features['effort_estimate'].sum():.0f} story points\n"
            response += f"- Most features target: {top_features['recommended_quarter'].mode().iloc[0]}\n"
        
        return response
    
    def _handle_timeline_query(self, query, df, role):
        """Handle timeline-related queries"""
        # Check for specific quarter
        quarter_match = re.search(r'Q[1-4]\s*20\d{2}', query, re.IGNORECASE)
        if quarter_match:
            quarter = quarter_match.group().upper()
            quarter_features = df[df['recommended_quarter'] == quarter]
            
            response = f"## 📅 {quarter} Roadmap\n\n"
            
            if not quarter_features.empty:
                response += f"**Features planned for {quarter}:**\n\n"
                
                for i, (_, feature) in enumerate(quarter_features.head(10).iterrows(), 1):
                    response += f"{i}. **{feature['feature_name']}**\n"
                    response += f"   - Priority Score: {feature['composite_score']:.2f}\n"
                    response += f"   - Effort: {feature['effort_estimate']:.0f} story points\n"
                    response += f"   - Business Impact: {feature.get('business_impact_score', 0):.1f}/100\n\n"
                
                response += f"**{quarter} Summary:**\n"
                response += f"- Total features: {len(quarter_features)}\n"
                response += f"- Total effort: {quarter_features['effort_estimate'].sum():.0f} story points\n"
                response += f"- Average priority: {quarter_features['composite_score'].mean():.2f}\n"
                
                # Capacity warning
                if quarter_features['effort_estimate'].sum() > 100:
                    response += f"\n⚠️ **Capacity Alert:** This quarter appears overloaded. Consider redistributing some features."
            else:
                response += f"No features are currently planned for {quarter}."
        
        else:
            # Full timeline overview
            timeline_summary = df.groupby('recommended_quarter').agg({
                'feature_name': 'count',
                'effort_estimate': 'sum',
                'composite_score': 'mean'
            }).round(2)
            
            response = f"## 🗓️ Complete Roadmap Timeline\n\n"
            
            for quarter, data in timeline_summary.iterrows():
                response += f"**{quarter}:**\n"
                response += f"- Features: {data['feature_name']}\n"
                response += f"- Total Effort: {data['effort_estimate']:.0f} story points\n"
                response += f"- Avg Priority: {data['composite_score']:.2f}\n\n"
            
            response += f"**Timeline Insights:**\n"
            response += f"- Total roadmap span: 4 quarters\n"
            response += f"- Most loaded quarter: {timeline_summary['effort_estimate'].idxmax()}\n"
            response += f"- Highest priority quarter: {timeline_summary['composite_score'].idxmax()}\n"
        
        return response
    
    def _handle_roi_query(self, query, roi_df, role):
        """Handle ROI and financial queries"""
        if roi_df.empty:
            return "❌ **ROI analysis unavailable** - need more revenue impact data in customer feedback."
        
        response = f"## 💰 ROI Analysis\n\n"
        
        # Portfolio overview
        total_investment = roi_df['development_cost'].sum()
        total_revenue = roi_df['projected_annual_revenue'].sum()
        portfolio_roi = ((total_revenue - total_investment) / total_investment * 100) if total_investment > 0 else 0
        
        response += f"**Portfolio Overview:**\n"
        response += f"- Total Investment: ${total_investment:,.0f}\n"
        response += f"- Projected Annual Revenue: ${total_revenue:,.0f}\n"
        response += f"- Portfolio ROI: {portfolio_roi:.1f}%\n\n"
        
        # Best ROI features
        best_roi = roi_df.nlargest(5, 'roi_percentage')
        
        response += f"**🏆 Highest ROI Features:**\n\n"
        for i, (_, feature) in enumerate(best_roi.iterrows(), 1):
            response += f"{i}. **{feature['feature_name']}**\n"
            response += f"   - ROI: {feature['roi_percentage']:.1f}%\n"
            response += f"   - Investment: ${feature['development_cost']:,.0f}\n"
            response += f"   - Projected Revenue: ${feature['projected_annual_revenue']:,.0f}\n"
            response += f"   - Payback: {feature['payback_months']:.1f} months\n\n"
        
        # Risk assessment
        high_risk_features = roi_df[roi_df['risk_score'] > 60]
        if not high_risk_features.empty:
            response += f"⚠️ **High Risk Features:** {len(high_risk_features)} features have elevated risk scores\n"
        
        return response
    
    def _handle_comparison_query(self, query, df, role):
        """Handle feature comparison queries"""
        # Extract feature names from query
        features_mentioned = []
        for feature in df['feature_name']:
            if feature.lower() in query.lower():
                features_mentioned.append(feature)
        
        if len(features_mentioned) < 2:
            return "❓ **Comparison unavailable** - please specify which features you'd like to compare."
        
        comparison_data = df[df['feature_name'].isin(features_mentioned)].head(4)  # Limit to 4 features
        
        response = f"## ⚖️ Feature Comparison\n\n"
        response += f"*Comparing: {', '.join(features_mentioned[:4])}*\n\n"
        
        # Create comparison table format
        response += "| Feature | Priority Rank | Composite Score | Effort (SP) | Quarter |\n"
        response += "|---------|---------------|-----------------|-------------|----------|\n"
        
        for _, feature in comparison_data.iterrows():
            response += f"| {feature['feature_name'][:25]}... | #{feature['priority_rank']:.0f} | {feature['composite_score']:.2f} | {feature['effort_estimate']:.0f} | {feature['recommended_quarter']} |\n"
        
        # Winner analysis
        winner = comparison_data.loc[comparison_data['composite_score'].idxmax()]
        
        response += f"\n**🏆 Recommendation: {winner['feature_name']}**\n"
        response += f"- Highest composite score: {winner['composite_score']:.2f}\n"
        response += f"- Priority rank: #{winner['priority_rank']:.0f}\n"
        response += f"- Best balance of impact, reach, confidence, and effort\n"
        
        return response
    
    def _handle_capacity_query(self, query, df, role):
        """Handle capacity and resource queries"""
        capacity_analysis = self.analytics.create_capacity_analysis(df)
        
        response = f"## 👥 Team Capacity Analysis\n\n"
        
        # Quarterly breakdown
        for _, quarter_data in capacity_analysis.iterrows():
            response += f"**{quarter_data['quarter']}:**\n"
            response += f"- Features: {quarter_data['feature_count']}\n"
            response += f"- Total Effort: {quarter_data['total_effort']} story points\n"
            response += f"- Recommendation: {quarter_data['recommended_capacity']}\n\n"
        
        # Team assignment analysis
        team_analysis = df.groupby(df.apply(lambda x: self.analytics._assign_team(x), axis=1)).agg({
            'effort_estimate': 'sum',
            'feature_name': 'count'
        })
        
        response += f"**Team Workload Distribution:**\n"
        for team, data in team_analysis.iterrows():
            response += f"- **{team}:** {data['feature_name']} features, {data['effort_estimate']:.0f} story points\n"
        
        # Capacity recommendations
        total_effort = df['effort_estimate'].sum()
        response += f"\n**Capacity Insights:**\n"
        response += f"- Total roadmap effort: {total_effort:.0f} story points\n"
        response += f"- Quarterly average: {total_effort/4:.0f} story points\n"
        
        if total_effort > 400:  # Assuming 100 SP per quarter capacity
            response += f"- ⚠️ **Over capacity** - consider extending timeline or increasing team size\n"
        elif total_effort > 320:
            response += f"- ⚡ **Near capacity** - monitor progress closely\n"
        else:
            response += f"- ✅ **Within capacity** - good workload distribution\n"
        
        return response
    
    def _handle_risk_query(self, query, df, roi_df, role):
        """Handle risk assessment queries"""
        response = f"## ⚠️ Risk Assessment\n\n"
        
        # High risk features (high effort + low confidence)
        df['risk_score'] = ((df['effort_estimate'] / df['effort_estimate'].max()) * 40 + 
                           (1 - df['confidence_score']) * 60)
        
        high_risk = df.nlargest(5, 'risk_score')
        
        response += f"**🔴 Highest Risk Features:**\n\n"
        for i, (_, feature) in enumerate(high_risk.iterrows(), 1):
            response += f"{i}. **{feature['feature_name']}**\n"
            response += f"   - Risk Score: {feature['risk_score']:.0f}/100\n"
            response += f"   - Effort: {feature['effort_estimate']:.0f} SP\n"
            response += f"   - Confidence: {feature['confidence_score']:.1%}\n\n"
        
        # Risk categories
        technical_risks = df[df['effort_estimate'] > df['effort_estimate'].quantile(0.8)]
        confidence_risks = df[df['confidence_score'] < 0.6]
        
        response += f"**Risk Categories:**\n"
        response += f"- **Technical Risk:** {len(technical_risks)} high-effort features\n"
        response += f"- **Confidence Risk:** {len(confidence_risks)} low-confidence features\n"
        
        # Mitigation strategies
        response += f"\n**🛡️ Recommended Mitigation Strategies:**\n"
        response += f"1. **Technical Risks:** Break down large features, create prototypes\n"
        response += f"2. **Confidence Risks:** Conduct user research, validate assumptions\n"
        response += f"3. **Timeline Risks:** Add buffer time, prioritize ruthlessly\n"
        response += f"4. **Resource Risks:** Cross-train team members, consider external help\n"
        
        return response
    
    def _handle_general_query(self, query, df, roi_df, role):
        """Handle general queries"""
        summary = self.analytics.generate_executive_summary(df, roi_df)
        
        response = f"## 📊 Product Roadmap Overview\n\n"
        response += f"**Current Status:**\n"
        response += f"- Total Features: {summary['total_features']}\n"
        response += f"- High Priority: {summary['high_priority_features']}\n"
        response += f"- Quick Wins Available: {summary['quick_wins']}\n"
        response += f"- Total Effort: {summary['total_effort_sp']} story points\n\n"
        
        if summary['avg_roi'] > 0:
            response += f"**Financial Outlook:**\n"
            response += f"- Average ROI: {summary['avg_roi']:.1f}%\n"
            response += f"- Projected Revenue: ${summary['total_projected_revenue']:,.0f}\n"
            response += f"- Total Investment: ${summary['total_investment']:,.0f}\n\n"
        
        response += f"**Strategic Metrics:**\n"
        response += f"- Business Impact Score: {summary['avg_business_impact']:.1f}/100\n"
        response += f"- Strategic Alignment: {summary['strategic_alignment_score']:.1f}/100\n\n"
        
        response += f"**🎯 Key Recommendations:**\n"
        response += f"1. Focus on the top {summary['high_priority_features']} high-priority features\n"
        response += f"2. Prioritize the {summary['quick_wins']} quick win opportunities\n"
        response += f"3. Monitor {summary['high_risk_features']} features with elevated risk\n"
        response += f"4. Consider team capacity for {summary['total_effort_sp']} total story points\n"
        
        return response
    
    def _extract_feature_name(self, query, feature_list):
        """Extract feature name from query text"""
        query_lower = query.lower()
        
        # Look for exact or partial matches
        for feature in feature_list:
            feature_words = feature.lower().split()
            if len(feature_words) > 1:
                # Check if multiple words from feature are in query
                if sum(word in query_lower for word in feature_words) >= len(feature_words) // 2:
                    return feature
            elif feature.lower() in query_lower:
                return feature
        
        return None
    
    def simulate_scenario(self, scenario_params):
        """Simulate different roadmap scenarios"""
        df, _ = self.analytics.generate_comprehensive_analysis()
        
        modified_df = df.copy()
        
        # Apply scenario modifications
        if 'boost_features' in scenario_params:
            boost_features = scenario_params['boost_features']
            for feature in boost_features:
                mask = modified_df['feature_name'].str.contains(feature, case=False, na=False)
                modified_df.loc[mask, 'composite_score'] *= 1.5
        
        if 'reduce_effort' in scenario_params:
            effort_reduction = scenario_params['reduce_effort']
            modified_df['effort_estimate'] *= (1 - effort_reduction)
        
        if 'exclude_features' in scenario_params:
            exclude_features = scenario_params['exclude_features']
            for feature in exclude_features:
                mask = ~modified_df['feature_name'].str.contains(feature, case=False, na=False)
                modified_df = modified_df[mask]
        
        # Recalculate rankings
        modified_df = modified_df.sort_values('composite_score', ascending=False)
        modified_df['priority_rank'] = range(1, len(modified_df) + 1)
        
        # Generate scenario analysis
        scenario_analysis = {
            'scenario_name': scenario_params.get('name', 'Custom Scenario'),
            'total_features': len(modified_df),
            'top_5_features': modified_df.head(5)['feature_name'].tolist(),
            'total_effort': modified_df['effort_estimate'].sum(),
            'avg_priority_score': modified_df['composite_score'].mean(),
            'changes_from_baseline': len(set(df['feature_name'].head(10)) - set(modified_df['feature_name'].head(10)))
        }
        
        return scenario_analysis

