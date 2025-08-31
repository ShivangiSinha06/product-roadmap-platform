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

# Enhanced CSS Styling with Better Color Schemes
st.markdown("""
<style>
    /* Modern Color Palette */
    :root {
        --primary-blue: #3b82f6;
        --primary-blue-dark: #1d4ed8;
        --secondary-purple: #8b5cf6;
        --success-green: #10b981;
        --warning-orange: #f59e0b;
        --danger-red: #ef4444;
        --neutral-gray: #6b7280;
        --light-gray: #f8fafc;
        --dark-gray: #374151;
    }
    
    /* Main Header Styling */
    .main-header {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-purple) 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header h3 {
        font-size: 1.3rem;
        margin-bottom: 0.5rem;
        font-weight: 400;
        opacity: 0.95;
    }
    
    .main-header p {
        font-size: 1rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Enhanced Metric Cards */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-left: 5px solid var(--primary-blue);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 1rem;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .priority-high { 
        border-left-color: var(--danger-red) !important;
        background: linear-gradient(135deg, #fef2f2 0%, #ffffff 100%);
    }
    .priority-medium { 
        border-left-color: var(--warning-orange) !important;
        background: linear-gradient(135deg, #fffbeb 0%, #ffffff 100%);
    }
    .priority-low { 
        border-left-color: var(--success-green) !important;
        background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 100%);
    }
    
    /* Enhanced Footer */
    .footer {
        background: linear-gradient(135deg, var(--dark-gray) 0%, var(--neutral-gray) 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 15px;
        text-align: center;
        margin-top: 3rem;
        box-shadow: 0 -5px 20px rgba(0,0,0,0.1);
    }
    
    .footer h3 {
        color: white;
        margin-bottom: 1rem;
        font-size: 1.5rem;
    }
    
    .footer p {
        margin: 0.5rem 0;
        opacity: 0.9;
    }
    
    .footer small {
        opacity: 0.7;
        font-size: 0.85rem;
    }
    
    /* Enhanced Sidebar */
    .sidebar-content {
        background: linear-gradient(135deg, var(--light-gray) 0%, #ffffff 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    /* Status Indicators */
    .status-green { color: var(--success-green); font-weight: 600; }
    .status-yellow { color: var(--warning-orange); font-weight: 600; }
    .status-red { color: var(--danger-red); font-weight: 600; }
    
    /* Enhanced Tables */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-blue-dark) 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    
    /* Enhanced Selectbox */
    .stSelectbox > div > div {
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        background: white;
    }
    
    /* Chart Container Enhancement */
    .plotly-graph-div {
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #e5e7eb;
        overflow: hidden;
    }
    
    /* Success/Warning/Error Messages */
    .stSuccess {
        border-radius: 8px;
        border-left: 4px solid var(--success-green);
    }
    
    .stWarning {
        border-radius: 8px;
        border-left: 4px solid var(--warning-orange);
    }
    
    .stError {
        border-radius: 8px;
        border-left: 4px solid var(--danger-red);
    }
    
    /* Chat Interface Enhancements */
    .stChatMessage {
        border-radius: 12px;
        margin-bottom: 1rem;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    /* Progress Bar Enhancement */
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--primary-blue) 0%, var(--secondary-purple) 100%);
        border-radius: 10px;
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
                "content": "Hello! 👋 I'm your AI Product Assistant. I can help you analyze feature priorities, roadmap planning, ROI calculations, and strategic decisions. What would you like to know?"
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
            with st.spinner("🔄 Generating sample data..."):
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
    """Show main header with enhanced styling"""
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Product Roadmap Platform</h1>
        <h3>AI-Driven Feature Prioritization & Strategic Planning</h3>
        <p>Make data-driven product decisions with advanced analytics and ML-powered insights</p>
    </div>
    """, unsafe_allow_html=True)

def create_enhanced_metric_card(title, value, delta=None, help_text="", priority_class=""):
    """Create enhanced metric cards with better styling"""
    delta_html = ""
    if delta:
        color = "green" if delta > 0 else "red" if delta < 0 else "gray"
        delta_html = f'<div style="color: {color}; font-size: 0.8rem; margin-top: 0.3rem;">△ {delta}</div>'
    
    card_class = f"metric-card {priority_class}"
    
    return f"""
    <div class="{card_class}" title="{help_text}">
        <div style="font-size: 0.9rem; color: #6b7280; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">{title}</div>
        <div style="font-size: 2rem; font-weight: 700; color: #374151; margin: 0.5rem 0;">{value}</div>
        {delta_html}
    </div>
    """

