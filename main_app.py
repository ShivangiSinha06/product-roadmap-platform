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

def get_theme_css(is_dark_mode=False):
    """Return CSS based on selected theme"""
    if is_dark_mode:
        return """
<style>
    /* Dark Theme */
    :root {
        --primary-blue: #60a5fa;
        --primary-blue-dark: #3b82f6;
        --secondary-purple: #a78bfa;
        --success-green: #34d399;
        --warning-orange: #fbbf24;
        --danger-red: #f87171;
        --neutral-gray: #9ca3af;
        --light-gray: #1f2937;
        --dark-gray: #111827;
        --text-primary: #f9fafb;
        --text-secondary: #d1d5db;
        --bg-primary: #111827;
        --bg-secondary: #1f2937;
        --bg-card: #374151;
        --border-color: #4b5563;
    }
    
    .stApp {
        background-color: var(--bg-primary);
        color: var(--text-primary);
    }
    
    .main-header {
        background: linear-gradient(135deg, #1e40af 0%, #7c3aed 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(30, 64, 175, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        color: white !important;
    }
    
    .main-header h3 {
        font-size: 1.3rem;
        margin-bottom: 0.5rem;
        font-weight: 400;
        opacity: 0.95;
        color: white !important;
    }
    
    .main-header p {
        font-size: 1rem;
        opacity: 0.9;
        margin: 0;
        color: white !important;
    }
    
    .metric-card {
        background: var(--bg-card);
        color: var(--text-primary);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        border-left: 5px solid var(--primary-blue);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 1rem;
        border: 1px solid var(--border-color);
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.4);
    }
    
    .metric-card .metric-title {
        font-size: 0.9rem;
        color: var(--text-secondary) !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .metric-card .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--text-primary) !important;
        margin: 0.5rem 0;
        line-height: 1;
    }
    
    .priority-high { 
        border-left-color: var(--danger-red) !important;
        background: linear-gradient(135deg, #451a1a 0%, var(--bg-card) 100%);
    }
    .priority-medium { 
        border-left-color: var(--warning-orange) !important;
        background: linear-gradient(135deg, #451a03 0%, var(--bg-card) 100%);
    }
    .priority-low { 
        border-left-color: var(--success-green) !important;
        background: linear-gradient(135deg, #064e3b 0%, var(--bg-card) 100%);
    }
    
    .footer {
        background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--dark-gray) 100%);
        color: var(--text-primary);
        padding: 3rem 2rem;
        border-radius: 15px;
        text-align: center;
        margin-top: 3rem;
        box-shadow: 0 -5px 25px rgba(0,0,0,0.2);
        border: 1px solid var(--border-color);
    }
    
    .footer h3, .footer p, .footer small {
        color: var(--text-primary) !important;
    }
    
    .sidebar-content {
        background: var(--bg-card);
        color: var(--text-primary);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid var(--border-color);
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .insight-card {
        background: var(--bg-card);
        color: var(--text-primary) !important;
        border-radius: 10px;
        padding: 1.2rem;
        margin: 1rem 0;
        border-left: 4px solid var(--primary-blue);
        box-shadow: 0 3px 12px rgba(0,0,0,0.2);
        border: 1px solid var(--border-color);
    }
    
    .quadrant-analysis {
        background: var(--bg-card);
        color: var(--text-primary) !important;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        border: 1px solid var(--border-color);
    }
    
    .quarter-card {
        background: var(--bg-card);
        color: var(--text-primary) !important;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 3px 12px rgba(0,0,0,0.2);
        border: 1px solid var(--border-color);
    }
</style>
"""
    else:
        return """
<style>
    /* Light Theme */
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
        --text-primary: #111827;
        --text-secondary: #4b5563;
        --bg-primary: #ffffff;
        --bg-secondary: #f8fafc;
        --bg-card: #ffffff;
        --border-color: #e5e7eb;
    }
    
    .stApp {
        background-color: var(--bg-primary);
        color: var(--text-primary);
    }
    
    .main-header {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-purple) 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        color: white !important;
    }
    
    .main-header h3 {
        font-size: 1.3rem;
        margin-bottom: 0.5rem;
        font-weight: 400;
        opacity: 0.95;
        color: white !important;
    }
    
    .main-header p {
        font-size: 1rem;
        opacity: 0.9;
        margin: 0;
        color: white !important;
    }
    
    .metric-card {
        background: var(--bg-card);
        color: var(--text-primary);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 5px solid var(--primary-blue);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 1rem;
        border: 1px solid var(--border-color);
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .metric-card .metric-title {
        font-size: 0.9rem;
        color: var(--text-secondary) !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .metric-card .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--text-primary) !important;
        margin: 0.5rem 0;
        line-height: 1;
    }
    
    .priority-high { 
        border-left-color: var(--danger-red) !important;
        background: linear-gradient(135deg, #fef2f2 0%, var(--bg-card) 100%);
    }
    .priority-medium { 
        border-left-color: var(--warning-orange) !important;
        background: linear-gradient(135deg, #fffbeb 0%, var(--bg-card) 100%);
    }
    .priority-low { 
        border-left-color: var(--success-green) !important;
        background: linear-gradient(135deg, #f0fdf4 0%, var(--bg-card) 100%);
    }
    
    .footer {
        background: linear-gradient(135deg, var(--dark-gray) 0%, var(--neutral-gray) 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 15px;
        text-align: center;
        margin-top: 3rem;
        box-shadow: 0 -5px 25px rgba(0,0,0,0.1);
    }
    
    .footer h3, .footer p, .footer small {
        color: white !important;
    }
    
    .sidebar-content {
        background: var(--bg-card);
        color: var(--text-primary);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid var(--border-color);
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .status-green { color: var(--success-green); font-weight: 600; }
    .status-yellow { color: var(--warning-orange); font-weight: 600; }
    .status-red { color: var(--danger-red); font-weight: 600; }
    
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 1px solid var(--border-color);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-blue-dark) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 3px 10px rgba(59, 130, 246, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4) !important;
    }
    
    .plotly-graph-div {
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid var(--border-color);
        overflow: hidden;
        background: var(--bg-card);
    }
    
    .insight-card {
        background: var(--bg-card);
        color: var(--text-primary) !important;
        border-radius: 10px;
        padding: 1.2rem;
        margin: 1rem 0;
        border-left: 4px solid var(--primary-blue);
        box-shadow: 0 3px 12px rgba(0,0,0,0.08);
        border: 1px solid var(--border-color);
    }
    
    .quadrant-analysis {
        background: var(--bg-card);
        color: var(--text-primary) !important;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 1px solid var(--border-color);
    }
    
    .quarter-card {
        background: var(--bg-card);
        color: var(--text-primary) !important;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 3px 12px rgba(0,0,0,0.08);
        border: 1px solid var(--border-color);
    }
</style>
"""

