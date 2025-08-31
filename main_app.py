# 🚀 Product Roadmap Platform
# AI-Driven Feature Prioritization & Strategic Planning

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import sqlite3
import os

# Import your custom modules with error handling
try:
    from utils.database_manager import DatabaseManager
    from utils.prioritization_engine import FeaturePrioritizationEngine
    from utils.analytics_engine import ProductAnalytics
    from utils.ai_assistant import ProductAIAssistant
except ImportError as e:
    st.error(f"Error importing modules: {str(e)}")
    st.stop()

# Set page config
st.set_page_config(
    page_title="Product Roadmap Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    
    .priority-high { border-left-color: #e74c3c !important; }
    .priority-medium { border-left-color: #f39c12 !important; }
    .priority-low { border-left-color: #2ecc71 !important; }
    
    .footer {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-top: 3rem;
    }
    
    .sidebar-content {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state with error handling"""
    try:
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
        
        if 'chat_messages' not in st.session_state:
            st.session_state.chat_messages = [{
                "role": "assistant",
                "content": "Hello! I'm your AI Product Assistant. I can help you analyze feature priorities, roadmap planning, ROI calculations, and strategic decisions. What would you like to know?"
            }]
            
    except Exception as e:
        st.error(f"Error initializing application: {str(e)}")
        st.info("The app is having trouble starting. Please refresh the page or contact support.")
        return False
    
    return True

@st.cache_data(ttl=300, show_spinner=True)
def load_dashboard_data():
    """Load dashboard data with comprehensive error handling"""
    try:
        # Check if database manager exists
        if 'db_manager' not in st.session_state:
            raise Exception("Database manager not initialized")
        
        # Check if analytics engine exists  
        if 'analytics' not in st.session_state:
            raise Exception("Analytics engine not initialized")
        
        # Generate sample data if needed
        feedback_summary = st.session_state.db_manager.get_feedback_summary()
        if feedback_summary.empty:
            with st.spinner("Generating sample data..."):
                st.session_state.db_manager.generate_sample_data()
        
        # Generate analytics
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
        st.info("Using fallback mode with limited functionality.")
        
        # Return minimal fallback data
        return {
            'analysis_df': pd.DataFrame(),
            'roi_df': pd.DataFrame(),
            'segment_analysis': pd.DataFrame(),
            'segment_priorities': pd.DataFrame(),
            'executive_summary': {
                'total_features': 0,
                'high_priority_features': 0,
                'avg_roi': 0,
                'total_projected_revenue': 0,
                'quick_wins': 0
            },
            'model_stats': {'train_score': 0, 'test_score': 0},
            'last_updated': datetime.now()
        }

def show_header():
    """Show main header"""
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Product Roadmap Platform</h1>
        <h3>AI-Driven Feature Prioritization & Strategic Planning</h3>
        <p>Make data-driven product decisions with advanced analytics and ML-powered insights</p>
    </div>
    """, unsafe_allow_html=True)

def show_sidebar():
    """Enhanced sidebar with navigation and controls"""
    with st.sidebar:
        st.markdown("## 🧭 Navigation")
        
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
        
        # Quick actions
        st.markdown("## ⚡ Quick Actions")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh", width="stretch"):
                st.session_state.dashboard_data = None
                st.rerun()
        
        with col2:
            if st.button("🤖 Train ML", width="stretch"):
                with st.spinner("Training ML model..."):
                    st.session_state.prioritization_engine.train_ml_prioritization_model()
                st.success("Model updated!")
        
        # Dashboard stats
        if st.session_state.dashboard_data:
            summary = st.session_state.dashboard_data['executive_summary']
            
            st.markdown("## 📈 Quick Stats")
            st.metric("Total Features", summary['total_features'])
            st.metric("High Priority", summary['high_priority_features'])
            st.metric("Quick Wins", summary['quick_wins'])
            
            if summary['avg_roi'] > 0:
                st.metric("Avg ROI", f"{summary['avg_roi']:.1f}%")
        
        # Last updated
        st.markdown("---")
        if st.session_state.dashboard_data:
            last_updated = st.session_state.dashboard_data['last_updated']
            st.caption(f"Last updated: {last_updated.strftime('%Y-%m-%d %H:%M')}")
    
    return page

def show_dashboard_overview():
    """Main dashboard overview page"""
    st.title("📊 Dashboard Overview")
    
    if not st.session_state.dashboard_data:
        st.warning("⚠️ Dashboard data not loaded. Please refresh the page.")
        return
    
    data = st.session_state.dashboard_data
    summary = data['executive_summary']
    analysis_df = data['analysis_df']
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Features",
            summary['total_features'],
            delta=None,
            help="Total number of features in the roadmap"
        )
    
    with col2:
        st.metric(
            "High Priority",
            summary['high_priority_features'],
            delta=None,
            help="Features with high priority scores"
        )
    
    with col3:
        st.metric(
            "Quick Wins",
            summary['quick_wins'],
            delta=None,
            help="Low effort, high impact features"
        )
    
    with col4:
        if summary['avg_roi'] > 0:
            st.metric(
                "Average ROI",
                f"{summary['avg_roi']:.1f}%",
                delta=None,
                help="Average return on investment"
            )
        else:
            st.metric("ML Model Score", f"{data['model_stats']['train_score']:.2f}")
    
    st.markdown("---")
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        if not analysis_df.empty:
            # Priority distribution
            st.subheader("🎯 Priority Distribution")
            
            # Create priority categories
            analysis_df['priority_category'] = pd.cut(
                analysis_df['composite_score'], 
                bins=[0, 33, 66, 100], 
                labels=['Low', 'Medium', 'High']
            )
            
            priority_counts = analysis_df['priority_category'].value_counts()
            
            fig = px.pie(
                values=priority_counts.values,
                names=priority_counts.index,
                color_discrete_map={
                    'High': '#e74c3c',
                    'Medium': '#f39c12', 
                    'Low': '#2ecc71'
                }
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if not analysis_df.empty:
            # Top features
            st.subheader("🏆 Top Priority Features")
            
            top_features = analysis_df.head(8)
            
            fig = go.Figure(go.Bar(
                x=top_features['composite_score'],
                y=top_features['feature_name'],
                orientation='h',
                marker_color='#667eea'
            ))
            
            fig.update_layout(
                height=350,
                xaxis_title="Priority Score",
                yaxis_title=""
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Feature details table
    st.subheader("📋 Feature Details")
    
    if not analysis_df.empty:
        # Display top 10 features
        display_df = analysis_df.head(10)[
            ['feature_name', 'composite_score', 'effort_estimate', 'recommended_quarter']
        ].copy()
        
        display_df.columns = ['Feature Name', 'Priority Score', 'Effort (SP)', 'Quarter']
        display_df['Priority Score'] = display_df['Priority Score'].round(2)
        
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("No feature data available. Please check your data sources.")

def show_priority_matrix():
    """Priority matrix visualization"""
    st.title("🎯 Priority Matrix")
    
    if not st.session_state.dashboard_data:
        st.warning("⚠️ Dashboard data not loaded.")
        return
    
    analysis_df = st.session_state.dashboard_data['analysis_df']
    
    if analysis_df.empty:
        st.info("No data available for priority matrix.")
        return
    
    # Priority matrix scatter plot
    st.subheader("📊 Effort vs Impact Analysis")
    
    fig = px.scatter(
        analysis_df,
        x='effort_estimate',
        y='impact_score',
        size='composite_score',
        color='recommended_quarter',
        hover_name='feature_name',
        hover_data=['composite_score'],
        title="Feature Priority Matrix: Effort vs Impact",
        labels={
            'effort_estimate': 'Effort (Story Points)',
            'impact_score': 'Impact Score',
            'recommended_quarter': 'Quarter'
        }
    )
    
    # Add quadrant lines
    effort_median = analysis_df['effort_estimate'].median()
    impact_median = analysis_df['impact_score'].median()
    
    fig.add_hline(y=impact_median, line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_vline(x=effort_median, line_dash="dash", line_color="gray", opacity=0.5)
    
    # Add quadrant labels
    fig.add_annotation(x=effort_median/2, y=impact_median*1.5, text="Quick Wins", showarrow=False, font=dict(size=16, color="green"))
    fig.add_annotation(x=effort_median*1.5, y=impact_median*1.5, text="Major Projects", showarrow=False, font=dict(size=16, color="red"))
    fig.add_annotation(x=effort_median/2, y=impact_median/2, text="Fill-ins", showarrow=False, font=dict(size=16, color="blue"))
    fig.add_annotation(x=effort_median*1.5, y=impact_median/2, text="Questionable", showarrow=False, font=dict(size=16, color="orange"))
    
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    # Quadrant analysis
    st.subheader("📈 Quadrant Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Quick wins
        quick_wins = analysis_df[
            (analysis_df['effort_estimate'] <= effort_median) & 
            (analysis_df['impact_score'] > impact_median)
        ]
        
        st.markdown("### 🚀 Quick Wins")
        st.write(f"**{len(quick_wins)} features** - Low effort, high impact")
        
        if not quick_wins.empty:
            for _, feature in quick_wins.head(5).iterrows():
                st.write(f"• {feature['feature_name']} (Score: {feature['composite_score']:.1f})")
    
    with col2:
        # Major projects
        major_projects = analysis_df[
            (analysis_df['effort_estimate'] > effort_median) & 
            (analysis_df['impact_score'] > impact_median)
        ]
        
        st.markdown("### 🎯 Major Projects")
        st.write(f"**{len(major_projects)} features** - High effort, high impact")
        
        if not major_projects.empty:
            for _, feature in major_projects.head(5).iterrows():
                st.write(f"• {feature['feature_name']} (Score: {feature['composite_score']:.1f})")

def show_roadmap_timeline():
    """Roadmap timeline visualization"""
    st.title("📅 Roadmap Timeline")
    
    if not st.session_state.dashboard_data:
        st.warning("⚠️ Dashboard data not loaded.")
        return
    
    analysis_df = st.session_state.dashboard_data['analysis_df']
    
    if analysis_df.empty:
        st.info("No data available for timeline.")
        return
    
    # Timeline by quarter
    st.subheader("🗓️ Quarterly Roadmap")
    
    # Group by quarter
    quarterly_data = analysis_df.groupby('recommended_quarter').agg({
        'feature_name': 'count',
        'effort_estimate': 'sum',
        'composite_score': 'mean'
    }).round(2)
    
    quarterly_data.columns = ['Features', 'Total Effort', 'Avg Priority']
    
    # Display quarterly summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Q1 2026 Features", quarterly_data.loc['Q1 2026', 'Features'] if 'Q1 2026' in quarterly_data.index else 0)
    with col2:
        st.metric("Q2 2026 Features", quarterly_data.loc['Q2 2026', 'Features'] if 'Q2 2026' in quarterly_data.index else 0)
    with col3:
        st.metric("Q3 2026 Features", quarterly_data.loc['Q3 2026', 'Features'] if 'Q3 2026' in quarterly_data.index else 0)
    
    # Quarterly details
    st.dataframe(quarterly_data, use_container_width=True)
    
    # Feature timeline chart
    st.subheader("📊 Features by Quarter")
    
    if not quarterly_data.empty:
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Features',
            x=quarterly_data.index,
            y=quarterly_data['Features'],
            marker_color='#667eea'
        ))
        
        fig.update_layout(
            title="Features Distribution by Quarter",
            xaxis_title="Quarter",
            yaxis_title="Number of Features",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed quarter view
    st.subheader("🔍 Quarter Details")
    
    quarter = st.selectbox("Select Quarter:", analysis_df['recommended_quarter'].unique())
    
    quarter_features = analysis_df[analysis_df['recommended_quarter'] == quarter]
    
    if not quarter_features.empty:
        st.write(f"**{len(quarter_features)} features planned for {quarter}**")
        
        display_df = quarter_features[
            ['feature_name', 'composite_score', 'effort_estimate', 'impact_score']
        ].copy()
        
        display_df.columns = ['Feature Name', 'Priority Score', 'Effort (SP)', 'Impact']
        display_df = display_df.round(2)
        
        st.dataframe(display_df, use_container_width=True)
        
        # Quarter summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Effort", f"{quarter_features['effort_estimate'].sum():.0f} SP")
        with col2:
            st.metric("Avg Priority", f"{quarter_features['composite_score'].mean():.1f}")
        with col3:
            st.metric("Avg Impact", f"{quarter_features['impact_score'].mean():.1f}")

def show_roi_analysis():
    """ROI analysis page"""
    st.title("💰 ROI Analysis")
    
    if not st.session_state.dashboard_data:
        st.warning("⚠️ Dashboard data not loaded.")
        return
    
    roi_df = st.session_state.dashboard_data['roi_df']
    
    if roi_df.empty:
        st.info("📊 No ROI data available. This requires revenue impact data in customer feedback.")
        return
    
    # ROI overview
    st.subheader("💼 Investment Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_investment = roi_df['development_cost'].sum()
        st.metric("Total Investment", f"${total_investment:,.0f}")
    
    with col2:
        total_revenue = roi_df['projected_annual_revenue'].sum()
        st.metric("Projected Revenue", f"${total_revenue:,.0f}")
    
    with col3:
        avg_roi = roi_df['roi_percentage'].mean()
        st.metric("Average ROI", f"{avg_roi:.1f}%")
    
    with col4:
        avg_payback = roi_df['payback_months'].mean()
        st.metric("Avg Payback", f"{avg_payback:.1f} months")
    
    # ROI charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 ROI by Feature")
        
        top_roi = roi_df.nlargest(10, 'roi_percentage')
        
        fig = go.Figure(go.Bar(
            x=top_roi['roi_percentage'],
            y=top_roi['feature_name'],
            orientation='h',
            marker_color='#2ecc71'
        ))
        
        fig.update_layout(
            xaxis_title="ROI (%)",
            yaxis_title="",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💰 Investment vs Revenue")
        
        fig = px.scatter(
            roi_df,
            x='development_cost',
            y='projected_annual_revenue',
            size='roi_percentage',
            hover_name='feature_name',
            title="Investment vs Expected Revenue"
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # ROI table
    st.subheader("📋 Detailed ROI Analysis")
    
    display_roi = roi_df.copy()
    display_roi['development_cost'] = display_roi['development_cost'].apply(lambda x: f"${x:,.0f}")
    display_roi['projected_annual_revenue'] = display_roi['projected_annual_revenue'].apply(lambda x: f"${x:,.0f}")
    display_roi['roi_percentage'] = display_roi['roi_percentage'].apply(lambda x: f"{x:.1f}%")
    display_roi['payback_months'] = display_roi['payback_months'].apply(lambda x: f"{x:.1f}")
    
    display_roi = display_roi[['feature_name', 'development_cost', 'projected_annual_revenue', 'roi_percentage', 'payback_months']]
    display_roi.columns = ['Feature', 'Investment', 'Annual Revenue', 'ROI', 'Payback (Months)']
    
    st.dataframe(display_roi, use_container_width=True)

def show_ai_assistant():
    """AI Assistant chat interface"""
    st.title("🤖 AI Product Assistant")
    
    st.markdown("""
    Ask me anything about your product roadmap! I can help with:
    - Feature priority analysis
    - ROI calculations and projections
    - Timeline and capacity planning
    - Customer segment insights
    - Strategic recommendations
    """)
    
    # Chat interface
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about your product roadmap..."):
        # Add user message
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Get AI response
                    response = st.session_state.ai_assistant.process_query(prompt)
                    st.markdown(response)
                    
                    # Add assistant response
                    st.session_state.chat_messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_messages.append({"role": "assistant", "content": error_msg})
    
    # Quick action buttons
    st.markdown("### 🎯 Quick Questions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("What are my top priorities?"):
            st.session_state.chat_messages.append({
                "role": "user", 
                "content": "What are my top priority features?"
            })
            st.rerun()
    
    with col2:
        if st.button("Show ROI analysis"):
            st.session_state.chat_messages.append({
                "role": "user",
                "content": "Can you analyze the ROI for my features?"
            })
            st.rerun()
    
    with col3:
        if st.button("Capacity planning help"):
            st.session_state.chat_messages.append({
                "role": "user",
                "content": "Help me with capacity and timeline planning"
            })
            st.rerun()

def show_analytics_deep_dive():
    """Advanced analytics page"""
    st.title("📈 Analytics Deep Dive")
    
    if not st.session_state.dashboard_data:
        st.warning("⚠️ Dashboard data not loaded.")
        return
    
    analysis_df = st.session_state.dashboard_data['analysis_df']
    model_stats = st.session_state.dashboard_data['model_stats']
    
    if analysis_df.empty:
        st.info("No analytics data available.")
        return
    
    # Model performance
    st.subheader("🤖 ML Model Performance")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Training Score", f"{model_stats['train_score']:.3f}")
    
    with col2:
        st.metric("Test Score", f"{model_stats['test_score']:.3f}")
    
    with col3:
        st.metric("Features Analyzed", len(analysis_df))
    
    # Feature correlations
    st.subheader("🔗 Feature Correlations")
    
    # Select numeric columns for correlation
    numeric_cols = ['composite_score', 'effort_estimate', 'impact_score', 'reach_score']
    available_cols = [col for col in numeric_cols if col in analysis_df.columns]
    
    if len(available_cols) > 1:
        corr_matrix = analysis_df[available_cols].corr()
        
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            color_continuous_scale='RdBu_r'
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Distribution analysis
    st.subheader("📊 Score Distributions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Priority score distribution
        fig = px.histogram(
            analysis_df,
            x='composite_score',
            nbins=20,
            title="Priority Score Distribution"
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Effort distribution
        fig = px.histogram(
            analysis_df,
            x='effort_estimate',
            nbins=15,
            title="Effort Estimate Distribution"
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    # Advanced metrics table
    st.subheader("📋 Advanced Metrics")
    
    if not analysis_df.empty:
        metrics_df = analysis_df[
            ['feature_name', 'composite_score', 'rice_score', 'effort_estimate', 'confidence_score']
        ].copy()
        
        metrics_df.columns = ['Feature', 'Composite Score', 'RICE Score', 'Effort', 'Confidence']
        metrics_df = metrics_df.round(2)
        
        st.dataframe(metrics_df, use_container_width=True)

def show_customer_segments():
    """Customer segments analysis"""
    st.title("👥 Customer Segments")
    
    if not st.session_state.dashboard_data:
        st.warning("⚠️ Dashboard data not loaded.")
        return
    
    segment_analysis = st.session_state.dashboard_data['segment_analysis']
    segment_priorities = st.session_state.dashboard_data['segment_priorities']
    
    if segment_analysis.empty and segment_priorities.empty:
        st.info("No customer segment data available.")
        return
    
    # Segment overview
    if not segment_priorities.empty:
        st.subheader("🎯 Segment Priorities")
        
        # Segment metrics
        for _, segment in segment_priorities.iterrows():
            with st.expander(f"📊 {segment['customer_segment']} Segment"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Requests", int(segment['request_count']))
                
                with col2:
                    st.metric("Avg Revenue Impact", f"${segment['avg_revenue_impact']:,.0f}")
                
                with col3:
                    st.metric("Avg Business Value", f"{segment['avg_business_value']:.1f}/10")
    
    # Segment comparison
    if not segment_analysis.empty:
        st.subheader("📈 Feature Requests by Segment")
        
        # Group by segment and feature
        segment_pivot = segment_analysis.pivot_table(
            index='feature_request',
            columns='customer_segment',
            values='request_count',
            fill_value=0
        )
        
        # Show top features
        top_features = segment_pivot.sum(axis=1).sort_values(ascending=False).head(10)
        segment_chart_data = segment_pivot.loc[top_features.index]
        
        fig = px.bar(
            segment_chart_data,
            title="Top 10 Features by Customer Segment",
            height=500
        )
        fig.update_layout(xaxis_title="Features", yaxis_title="Request Count")
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed segment analysis
        st.subheader("📋 Segment Analysis Details")
        
        display_segments = segment_analysis.copy()
        display_segments = display_segments.round(2)
        
        st.dataframe(display_segments, use_container_width=True)

def show_data_management():
    """Data management page"""
    st.title("⚙️ Data Management")
    
    st.markdown("""
    Manage your product roadmap data, import/export features, and configure settings.
    """)
    
    # Data operations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📥 Data Import")
        
        if st.button("🔄 Generate Sample Data", width="stretch"):
            with st.spinner("Generating sample data..."):
                try:
                    st.session_state.db_manager.generate_sample_data()
                    st.session_state.dashboard_data = None  # Force refresh
                    st.success("✅ Sample data generated successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error generating data: {str(e)}")
        
        # File upload
        uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.write("Preview of uploaded data:")
                st.dataframe(df.head())
                
                if st.button("Import Data"):
                    st.success("Data import functionality coming soon!")
                    
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
    
    with col2:
        st.subheader("📤 Data Export")
        
        if st.session_state.dashboard_data:
            analysis_df = st.session_state.dashboard_data['analysis_df']
            
            if not analysis_df.empty:
                csv = analysis_df.to_csv(index=False)
                
                st.download_button(
                    label="📄 Download Analysis Data",
                    data=csv,
                    file_name="roadmap_analysis.csv",
                    mime="text/csv",
                    width=200
                )
        
        if st.button("🗑️ Clear All Data", width="stretch"):
            if st.checkbox("I confirm I want to delete all data"):
                try:
                    # Clear database
                    conn = sqlite3.connect(st.session_state.db_manager.db_path)
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM customer_feedback")
                    cursor.execute("DELETE FROM usage_metrics")
                    conn.commit()
                    conn.close()
                    
                    st.session_state.dashboard_data = None
                    st.success("✅ All data cleared successfully!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error clearing data: {str(e)}")
    
    # System status
    st.subheader("🔍 System Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Database status
        try:
            feedback_summary = st.session_state.db_manager.get_feedback_summary()
            db_status = "🟢 Connected" if not feedback_summary.empty else "🟡 Empty"
            st.write(f"**Database:** {db_status}")
        except:
            st.write("**Database:** 🔴 Error")
    
    with col2:
        # ML Model status
        try:
            model_stats = st.session_state.dashboard_data.get('model_stats', {})
            model_status = "🟢 Trained" if model_stats.get('train_score', 0) > 0 else "🟡 Not Trained"
            st.write(f"**ML Model:** {model_status}")
        except:
            st.write("**ML Model:** 🔴 Error")
    
    with col3:
        # Data freshness
        if st.session_state.dashboard_data:
            last_updated = st.session_state.dashboard_data['last_updated']
            time_diff = datetime.now() - last_updated
            if time_diff.seconds < 300:
                freshness = "🟢 Fresh"
            elif time_diff.seconds < 1800:
                freshness = "🟡 Moderate"
            else:
                freshness = "🔴 Stale"
            st.write(f"**Data:** {freshness}")

def show_footer():
    """Show application footer"""
    st.markdown("""
    <div class="footer">
        <h3>🚀 Product Roadmap Platform</h3>
        <p>AI-Driven Feature Prioritization & Strategic Planning</p>
        <p>Built with ❤️ using Streamlit • Machine Learning • Advanced Analytics</p>
        <p><small>© 2025 Product Roadmap Platform. All rights reserved.</small></p>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main application function"""
    # Initialize session state
    if not initialize_session_state():
        st.stop()
    
    # Load dashboard data
    if st.session_state.dashboard_data is None:
        with st.spinner("Loading dashboard data..."):
            st.session_state.dashboard_data = load_dashboard_data()
    
    # Show header
    show_header()
    
    # Get selected page from sidebar
    selected_page = show_sidebar()
    
    # Route to appropriate page
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
    
    # Show footer
    show_footer()

if __name__ == "__main__":
    main()

