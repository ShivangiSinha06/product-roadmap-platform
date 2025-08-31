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
    
    .sidebar-content {
        background: var(--bg-card);
        color: var(--text-primary);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid var(--border-color);
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .theme-toggle {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 999;
        background: var(--bg-card);
        border: 2px solid var(--primary-blue);
        border-radius: 50px;
        padding: 0.5rem 1rem;
        color: var(--text-primary);
        font-weight: bold;
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
        color: white;
    }
    
    .main-header h3 {
        font-size: 1.3rem;
        margin-bottom: 0.5rem;
        font-weight: 400;
        opacity: 0.95;
        color: white;
    }
    
    .main-header p {
        font-size: 1rem;
        opacity: 0.9;
        margin: 0;
        color: white;
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
        color: var(--text-secondary);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .metric-card .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--text-primary);
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
    
    .footer h3 {
        color: white;
        margin-bottom: 1rem;
        font-size: 1.5rem;
        font-weight: 600;
    }
    
    .footer p {
        margin: 0.5rem 0;
        opacity: 0.9;
        color: white;
    }
    
    .footer small {
        opacity: 0.7;
        font-size: 0.85rem;
        color: white;
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
    
    .theme-toggle {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 999;
        background: var(--bg-card);
        border: 2px solid var(--primary-blue);
        border-radius: 50px;
        padding: 0.5rem 1rem;
        color: var(--text-primary);
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .theme-toggle:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }
    
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
    
    .stSelectbox > div > div {
        border-radius: 8px !important;
        border: 2px solid var(--border-color) !important;
        background: var(--bg-card) !important;
        color: var(--text-primary) !important;
    }
    
    .plotly-graph-div {
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid var(--border-color);
        overflow: hidden;
        background: var(--bg-card);
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #dcfce7 0%, #f0fdf4 100%) !important;
        border-radius: 8px !important;
        border-left: 4px solid var(--success-green) !important;
        color: #14532d !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fef3c7 0%, #fffbeb 100%) !important;
        border-radius: 8px !important;
        border-left: 4px solid var(--warning-orange) !important;
        color: #92400e !important;
    }
    
    .stError {
        background: linear-gradient(135deg, #fee2e2 0%, #fef2f2 100%) !important;
        border-radius: 8px !important;
        border-left: 4px solid var(--danger-red) !important;
        color: #991b1b !important;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #dbeafe 0%, #eff6ff 100%) !important;
        border-radius: 8px !important;
        border-left: 4px solid var(--primary-blue) !important;
        color: #1e40af !important;
    }
    
    .stChatMessage {
        border-radius: 12px !important;
        margin-bottom: 1rem !important;
        padding: 1rem !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important;
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
    }
    
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--primary-blue) 0%, var(--secondary-purple) 100%) !important;
        border-radius: 10px !important;
    }
    
    .insight-card {
        background: var(--bg-card);
        color: var(--text-primary);
        border-radius: 10px;
        padding: 1.2rem;
        margin: 1rem 0;
        border-left: 4px solid var(--primary-blue);
        box-shadow: 0 3px 12px rgba(0,0,0,0.08);
        border: 1px solid var(--border-color);
    }
    
    .quadrant-analysis {
        background: var(--bg-card);
        color: var(--text-primary);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 1px solid var(--border-color);
    }
    
    .quarter-card {
        background: var(--bg-card);
        color: var(--text-primary);
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 3px 12px rgba(0,0,0,0.08);
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
        color: white;
    }
    
    .main-header h3 {
        font-size: 1.3rem;
        margin-bottom: 0.5rem;
        font-weight: 400;
        opacity: 0.95;
        color: white;
    }
    
    .main-header p {
        font-size: 1rem;
        opacity: 0.9;
        margin: 0;
        color: white;
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
        color: var(--text-secondary);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .metric-card .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--text-primary);
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
    
    .footer h3 {
        color: white;
        margin-bottom: 1rem;
        font-size: 1.5rem;
        font-weight: 600;
    }
    
    .footer p {
        margin: 0.5rem 0;
        opacity: 0.9;
        color: white;
    }
    
    .footer small {
        opacity: 0.7;
        font-size: 0.85rem;
        color: white;
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
    
    .theme-toggle {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 999;
        background: var(--bg-card);
        border: 2px solid var(--primary-blue);
        border-radius: 50px;
        padding: 0.5rem 1rem;
        color: var(--text-primary);
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .theme-toggle:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }
    
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
    
    .stSelectbox > div > div {
        border-radius: 8px !important;
        border: 2px solid var(--border-color) !important;
        background: var(--bg-card) !important;
        color: var(--text-primary) !important;
    }
    
    .plotly-graph-div {
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid var(--border-color);
        overflow: hidden;
        background: var(--bg-card);
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #dcfce7 0%, #f0fdf4 100%) !important;
        border-radius: 8px !important;
        border-left: 4px solid var(--success-green) !important;
        color: #14532d !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fef3c7 0%, #fffbeb 100%) !important;
        border-radius: 8px !important;
        border-left: 4px solid var(--warning-orange) !important;
        color: #92400e !important;
    }
    
    .stError {
        background: linear-gradient(135deg, #fee2e2 0%, #fef2f2 100%) !important;
        border-radius: 8px !important;
        border-left: 4px solid var(--danger-red) !important;
        color: #991b1b !important;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #dbeafe 0%, #eff6ff 100%) !important;
        border-radius: 8px !important;
        border-left: 4px solid var(--primary-blue) !important;
        color: #1e40af !important;
    }
    
    .stChatMessage {
        border-radius: 12px !important;
        margin-bottom: 1rem !important;
        padding: 1rem !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important;
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
    }
    
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--primary-blue) 0%, var(--secondary-purple) 100%) !important;
        border-radius: 10px !important;
    }
    
    .insight-card {
        background: var(--bg-card);
        color: var(--text-primary);
        border-radius: 10px;
        padding: 1.2rem;
        margin: 1rem 0;
        border-left: 4px solid var(--primary-blue);
        box-shadow: 0 3px 12px rgba(0,0,0,0.08);
        border: 1px solid var(--border-color);
    }
    
    .quadrant-analysis {
        background: var(--bg-card);
        color: var(--text-primary);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 1px solid var(--border-color);
    }
    
    .quarter-card {
        background: var(--bg-card);
        color: var(--text-primary);
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 3px 12px rgba(0,0,0,0.08);
        border: 1px solid var(--border-color);
    }
    
    /* Force dark text in light mode for better readability */
    .metric-card .metric-title,
    .metric-card .metric-value {
        color: var(--text-primary) !important;
    }
    
    /* Ensure proper text contrast in all components */
    .stMarkdown, .stText, .stCaption {
        color: var(--text-primary) !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
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
    
    # Enhanced Priority Matrix with Theme Support
    st.markdown("### 📊 **Effort vs Impact Analysis**")
    
    # Theme-aware colors
    text_color = '#f9fafb' if st.session_state.dark_mode else '#111827'
    bg_color = '#111827' if st.session_state.dark_mode else '#ffffff'
    
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
    
    # Add enhanced quadrant lines
    effort_median = analysis_df['effort_estimate'].median()
    impact_median = analysis_df['impact_score'].median()
    
    line_color = 'rgba(156, 163, 175, 0.6)' if st.session_state.dark_mode else 'rgba(107, 114, 128, 0.5)'
    
    fig.add_hline(y=impact_median, line_dash="dash", line_color=line_color, line_width=2)
    fig.add_vline(x=effort_median, line_dash="dash", line_color=line_color, line_width=2)
    
    # Enhanced quadrant labels with better contrast
    annotation_style = dict(
        showarrow=False,
        font=dict(size=14, weight="bold"),
        borderwidth=2,
        borderpad=8,
        bgcolor="rgba(0,0,0,0.8)" if st.session_state.dark_mode else "rgba(255,255,255,0.9)"
    )
    
    fig.add_annotation(
        x=effort_median*0.5, y=impact_median*1.4, 
        text="🚀 Quick Wins", 
        font=dict(color="#10b981"),
        bordercolor="#10b981",
        **annotation_style
    )
    
    fig.add_annotation(
        x=effort_median*1.4, y=impact_median*1.4, 
        text="🎯 Major Projects", 
        font=dict(color="#ef4444"),
        bordercolor="#ef4444",
        **annotation_style
    )
    
    fig.add_annotation(
        x=effort_median*0.5, y=impact_median*0.6, 
        text="📝 Fill-ins", 
        font=dict(color="#6366f1"),
        bordercolor="#6366f1",
        **annotation_style
    )
    
    fig.add_annotation(
        x=effort_median*1.4, y=impact_median*0.6, 
        text="❓ Questionable", 
        font=dict(color="#f59e0b"),
        bordercolor="#f59e0b",
        **annotation_style
    )
    
    fig.update_layout(
        height=600,
        showlegend=True,
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=-0.15,
            font=dict(color=text_color)
        ),
        margin=dict(t=50, b=100, l=50, r=50),
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        font=dict(color=text_color),
        title=dict(font=dict(color=text_color)),
        xaxis=dict(
            titlefont=dict(color=text_color),
            tickfont=dict(color=text_color),
            gridcolor=line_color
        ),
        yaxis=dict(
            titlefont=dict(color=text_color),
            tickfont=dict(color=text_color),
            gridcolor=line_color
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Enhanced Quadrant Analysis with Better Styling
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
    
    # Enhanced quadrant display
    quad_col1, quad_col2 = st.columns(2)
    
    with quad_col1:
        # Quick Wins Section
        st.markdown("""
        <div class="quadrant-analysis">
            <h4 style="color: #10b981; margin-bottom: 1rem;">🚀 Quick Wins (Low Effort, High Impact)</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.success(f"**{len(quick_wins)} features** - Prioritize these for immediate wins!")
        
        if not quick_wins.empty:
            for i, (_, feature) in enumerate(quick_wins.head(5).iterrows(), 1):
                st.markdown(f"**{i}.** {feature['feature_name']} *(Score: {feature['composite_score']:.1f})*")
        
        # Fill-ins Section
        st.markdown("""
        <div class="quadrant-analysis">
            <h4 style="color: #6366f1; margin-bottom: 1rem;">📝 Fill-ins (Low Effort, Low Impact)</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.info(f"**{len(fill_ins)} features** - Consider for capacity utilization")
        
        if not fill_ins.empty:
            for i, (_, feature) in enumerate(fill_ins.head(3).iterrows(), 1):
                st.markdown(f"**{i}.** {feature['feature_name']} *(Score: {feature['composite_score']:.1f})*")
    
    with quad_col2:
        # Major Projects Section
        st.markdown("""
        <div class="quadrant-analysis">
            <h4 style="color: #ef4444; margin-bottom: 1rem;">🎯 Major Projects (High Effort, High Impact)</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.warning(f"**{len(major_projects)} features** - Plan carefully with adequate resources")
        
        if not major_projects.empty:
            for i, (_, feature) in enumerate(major_projects.head(5).iterrows(), 1):
                st.markdown(f"**{i}.** {feature['feature_name']} *(Score: {feature['composite_score']:.1f})*")
        
        # Questionable Section
        st.markdown("""
        <div class="quadrant-analysis">
            <h4 style="color: #f59e0b; margin-bottom: 1rem;">❓ Questionable (High Effort, Low Impact)</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.error(f"**{len(questionable)} features** - Reconsider or redesign approach")
        
        if not questionable.empty:
            for i, (_, feature) in enumerate(questionable.head(3).iterrows(), 1):
                st.markdown(f"**{i}.** {feature['feature_name']} *(Score: {feature['composite_score']:.1f})*")

def show_roadmap_timeline():
    """Enhanced roadmap timeline with theme support"""
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
    
    # Enhanced quarterly cards with theme support
    quarters = ['Q1 2026', 'Q2 2026', 'Q3 2026', 'Q4 2026']
    quarter_cols = st.columns(4)
    
    colors = ['#ef4444', '#f59e0b', '#10b981', '#6366f1']
    
    for i, (quarter, color) in enumerate(zip(quarters, colors)):
        with quarter_cols[i]:
            if quarter in quarterly_data.index:
                data = quarterly_data.loc[quarter]
                
                # Theme-aware card styling
                bg_opacity = '25' if st.session_state.dark_mode else '15'
                
                st.markdown(f"""
                <div class="quarter-card" style="
                    background: linear-gradient(135deg, {color}{bg_opacity} 0%, transparent 100%);
                    border-left: 4px solid {color};
                ">
                    <h4 style="color: {color}; margin: 0; font-weight: bold;">{quarter}</h4>
                    <p style="margin: 0.5rem 0; font-size: 1.4rem; font-weight: bold; color: var(--text-primary);">{data['Features']} Features</p>
                    <p style="margin: 0; font-size: 1rem; color: var(--text-secondary);">{data['Total Effort']:.0f} Story Points</p>
                    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: var(--text-secondary);">Avg Priority: {data['Avg Priority']:.1f}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                border_color = 'rgba(156, 163, 175, 0.3)' if st.session_state.dark_mode else '#e5e7eb'
                
                st.markdown(f"""
                <div class="quarter-card" style="
                    border-left: 4px solid {border_color};
                    opacity: 0.6;
                ">
                    <h4 style="color: var(--text-secondary); margin: 0;">{quarter}</h4>
                    <p style="margin: 0.5rem 0; font-size: 1.4rem; font-weight: bold; color: var(--text-secondary);">0 Features</p>
                    <p style="margin: 0; font-size: 1rem; color: var(--text-secondary);">0 Story Points</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Enhanced Feature Timeline Chart with Theme Support
    st.markdown("### 📊 **Features Distribution by Quarter**")
    
    if not quarterly_data.empty:
        text_color = '#f9fafb' if st.session_state.dark_mode else '#111827'
        bg_color = '#111827' if st.session_state.dark_mode else '#ffffff'
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Number of Features',
            x=quarterly_data.index,
            y=quarterly_data['Features'],
            marker_color=colors[:len(quarterly_data)],
            text=quarterly_data['Features'],
            textposition='outside',
            textfont=dict(color=text_color),
            hovertemplate='<b>%{x}</b><br>Features: %{y}<br>Total Effort: %{customdata:.0f} SP<extra></extra>',
            customdata=quarterly_data['Total Effort']
        ))
        
        fig.update_layout(
            title=dict(text="Quarterly Feature Distribution", font=dict(color=text_color)),
            xaxis=dict(
                title="Quarter",
                titlefont=dict(color=text_color),
                tickfont=dict(color=text_color)
            ),
            yaxis=dict(
                title="Number of Features",
                titlefont=dict(color=text_color),
                tickfont=dict(color=text_color)
            ),
            height=400,
            showlegend=False,
            margin=dict(t=50, b=50, l=50, r=50),
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color,
            font=dict(color=text_color)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Enhanced Capacity Analysis
    st.markdown("### ⚖️ **Capacity Analysis**")
    
    if not quarterly_data.empty:
        capacity_col1, capacity_col2, capacity_col3 = st.columns(3)
        
        total_effort = quarterly_data['Total Effort'].sum()
        avg_quarterly = total_effort / 4
        max_quarter = quarterly_data['Total Effort'].max()
        heaviest_quarter = quarterly_data['Total Effort'].idxmax()
        
        with capacity_col1:
            st.markdown(f"""
            <div class="insight-card">
                <strong>🏋️ Total Roadmap Effort</strong><br>
                <span style="font-size: 1.8rem; font-weight: bold; color: var(--primary-blue);">{total_effort:.0f} SP</span>
            </div>
            """, unsafe_allow_html=True)
        
        with capacity_col2:
            st.markdown(f"""
            <div class="insight-card">
                <strong>📊 Quarterly Average</strong><br>
                <span style="font-size: 1.8rem; font-weight: bold; color: var(--warning-orange);">{avg_quarterly:.0f} SP</span>
            </div>
            """, unsafe_allow_html=True)
        
        with capacity_col3:
            st.markdown(f"""
            <div class="insight-card">
                <strong>⚡ Heaviest Quarter</strong><br>
                <span style="font-size: 1.8rem; font-weight: bold; color: var(--danger-red);">{heaviest_quarter}</span>
                <p style="margin: 0.3rem 0 0 0; font-size: 0.9rem;">({max_quarter:.0f} SP)</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Enhanced capacity warnings
        if max_quarter > 120:
            st.error(f"⚠️ **Capacity Alert:** {heaviest_quarter} appears overloaded ({max_quarter:.0f} SP). Consider redistributing features.")
        elif max_quarter > 100:
            st.warning(f"🔔 **Capacity Warning:** {heaviest_quarter} is near capacity ({max_quarter:.0f} SP). Monitor progress closely.")
        else:
            st.success("✅ **Capacity Status:** Good workload distribution across quarters.")

def show_roi_analysis():
    """Enhanced ROI analysis with theme support and better contrast"""
    st.title("💰 ROI Analysis")
    
    if not st.session_state.dashboard_data:
        st.warning("⚠️ Dashboard data not loaded.")
        return
    
    roi_df = st.session_state.dashboard_data['roi_df']
    
    if roi_df.empty:
        st.markdown("""
        ### 📊 **ROI Analysis Unavailable**
        
        ROI analysis requires revenue impact data in customer feedback. To enable ROI projections:
        
        #### 💡 **How to Enable ROI Analysis:**
        """)
        
        roi_col1, roi_col2 = st.columns(2)
        
        with roi_col1:
            st.markdown("""
            <div class="insight-card">
                <h4 style="color: var(--primary-blue);">📝 Step 1: Add Revenue Data</h4>
                <p>Include revenue estimates in customer feedback entries</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="insight-card">
                <h4 style="color: var(--success-green);">📊 Step 3: View Results</h4>
                <p>ROI calculations will appear automatically with complete data</p>
            </div>
            """, unsafe_allow_html=True)
        
        with roi_col2:
            st.markdown("""
            <div class="insight-card">
                <h4 style="color: var(--warning-orange);">🔄 Step 2: Refresh Data</h4>
                <p>Use the refresh button in the sidebar to reload analytics</p>
            </div>
            """, unsafe_allow_html=True)
        
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
            "Avg Payback",
            f"{avg_payback:.1f} months",
            priority_class=payback_class,
            help_text="Average time to recover investment"
        ), unsafe_allow_html=True)
    
    # Enhanced ROI Charts with Theme Support
    col1, col2 = st.columns(2)
    
    # Theme-aware colors
    text_color = '#f9fafb' if st.session_state.dark_mode else '#111827'
    bg_color = '#111827' if st.session_state.dark_mode else '#ffffff'
    
    with col1:
        st.markdown("### 🎯 **ROI by Feature**")
        
        top_roi = roi_df.nlargest(10, 'roi_percentage')
        
        # Create theme-aware color scale
        colors = ['#ef4444' if x < 50 else '#f59e0b' if x < 100 else '#10b981' for x in top_roi['roi_percentage']]
        
        fig = go.Figure(go.Bar(
            x=top_roi['roi_percentage'],
            y=top_roi['feature_name'],
            orientation='h',
            marker_color=colors,
            text=[f"{x:.1f}%" for x in top_roi['roi_percentage']],
            textposition='outside',
            textfont=dict(color=text_color)
        ))
        
        fig.update_layout(
            xaxis=dict(
                title="ROI (%)",
                titlefont=dict(color=text_color),
                tickfont=dict(color=text_color)
            ),
            yaxis=dict(
                title="",
                tickfont=dict(color=text_color)
            ),
            height=400,
            margin=dict(t=20, b=20, l=20, r=20),
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color,
            font=dict(color=text_color)
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
            line=dict(color="#ef4444", width=2, dash="dash"),
            name="Break-even line"
        )
        
        fig.update_layout(
            height=400,
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color,
            font=dict(color=text_color),
            title=dict(font=dict(color=text_color)),
            xaxis=dict(titlefont=dict(color=text_color), tickfont=dict(color=text_color)),
            yaxis=dict(titlefont=dict(color=text_color), tickfont=dict(color=text_color))
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Enhanced ROI Table with Better Styling
    st.markdown("### 📋 **Detailed ROI Analysis**")
    
    display_roi = roi_df.copy().sort_values('roi_percentage', ascending=False)
    
    # Add enhanced ROI categories
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
    
    # Enhanced table
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

def show_ai_assistant():
    """Enhanced AI Assistant with theme support"""
    st.title("🤖 AI Product Assistant")
    
    # Enhanced introduction with theme support
    st.markdown(f"""
    <div class="insight-card" style="border-left-color: #0ea5e9;">
        <h4 style="color: #0369a1; margin-bottom: 1rem;">💡 What I can help you with:</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
            <div>
                <p style="margin: 0.5rem 0; color: var(--text-primary);"><strong>🎯 Feature Analysis:</strong> Priority rankings, RICE scores</p>
                <p style="margin: 0.5rem 0; color: var(--text-primary);"><strong>💰 Financial Planning:</strong> ROI calculations, budget projections</p>
            </div>
            <div>
                <p style="margin: 0.5rem 0; color: var(--text-primary);"><strong>📅 Timeline Planning:</strong> Capacity analysis, quarter assignments</p>
                <p style="margin: 0.5rem 0; color: var(--text-primary);"><strong>👥 Strategic Insights:</strong> Customer segments, market analysis</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Chat Interface with Theme Support
    st.markdown("### 💬 **Chat with Your AI Assistant**")
    
    # Display chat messages with enhanced theme-aware styling
    for i, message in enumerate(st.session_state.chat_messages):
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                bg_color = '#374151' if st.session_state.dark_mode else '#f8fafc'
                border_color = '#3b82f6'
                st.markdown(f'<div style="background: {bg_color}; padding: 1rem; border-radius: 8px; border-left: 3px solid {border_color}; color: var(--text-primary);">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                bg_color = '#1f2937' if st.session_state.dark_mode else '#eff6ff'
                border_color = '#10b981'
                st.markdown(f'<div style="background: {bg_color}; padding: 1rem; border-radius: 8px; border-left: 3px solid {border_color}; color: var(--text-primary);">{message["content"]}</div>', unsafe_allow_html=True)
    
    # Enhanced chat input
    if prompt := st.chat_input("💭 Ask me anything about your product roadmap..."):
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            bg_color = '#1f2937' if st.session_state.dark_mode else '#eff6ff'
            st.markdown(f'<div style="background: {bg_color}; padding: 1rem; border-radius: 8px; border-left: 3px solid #10b981; color: var(--text-primary);">{prompt}</div>', unsafe_allow_html=True)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Analyzing your request..."):
                try:
                    response = st.session_state.ai_assistant.process_query(prompt)
                    bg_color = '#374151' if st.session_state.dark_mode else '#f8fafc'
                    st.markdown(f'<div style="background: {bg_color}; padding: 1rem; border-radius: 8px; border-left: 3px solid #3b82f6; color: var(--text-primary);">{response}</div>', unsafe_allow_html=True)
                    st.session_state.chat_messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"❌ Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_messages.append({"role": "assistant", "content": error_msg})
    
    # Enhanced Quick Action Buttons
    st.markdown("### 🎯 **Quick Questions**")
    
    col1, col2, col3 = st.columns(3)
    
    quick_questions = [
        ("🏆 What are my top priorities?", "What are my top priority features and why?"),
        ("⚡ Show me quick wins", "What are the best quick win opportunities?"),
        ("💰 Analyze ROI potential", "Can you analyze the ROI for my top features?"),
        ("📊 Compare features", "Compare the top 3 features in my roadmap"),
        ("📅 Plan my quarters", "Help me with capacity and timeline planning for the next quarters"),
        ("⚠️ Identify risks", "What are the biggest risks in my current roadmap?")
    ]
    
    for i, (button_text, query_text) in enumerate(quick_questions):
        col = [col1, col2, col3][i % 3]
        
        with col:
            if st.button(button_text, use_container_width=True, key=f"quick_{i}"):
                st.session_state.chat_messages.append({
                    "role": "user",
                    "content": query_text
                })
                st.rerun()
    
    # Clear Chat Button
    if st.button("🗑️ Clear Chat History", type="secondary", use_container_width=True):
        st.session_state.chat_messages = [{
            "role": "assistant",
            "content": "Hello! 👋 I'm your AI Product Assistant. I can help you analyze feature priorities, roadmap planning, ROI calculations, and strategic decisions. What would you like to know?"
        }]
        st.rerun()

def show_analytics_deep_dive():
    """Enhanced analytics with theme support"""
    st.title("📈 Analytics Deep Dive")
    
    if not st.session_state.dashboard_data:
        st.warning("⚠️ Dashboard data not loaded.")
        return
    
    analysis_df = st.session_state.dashboard_data['analysis_df']
    model_stats = st.session_state.dashboard_data['model_stats']
    
    if analysis_df.empty:
        st.info("📊 No analytics data available.")
        return
    
    # Enhanced Model Performance Section
    st.markdown("### 🤖 **ML Model Performance**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(create_enhanced_metric_card(
            "Training Score",
            f"{model_stats['train_score']:.3f}",
            help_text="Model performance on training data"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_enhanced_metric_card(
            "Test Score",
            f"{model_stats['test_score']:.3f}",
            help_text="Model performance on test data"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_enhanced_metric_card(
            "Features Analyzed",
            len(analysis_df),
            help_text="Number of features in analysis"
        ), unsafe_allow_html=True)

def show_customer_segments():
    """Enhanced customer segments with theme support"""
    st.title("👥 Customer Segments")
    
    if not st.session_state.dashboard_data:
        st.warning("⚠️ Dashboard data not loaded.")
        return
    
    segment_analysis = st.session_state.dashboard_data['segment_analysis']
    segment_priorities = st.session_state.dashboard_data['segment_priorities']
    
    if segment_analysis.empty and segment_priorities.empty:
        st.info("📊 No customer segment data available.")
        return
    
    # Enhanced segment display with theme support
    if not segment_priorities.empty:
        st.markdown("### 🎯 **Customer Segment Priorities**")
        
        for _, segment in segment_priorities.iterrows():
            with st.expander(f"📊 **{segment['customer_segment']} Segment Analysis**"):
                seg_col1, seg_col2, seg_col3 = st.columns(3)
                
                with seg_col1:
                    st.markdown(create_enhanced_metric_card(
                        "Total Requests",
                        int(segment['request_count']),
                        help_text="Number of feature requests from this segment"
                    ), unsafe_allow_html=True)
                
                with seg_col2:
                    st.markdown(create_enhanced_metric_card(
                        "Avg Revenue Impact",
                        f"${segment['avg_revenue_impact']:,.0f}",
                        help_text="Average revenue impact per request"
                    ), unsafe_allow_html=True)
                
                with seg_col3:
                    st.markdown(create_enhanced_metric_card(
                        "Avg Business Value",
                        f"{segment['avg_business_value']:.1f}/10",
                        help_text="Average business value rating"
                    ), unsafe_allow_html=True)

def show_data_management():
    """Enhanced data management with theme support"""
    st.title("⚙️ Data Management")
    
    st.markdown("""
    <div class="insight-card">
        <h4 style="color: var(--primary-blue);">🛠️ Manage Your Product Roadmap Data</h4>
        <p style="color: var(--text-primary);">Import/export features, generate sample data, and configure system settings.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Data Operations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📥 **Data Import & Generation**")
        
        if st.button("🔄 Generate Sample Data", use_container_width=True, type="primary"):
            with st.spinner("🔄 Generating comprehensive sample data..."):
                try:
                    st.session_state.db_manager.generate_sample_data()
                    st.session_state.dashboard_data = None  # Force refresh
                    st.success("✅ Sample data generated successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error generating data: {str(e)}")
        
        # Enhanced file upload
        uploaded_file = st.file_uploader(
            "📁 Upload CSV file", 
            type=['csv'],
            help="Upload customer feedback or feature data in CSV format"
        )
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.markdown("#### 👁️ **Preview of uploaded data:**")
                st.dataframe(df.head(), use_container_width=True)
                
                if st.button("📤 Import Data", use_container_width=True):
                    st.info("📊 Data import functionality coming soon!")
                    
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
    
    with col2:
        st.markdown("### 📤 **Data Export & Management**")
        
        if st.session_state.dashboard_data:
            analysis_df = st.session_state.dashboard_data['analysis_df']
            
            if not analysis_df.empty:
                csv = analysis_df.to_csv(index=False)
                
                st.download_button(
                    label="📄 Download Analysis Data",
                    data=csv,
                    file_name=f"roadmap_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                    type="primary"
                )
                
                # Additional export options
                roi_df = st.session_state.dashboard_data['roi_df']
                if not roi_df.empty:
                    roi_csv = roi_df.to_csv(index=False)
                    st.download_button(
                        label="💰 Download ROI Data",
                        data=roi_csv,
                        file_name=f"roi_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
        
        # Enhanced clear data section
        st.markdown("#### 🗑️ **Clear All Data**")
        
        if st.checkbox("⚠️ I understand this will delete all data", key="confirm_delete"):
            if st.button("🗑️ Clear Database", use_container_width=True, type="secondary"):
                with st.spinner("🔄 Clearing all data..."):
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
    
    # Enhanced System Status Dashboard
    st.markdown("### 🔍 **System Status Dashboard**")
    
    status_col1, status_col2, status_col3, status_col4 = st.columns(4)
    
    with status_col1:
        # Database status
        try:
            feedback_summary = st.session_state.db_manager.get_feedback_summary()
            db_records = len(feedback_summary) if not feedback_summary.empty else 0
            
            if db_records > 0:
                st.markdown(create_enhanced_metric_card(
                    "Database Status",
                    f"🟢 {db_records} records",
                    priority_class="priority-low",
                    help_text="Database connection and record count"
                ), unsafe_allow_html=True)
            else:
                st.markdown(create_enhanced_metric_card(
                    "Database Status",
                    "🟡 Empty",
                    priority_class="priority-medium",
                    help_text="Database is connected but empty"
                ), unsafe_allow_html=True)
        except:
            st.markdown(create_enhanced_metric_card(
                "Database Status",
                "🔴 Error",
                priority_class="priority-high",
                help_text="Database connection failed"
            ), unsafe_allow_html=True)
    
    with status_col2:
        # ML Model status
        try:
            model_stats = st.session_state.dashboard_data.get('model_stats', {}) if st.session_state.dashboard_data else {}
            train_score = model_stats.get('train_score', 0)
            
            if train_score > 0.8:
                st.markdown(create_enhanced_metric_card(
                    "ML Model",
                    f"🟢 {train_score:.2f}",
                    priority_class="priority-low",
                    help_text="Model is trained and performing well"
                ), unsafe_allow_html=True)
            elif train_score > 0.5:
                st.markdown(create_enhanced_metric_card(
                    "ML Model",
                    f"🟡 {train_score:.2f}",
                    priority_class="priority-medium",
                    help_text="Model is trained but needs improvement"
                ), unsafe_allow_html=True)
            else:
                st.markdown(create_enhanced_metric_card(
                    "ML Model",
                    "🔴 Not Trained",
                    priority_class="priority-high",
                    help_text="Model needs training"
                ), unsafe_allow_html=True)
        except:
            st.markdown(create_enhanced_metric_card(
                "ML Model",
                "🔴 Error",
                priority_class="priority-high",
                help_text="Model status unknown"
            ), unsafe_allow_html=True)
    
    with status_col3:
        # Data freshness
        if st.session_state.dashboard_data:
            last_updated = st.session_state.dashboard_data['last_updated']
            time_diff = datetime.now() - last_updated
            minutes_old = time_diff.total_seconds() / 60
            
            if minutes_old < 5:
                st.markdown(create_enhanced_metric_card(
                    "Data Freshness",
                    "🟢 Fresh",
                    priority_class="priority-low",
                    help_text=f"Updated {minutes_old:.0f} minutes ago"
                ), unsafe_allow_html=True)
            elif minutes_old < 30:
                st.markdown(create_enhanced_metric_card(
                    "Data Freshness",
                    "🟡 Moderate",
                    priority_class="priority-medium",
                    help_text=f"Updated {minutes_old:.0f} minutes ago"
                ), unsafe_allow_html=True)
            else:
                st.markdown(create_enhanced_metric_card(
                    "Data Freshness",
                    "🔴 Stale",
                    priority_class="priority-high",
                    help_text=f"Updated {minutes_old:.0f} minutes ago"
                ), unsafe_allow_html=True)
        else:
            st.markdown(create_enhanced_metric_card(
                "Data Freshness",
                "🔴 No Data",
                priority_class="priority-high",
                help_text="No data loaded"
            ), unsafe_allow_html=True)
    
    with status_col4:
        # System performance
        if st.session_state.dashboard_data:
            total_features = st.session_state.dashboard_data['executive_summary']['total_features']
            
            if total_features > 10:
                st.markdown(create_enhanced_metric_card(
                    "System Load",
                    f"🟢 {total_features} features",
                    priority_class="priority-low",
                    help_text="System running optimally"
                ), unsafe_allow_html=True)
            elif total_features > 0:
                st.markdown(create_enhanced_metric_card(
                    "System Load",
                    f"🟡 {total_features} features",
                    priority_class="priority-medium",
                    help_text="Limited data available"
                ), unsafe_allow_html=True)
            else:
                st.markdown(create_enhanced_metric_card(
                    "System Load",
                    "🔴 No features",
                    priority_class="priority-high",
                    help_text="No features to analyze"
                ), unsafe_allow_html=True)

def show_footer():
    """Enhanced footer with theme support"""
    st.markdown("""
    <div class="footer">
        <h3>🚀 Product Roadmap Platform</h3>
        <p><strong>AI-Driven Feature Prioritization & Strategic Planning</strong></p>
        <p>Built with ❤️ using Streamlit • Machine Learning • Advanced Analytics</p>
        <div style="margin: 2rem 0; display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
            <span>📊 RICE Methodology</span>
            <span>🤖 ML-Powered Insights</span>
            <span>💰 ROI Analytics</span>
            <span>📈 Real-time Dashboards</span>
        </div>
        <div style="margin: 1.5rem 0;">
            <p><strong>✨ Features:</strong> Priority Matrix • Timeline Planning • Customer Segments • Risk Assessment</p>
        </div>
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
    
    # Load dashboard data with enhanced progress tracking
    if st.session_state.dashboard_data is None:
        progress_container = st.container()
        
        with progress_container:
            st.info("🔄 Loading dashboard data...")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Enhanced loading sequence
            loading_steps = [
                ("🔌 Connecting to database...", 20),
                ("📊 Analyzing features...", 40),
                ("🤖 Training ML models...", 60),
                ("💰 Calculating ROI projections...", 80),
                ("✅ Finalizing analytics...", 100)
            ]
            
            for step_text, progress in loading_steps:
                status_text.text(step_text)
                progress_bar.progress(progress)
                
                if progress == 40:  # Load data at 40% progress
                    st.session_state.dashboard_data = load_dashboard_data()
            
            # Clear loading indicators
            import time
            time.sleep(0.5)
            progress_container.empty()
    
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
        st.info("🔄 Please try refreshing the page or contact support if the issue persists.")
        
        # Show error details in development mode
        if st.checkbox("🔍 Show detailed error information"):
            st.exception(e)
    
    # Show enhanced footer
    show_footer()

# Enhanced error handling for the entire application
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"🚨 Critical application error: {str(e)}")
        st.info("🔄 Please refresh the page. If the problem persists, check your internet connection and try again.")
        
        # Emergency fallback
        if st.button("🆘 Emergency Reset"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.success("✅ Session reset completed. Please refresh the page.")

