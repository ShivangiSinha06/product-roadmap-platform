import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import sqlite3
import os

from utils.database_manager import DatabaseManager
from utils.prioritization_engine import FeaturePrioritizationEngine
from utils.analytics_engine import ProductAnalytics
from utils.ai_assistant import ProductAIAssistant

st.set_page_config(
    page_title="Product Roadmap Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .priority-high {
        background-color: #ff4757;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .priority-medium {
        background-color: #ffa502;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .priority-low {
        background-color: #2ed573;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .quarter-q1 {
        background-color: #e74c3c;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
    }
    
    .quarter-q2 {
        background-color: #f39c12;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
    }
    
    .quarter-q3 {
        background-color: #27ae60;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
    }
    
    .quarter-q4 {
        background-color: #3498db;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
    }
    
    .chat-message-user {
        background-color: #007bff;
        color: white;
        padding: 15px 20px;
        border-radius: 18px;
        margin: 10px 0;
        max-width: 80%;
        margin-left: auto;
        margin-right: 0;
        box-shadow: 0 2px 10px rgba(0, 123, 255, 0.3);
    }
    
    .chat-message-assistant {
        background-color: #ffffff;
        color: #2c3e50;
        padding: 15px 20px;
        border-radius: 18px;
        margin: 10px 0;
        max-width: 80%;
        margin-left: 0;
        margin-right: auto;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        border: 1px solid #e9ecef;
        font-size: 14px;
        line-height: 1.6;
    }
    
    .chat-container {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 15px;
        max-height: 600px;
        overflow-y: auto;
        border: 1px solid #dee2e6;
    }
    
    .footer {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        padding: 30px 20px;
        margin-top: 50px;
        border-radius: 10px;
        box-shadow: 0 -4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .footer h3 {
        margin-bottom: 15px;
        font-size: 1.2rem;
    }
    
    .footer p {
        margin: 5px 0;
        opacity: 0.9;
    }
    
    .footer a {
        color: #ffd700;
        text-decoration: none;
        font-weight: bold;
    }
    
    .footer a:hover {
        text-decoration: underline;
    }
    
    .sidebar .element-container {
        margin-bottom: 1rem;
    }
    
    .dataframe {
        border: none;
    }
    
    .dataframe th {
        background-color: #667eea !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    if 'db_manager' not in st.session_state:
        st.session_state.db_manager = DatabaseManager()
    
    if 'prioritization_engine' not in st.session_state:
        st.session_state.prioritization_engine = FeaturePrioritizationEngine(st.session_state.db_manager)
    
    if 'analytics' not in st.session_state:
        st.session_state.analytics = ProductAnalytics(
            st.session_state.db_manager, 
            st.session_state.prioritization_engine
        )
    
    if 'ai_assistant' not in st.session_state:
        st.session_state.ai_assistant = ProductAIAssistant(
            st.session_state.db_manager,
            st.session_state.analytics
        )
    
    if 'dashboard_data' not in st.session_state:
        st.session_state.dashboard_data = None
    
    if 'data_last_updated' not in st.session_state:
        st.session_state.data_last_updated = None
    
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = [{
            "role": "assistant", 
            "content": "Hello! I'm your AI Product Assistant. I can help you analyze feature priorities, roadmap planning, ROI calculations, and strategic decisions. What would you like to know?"
        }]

@st.cache_data(ttl=300)
def load_dashboard_data():
    try:
        feedback_summary = st.session_state.db_manager.get_feedback_summary()
        
        if feedback_summary.empty:
            with st.spinner("Generating sample data for demonstration..."):
                st.session_state.db_manager.generate_sample_data()
        
        analysis_df, model_stats = st.session_state.analytics.generate_comprehensive_analysis()
        roi_df = st.session_state.analytics.calculate_roi_projections(analysis_df)
        segment_analysis, segment_priorities = st.session_state.analytics.analyze_customer_segments()
        executive_summary = st.session_state.analytics.generate_executive_summary(analysis_df, roi_df)
        
        return {
            'analysis_df': analysis_df,
            'roi_df': roi_df,
            'segment_analysis': segment_analysis,
            'segment_priorities': segment_priorities,
            'executive_summary': executive_summary,
            'model_stats': model_stats,
            'last_updated': datetime.now()
        }
    
    except Exception as e:
        st.error(f"Error loading dashboard data: {str(e)}")
        return None

def show_header():
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Product Roadmap Platform</h1>
        <p>AI-Driven Feature Prioritization & Strategic Planning</p>
    </div>
    """, unsafe_allow_html=True)

def show_sidebar():
    with st.sidebar:
        st.title("🎯 Navigation")
        
        page = st.selectbox(
            "Choose a page:",
            [
                "📊 Dashboard Overview",
                "🎯 Priority Matrix",
                "📅 Roadmap Timeline", 
                "💰 ROI Analysis",
                "🤖 AI Assistant",
                "📈 Analytics Deep Dive",
                "👥 Customer Segments",
                "⚙️ Data Management"
            ]
        )
        
        st.markdown("---")
        
        st.subheader("🔧 Quick Actions")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh", use_container_width=True):
                st.cache_data.clear()
                st.rerun()
        
        with col2:
            if st.button("🤖 Train ML", use_container_width=True):
                with st.spinner("Training ML model..."):
                    st.session_state.prioritization_engine.train_ml_prioritization_model()
                st.success("Model updated!")
        
        if st.session_state.dashboard_data:
            st.markdown("---")
            st.subheader("📊 System Status")
            
            last_updated = st.session_state.dashboard_data['last_updated']
            st.caption(f"Last updated: {last_updated.strftime('%H:%M:%S')}")
            
            stats = st.session_state.dashboard_data['executive_summary']
            st.metric("Total Features", stats['total_features'])
            st.metric("High Priority", stats['high_priority_features'])
            
            model_stats = st.session_state.dashboard_data['model_stats']
            if model_stats['test_score'] > 0:
                st.metric("ML Model Score", f"{model_stats['test_score']:.2f}")
        
        return page

def show_dashboard_overview():
    st.header("📊 Dashboard Overview")
    
    if not st.session_state.dashboard_data:
        st.error("No data available. Please refresh the page.")
        return
    
    data = st.session_state.dashboard_data
    analysis_df = data['analysis_df']
    roi_df = data['roi_df']
    summary = data['executive_summary']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Features",
            value=summary['total_features'],
            delta=f"{summary['high_priority_features']} high priority"
        )
    
    with col2:
        st.metric(
            label="Quick Wins",
            value=summary['quick_wins'],
            delta="Low effort, high impact"
        )
    
    with col3:
        avg_roi = summary['avg_roi']
        st.metric(
            label="Average ROI",
            value=f"{avg_roi:.1f}%" if avg_roi > 0 else "N/A",
            delta="Expected return"
        )
    
    with col4:
        revenue = summary['total_projected_revenue']
        st.metric(
            label="Projected Revenue",
            value=f"${revenue/1000000:.1f}M" if revenue > 0 else "N/A",
            delta="Annual estimate"
        )
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Top Priority Features")
        top_features = analysis_df.head(10)
        
        fig = px.bar(
            top_features,
            x='composite_score',
            y='feature_name',
            color='impact_score',
            orientation='h',
            title="Feature Priority Scores",
            color_continuous_scale='viridis',
            hover_data=['effort_estimate', 'rice_score']
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📅 Quarterly Distribution")
        quarter_dist = analysis_df['recommended_quarter'].value_counts()
        
        fig = px.pie(
            values=quarter_dist.values,
            names=quarter_dist.index,
            title="Features by Quarter",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("📋 Feature Priority Rankings")
    
    display_df = analysis_df[['feature_name', 'priority_rank', 'composite_score', 'rice_score', 'effort_estimate', 'recommended_quarter']].head(15).copy()
    display_df['composite_score'] = display_df['composite_score'].round(2)
    display_df['rice_score'] = display_df['rice_score'].round(2)
    
    display_df.columns = ['Feature Name', 'Rank', 'Priority Score', 'RICE Score', 'Effort (SP)', 'Quarter']
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Rank": st.column_config.NumberColumn("Rank", format="%d"),
            "Priority Score": st.column_config.NumberColumn("Priority Score", format="%.2f"),
            "RICE Score": st.column_config.NumberColumn("RICE Score", format="%.2f"),
            "Effort (SP)": st.column_config.NumberColumn("Effort (SP)", format="%d"),
        }
    )

def show_priority_matrix():
    st.header("🎯 Priority Matrix: Impact vs Effort")
    
    if not st.session_state.dashboard_data:
        st.error("No data available.")
        return
    
    analysis_df = st.session_state.dashboard_data['analysis_df']
    
    st.subheader("🔍 Filters")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        quarters = st.multiselect(
            "Quarters:",
            options=analysis_df['recommended_quarter'].unique(),
            default=analysis_df['recommended_quarter'].unique()
        )
    
    with col2:
        min_score = st.slider(
            "Minimum Priority Score:",
            min_value=float(analysis_df['composite_score'].min()),
            max_value=float(analysis_df['composite_score'].max()),
            value=float(analysis_df['composite_score'].min())
        )
    
    with col3:
        max_effort = st.slider(
            "Maximum Effort (SP):",
            min_value=int(analysis_df['effort_estimate'].min()),
            max_value=int(analysis_df['effort_estimate'].max()),
            value=int(analysis_df['effort_estimate'].max())
        )
    
    filtered_df = analysis_df[
        (analysis_df['recommended_quarter'].isin(quarters)) &
        (analysis_df['composite_score'] >= min_score) &
        (analysis_df['effort_estimate'] <= max_effort)
    ]
    
    if filtered_df.empty:
        st.warning("No features match the selected filters.")
        return
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Priority Matrix")
        
        fig = px.scatter(
            filtered_df,
            x='effort_estimate',
            y='impact_score',
            size='reach_score',
            color='composite_score',
            hover_name='feature_name',
            hover_data=['rice_score', 'confidence_score'],
            title='Impact vs Effort Analysis',
            labels={
                'effort_estimate': 'Effort (Story Points)',
                'impact_score': 'Impact Score',
                'composite_score': 'Priority Score'
            },
            color_continuous_scale='RdYlGn'
        )
        
        median_effort = filtered_df['effort_estimate'].median()
        median_impact = filtered_df['impact_score'].median()
        
        fig.add_hline(y=median_impact, line_dash="dash", line_color="gray", opacity=0.7)
        fig.add_vline(x=median_effort, line_dash="dash", line_color="gray", opacity=0.7)
        
        fig.add_annotation(x=median_effort*0.5, y=median_impact*1.3, text="Quick Wins", showarrow=False, bgcolor="rgba(0,255,0,0.2)", bordercolor="green")
        fig.add_annotation(x=median_effort*1.5, y=median_impact*1.3, text="Major Projects", showarrow=False, bgcolor="rgba(255,255,0,0.2)", bordercolor="orange")
        fig.add_annotation(x=median_effort*0.5, y=median_impact*0.7, text="Fill-ins", showarrow=False, bgcolor="rgba(128,128,128,0.2)", bordercolor="gray")
        fig.add_annotation(x=median_effort*1.5, y=median_impact*0.7, text="Questionable", showarrow=False, bgcolor="rgba(255,0,0,0.2)", bordercolor="red")
        
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Quadrant Analysis")
        
        quick_wins = filtered_df[(filtered_df['effort_estimate'] <= median_effort) & (filtered_df['impact_score'] > median_impact)]
        major_projects = filtered_df[(filtered_df['effort_estimate'] > median_effort) & (filtered_df['impact_score'] > median_impact)]
        fill_ins = filtered_df[(filtered_df['effort_estimate'] <= median_effort) & (filtered_df['impact_score'] <= median_impact)]
        questionable = filtered_df[(filtered_df['effort_estimate'] > median_effort) & (filtered_df['impact_score'] <= median_impact)]
        
        st.success(f"**🟢 Quick Wins ({len(quick_wins)})**")
        if not quick_wins.empty:
            for feature in quick_wins['feature_name'].head(3):
                st.write(f"• {feature}")
        
        st.warning(f"**🟡 Major Projects ({len(major_projects)})**")
        if not major_projects.empty:
            for feature in major_projects['feature_name'].head(3):
                st.write(f"• {feature}")
        
        st.info(f"**⚪ Fill-ins ({len(fill_ins)})**")
        if not fill_ins.empty:
            for feature in fill_ins['feature_name'].head(3):
                st.write(f"• {feature}")
        
        st.error(f"**🔴 Questionable ({len(questionable)})**")
        if not questionable.empty:
            for feature in questionable['feature_name'].head(3):
                st.write(f"• {feature}")

def show_roadmap_timeline():
    st.header("📅 Roadmap Timeline")
    
    if not st.session_state.dashboard_data:
        st.error("No data available.")
        return
    
    analysis_df = st.session_state.dashboard_data['analysis_df']
    
    st.subheader("📊 Quarterly Overview")
    
    quarterly_summary = analysis_df.groupby('recommended_quarter').agg({
        'feature_name': 'count',
        'effort_estimate': 'sum',
        'composite_score': 'mean'
    }).round(2)
    quarterly_summary.columns = ['Features', 'Total Effort (SP)', 'Avg Priority Score']
    
    team_capacity_per_quarter = st.number_input("Team Capacity (SP per Quarter):", min_value=50, max_value=300, value=120, step=10)
    
    quarterly_summary['Capacity Utilization %'] = (quarterly_summary['Total Effort (SP)'] / team_capacity_per_quarter * 100).round(1)
    quarterly_summary['Status'] = quarterly_summary['Capacity Utilization %'].apply(
        lambda x: '🔴 Over' if x > 100 else '🟡 High' if x > 80 else '🟢 OK'
    )
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.dataframe(quarterly_summary, use_container_width=True)
    
    with col2:
        fig = px.bar(
            x=quarterly_summary.index,
            y=quarterly_summary['Total Effort (SP)'],
            title="Effort vs Capacity by Quarter",
            color=quarterly_summary['Capacity Utilization %'],
            color_continuous_scale='RdYlGn_r'
        )
        fig.add_hline(y=team_capacity_per_quarter, line_dash="dash", line_color="red", annotation_text="Team Capacity")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("🗓️ Feature Timeline")
    
    timeline_data = st.session_state.analytics.create_timeline_data(analysis_df)
    
    if not timeline_data.empty:
        fig = px.timeline(
            timeline_data.head(20),
            x_start='start_date',
            x_end='end_date',
            y='feature_name',
            color='quarter',
            hover_data=['effort', 'priority_score', 'team'],
            title="Feature Development Timeline (Top 20)"
        )
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(height=800)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("🔍 Quarterly Details")
    
    selected_quarter = st.selectbox(
        "Select Quarter for Details:",
        options=analysis_df['recommended_quarter'].unique()
    )
    
    quarter_features = analysis_df[analysis_df['recommended_quarter'] == selected_quarter]
    
    if not quarter_features.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**{selected_quarter} Features:**")
            
            for _, feature in quarter_features.head(10).iterrows():
                with st.container():
                    st.write(f"**{feature['feature_name']}**")
                    
                    subcol1, subcol2, subcol3 = st.columns(3)
                    with subcol1:
                        st.caption(f"Score: {feature['composite_score']:.2f}")
                    with subcol2:
                        st.caption(f"Effort: {feature['effort_estimate']:.0f} SP")
                    with subcol3:
                        st.caption(f"Impact: {feature['impact_score']:.1f}")
                    
                    st.markdown("---")
        
        with col2:
            st.write(f"**{selected_quarter} Statistics:**")
            
            quarter_stats = {
                "Total Features": len(quarter_features),
                "Total Effort": f"{quarter_features['effort_estimate'].sum():.0f} SP",
                "Average Priority": f"{quarter_features['composite_score'].mean():.2f}",
                "Capacity Utilization": f"{(quarter_features['effort_estimate'].sum() / team_capacity_per_quarter * 100):.1f}%",
                "High Impact Features": len(quarter_features[quarter_features['impact_score'] >= 2]),
                "Quick Wins": len(quarter_features[(quarter_features['effort_estimate'] <= quarter_features['effort_estimate'].median()) & (quarter_features['impact_score'] > quarter_features['impact_score'].median())])
            }
            
            for key, value in quarter_stats.items():
                st.metric(key, value)

def show_roi_analysis():
    st.header("💰 ROI Analysis")
    
    if not st.session_state.dashboard_data:
        st.error("No data available.")
        return
    
    roi_df = st.session_state.dashboard_data['roi_df']
    analysis_df = st.session_state.dashboard_data['analysis_df']
    
    if roi_df.empty:
        st.warning("ROI analysis requires revenue impact data. Please add revenue estimates in Data Management.")
        return
    
    st.subheader("📊 Portfolio Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_investment = roi_df['development_cost'].sum()
    total_revenue = roi_df['projected_annual_revenue'].sum()
    portfolio_roi = ((total_revenue - total_investment) / total_investment * 100) if total_investment > 0 else 0
    avg_payback = roi_df[roi_df['payback_months'] != float('inf')]['payback_months'].mean()
    
    with col1:
        st.metric("Total Investment", f"${total_investment:,.0f}")
    with col2:
        st.metric("Projected Revenue", f"${total_revenue:,.0f}")
    with col3:
        st.metric("Portfolio ROI", f"{portfolio_roi:.1f}%")
    with col4:
        st.metric("Avg Payback", f"{avg_payback:.1f} months" if not pd.isna(avg_payback) else "N/A")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 ROI by Feature")
        top_roi = roi_df.nlargest(10, 'roi_percentage')
        
        fig = px.bar(
            top_roi,
            x='roi_percentage',
            y='feature_name',
            orientation='h',
            title="Return on Investment (%)",
            color='roi_percentage',
            color_continuous_scale='RdYlGn',
            hover_data=['development_cost', 'projected_annual_revenue']
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💡 Investment vs Revenue")
        
        fig = px.scatter(
            roi_df,
            x='development_cost',
            y='projected_annual_revenue',
            size='roi_percentage',
            color='payback_months',
            hover_name='feature_name',
            title="Investment vs Revenue Scatter",
            labels={
                'development_cost': 'Development Cost ($)',
                'projected_annual_revenue': 'Projected Revenue ($)'
            },
            color_continuous_scale='RdYlGn_r'
        )
        
        max_val = max(roi_df['development_cost'].max(), roi_df['projected_annual_revenue'].max())
        fig.add_trace(
            go.Scatter(
                x=[0, max_val],
                y=[0, max_val],
                mode='lines',
                name='Break-even Line',
                line=dict(dash='dash', color='red')
            )
        )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("⚖️ Risk vs ROI Analysis")
    
    if 'risk_score' in roi_df.columns:
        fig = px.scatter(
            roi_df,
            x='risk_score',
            y='roi_percentage',
            size='development_cost',
            color='confidence_level',
            hover_name='feature_name',
            title="Risk vs ROI Matrix",
            labels={
                'risk_score': 'Risk Score (0-100)',
                'roi_percentage': 'ROI (%)'
            }
        )
        
        risk_median = roi_df['risk_score'].median()
        roi_median = roi_df['roi_percentage'].median()
        
        fig.add_hline(y=roi_median, line_dash="dash", line_color="gray", opacity=0.5)
        fig.add_vline(x=risk_median, line_dash="dash", line_color="gray", opacity=0.5)
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("📋 Detailed ROI Analysis")
    
    display_roi = roi_df.copy()
    display_roi['development_cost'] = display_roi['development_cost'].apply(lambda x: f"${x:,.0f}")
    display_roi['projected_annual_revenue'] = display_roi['projected_annual_revenue'].apply(lambda x: f"${x:,.0f}")
    display_roi['roi_percentage'] = display_roi['roi_percentage'].apply(lambda x: f"{x:.1f}%")
    display_roi['payback_months'] = display_roi['payback_months'].apply(lambda x: f"{x:.1f}" if x != float('inf') else "Never")
    
    display_cols = ['feature_name', 'development_cost', 'projected_annual_revenue', 'roi_percentage', 'payback_months']
    if 'risk_score' in display_roi.columns:
        display_roi['risk_score'] = display_roi['risk_score'].apply(lambda x: f"{x:.0f}/100")
        display_cols.append('risk_score')
    
    st.dataframe(
        display_roi[display_cols],
        column_config={
            "feature_name": "Feature Name",
            "development_cost": "Investment", 
            "projected_annual_revenue": "Projected Revenue",
            "roi_percentage": "ROI",
            "payback_months": "Payback (Months)",
            "risk_score": "Risk Score"
        },
        use_container_width=True,
        hide_index=True
    )

def show_ai_assistant():
    st.header("🤖 AI Product Assistant")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.write("I can help you analyze feature priorities, roadmap planning, ROI calculations, and strategic decisions.")
    
    with col2:
        stakeholder_role = st.selectbox(
            "Your Role:",
            ["Product Manager", "Engineering Manager", "Executive", "Designer", "Data Analyst", "Marketing Manager"]
        )
    
    st.subheader("💬 Chat")
    
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for message in st.session_state.chat_messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message-user">
                <strong>You:</strong><br>{message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message-assistant">
                <strong>🤖 AI Assistant:</strong><br>{message["content"]}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("---")
        st.subheader("💡 Suggested Questions")
        
        suggested_queries = [
            "What are the top 5 priority features?",
            "Show me Q1 2026 roadmap details",
            "What's the ROI for dark mode support?",
            "Compare mobile app vs API improvements",
            "What are our biggest risks?",
            "How is our team capacity looking?",
            "Which features have the best ROI?",
            "Show me quick wins for this quarter"
        ]
        
        for query in suggested_queries:
            if st.button(query, key=f"suggest_{hash(query)}", use_container_width=True):
                st.session_state.chat_messages.append({"role": "user", "content": query})
                
                with st.spinner("Thinking..."):
                    response = st.session_state.ai_assistant.process_query(query, stakeholder_role)
                
                st.session_state.chat_messages.append({"role": "assistant", "content": response})
                st.rerun()
    
    user_input = st.chat_input("Ask me anything about your product roadmap...")
    
    if user_input:
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        
        with st.spinner("Analyzing..."):
            response = st.session_state.ai_assistant.process_query(user_input, stakeholder_role)
        
        st.session_state.chat_messages.append({"role": "assistant", "content": response})
        st.rerun()
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_messages = [{
            "role": "assistant", 
            "content": "Hello! I'm your AI Product Assistant. How can I help you today?"
        }]
        st.rerun()

def show_analytics_deep_dive():
    st.header("📈 Analytics Deep Dive")
    
    if not st.session_state.dashboard_data:
        st.error("No data available.")
        return
    
    analysis_df = st.session_state.dashboard_data['analysis_df']
    model_stats = st.session_state.dashboard_data['model_stats']
    
    st.subheader("🤖 ML Model Performance")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Training Score", f"{model_stats.get('train_score', 0):.3f}")
    with col2:
        st.metric("Test Score", f"{model_stats.get('test_score', 0):.3f}")
    with col3:
        if model_stats.get('test_score', 0) > 0.7:
            st.success("Model Performance: Good")
        elif model_stats.get('test_score', 0) > 0.5:
            st.warning("Model Performance: Fair")
        else:
            st.error("Model Performance: Poor")
    
    importance_df = st.session_state.prioritization_engine.get_feature_importance()
    if importance_df is not None:
        st.subheader("🎯 Feature Importance")
        
        fig = px.bar(
            importance_df,
            x='importance',
            y='feature',
            orientation='h',
            title="ML Model Feature Importance",
            color='importance',
            color_continuous_scale='viridis'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("📊 Statistical Analysis")
    
    tab1, tab2, tab3 = st.tabs(["Distribution Analysis", "Correlation Analysis", "Scoring Breakdown"])
    
    with tab1:
        fig = make_subplots(rows=2, cols=2, subplot_titles=["Priority Scores", "Effort Estimates", "Impact Scores", "Confidence Scores"])
        
        fig.add_trace(go.Histogram(x=analysis_df['composite_score'], name="Priority"), row=1, col=1)
        fig.add_trace(go.Histogram(x=analysis_df['effort_estimate'], name="Effort"), row=1, col=2)
        fig.add_trace(go.Histogram(x=analysis_df['impact_score'], name="Impact"), row=2, col=1)
        fig.add_trace(go.Histogram(x=analysis_df['confidence_score'], name="Confidence"), row=2, col=2)
        
        fig.update_layout(height=600, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Summary Statistics")
        numeric_cols = ['composite_score', 'rice_score', 'effort_estimate', 'impact_score', 'confidence_score', 'reach_score']
        summary_stats = analysis_df[numeric_cols].describe().round(2)
        st.dataframe(summary_stats, use_container_width=True)
    
    with tab2:
        corr_cols = ['composite_score', 'rice_score', 'reach_score', 'impact_score', 'confidence_score', 'effort_estimate']
        corr_matrix = analysis_df[corr_cols].corr()
        
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title="Feature Metrics Correlation Matrix",
            color_continuous_scale='RdBu'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("**Key Correlations:**")
        high_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                if abs(corr_val) > 0.5:
                    high_corr.append(f"• {corr_matrix.columns[i]} ↔ {corr_matrix.columns[j]}: {corr_val:.3f}")
        
        for corr in high_corr[:5]:
            st.write(corr)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**RICE Components Distribution:**")
            rice_components = analysis_df[['reach_score', 'impact_score', 'confidence_score', 'effort_estimate']].head(10)
            
            fig = px.bar(
                rice_components,
                x=rice_components.index,
                y=['reach_score', 'impact_score', 'confidence_score'],
                title="RICE Components by Feature",
                barmode='group'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Scoring Methods Comparison:**")
            
            fig = px.scatter(
                analysis_df,
                x='rice_score',
                y='composite_score',
                hover_name='feature_name',
                title="RICE vs Composite Score",
                trendline="ols"
            )
            st.plotly_chart(fig, use_container_width=True)

def show_customer_segments():
    st.header("👥 Customer Segments Analysis")
    
    if not st.session_state.dashboard_data:
        st.error("No data available.")
        return
    
    segment_analysis = st.session_state.dashboard_data['segment_analysis']
    segment_priorities = st.session_state.dashboard_data['segment_priorities']
    
    st.subheader("📊 Segment Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            segment_priorities,
            x='customer_segment',
            y='segment_priority_score',
            title="Segment Priority Scores",
            color='segment_priority_score',
            color_continuous_scale='viridis'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        segment_requests = segment_analysis.groupby('customer_segment')['request_count'].sum().reset_index()
        
        fig = px.pie(
            segment_requests,
            values='request_count',
            names='customer_segment',
            title="Requests by Segment"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("🔍 Segment Details")
    
    selected_segment = st.selectbox(
        "Select Segment:",
        options=segment_analysis['customer_segment'].unique()
    )
    
    segment_data = segment_analysis[segment_analysis['customer_segment'] == selected_segment]
    
    if not segment_data.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Top Features for {selected_segment}:**")
            
            top_segment_features = segment_data.nlargest(10, 'request_count')
            
            for _, feature in top_segment_features.iterrows():
                st.write(f"**{feature['feature_request']}**")
                st.write(f"  - Requests: {feature['request_count']}")
                st.write(f"  - Avg Revenue Impact: ${feature['avg_revenue_impact']:,.0f}")
                st.write(f"  - Business Value: {feature['avg_business_value']:.1f}/10")
                st.write("---")
        
        with col2:
            st.write(f"**{selected_segment} Metrics:**")
            
            segment_metrics = {
                "Total Features Requested": len(segment_data),
                "Total Requests": segment_data['request_count'].sum(),
                "Avg Revenue Impact": f"${segment_data['avg_revenue_impact'].mean():,.0f}",
                "Avg Business Value": f"{segment_data['avg_business_value'].mean():.1f}/10",
                "High-Value Features": len(segment_data[segment_data['avg_business_value'] > 7])
            }
            
            for metric, value in segment_metrics.items():
                st.metric(metric, value)

def show_data_management():
    st.header("⚙️ Data Management")
    
    st.subheader("📝 Add Customer Feedback")
    
    with st.form("feedback_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            customer_id = st.text_input("Customer ID", value="CUST_0001", help="Unique customer identifier")
            feature_request = st.text_input("Feature Request", value="", help="Name of the requested feature")
            feedback_type = st.selectbox("Feedback Type", ["feature_request", "enhancement", "bug_report"])
            priority_level = st.selectbox("Priority Level", ["low", "medium", "high", "critical"])
        
        with col2:
            source = st.selectbox("Source", ["support_ticket", "survey", "user_interview", "sales", "product_feedback"])
            customer_segment = st.selectbox("Customer Segment", ["Enterprise", "SMB", "Startup", "Individual"])
            revenue_impact = st.number_input("Revenue Impact ($)", min_value=0, value=10000, step=1000)
            effort_estimate = st.slider("Effort Estimate (Story Points)", min_value=1, max_value=25, value=8)
            business_value_score = st.slider("Business Value Score (1-10)", min_value=1, max_value=10, value=7)
        
        submitted = st.form_submit_button("➕ Add Feedback", use_container_width=True)
        
        if submitted and feature_request:
            try:
                feedback_data = (
                    customer_id, feature_request, feedback_type, priority_level, 
                    source, customer_segment, revenue_impact, effort_estimate, business_value_score
                )
                
                st.session_state.db_manager.add_feedback(feedback_data)
                st.success(f"✅ Feedback for '{feature_request}' added successfully!")
                
                st.cache_data.clear()
                
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ Error adding feedback: {str(e)}")
        elif submitted:
            st.warning("⚠️ Please fill in the feature request field.")
    
    st.markdown("---")
    
    st.subheader("📤 Export Data")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Export Priority Analysis", use_container_width=True):
            if st.session_state.dashboard_data:
                priority_df = st.session_state.dashboard_data['analysis_df']
                csv = priority_df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv,
                    file_name=f"feature_priorities_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    
    with col2:
        if st.button("💰 Export ROI Data", use_container_width=True):
            if st.session_state.dashboard_data and not st.session_state.dashboard_data['roi_df'].empty:
                roi_df = st.session_state.dashboard_data['roi_df']
                csv = roi_df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv,
                    file_name=f"roi_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.warning("No ROI data available")
    
    with col3:
        if st.button("👥 Export Segment Data", use_container_width=True):
            if st.session_state.dashboard_data:
                segment_df = st.session_state.dashboard_data['segment_analysis']
                csv = segment_df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv,
                    file_name=f"customer_segments_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    
    with col4:
        if st.button("🔄 Generate Sample Data", use_container_width=True):
            with st.spinner("Generating sample data..."):
                st.session_state.db_manager.generate_sample_data()
                st.cache_data.clear()
                st.success("✅ Sample data generated!")
                st.rerun()
    
    st.markdown("---")
    
    st.subheader("📈 Database Statistics")
    
    try:
        feedback_df = st.session_state.db_manager.get_feedback_summary()
        usage_df = st.session_state.db_manager.get_usage_analytics()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📝 Feedback Records", len(feedback_df))
        with col2:
            st.metric("📊 Usage Records", len(usage_df))
        with col3:
            st.metric("🎯 Unique Features", len(feedback_df['feature_request'].unique()) if not feedback_df.empty else 0)
        with col4:
            st.metric("👥 Customer Segments", len(feedback_df['customer_segment'].unique()) if not feedback_df.empty else 0)
        
        if not feedback_df.empty:
            st.subheader("🕒 Recent Activity")
            
            recent_features = feedback_df.nlargest(5, 'request_count')[['feature_request', 'request_count', 'avg_business_value']]
            
            st.write("**Most Requested Features:**")
            for _, feature in recent_features.iterrows():
                st.write(f"• **{feature['feature_request']}** - {feature['request_count']} requests (Value: {feature['avg_business_value']:.1f}/10)")
    
    except Exception as e:
        st.error(f"Error loading database statistics: {str(e)}")

def show_footer():
    st.markdown("""
    <div class="footer">
        <h3>🚀 Product Roadmap Platform</h3>
        <p>AI-Driven Feature Prioritization & Strategic Planning</p>
        <p>Built with Streamlit • Powered by Machine Learning</p>
        <hr style="margin: 20px 0; border: none; height: 1px; background: rgba(255,255,255,0.3);">
        <p><strong>Created by:</strong> <a href="mailto:shivangisinha.work@gmail.com">Shivangi Sinha</a></p>
        <p><strong>Contact:</strong> shivangisinha.work@gmail.com</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    initialize_session_state()
    
    show_header()
    
    selected_page = show_sidebar()
    
    if st.session_state.dashboard_data is None:
        with st.spinner("Loading dashboard data..."):
            st.session_state.dashboard_data = load_dashboard_data()
    
    if selected_page == "📊 Dashboard Overview":
        show_dashboard_overview()
    elif selected_page == "🎯 Priority Matrix":
        show_priority_matrix()
    elif selected_page == "📅 Roadmap Timeline":
        show_roadmap_timeline()
    elif selected_page == "💰 ROI Analysis":
        show_roi_analysis()
    elif selected_page == "🤖 AI Assistant":
        show_ai_assistant()
    elif selected_page == "📈 Analytics Deep Dive":
        show_analytics_deep_dive()
    elif selected_page == "👥 Customer Segments":
        show_customer_segments()
    elif selected_page == "⚙️ Data Management":
        show_data_management()
    
    show_footer()

if __name__ == "__main__":
    main()

