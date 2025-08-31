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

# Fixed Dark Mode CSS - Only Dark Theme
def get_dark_theme_css():
    """Return consistent dark theme CSS"""
    return """
<style>
    /* Dark Theme Variables */
    :root {
        --primary-blue: #60a5fa;
        --secondary-purple: #a78bfa;
        --success-green: #34d399;
        --warning-orange: #fbbf24;
        --danger-red: #f87171;
        --bg-primary: #0f172a;
        --bg-secondary: #1e293b;
        --bg-card: #334155;
        --text-primary: #f8fafc;
        --text-secondary: #cbd5e1;
        --border-color: #475569;
    }
    
    /* Main App Background */
    .stApp {
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }
    
    .main .block-container {
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #1e40af 0%, #7c3aed 100%);
        color: white !important;
        padding: 2.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(30, 64, 175, 0.4);
    }
    
    .main-header h1, .main-header h3, .main-header p {
        color: white !important;
    }
    
    /* Metric Cards */
    .metric-card {
        background: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        border-left: 5px solid var(--primary-blue);
        margin-bottom: 1rem;
        border: 1px solid var(--border-color);
    }
    
    .metric-card .metric-title {
        color: var(--text-secondary) !important;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    
    .metric-card .metric-value {
        color: var(--text-primary) !important;
        font-size: 2rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    /* Sidebar Styling */
    .stSidebar {
        background-color: var(--bg-secondary) !important;
    }
    
    .stSidebar > div {
        background-color: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
    }
    
    .sidebar-content {
        background: var(--bg-card) !important;
        color: var(--text-primary) !important;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid var(--border-color);
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-blue) 0%, #1d4ed8 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(96, 165, 250, 0.4) !important;
    }
    
    /* Text Elements */
    .stMarkdown, .stText, h1, h2, h3, h4, h5, h6, p, span, div {
        color: var(--text-primary) !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border: 2px solid var(--border-color) !important;
    }
    
    /* Dataframe */
    .dataframe {
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border-radius: 8px;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border: 2px solid var(--border-color) !important;
    }
    
    /* Chat Messages */
    .stChatMessage {
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border-radius: 12px !important;
        border: 1px solid var(--border-color) !important;
    }
    
    /* Status Colors */
    .status-green { color: var(--success-green) !important; font-weight: 600; }
    .status-yellow { color: var(--warning-orange) !important; font-weight: 600; }
    .status-red { color: var(--danger-red) !important; font-weight: 600; }
    
    /* Insight Cards */
    .insight-card {
        background: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border-radius: 10px;
        padding: 1.2rem;
        margin: 1rem 0;
        border-left: 4px solid var(--primary-blue);
        box-shadow: 0 3px 12px rgba(0,0,0,0.2);
        border: 1px solid var(--border-color);
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
        color: var(--text-primary) !important;
        padding: 3rem 2rem;
        border-radius: 15px;
        text-align: center;
        margin-top: 3rem;
        box-shadow: 0 -5px 25px rgba(0,0,0,0.2);
    }
    
    .footer h3, .footer p, .footer small {
        color: var(--text-primary) !important;
    }
    
    /* Fix any remaining light backgrounds */
    div[data-testid="stSidebar"] {
        background-color: var(--bg-secondary) !important;
    }
    
    div[data-testid="stSidebar"] > div {
        background-color: var(--bg-secondary) !important;
    }
</style>
"""

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
        return False
    
    return True

@st.cache_data(ttl=300, show_spinner=True)
def load_dashboard_data():
    """Load dashboard data with comprehensive error handling"""
    try:
        if 'db_manager' not in st.session_state:
            raise Exception("Database manager not initialized")
        
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

def create_metric_card(title, value, help_text=""):
    """Create metric cards with proper dark theme styling"""
    return f"""
    <div class="metric-card" title="{help_text}">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
    </div>
    """