def show_sidebar():
    """Enhanced sidebar with improved navigation and styling"""
    with st.sidebar:
        # Navigation Section
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.markdown("## 🧭 **Navigation**")
        
        # Enhanced page selector with emojis
        pages = [
            "📊 Dashboard Overview",
            "🎯 Priority Matrix", 
            "📅 Roadmap Timeline",
            "💰 ROI Analysis",
            "🤖 AI Assistant",
            "📈 Analytics Deep Dive",
            "👥 Customer Segments",
            "⚙️ Data Management"
        ]
        
        page = st.selectbox(
            "Choose a page:",
            pages,
            help="Navigate between different views of your product roadmap"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick Actions Section
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.markdown("## ⚡ **Quick Actions**")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh", help="Refresh dashboard data", use_container_width=True):
                st.session_state.dashboard_data = None
                st.rerun()
        
        with col2:
            if st.button("🤖 Train ML", help="Retrain ML model with latest data", use_container_width=True):
                with st.spinner("Training ML model..."):
                    try:
                        st.session_state.prioritization_engine.train_ml_prioritization_model()
                        st.success("✅ Model updated!")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Dashboard Stats Section
        if st.session_state.dashboard_data:
            st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
            summary = st.session_state.dashboard_data['executive_summary']
            
            st.markdown("## 📈 **Quick Stats**")
            
            # Enhanced metric display
            st.metric("📋 Total Features", summary['total_features'])
            st.metric("🔥 High Priority", summary['high_priority_features'])
            st.metric("⚡ Quick Wins", summary['quick_wins'])
            
            if summary['avg_roi'] > 0:
                st.metric("💰 Avg ROI", f"{summary['avg_roi']:.1f}%")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # System Status Section
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.markdown("## 🔍 **System Status**")
        
        # Database Status
        try:
            feedback_summary = st.session_state.db_manager.get_feedback_summary()
            if not feedback_summary.empty:
                st.markdown('**Database:** <span class="status-green">🟢 Connected</span>', unsafe_allow_html=True)
            else:
                st.markdown('**Database:** <span class="status-yellow">🟡 Empty</span>', unsafe_allow_html=True)
        except:
            st.markdown('**Database:** <span class="status-red">🔴 Error</span>', unsafe_allow_html=True)
        
        # ML Model Status
        try:
            model_stats = st.session_state.dashboard_data.get('model_stats', {}) if st.session_state.dashboard_data else {}
            if model_stats.get('train_score', 0) > 0:
                st.markdown('**ML Model:** <span class="status-green">🟢 Trained</span>', unsafe_allow_html=True)
            else:
                st.markdown('**ML Model:** <span class="status-yellow">🟡 Not Trained</span>', unsafe_allow_html=True)
        except:
            st.markdown('**ML Model:** <span class="status-red">🔴 Error</span>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Last updated info
        st.markdown("---")
        if st.session_state.dashboard_data:
            last_updated = st.session_state.dashboard_data['last_updated']
            st.caption(f"🕒 Last updated: {last_updated.strftime('%Y-%m-%d %H:%M')}")
    
    return page

def show_dashboard_overview():
    """Enhanced dashboard overview with better data presentation"""
    st.title("📊 Dashboard Overview")
    
    if not st.session_state.dashboard_data:
        st.warning("⚠️ Dashboard data not loaded. Please refresh the page.")
        return
    
    data = st.session_state.dashboard_data
    summary = data['executive_summary']
    analysis_df = data['analysis_df']
    
    # Enhanced Key Metrics with Custom Cards
    st.markdown("### 🎯 **Key Performance Indicators**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_enhanced_metric_card(
            "Total Features",
            summary['total_features'],
            help_text="Total number of features in the roadmap"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_enhanced_metric_card(
            "High Priority",
            summary['high_priority_features'],
            priority_class="priority-high",
            help_text="Features with high priority scores"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_enhanced_metric_card(
            "Quick Wins",
            summary['quick_wins'],
            priority_class="priority-medium",
            help_text="Low effort, high impact features"
        ), unsafe_allow_html=True)
    
    with col4:
        if summary['avg_roi'] > 0:
            st.markdown(create_enhanced_metric_card(
                "Average ROI",
                f"{summary['avg_roi']:.1f}%",
                priority_class="priority-low",
                help_text="Average return on investment"
            ), unsafe_allow_html=True)
        else:
            model_score = data['model_stats']['train_score']
            st.markdown(create_enhanced_metric_card(
                "ML Model Score",
                f"{model_score:.2f}",
                help_text="Machine learning model accuracy"
            ), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Enhanced Charts Section
    col1, col2 = st.columns(2)
    
    with col1:
        if not analysis_df.empty:
            st.markdown("### 🎯 **Priority Distribution**")
            
            # Create priority categories with better color scheme
            analysis_df['priority_category'] = pd.cut(
                analysis_df['composite_score'], 
                bins=[0, 33, 66, 100], 
                labels=['Low Priority', 'Medium Priority', 'High Priority']
            )
            
            priority_counts = analysis_df['priority_category'].value_counts()
            
            # Enhanced pie chart with modern colors
            fig = px.pie(
                values=priority_counts.values,
                names=priority_counts.index,
                color_discrete_map={
                    'High Priority': '#ef4444',
                    'Medium Priority': '#f59e0b', 
                    'Low Priority': '#10b981'
                },
                hole=0.4  # Donut chart for modern look
            )
            
            fig.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                textfont_size=12,
                marker=dict(line=dict(color='#ffffff', width=2))
            )
            
            fig.update_layout(
                height=350,
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2),
                font=dict(size=12),
                margin=dict(t=20, b=20, l=20, r=20)
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if not analysis_df.empty:
            st.markdown("### 🏆 **Top Priority Features**")
            
            top_features = analysis_df.head(8)
            
            # Enhanced horizontal bar chart
            fig = go.Figure(go.Bar(
                x=top_features['composite_score'],
                y=top_features['feature_name'],
                orientation='h',
                marker=dict(
                    color=top_features['composite_score'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Priority Score")
                ),
                text=top_features['composite_score'].round(1),
                textposition='outside'
            ))
            
            fig.update_layout(
                height=350,
                xaxis_title="Priority Score",
                yaxis_title="",
                margin=dict(t=20, b=20, l=20, r=20),
                font=dict(size=11),
                showlegend=False
            )
            
            fig.update_traces(textfont_size=10)
            st.plotly_chart(fig, use_container_width=True)
    
    # Enhanced Feature Details Table
    st.markdown("### 📋 **Feature Details**")
    
    if not analysis_df.empty:
        # Enhanced table presentation
        display_df = analysis_df.head(10)[
            ['feature_name', 'composite_score', 'effort_estimate', 'recommended_quarter']
        ].copy()
        
        display_df.columns = ['🎯 Feature Name', '📊 Priority Score', '⚙️ Effort (SP)', '📅 Quarter']
        display_df['📊 Priority Score'] = display_df['📊 Priority Score'].round(2)
        
        # Add priority badges
        def add_priority_badge(score):
            if score >= 66:
                return f"🔴 {score}"
            elif score >= 33:
                return f"🟡 {score}"
            else:
                return f"🟢 {score}"
        
        display_df['📊 Priority Score'] = display_df['📊 Priority Score'].apply(add_priority_badge)
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "🎯 Feature Name": st.column_config.TextColumn(width="large"),
                "📊 Priority Score": st.column_config.TextColumn(width="small"),
                "⚙️ Effort (SP)": st.column_config.NumberColumn(format="%.0f"),
                "📅 Quarter": st.column_config.TextColumn(width="small")
            }
        )
        
        # Summary insights
        st.markdown("### 💡 **Key Insights**")
        
        insight_col1, insight_col2, insight_col3 = st.columns(3)
        
        with insight_col1:
            st.info(f"**📈 Average Priority Score:** {analysis_df['composite_score'].mean():.1f}")
        
        with insight_col2:
            total_effort = analysis_df.head(10)['effort_estimate'].sum()
            st.info(f"**⚙️ Total Effort (Top 10):** {total_effort:.0f} SP")
        
        with insight_col3:
            popular_quarter = analysis_df['recommended_quarter'].mode().iloc[0]
            st.info(f"**📅 Most Popular Quarter:** {popular_quarter}")
    
    else:
        st.info("📝 No feature data available. Please check your data sources or generate sample data.")

def show_priority_matrix():
    """Enhanced priority matrix with better visualizations"""
    st.title("🎯 Priority Matrix")
    
    if not st.session_state.dashboard_data:
        st.warning("⚠️ Dashboard data not loaded.")
        return
    
    analysis_df = st.session_state.dashboard_data['analysis_df']
    
    if analysis_df.empty:
        st.info("📊 No data available for priority matrix.")
        return
    
    # Enhanced Priority Matrix Scatter Plot
    st.markdown("### 📊 **Effort vs Impact Analysis**")
    
    fig = px.scatter(
        analysis_df,
        x='effort_estimate',
        y='impact_score',
        size='composite_score',
        color='recommended_quarter',
        hover_name='feature_name',
        hover_data={
            'composite_score': ':.2f',
            'effort_estimate': ':.0f',
            'impact_score': ':.1f'
        },
        title="Feature Priority Matrix: Effort vs Impact",
        labels={
            'effort_estimate': 'Effort (Story Points)',
            'impact_score': 'Impact Score',
            'recommended_quarter': 'Recommended Quarter'
        },
        color_discrete_map={
            'Q1 2026': '#ef4444',
            'Q2 2026': '#f59e0b',
            'Q3 2026': '#10b981',
            'Q4 2026': '#6366f1'
        }
    )
    
    # Add quadrant lines
    effort_median = analysis_df['effort_estimate'].median()
    impact_median = analysis_df['impact_score'].median()
    
    fig.add_hline(y=impact_median, line_dash="dash", line_color="rgba(107, 114, 128, 0.5)", line_width=2)
    fig.add_vline(x=effort_median, line_dash="dash", line_color="rgba(107, 114, 128, 0.5)", line_width=2)
    
    # Enhanced quadrant labels with better positioning
    fig.add_annotation(
        x=effort_median*0.5, y=impact_median*1.4, 
        text="🚀 Quick Wins", 
        showarrow=False, 
        font=dict(size=16, color="#10b981", weight="bold"),
        bgcolor="rgba(16, 185, 129, 0.1)",
        bordercolor="#10b981",
        borderwidth=1,
        borderpad=4
    )
    
    fig.add_annotation(
        x=effort_median*1.4, y=impact_median*1.4, 
        text="🎯 Major Projects", 
        showarrow=False, 
        font=dict(size=16, color="#ef4444", weight="bold"),
        bgcolor="rgba(239, 68, 68, 0.1)",
        bordercolor="#ef4444",
        borderwidth=1,
        borderpad=4
    )
    
    fig.add_annotation(
        x=effort_median*0.5, y=impact_median*0.6, 
        text="📝 Fill-ins", 
        showarrow=False, 
        font=dict(size=16, color="#6366f1", weight="bold"),
        bgcolor="rgba(99, 102, 241, 0.1)",
        bordercolor="#6366f1",
        borderwidth=1,
        borderpad=4
    )
    
    fig.add_annotation(
        x=effort_median*1.4, y=impact_median*0.6, 
        text="❓ Questionable", 
        showarrow=False, 
        font=dict(size=16, color="#f59e0b", weight="bold"),
        bgcolor="rgba(245, 158, 11, 0.1)",
        bordercolor="#f59e0b",
        borderwidth=1,
        borderpad=4
    )
    
    fig.update_layout(
        height=600,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2),
        margin=dict(t=50, b=80, l=50, r=50)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Enhanced Quadrant Analysis
    st.markdown("### 📈 **Quadrant Analysis**")
    
    # Calculate quadrant data
    quick_wins = analysis_df[
        (analysis_df['effort_estimate'] <= effort_median) & 
        (analysis_df['impact_score'] > impact_median)
    ]
    
    major_projects = analysis_df[
        (analysis_df['effort_estimate'] > effort_median) & 
        (analysis_df['impact_score'] > impact_median)
    ]
    
    fill_ins = analysis_df[
        (analysis_df['effort_estimate'] <= effort_median) & 
        (analysis_df['impact_score'] <= impact_median)
    ]
    
    questionable = analysis_df[
        (analysis_df['effort_estimate'] > effort_median) & 
        (analysis_df['impact_score'] <= impact_median)
    ]
    
    # Display in enhanced cards
    quad_col1, quad_col2 = st.columns(2)
    
    with quad_col1:
        st.markdown("#### 🚀 **Quick Wins** (Low Effort, High Impact)")
        st.success(f"**{len(quick_wins)} features** - Prioritize these for immediate wins!")
        
        if not quick_wins.empty:
            for _, feature in quick_wins.head(5).iterrows():
                st.markdown(f"• **{feature['feature_name']}** (Score: {feature['composite_score']:.1f})")
        
        st.markdown("#### 📝 **Fill-ins** (Low Effort, Low Impact)")
        st.info(f"**{len(fill_ins)} features** - Consider for capacity utilization")
        
        if not fill_ins.empty:
            for _, feature in fill_ins.head(3).iterrows():
                st.markdown(f"• **{feature['feature_name']}** (Score: {feature['composite_score']:.1f})")
    
    with quad_col2:
        st.markdown("#### 🎯 **Major Projects** (High Effort, High Impact)")
        st.warning(f"**{len(major_projects)} features** - Plan carefully with adequate resources")
        
        if not major_projects.empty:
            for _, feature in major_projects.head(5).iterrows():
                st.markdown(f"• **{feature['feature_name']}** (Score: {feature['composite_score']:.1f})")
        
        st.markdown("#### ❓ **Questionable** (High Effort, Low Impact)")
        st.error(f"**{len(questionable)} features** - Reconsider or redesign approach")
        
        if not questionable.empty:
            for _, feature in questionable.head(3).iterrows():
                st.markdown(f"• **{feature['feature_name']}** (Score: {feature['composite_score']:.1f})")

def show_roadmap_timeline():
    """Enhanced roadmap timeline with better visualizations"""
    st.title("📅 Roadmap Timeline")
    
    if not st.session_state.dashboard_data:
        st.warning("⚠️ Dashboard data not loaded.")
        return
    
    analysis_df = st.session_state.dashboard_data['analysis_df']
    
    if analysis_df.empty:
        st.info("📊 No data available for timeline.")
        return
    
    # Enhanced Timeline Overview
    st.markdown("### 🗓️ **Quarterly Roadmap Overview**")
    
    # Calculate quarterly metrics
    quarterly_data = analysis_df.groupby('recommended_quarter').agg({
        'feature_name': 'count',
        'effort_estimate': 'sum',
        'composite_score': 'mean'
    }).round(2)
    
    quarterly_data.columns = ['Features', 'Total Effort', 'Avg Priority']
    
    # Enhanced quarterly cards
    quarters = ['Q1 2026', 'Q2 2026', 'Q3 2026', 'Q4 2026']
    quarter_cols = st.columns(4)
    
    colors = ['#ef4444', '#f59e0b', '#10b981', '#6366f1']
    
    for i, (quarter, color) in enumerate(zip(quarters, colors)):
        with quarter_cols[i]:
            if quarter in quarterly_data.index:
                data = quarterly_data.loc[quarter]
                
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, {color}15 0%, {color}05 100%);
                    border-left: 4px solid {color};
                    border-radius: 8px;
                    padding: 1rem;
                    text-align: center;
                    margin-bottom: 1rem;
                ">
                    <h4 style="color: {color}; margin: 0;">{quarter}</h4>
                    <p style="margin: 0.5rem 0; font-size: 1.2rem; font-weight: bold;">{data['Features']} Features</p>
                    <p style="margin: 0; font-size: 0.9rem; color: #6b7280;">{data['Total Effort']:.0f} Story Points</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="
                    background: #f8fafc;
                    border-left: 4px solid #e5e7eb;
                    border-radius: 8px;
                    padding: 1rem;
                    text-align: center;
                    margin-bottom: 1rem;
                ">
                    <h4 style="color: #6b7280; margin: 0;">{quarter}</h4>
                    <p style="margin: 0.5rem 0; font-size: 1.2rem; font-weight: bold;">0 Features</p>
                    <p style="margin: 0; font-size: 0.9rem; color: #6b7280;">0 Story Points</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Enhanced Feature Timeline Chart
    st.markdown("### 📊 **Features Distribution by Quarter**")
    
    if not quarterly_data.empty:
        # Create enhanced bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Number of Features',
            x=quarterly_data.index,
            y=quarterly_data['Features'],
            marker_color=colors[:len(quarterly_data)],
            text=quarterly_data['Features'],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Features: %{y}<br>Total Effort: %{customdata:.0f} SP<extra></extra>',
            customdata=quarterly_data['Total Effort']
        ))
        
        fig.update_layout(
            title="Quarterly Feature Distribution",
            xaxis_title="Quarter",
            yaxis_title="Number of Features",
            height=400,
            showlegend=False,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Capacity Analysis
        st.markdown("### ⚖️ **Capacity Analysis**")
        
        capacity_col1, capacity_col2, capacity_col3 = st.columns(3)
        
        with capacity_col1:
            total_effort = quarterly_data['Total Effort'].sum()
            st.metric("🏋️ Total Roadmap Effort", f"{total_effort:.0f} SP")
        
        with capacity_col2:
            avg_quarterly = total_effort / 4
            st.metric("📊 Quarterly Average", f"{avg_quarterly:.0f} SP")
        
        with capacity_col3:
            max_quarter = quarterly_data['Total Effort'].max()
            heaviest_quarter = quarterly_data['Total Effort'].idxmax()
            st.metric(f"⚡ Heaviest Quarter", f"{heaviest_quarter}")
        
        # Capacity warnings
        if max_quarter > 120:
            st.error(f"⚠️ **Capacity Alert:** {heaviest_quarter} appears overloaded ({max_quarter:.0f} SP). Consider redistributing features.")
        elif max_quarter > 100:
            st.warning(f"🔔 **Capacity Warning:** {heaviest_quarter} is near capacity ({max_quarter:.0f} SP). Monitor progress closely.")
        else:
            st.success("✅ **Capacity Status:** Good workload distribution across quarters.")
    
    # Detailed Quarter View
    st.markdown("### 🔍 **Detailed Quarter Analysis**")
    
    selected_quarter = st.selectbox("Select Quarter for Detailed View:", analysis_df['recommended_quarter'].unique())
    
    quarter_features = analysis_df[analysis_df['recommended_quarter'] == selected_quarter].sort_values('composite_score', ascending=False)
    
    if not quarter_features.empty:
        st.markdown(f"#### 📋 **{selected_quarter} Feature Details**")
        
        # Enhanced feature table
        display_df = quarter_features[
            ['feature_name', 'composite_score', 'effort_estimate', 'impact_score']
        ].copy()
        
        display_df.columns = ['🎯 Feature Name', '📊 Priority Score', '⚙️ Effort (SP)', '💫 Impact Score']
        display_df = display_df.round(2)
        
        st.dataframe(
            display_df, 
            use_container_width=True,
            hide_index=True,
            column_config={
                "🎯 Feature Name": st.column_config.TextColumn(width="large"),
                "📊 Priority Score": st.column_config.NumberColumn(format="%.2f"),
                "⚙️ Effort (SP)": st.column_config.NumberColumn(format="%.0f"),
                "💫 Impact Score": st.column_config.NumberColumn(format="%.1f")
            }
        )
        
        # Quarter Summary
        summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
        
        with summary_col1:
            st.metric("🎯 Features Count", len(quarter_features))
        
        with summary_col2:
            st.metric("⚙️ Total Effort", f"{quarter_features['effort_estimate'].sum():.0f} SP")
        
        with summary_col3:
            st.metric("📊 Avg Priority", f"{quarter_features['composite_score'].mean():.1f}")
        
        with summary_col4:
            st.metric("💫 Avg Impact", f"{quarter_features['impact_score'].mean():.1f}")

# Continue with remaining functions in next part due to length...

def show_roi_analysis():
    """Enhanced ROI analysis with better financial visualizations"""
    st.title("💰 ROI Analysis")
    
    if not st.session_state.dashboard_data:
        st.warning("⚠️ Dashboard data not loaded.")
        return
    
    roi_df = st.session_state.dashboard_data['roi_df']
    
    if roi_df.empty:
        st.info("📊 No ROI data available. This requires revenue impact data in customer feedback.")
        
        # Show how to enable ROI analysis
        st.markdown("""
        ### 💡 **How to Enable ROI Analysis**
        
        ROI analysis requires revenue impact data in customer feedback. To see ROI projections:
        
        1. 📝 **Add Revenue Impact** - Include revenue estimates in customer feedback
        2. 🔄 **Refresh Data** - Use the refresh button in the sidebar
        3. 📊 **View Results** - ROI calculations will appear automatically
        """)
        return
    
    # Enhanced ROI Overview
    st.markdown("### 💼 **Investment Portfolio Overview**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_investment = roi_df['development_cost'].sum()
    total_revenue = roi_df['projected_annual_revenue'].sum()
    avg_roi = roi_df['roi_percentage'].mean()
    avg_payback = roi_df['payback_months'].mean()
    
    with col1:
        st.markdown(create_enhanced_metric_card(
            "Total Investment",
            f"${total_investment:,.0f}",
            help_text="Total development investment required"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_enhanced_metric_card(
            "Projected Revenue",
            f"${total_revenue:,.0f}",
            priority_class="priority-low",
            help_text="Expected annual revenue from all features"
        ), unsafe_allow_html=True)
    
    with col3:
        roi_class = "priority-low" if avg_roi > 100 else "priority-medium" if avg_roi > 50 else "priority-high"
        st.markdown(create_enhanced_metric_card(
            "Average ROI",
            f"{avg_roi:.1f}%",
            priority_class=roi_class,
            help_text="Average return on investment"
        ), unsafe_allow_html=True)
    
    with col4:
        payback_class = "priority-low" if avg_payback < 12 else "priority-medium" if avg_payback < 24 else "priority-high"
        st.markdown(create_enhanced_metric_card(
            "Avg Payback Period",
            f"{avg_payback:.1f} months",
            priority_class=payback_class,
            help_text="Average time to recover investment"
        ), unsafe_allow_html=True)
    
    # Enhanced ROI Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 **ROI by Feature**")
        
        top_roi = roi_df.nlargest(10, 'roi_percentage')
        
        # Create color scale based on ROI values
        colors = ['#ef4444' if x < 50 else '#f59e0b' if x < 100 else '#10b981' for x in top_roi['roi_percentage']]
        
        fig = go.Figure(go.Bar(
            x=top_roi['roi_percentage'],
            y=top_roi['feature_name'],
            orientation='h',
            marker_color=colors,
            text=[f"{x:.1f}%" for x in top_roi['roi_percentage']],
            textposition='outside'
        ))
        
        fig.update_layout(
            xaxis_title="ROI (%)",
            yaxis_title="",
            height=400,
            margin=dict(t=20, b=20, l=20, r=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 💰 **Investment vs Revenue**")
        
        fig = px.scatter(
            roi_df,
            x='development_cost',
            y='projected_annual_revenue',
            size='roi_percentage',
            color='roi_percentage',
            hover_name='feature_name',
            hover_data={
                'development_cost': ':$,.0f',
                'projected_annual_revenue': ':$,.0f',
                'roi_percentage': ':.1f%',
                'payback_months': ':.1f'
            },
            color_continuous_scale='RdYlGn',
            title="Investment vs Expected Revenue"
        )
        
        # Add break-even line
        max_val = max(roi_df['development_cost'].max(), roi_df['projected_annual_revenue'].max())
        fig.add_shape(
            type="line",
            x0=0, y0=0, x1=max_val, y1=max_val,
            line=dict(color="red", width=2, dash="dash"),
            name="Break-even line"
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Enhanced ROI Table
    st.markdown("### 📋 **Detailed ROI Analysis**")
    
    display_roi = roi_df.copy().sort_values('roi_percentage', ascending=False)
    
    # Add ROI categories
    def get_roi_category(roi):
        if roi >= 200:
            return "🟢 Excellent"
        elif roi >= 100:
            return "🟡 Good"
        elif roi >= 50:
            return "🟠 Moderate"
        else:
            return "🔴 Poor"
    
    display_roi['ROI Category'] = display_roi['roi_percentage'].apply(get_roi_category)
    
    # Format monetary values
    display_roi['Investment'] = display_roi['development_cost'].apply(lambda x: f"${x:,.0f}")
    display_roi['Annual Revenue'] = display_roi['projected_annual_revenue'].apply(lambda x: f"${x:,.0f}")
    display_roi['ROI'] = display_roi['roi_percentage'].apply(lambda x: f"{x:.1f}%")
    display_roi['Payback'] = display_roi['payback_months'].apply(lambda x: f"{x:.1f} months")
    
    # Select columns for display
    table_df = display_roi[['feature_name', 'Investment', 'Annual Revenue', 'ROI', 'ROI Category', 'Payback']]
    table_df.columns = ['🎯 Feature', '💰 Investment', '📈 Annual Revenue', '📊 ROI', '⭐ Category', '⏱️ Payback']
    
    st.dataframe(
        table_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "🎯 Feature": st.column_config.TextColumn(width="large"),
            "💰 Investment": st.column_config.TextColumn(width="small"),
            "📈 Annual Revenue": st.column_config.TextColumn(width="medium"),
            "📊 ROI": st.column_config.TextColumn(width="small"),
            "⭐ Category": st.column_config.TextColumn(width="small"),
            "⏱️ Payback": st.column_config.TextColumn(width="small")
        }
    )
    
    # ROI Insights
    st.markdown("### 💡 **ROI Insights & Recommendations**")
    
    excellent_roi = len(roi_df[roi_df['roi_percentage'] >= 200])
    good_roi = len(roi_df[(roi_df['roi_percentage'] >= 100) & (roi_df['roi_percentage'] < 200)])
    poor_roi = len(roi_df[roi_df['roi_percentage'] < 50])
    
    insight_col1, insight_col2, insight_col3 = st.columns(3)
    
    with insight_col1:
        st.success(f"🟢 **{excellent_roi} Excellent ROI** features (>200%)")
        if excellent_roi > 0:
            st.write("✅ Prioritize these for maximum return")
    
    with insight_col2:
        st.info(f"🟡 **{good_roi} Good ROI** features (100-200%)")
        if good_roi > 0:
            st.write("📈 Strong candidates for development")
    
    with insight_col3:
        st.warning(f"🔴 **{poor_roi} Poor ROI** features (<50%)")
        if poor_roi > 0:
            st.write("⚠️ Consider redesign or deprioritization")

def show_ai_assistant():
    """Enhanced AI Assistant with better chat interface"""
    st.title("🤖 AI Product Assistant")
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border-left: 4px solid #0ea5e9;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 2rem;
    ">
        <h4 style="color: #0369a1; margin-bottom: 1rem;">💡 What I can help you with:</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
            <div>
                <p style="margin: 0.3rem 0;"><strong>🎯 Feature Analysis:</strong> Priority rankings, RICE scores</p>
                <p style="margin: 0.3rem 0;"><strong>💰 Financial Planning:</strong> ROI calculations, budget projections</p>
            </div>
            <div>
                <p style="margin: 0.3rem 0;"><strong>📅 Timeline Planning:</strong> Capacity analysis, quarter assignments</p>
                <p style="margin: 0.3rem 0;"><strong>👥 Strategic Insights:</strong> Customer segments, market analysis</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Chat Interface
    st.markdown("### 💬 **Chat with Your AI Assistant**")
    
    # Display chat messages with enhanced styling
    for i, message in enumerate(st.session_state.chat_messages):
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                st.markdown(f'<div style="background: #f8fafc; padding: 1rem; border-radius: 8px; border-left: 3px solid #3b82f6;">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="background: #eff6ff; padding: 1rem; border-radius: 8px; border-left: 3px solid #10b981;">{message["content"]}</div>', unsafe_allow_html=True)
    
    # Chat input with enhanced styling
    if prompt := st.chat_input("💭 Ask me anything about your product roadmap..."):
        # Add user message with enhanced styling
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(f'<div style="background: #eff6ff; padding: 1rem; border-radius: 8px; border-left: 3px solid #10b981;">{prompt}</div>', unsafe_allow_html=True)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Analyzing your request..."):
                try:
                    # Get AI response
                    response = st.session_state.ai_assistant.process_query(prompt)
                    st.markdown(f'<div style="background: #f8fafc; padding: 1rem; border-radius: 8px; border-left: 3px solid #3b82f6;">{response}</div>', unsafe_allow_html=True)
                    
                    # Add assistant response
                    st.session_state.chat_messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    error_msg = f"❌ Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_messages.append({"role": "assistant", "content": error_msg})
    
    # Enhanced Quick Action Buttons
    st.markdown("### 🎯 **Quick Questions**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏆 What are my top priorities?", use_container_width=True):
            st.session_state.chat_messages.append({
                "role": "user", 
                "content": "What are my top priority features and why?"
            })
            st.rerun()
        
        if st.button("⚡ Show me quick wins", use_container_width=True):
            st.session_state.chat_messages.append({
                "role": "user",
                "content": "What are the best quick win opportunities?"
            })
            st.rerun()
    
    with col2:
        if st.button("💰 Analyze ROI potential", use_container_width=True):
            st.session_state.chat_messages.append({
                "role": "user",
                "content": "Can you analyze the ROI for my top features?"
            })
            st.rerun()
        
        if st.button("📊 Compare features", use_container_width=True):
            st.session_state.chat_messages.append({
                "role": "user",
                "content": "Compare the top 3 features in my roadmap"
            })
            st.rerun()
    
    with col3:
        if st.button("📅 Plan my quarters", use_container_width=True):
            st.session_state.chat_messages.append({
                "role": "user",
                "content": "Help me with capacity and timeline planning for the next quarters"
            })
            st.rerun()
        
        if st.button("⚠️ Identify risks", use_container_width=True):
            st.session_state.chat_messages.append({
                "role": "user",
                "content": "What are the biggest risks in my current roadmap?"
            })
            st.rerun()
    
    # Clear Chat Button
    if st.button("🗑️ Clear Chat History", type="secondary"):
        st.session_state.chat_messages = [{
            "role": "assistant",
            "content": "Hello! 👋 I'm your AI Product Assistant. I can help you analyze feature priorities, roadmap planning, ROI calculations, and strategic decisions. What would you like to know?"
        }]
        st.rerun()

# Additional enhanced functions would continue here...
# For brevity, I'll provide the remaining key functions

def show_footer():
    """Enhanced footer with better styling and information"""
    st.markdown("""
    <div class="footer">
        <h3>🚀 Product Roadmap Platform</h3>
        <p><strong>AI-Driven Feature Prioritization & Strategic Planning</strong></p>
        <p>Built with ❤️ using Streamlit • Machine Learning • Advanced Analytics</p>
        <div style="margin: 2rem 0;">
            <span style="margin: 0 1rem;">📊 RICE Methodology</span>
            <span style="margin: 0 1rem;">🤖 ML-Powered Insights</span>
            <span style="margin: 0 1rem;">💰 ROI Analytics</span>
            <span style="margin: 0 1rem;">📈 Real-time Dashboards</span>
        </div>
        <p><small>© 2025 Product Roadmap Platform. All rights reserved.</small></p>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Enhanced main application function"""
    # Initialize session state
    if not initialize_session_state():
        st.stop()
    
    # Load dashboard data with progress indicator
    if st.session_state.dashboard_data is None:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("🔄 Loading dashboard data...")
        progress_bar.progress(25)
        
        st.session_state.dashboard_data = load_dashboard_data()
        
        progress_bar.progress(100)
        status_text.text("✅ Dashboard loaded successfully!")
        
        # Clear progress indicators
        import time
        time.sleep(0.5)
        progress_bar.empty()
        status_text.empty()
    
    # Show enhanced header
    show_header()
    
    # Get selected page from enhanced sidebar
    selected_page = show_sidebar()
    
    # Route to appropriate page with enhanced functions
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
    
    # Show enhanced footer
    show_footer()

if __name__ == "__main__":
    main()

