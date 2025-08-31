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

# Your existing CSS code here...
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
    
    .footer {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        padding: 30px 20px;
        margin-top: 50px;
        border-radius: 10px;
        box-shadow: 0 -4px 6px rgba(0, 0, 0, 0.1);
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
        <p>AI-Driven Feature Prioritization & Strategic Planning</p>
    </div>
    """, unsafe_allow_html=True)

def show_sidebar():
    """Show sidebar navigation"""
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
                try:
                    with st.spinner("Training ML model..."):
                        st.session_state.prioritization_engine.train_ml_prioritization_model()
                    st.success("Model updated!")
                except Exception as e:
                    st.error(f"Error training model: {str(e)}")
        
        return page

def show_error_page():
    """Show error page when app fails to initialize"""
    st.title("🚨 Application Error")
    st.error("The application failed to initialize properly.")
    
    st.subheader("Possible Solutions:")
    st.write("1. **Refresh the page** - This often resolves temporary issues")
    st.write("2. **Clear browser cache** - Old cached data might be causing conflicts")
    st.write("3. **Check internet connection** - Ensure stable connectivity")
    st.write("4. **Try again later** - The issue might be temporary")
    
    if st.button("🔄 Refresh Page"):
        st.rerun()
    
    st.subheader("📞 Contact Information")
    st.info("If the issue persists, please contact: **Shivangi Sinha** at shivangisinha.work@gmail.com")

def show_dashboard_overview():
    """Show dashboard overview with error handling"""
    st.header("📊 Dashboard Overview")
    
    if not st.session_state.dashboard_data:
        st.error("No data available. Please refresh the page.")
        return
    
    data = st.session_state.dashboard_data
    summary = data['executive_summary']
    
    # Show basic KPIs
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
    
    # Show charts if data is available
    if not data['analysis_df'].empty:
        st.subheader("🏆 Top Priority Features")
        top_features = data['analysis_df'].head(10)
        
        fig = px.bar(
            top_features,
            x='composite_score',
            y='feature_name',
            orientation='h',
            title="Feature Priority Scores"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No feature data available. The app is running in demo mode.")

def show_ai_assistant():
    """Show AI assistant with improved error handling"""
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
    
    # Display chat messages
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
    
    # Chat input
    user_input = st.chat_input("Ask me anything about your product roadmap...")
    
    if user_input:
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        
        try:
            with st.spinner("Analyzing..."):
                response = st.session_state.ai_assistant.process_query(user_input, stakeholder_role)
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
            st.rerun()
        except Exception as e:
            st.error(f"Error processing query: {str(e)}")
            st.session_state.chat_messages.append({
                "role": "assistant", 
                "content": "I'm sorry, I encountered an error while processing your request. Please try again or rephrase your question."
            })

def show_footer():
    """Show footer with contact information"""
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
    """Main application function with comprehensive error handling"""
    try:
        # Initialize session state
        if not initialize_session_state():
            show_error_page()
            return
        
        # Show header
        show_header()
        
        # Show sidebar and get selected page
        selected_page = show_sidebar()
        
        # Load dashboard data if not already loaded
        if st.session_state.dashboard_data is None:
            with st.spinner("Loading dashboard data..."):
                st.session_state.dashboard_data = load_dashboard_data()
        
        # Route to selected page
        if selected_page == "📊 Dashboard Overview":
            show_dashboard_overview()
        elif selected_page == "🤖 AI Assistant":
            show_ai_assistant()
        else:
            st.info(f"The '{selected_page}' page is currently under development.")
            st.write("Available pages:")
            st.write("- 📊 Dashboard Overview")
            st.write("- 🤖 AI Assistant")
            st.write("- More pages coming soon!")
        
        # Show footer
        show_footer()
        
    except Exception as e:
        st.error(f"Critical application error: {str(e)}")
        st.info("Please refresh the page or contact support at shivangisinha.work@gmail.com")
        
        if st.button("🔄 Refresh Application"):
            st.rerun()

if __name__ == "__main__":
    main()