def show_sidebar():
    """Enhanced sidebar"""
    with st.sidebar:
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
        
        page = st.selectbox("Choose a page:", pages)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick Actions
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.markdown("## ⚡ **Quick Actions**")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh", use_container_width=True):
                st.session_state.dashboard_data = None
                st.rerun()
        
        with col2:
            if st.button("🤖 Train ML", use_container_width=True):
                with st.spinner("Training..."):
                    try:
                        st.session_state.prioritization_engine.train_ml_prioritization_model()
                        st.success("✅ Updated!")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # System Status
        if st.session_state.dashboard_data:
            st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
            summary = st.session_state.dashboard_data['executive_summary']
            
            st.markdown("## 📈 **Quick Stats**")
            st.metric("📋 Total Features", summary['total_features'])
            st.metric("🔥 High Priority", summary['high_priority_features'])
            st.metric("⚡ Quick Wins", summary['quick_wins'])
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Status indicators
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.markdown("## 🔍 **System Status**")
        
        try:
            feedback_summary = st.session_state.db_manager.get_feedback_summary()
            if not feedback_summary.empty:
                st.markdown('**Database:** <span class="status-green">🟢 Connected</span>', unsafe_allow_html=True)
            else:
                st.markdown('**Database:** <span class="status-yellow">🟡 Empty</span>', unsafe_allow_html=True)
        except:
            st.markdown('**Database:** <span class="status-red">🔴 Error</span>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    return page

def show_dashboard_overview():
    """Dashboard overview with fixed styling"""
    st.title("📊 Dashboard Overview")
    
    if not st.session_state.dashboard_data:
        st.warning("⚠️ Dashboard data not loaded. Please refresh the page.")
        return
    
    data = st.session_state.dashboard_data
    summary = data['executive_summary']
    analysis_df = data['analysis_df']
    
    # Key Metrics
    st.markdown("### 🎯 **Key Performance Indicators**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_metric_card(
            "Total Features",
            summary['total_features'],
            "Total number of features in the roadmap"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_metric_card(
            "High Priority",
            summary['high_priority_features'],
            "Features with high priority scores"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_metric_card(
            "Quick Wins",
            summary['quick_wins'],
            "Low effort, high impact features"
        ), unsafe_allow_html=True)
    
    with col4:
        if summary['avg_roi'] > 0:
            st.markdown(create_metric_card(
                "Average ROI",
                f"{summary['avg_roi']:.1f}%",
                "Average return on investment"
            ), unsafe_allow_html=True)
        else:
            model_score = data['model_stats']['train_score']
            st.markdown(create_metric_card(
                "ML Model Score",
                f"{model_score:.2f}",
                "Machine learning model accuracy"
            ), unsafe_allow_html=True)
    
    # Charts
    if not analysis_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 **Priority Distribution**")
            
            analysis_df['priority_category'] = pd.cut(
                analysis_df['composite_score'], 
                bins=[0, 33, 66, 100], 
                labels=['Low Priority', 'Medium Priority', 'High Priority']
            )
            
            priority_counts = analysis_df['priority_category'].value_counts()
            
            fig = px.pie(
                values=priority_counts.values,
                names=priority_counts.index,
                color_discrete_map={
                    'High Priority': '#ef4444',
                    'Medium Priority': '#f59e0b', 
                    'Low Priority': '#10b981'
                },
                hole=0.4
            )
            
            # Apply dark theme to chart
            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='#0f172a',
                plot_bgcolor='#0f172a',
                font=dict(color='#f8fafc'),
                height=350
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🏆 **Top Priority Features**")
            
            top_features = analysis_df.head(8)
            
            fig = go.Figure(go.Bar(
                x=top_features['composite_score'],
                y=top_features['feature_name'],
                orientation='h',
                marker_color='#60a5fa'
            ))
            
            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='#0f172a',
                plot_bgcolor='#0f172a',
                font=dict(color='#f8fafc'),
                height=350,
                xaxis_title="Priority Score",
                yaxis_title=""
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Feature Details Table
        st.markdown("### 📋 **Feature Details**")
        
        display_df = analysis_df.head(10)[
            ['feature_name', 'composite_score', 'effort_estimate', 'recommended_quarter']
        ].copy()
        
        display_df.columns = ['🎯 Feature Name', '📊 Priority Score', '⚙️ Effort (SP)', '📅 Quarter']
        display_df['📊 Priority Score'] = display_df['📊 Priority Score'].round(2)
        
        st.dataframe(display_df, use_container_width=True)
        
        # Insights
        st.markdown("### 💡 **Key Insights**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_score = analysis_df['composite_score'].mean()
            st.markdown(f"""
            <div class="insight-card">
                <strong>📈 Average Priority Score</strong><br>
                <span style="font-size: 1.5rem; font-weight: bold; color: #60a5fa;">{avg_score:.1f}</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_effort = analysis_df.head(10)['effort_estimate'].sum()
            st.markdown(f"""
            <div class="insight-card">
                <strong>⚙️ Total Effort (Top 10)</strong><br>
                <span style="font-size: 1.5rem; font-weight: bold; color: #fbbf24;">{total_effort:.0f} SP</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            popular_quarter = analysis_df['recommended_quarter'].mode().iloc[0]
            st.markdown(f"""
            <div class="insight-card">
                <strong>📅 Most Popular Quarter</strong><br>
                <span style="font-size: 1.5rem; font-weight: bold; color: #34d399;">{popular_quarter}</span>
            </div>
            """, unsafe_allow_html=True)

def show_priority_matrix():
    """Priority matrix with dark theme"""
    st.title("🎯 Priority Matrix")
    
    if not st.session_state.dashboard_data:
        st.warning("⚠️ Dashboard data not loaded.")
        return
    
    analysis_df = st.session_state.dashboard_data['analysis_df']
    
    if analysis_df.empty:
        st.info("📊 No data available for priority matrix.")
        return
    
    st.markdown("### 📊 **Effort vs Impact Analysis**")
    
    fig = px.scatter(
        analysis_df,
        x='effort_estimate',
        y='impact_score',
        size='composite_score',
        color='recommended_quarter',
        hover_name='feature_name',
        title="Feature Priority Matrix",
        template='plotly_dark'
    )
    
    fig.update_layout(
        paper_bgcolor='#0f172a',
        plot_bgcolor='#0f172a',
        font=dict(color='#f8fafc'),
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_roadmap_timeline():
    """Roadmap timeline with dark theme"""
    st.title("📅 Roadmap Timeline")
    
    if not st.session_state.dashboard_data:
        st.warning("⚠️ Dashboard data not loaded.")
        return
    
    analysis_df = st.session_state.dashboard_data['analysis_df']
    
    if analysis_df.empty:
        st.info("📊 No data available for timeline.")
        return
    
    st.markdown("### 🗓️ **Quarterly Roadmap Overview**")
    
    quarterly_data = analysis_df.groupby('recommended_quarter').agg({
        'feature_name': 'count',
        'effort_estimate': 'sum',
        'composite_score': 'mean'
    }).round(2)
    
    quarterly_data.columns = ['Features', 'Total Effort', 'Avg Priority']
    st.dataframe(quarterly_data, use_container_width=True)

def show_roi_analysis():
    """ROI analysis with dark theme"""
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
    """AI Assistant with dark theme"""
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
    
    model_stats = st.session_state.dashboard_data['model_stats']
    
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
    """Main application function"""
    # Apply dark theme CSS
    st.markdown(get_dark_theme_css(), unsafe_allow_html=True)
    
    # Initialize session state
    if not initialize_session_state():
        st.stop()
    
    # Load dashboard data
    if st.session_state.dashboard_data is None:
        with st.spinner("🔄 Loading dashboard data..."):
            st.session_state.dashboard_data = load_dashboard_data()
    
    # Show header
    show_header()
    
    # Get selected page
    selected_page = show_sidebar()
    
    # Route to appropriate page
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
        
        if st.checkbox("🔍 Show error details"):
            st.exception(e)
    
    # Show footer
    show_footer()

# Main execution
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

