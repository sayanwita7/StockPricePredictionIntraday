import streamlit as st
def load_styles():    
    st.markdown("""
    <style>
    /* Hide Sidebar */
    [data-testid="stSidebar"]{
        display:none;
    }
    #MainMenu{
        visibility:hidden;
    }
    footer{
        visibility:hidden;
    }
    header{
        visibility:hidden;
    }
    /* Background Image Properly Adjusted */
    .stApp{
        background:
        linear-gradient(
            rgba(0,0,0,0.60),
            rgba(0,0,0,0.70)
        ),
        url("https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3");
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    /* Main Container */
    [data-testid="stAppViewContainer"] .block-container{
        background: rgba(0,0,0,0.45);
        backdrop-filter: blur(6px);
        border-radius:25px;
        padding:40px;
        margin-top:20px;
    }
    /* Title */
    .title{
        text-align:center;
        font-size:65px;
        font-weight:bold;
        color:#00ffcc;
        text-shadow:2px 2px 12px black;
    }
    /* Subtitle */
    .subtitle{
        text-align:center;
        font-size:26px;
        color:white;
        margin-top:-10px;
    }
    /* Moving Text */
    .marquee-container{
        width:100%;
        overflow:hidden;
        white-space:nowrap;
        background:rgba(255,255,255,0.08);
        border-radius:15px;
        padding:15px;
        margin-top:30px;
    }
    .marquee{
        display:inline-block;
        animation:moveText 18s linear infinite;
        color:#00ffcc;
        font-size:24px;
        font-weight:bold;
    }
    @keyframes moveText{
        0%{
            transform:translateX(100%);
        }
        100%{
            transform:translateX(-100%);
        }
    }
    /* Cards */
    .card{
        background:rgba(255,255,255,0.12);
        backdrop-filter: blur(10px);
        border-radius:25px;
        padding:30px;
        text-align:center;
        color:white;
        box-shadow:0px 0px 20px rgba(0,255,204,0.15);
        transition:0.4s;
        height:220px;
    }
    .card:hover{
        transform:translateY(-8px);
    }
    /* Buttons */
    .stButton > button{
        width:100%;
        height:60px;
        border-radius:15px;
        border:none;
        font-size:22px;
        font-weight:bold;
        transition:0.3s;
    }
    .stButton > button:hover{
        transform:scale(1.03);
    }
    /* Footer */
    .footer{
        text-align:center;
        color:white;
        margin-top:20px;
        font-size:18px;
    }
    </style>
    """, unsafe_allow_html=True)

def load_dashboard_styles():
    st.markdown("""
    <style>
    /* MAIN APP */
    .stApp{
        background: linear-gradient(
            135deg,
            #0f172a,
            #111827,
            #1e293b
        );
        color:white;
    }
        section[data-testid="stSidebar"]{
        background: linear-gradient(
            180deg,
            rgba(15,23,42,0.98),
            rgba(30,41,59,0.96)
        );
        border-right: 1px solid rgba(255,255,255,0.08);
        backdrop-filter: blur(18px);
    }
    /* TITLE */
    .main-title{
        font-size:42px;
        font-weight:bold;
        color:white;
    }
    /* CARD */
    .card{
        background: rgba(30,41,59,0.85);
        padding:22px;
        border-radius:20px;
        border:1px solid rgba(255,255,255,0.08);
        box-shadow:0 8px 25px rgba(0,0,0,0.35);
        text-align:center;
        margin-bottom:20px;   
        height:120px;         
        display:flex;
        flex-direction:column;
        justify-content:center;
    }     
    .card:hover{
        transform: translateY(-5px);
        box-shadow:0 10px 35px rgba(59,130,246,0.25);
    }
    /* METRIC */
    .metric{
        font-size:28px;
        font-weight:bold;
        color:#C47BE4;
        margin-bottom:6px;
    }
    .label{
        color:#cbd5e1;
        font-size:18px;
        margin-bottom:8px;
    }
    /* STREAMLIT METRIC */
    [data-testid="metric-container"]{
        background: rgba(30,41,59,0.85);
        border-radius:20px;
        padding:18px;
        border:1px solid rgba(255,255,255,0.08);
    }
    /* SIDEBAR MENU */
    .nav-link{
        border-radius:12px;
        margin-bottom:8px;
    }
    .nav-link-selected{
        background: linear-gradient(
            135deg,
            #3b82f6,
            #2563eb
        ) !important;
        color:white !important;
    }      
    [data-testid="stSidebarNav"]{
        display:none;
    }

    [data-testid="stHeader"]{
        background: transparent;
    }

    /* Style sidebar toggle button */
    button[kind="header"]{
        color:white !important;
    }
    #MainMenu{
        visibility:hidden;
    }
    footer{
        visibility:hidden;
    }
    </style>
    """, unsafe_allow_html=True)