def initialize_session_state():
    """Initialize session state with error handling"""
    try:
        if 'dark_mode' not in st.session_state:
            st.session_state.dark_mode = False
            
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
    """Create enhanced metric cards with better contrast and styling"""
    delta_html = ""
    if delta:
        color = "#10b981" if delta > 0 else "#ef4444" if delta < 0 else "#6b7280"
        delta_html = f'<div style="color: {color}; font-size: 0.9rem; margin-top: 0.5rem; font-weight: 600;">△ {delta}</div>'
    
    card_class = f"metric-card {priority_class}"
    
    return f"""
    <div class="{card_class}" title="{help_text}">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """

def show_sidebar():
    """Enhanced sidebar with improved styling and theme toggle"""
    with st.sidebar:
        # Theme Toggle
        st.markdown("### 🎨 **Theme**")
        
        # Create two columns for theme toggle
        theme_col1, theme_col2 = st.columns(2)
        
        with theme_col1:
            if st.button("☀️ Light", use_container_width=True, 
                        type="primary" if not st.session_state.dark_mode else "secondary"):
                st.session_state.dark_mode = False
                st.rerun()
        
        with theme_col2:
            if st.button("🌙 Dark", use_container_width=True,
                        type="primary" if st.session_state.dark_mode else "secondary"):
                st.session_state.dark_mode = True
                st.rerun()
        
        st.markdown("---")
        
        # Navigation Section
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.markdown("## 🧭 **Navigation**")
        
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
            
            # Enhanced metric display with better contrast
            st.metric("📋 Total Features", summary['total_features'])
            st.metric("🔥 High Priority", summary['high_priority_features'])
            st.metric("⚡ Quick Wins", summary['quick_wins'])
            
            if summary['avg_roi'] > 0:
                st.metric("💰 Avg ROI", f"{summary['avg_roi']:.1f}%")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Enhanced System Status Section
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
    """Enhanced dashboard overview with fixed contrast issues"""
    st.title("📊 Dashboard Overview")
    
    if not st.session_state.dashboard_data:
        st.warning("⚠️ Dashboard data not loaded. Please refresh the page.")
        return
    
    data = st.session_state.dashboard_data
    summary = data['executive_summary']
    analysis_df = data['analysis_df']
    
    # Enhanced Key Metrics with Fixed Contrast
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
    
    # Enhanced Charts Section with Theme Support
    col1, col2 = st.columns(2)
    
    with col1:
        if not analysis_df.empty:
            st.markdown("### 🎯 **Priority Distribution**")
            
            # Create priority categories
            analysis_df['priority_category'] = pd.cut(
                analysis_df['composite_score'], 
                bins=[0, 33, 66, 100], 
                labels=['Low Priority', 'Medium Priority', 'High Priority']
            )
            
            priority_counts = analysis_df['priority_category'].value_counts()
            
            # Theme-aware colors
            colors = {
                'High Priority': '#ef4444',
                'Medium Priority': '#f59e0b', 
                'Low Priority': '#10b981'
            }
            
            fig = px.pie(
                values=priority_counts.values,
                names=priority_counts.index,
                color_discrete_map=colors,
                hole=0.4
            )
            
            # Theme-aware styling
            text_color = '#f9fafb' if st.session_state.dark_mode else '#111827'
            bg_color = '#111827' if st.session_state.dark_mode else '#ffffff'
            
            fig.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                textfont=dict(size=12, color=text_color),
                marker=dict(line=dict(color=bg_color, width=2))
            )
            
            fig.update_layout(
                height=350,
                showlegend=True,
                legend=dict(
                    orientation="h", 
                    yanchor="bottom", 
                    y=-0.2,
                    font=dict(color=text_color)
                ),
                font=dict(size=12, color=text_color),
                margin=dict(t=20, b=60, l=20, r=20),
                paper_bgcolor=bg_color,
                plot_bgcolor=bg_color
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if not analysis_df.empty:
            st.markdown("### 🏆 **Top Priority Features**")
            
            top_features = analysis_df.head(8)
            
            # Theme-aware bar chart
            text_color = '#f9fafb' if st.session_state.dark_mode else '#111827'
            bg_color = '#111827' if st.session_state.dark_mode else '#ffffff'
            
            fig = go.Figure(go.Bar(
                x=top_features['composite_score'],
                y=top_features['feature_name'],
                orientation='h',
                marker=dict(
                    color=top_features['composite_score'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(
                        title=dict(text="Priority Score", font=dict(color=text_color)),
                        tickfont=dict(color=text_color)
                    )
                ),
                text=top_features['composite_score'].round(1),
                textposition='outside',
                textfont=dict(color=text_color)
            ))
            
            fig.update_layout(
                height=350,
                xaxis=dict(
                    title="Priority Score",
                    titlefont=dict(color=text_color),
                    tickfont=dict(color=text_color),
                    gridcolor='rgba(107, 114, 128, 0.3)'
                ),
                yaxis=dict(
                    title="",
                    titlefont=dict(color=text_color),
                    tickfont=dict(color=text_color),
                    gridcolor='rgba(107, 114, 128, 0.3)'
                ),
                margin=dict(t=20, b=20, l=20, r=20),
                font=dict(size=11, color=text_color),
                showlegend=False,
                paper_bgcolor=bg_color,
                plot_bgcolor=bg_color
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Enhanced Feature Details Table with Better Styling
    st.markdown("### 📋 **Feature Details**")
    
    if not analysis_df.empty:
        display_df = analysis_df.head(10)[
            ['feature_name', 'composite_score', 'effort_estimate', 'recommended_quarter']
        ].copy()
        
        display_df.columns = ['🎯 Feature Name', '📊 Priority Score', '⚙️ Effort (SP)', '📅 Quarter']
        display_df['📊 Priority Score'] = display_df['📊 Priority Score'].round(2)
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "🎯 Feature Name": st.column_config.TextColumn(width="large"),
                "📊 Priority Score": st.column_config.NumberColumn(format="%.2f"),
                "⚙️ Effort (SP)": st.column_config.NumberColumn(format="%.0f"),
                "📅 Quarter": st.column_config.TextColumn(width="small")
            }
        )
        
        # Enhanced Insights Cards with Fixed Contrast
        st.markdown("### 💡 **Key Insights**")
        
        insight_col1, insight_col2, insight_col3 = st.columns(3)
        
        with insight_col1:
            st.markdown(f"""
            <div class="insight-card">
                <strong>📈 Average Priority Score</strong><br>
                <span style="font-size: 1.5rem; font-weight: bold; color: var(--primary-blue);">{analysis_df['composite_score'].mean():.1f}</span>
            </div>
            """, unsafe_allow_html=True)
        
        with insight_col2:
            total_effort = analysis_df.head(10)['effort_estimate'].sum()
            st.markdown(f"""
            <div class="insight-card">
                <strong>⚙️ Total Effort (Top 10)</strong><br>
                <span style="font-size: 1.5rem; font-weight: bold; color: var(--warning-orange);">{total_effort:.0f} SP</span>
            </div>
            """, unsafe_allow_html=True)
        
        with insight_col3:
            popular_quarter = analysis_df['recommended_quarter'].mode().iloc[0]
            st.markdown(f"""
            <div class="insight-card">
                <strong>📅 Most Popular Quarter</strong><br>
                <span style="font-size: 1.5rem; font-weight: bold; color: var(--success-green);">{popular_quarter}</span>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        st.info("📝 No feature data available. Please check your data sources or generate sample data.")

def show_priority_matrix():
    """Enhanced priority matrix with theme support"""
    st.title("🎯 Priority Matrix")
    
    if not st.session_state.dashboard_data:
        st.warning("⚠️ Dashboard data not loaded.")
        return
    
    analysis_df = st.session_state.dashboard_data['analysis_df']
    
    if analysis_df.empty:
        st.info("📊 No data available for priority matrix.")
        return
    
    st.markdown("### 📊 **Effort vs Impact Analysis**")
    
    # Basic scatter plot for priority matrix
    fig = px.scatter(
        analysis_df,
        x='effort_estimate',
        y='impact_score',
        size='composite_score',
        color='recommended_quarter',
        hover_name='feature_name',
        title="Feature Priority Matrix"
    )
    
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

def show_roadmap_timeline():
    """Enhanced roadmap timeline"""
    st.title("📅 Roadmap Timeline")
    
    if not st.session_state.dashboard_data:
        st.warning("⚠️ Dashboard data not loaded.")
        return
    
    analysis_df = st.session_state.dashboard_data['analysis_df']
    
    if analysis_df.empty:
        st.info("📊 No data available for timeline.")
        return
    
    # Quarterly summary
    st.markdown("### 🗓️ **Quarterly Roadmap Overview**")
    
    quarterly_data = analysis_df.groupby('recommended_quarter').agg({
        'feature_name': 'count',
        'effort_estimate': 'sum',
        'composite_score': 'mean'
    }).round(2)
    
    st.dataframe(quarterly_data, use_container_width=True)

def show_roi_analysis():
    """Enhanced ROI analysis"""
    st.title("💰 ROI Analysis")
    
    if not st.session_state.dashboard_data:
        st.warning("⚠️ Dashboard data not loaded.")
        return
    
    roi_df = st.session_state.dashboard_data['roi_df']
    
    if roi_df.empty:
        st.info("📊 No ROI data available.")
        return
    
    st.markdown("### 💼 **ROI Overview**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_investment = roi_df['development_cost'].sum()
        st.metric("Total Investment", f"${total_investment:,.0f}")
    
    with col2:
        total_revenue = roi_df['projected_annual_revenue'].sum()
        st.metric("Projected Revenue", f"${total_revenue:,.0f}")
    
    with col3:
        avg_roi = roi_df['roi_percentage'].mean()
        st.metric("Average ROI", f"{avg_roi:.1f}%")

def show_ai_assistant():
    """Enhanced AI Assistant"""
    st.title("🤖 AI Product Assistant")
    
    st.info("💡 Ask me anything about your product roadmap!")
    
    # Display chat messages
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about your roadmap..."):
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            try:
                response = st.session_state.ai_assistant.process_query(prompt)
                st.write(response)
                st.session_state.chat_messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.chat_messages.append({"role": "assistant", "content": error_msg})

def show_analytics_deep_dive():
    """Analytics deep dive"""
    st.title("📈 Analytics Deep Dive")
    
    if not st.session_state.dashboard_data:
        st.warning("⚠️ Dashboard data not loaded.")
        return
    
    analysis_df = st.session_state.dashboard_data['analysis_df']
    model_stats = st.session_state.dashboard_data['model_stats']
    
    if analysis_df.empty:
        st.info("📊 No analytics data available.")
        return
    
    st.markdown("### 🤖 **ML Model Performance**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Training Score", f"{model_stats['train_score']:.3f}")
    
    with col2:
        st.metric("Test Score", f"{model_stats['test_score']:.3f}")

def show_customer_segments():
    """Customer segments analysis"""
    st.title("👥 Customer Segments")
    
    if not st.session_state.dashboard_data:
        st.warning("⚠️ Dashboard data not loaded.")
        return
    
    segment_priorities = st.session_state.dashboard_data['segment_priorities']
    
    if segment_priorities.empty:
        st.info("📊 No customer segment data available.")
        return
    
    st.markdown("### 🎯 **Customer Segment Priorities**")
    st.dataframe(segment_priorities, use_container_width=True)

def show_data_management():
    """Data management page"""
    st.title("⚙️ Data Management")
    
    st.markdown("### 📊 **Data Operations**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📥 **Data Import**")
        
        if st.button("🔄 Generate Sample Data", use_container_width=True):
            with st.spinner("Generating sample data..."):
                try:
                    st.session_state.db_manager.generate_sample_data()
                    st.session_state.dashboard_data = None
                    st.success("✅ Sample data generated!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    with col2:
        st.markdown("#### 📤 **Data Export**")
        
        if st.session_state.dashboard_data:
            analysis_df = st.session_state.dashboard_data['analysis_df']
            
            if not analysis_df.empty:
                csv = analysis_df.to_csv(index=False)
                
                st.download_button(
                    label="📄 Download Analysis Data",
                    data=csv,
                    file_name=f"roadmap_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

def show_footer():
    """Enhanced footer"""
    st.markdown("""
    <div class="footer">
        <h3>🚀 Product Roadmap Platform</h3>
        <p><strong>AI-Driven Feature Prioritization & Strategic Planning</strong></p>
        <p>Built with ❤️ using Streamlit • Machine Learning • Advanced Analytics</p>
        <p><small>© 2025 Product Roadmap Platform. All rights reserved.</small></p>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Enhanced main application function with theme support"""
    # Initialize session state
    if not initialize_session_state():
        st.stop()
    
    # Apply theme-aware CSS
    st.markdown(get_theme_css(st.session_state.dark_mode), unsafe_allow_html=True)
    
    # Load dashboard data
    if st.session_state.dashboard_data is None:
        with st.spinner("🔄 Loading dashboard data..."):
            st.session_state.dashboard_data = load_dashboard_data()
    
    # Show enhanced header
    show_header()
    
    # Get selected page from enhanced sidebar
    selected_page = show_sidebar()
    
    # Enhanced page routing with error handling
    try:
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
        else:
            st.error(f"❌ Unknown page: {selected_page}")
            
    except Exception as e:
        st.error(f"❌ Error loading page '{selected_page}': {str(e)}")
        st.info("🔄 Please try refreshing the page.")
        
        # Show error details
        if st.checkbox("🔍 Show error details"):
            st.exception(e)
    
    # Show enhanced footer
    show_footer()

# Main execution with error handling
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"🚨 Critical error: {str(e)}")
        st.info("🔄 Please refresh the page.")
        
        if st.button("🆘 Reset Session"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.success("✅ Session reset. Please refresh.")

