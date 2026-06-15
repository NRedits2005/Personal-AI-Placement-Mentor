import streamlit as st

def set_page_theme():
    """Injects high-readability CSS overrides to improve contrast and look-and-feel."""
    st.markdown("""
        <style>
        /* Fonts and General Readability */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
        
        html, body, [data-testid="stAppViewContainer"] {
            font-family: 'Inter', -apple-system, sans-serif;
            background-color: #0f172a !important;
            color: #f1f5f9 !important;
        }
        
        /* Sidebar layout and text readability */
        [data-testid="stSidebar"] {
            background-color: #0b0f19 !important;
            border-right: 1px solid #1e293b;
        }
        [data-testid="stSidebar"] * {
            color: #cbd5e1 !important;
        }
        
        /* Titles & Subheaders */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Inter', sans-serif;
            color: #f8fafc !important;
            font-weight: 700;
        }
        
        /* Markdown / Paragraph text contrast */
        div.stMarkdown p, div.stMarkdown li, div.stMarkdown span {
            color: #cbd5e1 !important;
            line-height: 1.6;
            font-size: 1rem;
        }
        
        /* Strong highlights */
        strong {
            color: #f8fafc !important;
            font-weight: 600;
        }
        
        /* Code blocks & Inline Code */
        code {
            font-family: 'JetBrains Mono', monospace !important;
            background-color: #1e293b !important;
            color: #38bdf8 !important;
            padding: 0.15rem 0.4rem;
            border-radius: 4px;
            font-size: 0.9em;
        }
        
        /* Block code styling */
        pre {
            background-color: #0b0f19 !important;
            border: 1px solid #334155 !important;
            border-radius: 8px;
            padding: 1rem;
        }
        pre code {
            color: #e2e8f0 !important;
            background-color: transparent !important;
            padding: 0 !important;
        }

        /* Metric Styling with prominent numbers */
        [data-testid="stMetricValue"] {
            color: #3b82f6 !important;
            font-weight: 800 !important;
            font-size: 2.2rem !important;
        }
        [data-testid="stMetricLabel"] {
            color: #94a3b8 !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* Expander headers & panels */
        div[data-testid="stExpander"] {
            background-color: #1e293b !important;
            border: 1px solid #334155 !important;
            border-radius: 8px !important;
            margin-bottom: 0.8rem;
        }
        div[data-testid="stExpander"] p {
            color: #f1f5f9 !important;
        }
        div[data-testid="stExpander"] [data-testid="stMarkdownContainer"] p {
            color: #cbd5e1 !important;
        }

        /* Tab buttons */
        div[data-baseweb="tab-list"] {
            gap: 12px;
            background-color: #0b0f19;
            padding: 6px;
            border-radius: 8px;
            border: 1px solid #1e293b;
        }
        button[data-baseweb="tab"] {
            background-color: transparent !important;
            color: #94a3b8 !important;
            border: none !important;
            font-weight: 600 !important;
            border-radius: 6px !important;
            padding: 8px 16px !important;
            transition: all 0.2s ease !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            background-color: #3b82f6 !important;
            color: #ffffff !important;
        }
        button[data-baseweb="tab"]:hover {
            color: #f8fafc !important;
        }

        /* Buttons styles (Streamlit button defaults override) */
        div.stButton > button {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
            color: #ffffff !important;
            border: 1px solid #3b82f6 !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            padding: 0.5rem 1.5rem !important;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2) !important;
            transition: all 0.2s ease !important;
        }
        div.stButton > button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4) !important;
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        }

        /* Forms, selects and text inputs */
        input, textarea, [data-baseweb="select"] {
            background-color: #1e293b !important;
            color: #f8fafc !important;
            border: 1px solid #334155 !important;
            border-radius: 8px !important;
        }
        div[data-baseweb="select"] > div {
            background-color: #1e293b !important;
            color: #f8fafc !important;
            border: none !important;
        }
        
        /* Custom Info/Success/Warning containers contrast */
        div[data-testid="stAlert"] {
            background-color: #1e293b !important;
            color: #f8fafc !important;
            border-left: 5px solid #3b82f6 !important;
            border-radius: 8px;
        }
        div[data-testid="stAlert"] [data-testid="stMarkdownContainer"] p {
            color: #f1f5f9 !important;
        }
        </style>
    """, unsafe_allow_html=True)