def load_sidebar_styles():
    st.markdown(
            """
        </style>
            <div style="
                background: rgba(59,130,246,0.15);
                padding:18px;
                border-radius:18px;
                border:1px solid rgba(255,255,255,0.08);
                text-align:center;
                margin-bottom:20px;
                box-shadow:0 8px 25px rgba(0,0,0,0.25);
            ">
                <h2 style="color:white; margin:0;">
                    📊 Stock Dashboard
                </h2>
                <p style="color:#cbd5e1; margin-top:8px;">
                    Smart Market Prediction
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
def load_login_styles():
    st.markdown("""
    <style>
    /* Hide Streamlit UI */
    #MainMenu,
    header,
    footer,
    [data-testid="stSidebar"],
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"]{
        display:none;
    }
    /* Remove top spacing */
    .block-container{
        padding-top:1rem;
        max-width:500px;
    }
    /* Background */
    .stApp{
        background:
        linear-gradient(
            rgba(0,0,0,0.65),
            rgba(0,0,0,0.75)
        ),
        url("https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3");
        background-size:cover;
        background-position:center;
        background-repeat:no-repeat;
        background-attachment:fixed;
    }
    /* Glass Card */
    .card{
        background:rgba(111,66,193,0.12);
        backdrop-filter:blur(18px);
        -webkit-backdrop-filter:blur(18px);
        border:1px solid rgba(255,255,255,0.10);
        border-radius:28px;
        padding:35px;
        box-shadow:
        0px 8px 30px rgba(111,66,193,0.20);
    }
    /* Logo */
    .logo{
        text-align:center;
        font-size:52px;
        margin-bottom:5px;
    }
    /* Title */
    .title{
        text-align:center;
        color:white;
        font-size:36px;
        font-weight:700;
        margin-bottom:5px;
    }
    /* Subtitle */
    .subtitle{
        text-align:center;
        color:#d1d5db;
        font-size:15px;
        margin-bottom:20px;
    }
    /* Labels */
    .stTextInput label{
        color:white !important;
        font-size:14px !important;
        font-weight:500 !important;
    }
    /* Inputs */
    .stTextInput input{
        background:
        rgba(255,255,255,0.10)!important;
        border:1px solid
        rgba(255,255,255,0.12)!important;
        border-radius:14px!important;
        color:white!important;
    }
    /* Buttons */
    div.stButton > button{
        width:100%;
        height:48px;
        border:none;
        border-radius:14px;
        background:
        linear-gradient(
            90deg,
            #7e22ce,
            #9333ea
        );
        color:white;
        font-size:17px;
        font-weight:600;
    }
    div.stButton > button:hover{
        background:
        linear-gradient(
            90deg,
            #6d28d9,
            #7e22ce
        );
    }
    /* Bottom Text */
    .bottom-text{
        text-align:center;
        color:#d1d5db;
        margin-top:10px;
    }
    </style>
    """, unsafe_allow_html=True)

def load_register_styles():
    st.markdown("""
    <style>
    /* Hide Streamlit UI */
    #MainMenu,
    header,
    footer,
    [data-testid="stSidebar"]{
        display:none;
    }
    [data-testid="stHeader"]{
        display:none;
    }
    /* Remove top spacing */
    .block-container{
        padding-top:1rem;
        max-width:500px;
    }
    /* Background */
    .stApp{
        background:
        linear-gradient(
            rgba(0,0,0,0.65),
            rgba(0,0,0,0.75)
        ),
        url("https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3");

        background-size:cover;
        background-position:center;
        background-repeat:no-repeat;
        background-attachment:fixed;
    }
    /* Glass Card */
    .card{
        background:rgba(111,66,193,0.12);
        backdrop-filter:blur(18px);
        -webkit-backdrop-filter:blur(18px);
        border:1px solid rgba(255,255,255,0.10);
        border-radius:28px;
        padding:35px;
        box-shadow:
        0px 8px 30px rgba(111,66,193,0.20);
    }
    /* Logo */
    .logo{
        text-align:center;
        font-size:52px;
        margin-bottom:5px;
    }
    /* Title */
    .title{
        text-align:center;
        color:white;
        font-size:36px;
        font-weight:700;
        margin-bottom:5px;
    }
    /* Subtitle */
    .subtitle{
        text-align:center;
        color:#d1d5db;
        font-size:15px;
        margin-bottom:20px;
    }
    /* Labels */
    .stTextInput label{
        color:white !important;
        font-size:14px !important;
        font-weight:500 !important;
    }
    /* Inputs */
    .stTextInput input{
        background:
        rgba(255,255,255,0.10)!important;

        border:1px solid
        rgba(255,255,255,0.12)!important;

        border-radius:14px!important;

        color:white!important;
    }
    /* Button */
    div.stButton > button{
        width:100%;
        height:48px;
        border:none;
        border-radius:14px;

        background:
        linear-gradient(
            90deg,
            #7e22ce,
            #9333ea
        );
        color:white;
        font-size:17px;
        font-weight:600;
    }
    /* Bottom Text */
    .bottom-text{
        text-align:center;
        color:#d1d5db;
        margin-top:10px;
    }
    /* Small Sign In button */
    .sign-btn button{
        height:40px !important;
    }
    </style>
    """, unsafe_allow_html=True)

def load_settings_styles():
    st.markdown("""
    <style>
    .setting-card{
        background:
        rgba(30,41,59,0.85);
        border:
        1px solid rgba(255,255,255,0.08);
        padding:25px;
        border-radius:20px;
        box-shadow:
        0 8px 25px rgba(0,0,0,0.35);
        margin-bottom:25px;
    }
    div.stButton > button{
        width:100%;
        height:50px;
        border:none;
        border-radius:14px;
        background: #C47BE4;
        color:white;
        font-size:17px;
        font-weight:bold;
        transition:0.3s;
        box-shadow:
        0 8px 20px rgba(147,51,234,0.35);
    }
    </style>
    """, unsafe_allow_html=True)