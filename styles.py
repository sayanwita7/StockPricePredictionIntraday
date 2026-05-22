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
            135deg,
            rgba(11,17,32,0.96),
            rgba(15,23,42,0.95),
            rgba(30,41,59,0.93)
        ),
        url("https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3");


        background-size:cover;
        background-position:center;
        background-repeat:no-repeat;
        background-attachment:fixed;
    }
    /* Main Container */
    /* Center homepage */
[data-testid="stAppViewContainer"]{
    display:flex;
    justify-content:center;
    align-items:center;
    min-height:100vh;
    padding:20px;
}


/* Main homepage container */
[data-testid="stAppViewContainer"] .block-container{
    width:100%;
    max-width:1200px;


    background:
    rgba(15,23,42,0.78);


    border:
    1px solid rgba(255,255,255,0.08);


    backdrop-filter:
    blur(18px);


    border-radius:30px;


    padding:50px;


    margin:auto;


    box-shadow:
    0 15px 45px rgba(0,0,0,0.40);
}


/* Responsive */
@media(max-width:768px){
    [data-testid="stAppViewContainer"] .block-container{
        max-width:95%;
        padding:25px;
        border-radius:24px;
    }
}
    /* Title */
    .title{
        text-align:center;
        font-size:68px;
        font-weight:800;
        background:linear-gradient(
            90deg,
            #60A5FA,
            #2563EB
        );
        -webkit-background-clip:text;
        -webkit-text-fill-color:transparent;
        text-shadow:
        0 0 25px rgba(59,130,246,0.20);
        letter-spacing:1px;
    }
    /* Subtitle */
    .subtitle{
        text-align:center;
        font-size:22px;
        color:#94A3B8;
        line-height:1.8;
    }
    /* Moving Text */
    .marquee-container{
        width:100%;
        overflow:hidden;
        white-space:nowrap;


        background:
        rgba(15,23,42,0.92);


        border:
        1px solid rgba(59,130,246,0.18);


        border-radius:18px;


        padding:16px;


        box-shadow:
        0 8px 30px rgba(0,0,0,0.30);
    }
    .marquee{
        display:inline-block;
    white-space:nowrap;


    color:#E2E8F0;
    font-size:22px;
    font-weight:700;


    padding-left:100%;


    animation:moveText 15s linear infinite;
    }
    @keyframes moveText{
        from{
        transform:translateX(0%);
    }
    to{
        transform:translateX(-100%);
    }
    }
    /* Cards */
    .card{
        background:
        linear-gradient(
            145deg,
            rgba(15,23,42,0.95),
            rgba(30,41,59,0.92)
        );


        backdrop-filter: blur(18px);


        border-radius:28px;


        padding:30px;


        text-align:center;


        color:#F8FAFC;


        border:
        1px solid rgba(255,255,255,0.08);


        box-shadow:
        0 12px 35px rgba(0,0,0,0.35);


        transition:all 0.4s ease;


        height:220px;
    }
    .card:hover{
        transform:
        translateY(-10px);
        border:
        1px solid rgba(59,130,246,0.35);
        box-shadow:
        0 12px 40px rgba(59,130,246,0.20);
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
    div.stButton > button{
        width:100%;
        height:58px;


        border:none;


        border-radius:18px;


        background:
        linear-gradient(
            135deg,
            #2563EB,
            #3B82F6
        );


        color:white;


        font-size:18px;
        font-weight:700;


        transition:all 0.3s ease;


        box-shadow:
        0 8px 25px rgba(37,99,235,0.30);
    }
    div.stButton > button:hover{
        transform:
        translateY(-3px);


        box-shadow:
        0 10px 35px rgba(37,99,235,0.40);


        background:
        linear-gradient(
            135deg,
            #1D4ED8,
            #2563EB
        );
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
            #0a0f1c,
            #111826,
            #161e2b
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
        color:#442ad4;
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
    /* Center content perfectly */
[data-testid="stAppViewContainer"]{
    display:flex;
    justify-content:center;
    align-items:center;
    min-height:100vh;
    padding:20px;
}
/* Container responsive */
.block-container{
    width:100%;
    max-width:500px;
    padding:0 !important;
    margin:auto !important;
}
/* Responsive mobile */
@media(max-width:768px){
    .block-container{
        max-width:95%;
    }
}
    /* Background */
    .stApp{
        background:
        linear-gradient(
            135deg,
            rgba(11,17,32,0.96),
            rgba(15,23,42,0.95),
            rgba(30,41,59,0.93)
        ),
        url("https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3");
        background-size:cover;
        background-position:center;
        background-repeat:no-repeat;
        background-attachment:fixed;
    }
    /* Glass Card */
    .card{
        background:
        rgba(15,23,42,0.88);
        border:
        1px solid rgba(255,255,255,0.08);
        backdrop-filter:
        blur(20px);
        border-radius:30px;
        padding:35px;
        box-shadow:
        0 15px 40px rgba(0,0,0,0.40);
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
        rgba(255,255,255,0.05)!important;
        border:
        1px solid rgba(255,255,255,0.08)!important;
        border-radius:16px!important;
        color:#F8FAFC!important;
        height:52px;
    }
    .stTextInput input:focus{
        border:
        1px solid #3B82F6!important;
        box-shadow:
        0 0 0 3px rgba(59,130,246,0.18)!important;
    }
    /* Buttons */
    div.stButton > button{
        width:100%;
        height:48px;
        border:none;
        border-radius:14px;
        background: #304abf
        color:white;
        font-size:17px;
        font-weight:600;
    }
    div.stButton > button:hover{
        background:#304abf
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
    /* Center content perfectly */
[data-testid="stAppViewContainer"]{
    display:flex;
    justify-content:center;
    align-items:center;
    min-height:100vh;
    padding:20px;
}
/* Container responsive */
.block-container{
    width:100%;
    max-width:500px;
    padding:0 !important;
    margin:auto !important;
}
/* Responsive mobile */
@media(max-width:768px){
    .block-container{
        max-width:95%;
    }
}
    /* Background */
    .stApp{
        background:
        linear-gradient(
            135deg,
            rgba(11,17,32,0.96),
            rgba(15,23,42,0.95),
            rgba(30,41,59,0.93)
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
        background:#304abf
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
        background: #304abf;
        color:white;
        font-size:17px;
        font-weight:bold;
        transition:0.3s;
        box-shadow:
        0 8px 20px rgba(147,51,234,0.35);
    }
    </style>
    """, unsafe_allow_html=True)