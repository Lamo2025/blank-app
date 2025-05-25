import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time


# Seitenkonfiguration
st.set_page_config(
    page_title="KI-Cockpit - Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS für das Dashboard
def load_css():
    st.markdown("""
    <style>
    /* Hauptfarben */
    :root {
        --primary-color: #0d6efd;
        --secondary-color: #6c757d;
        --success-color: #28a745;
        --info-color: #17a2b8;
        --warning-color: #ffc107;
        --danger-color: #dc3545;
        --light-color: #f8f9fa;
        --dark-color: #343a40;
    }
    
    /* Tab-Farben */
    .dashboard-tab { background-color: #e9f7ef; border-color: #a6d7b5; }
    .tickets-tab { background-color: #e7f3fe; border-color: #a3cbfd; }
    .ki-agent-tab { background-color: #fff4e6; border-color: #ffdcb0; }
    .skill-tree-tab { background-color: #f4eefe; border-color: #d8c0fd; }
    .prognose-tab { background-color: #e6fafa; border-color: #a0e5e5; }
    .profil-tab { background-color: #feeff5; border-color: #fdb0d0; }
    
    /* Allgemeine Styles */
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #0d6efd;
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        color: #343a40;
    }
    
    .card {
        background-color: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: bold;
        color: #0d6efd;
    }
    
    .stat-label {
        font-size: 1rem;
        color: #6c757d;
    }
    
    /* Navigation Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        border-radius: 5px 5px 0px 0px;
        padding: 10px 16px;
        font-weight: 500;
    }
    
    /* Level-Anzeige */
    .level-circle {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background-color: #0d6efd;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        font-weight: bold;
        margin-right: 1rem;
    }
    
    /* Skill-Badges */
    .skill-badge {
        background-color: #ff9800;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    
    /* Chat-Nachrichten */
    .chat-message {
        padding: 0.5rem 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        max-width: 80%;
    }
    
    .agent-message {
        background-color: #f1f3f4;
        margin-right: auto;
    }
    
    .user-message {
        background-color: #d1e7ff;
        margin-left: auto;
    }
    
    .message-time {
        font-size: 0.8rem;
        color: #6c757d;
        margin-top: 0.2rem;
    }
    
    /* Ranking */
    .rank-circle {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 1rem;
    }
    
    .rank-1 { background-color: #0d6efd; color: white; }
    .rank-2 { background-color: #6c757d; color: white; }
    .rank-3 { background-color: #cd7f32; color: white; }
    .rank-4, .rank-5 { background-color: #e9ecef; color: #343a40; }
    
    /* Glücks-Bubble */
    .bubble-challenge {
        background-color: #ff9800;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    /* Shop Performance */
    .performance-bar {
        height: 20px;
        border-radius: 10px;
        margin-bottom: 0.5rem;
    }
    
    /* Buttons */
    .primary-button {
        background-color: #0d6efd;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        cursor: pointer;
    }
    
    .secondary-button {
        background-color: #6c757d;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        cursor: pointer;
    }
    
    .warning-button {
        background-color: #ffc107;
        color: #343a40;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        cursor: pointer;
    }
    
    .danger-button {
        background-color: #dc3545;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        cursor: pointer;
    }
    
    /* Verstecke Streamlit-Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Beispieldaten
def load_sample_data():
    # Benutzerfortschritt
    user_progress = {
        "level": 7,
        "level_title": "Verkaufsprofi",
        "current_points": 1250,
        "total_points": 1500,
        "skills": [
            {"name": "Smartphone-Experte", "icon": "📱"},
            {"name": "DSL-Spezialist", "icon": "📶"},
            {"name": "Wertgarantie-Profi", "icon": "🛡️"},
            {"name": "Kundendienst-Ass", "icon": "🎧"}
        ]
    }
    
    # Umsatzdaten
    revenue = {
        "total": 12450,
        "personal": 3250,
        "dsl": 1850,
        "warranty": 950
    }
    
    # Umsatzverlauf für das Diagramm
    revenue_history = [
        {"month": "Jan", "total": 8300, "personal": 2100},
        {"month": "Feb", "total": 9000, "personal": 2300},
        {"month": "Mär", "total": 10300, "personal": 2800},
        {"month": "Apr", "total": 11200, "personal": 3000},
        {"month": "Mai", "total": 11900, "personal": 3200},
        {"month": "Jun", "total": 12450, "personal": 3250}
    ]
    
    # Shop Performance
    shop_performance = [
        {"name": "Shop Berlin", "performance": 85, "color": "#5c6bc0"},
        {"name": "Shop Hamburg", "performance": 75, "color": "#26a69a"},
        {"name": "Shop München", "performance": 90, "color": "#ef5350"},
        {"name": "Shop Köln", "performance": 65, "color": "#8e24aa"}
    ]
    
    # KI-Agent Chat
    agent_chat = {
        "id": "sales-chat-1",
        "messages": [
            {
                "role": "agent",
                "content": "Hallo Max! Ich habe heute 3 neue Verkaufschancen für dich identifiziert. Wie kann ich dir helfen?",
                "timestamp": "Heute, 09:30"
            },
            {
                "role": "user",
                "content": "Zeige mir die wichtigste Chance",
                "timestamp": "Heute, 09:31"
            },
            {
                "role": "agent",
                "content": "Die wichtigste Chance ist ein Vodafone Red L Vertrag für Herrn Schmidt. Er hat seinen aktuellen Vertrag seit 24 Monaten und zahlt derzeit 39,99€ monatlich. Mit dem neuen Angebot könnten wir ihm mehr Datenvolumen für den gleichen Preis anbieten. Die Wahrscheinlichkeit für einen erfolgreichen Abschluss liegt bei 85%.",
                "timestamp": "Heute, 09:31"
            }
        ]
    }
    
    # Mitarbeiter Ranking
    ranking = [
        {"rank": 1, "name": "Max Mustermann", "points": 1250, "is_current_user": True},
        {"rank": 2, "name": "Anna Schmidt", "points": 1180, "is_current_user": False},
        {"rank": 3, "name": "Thomas Weber", "points": 1050, "is_current_user": False},
        {"rank": 4, "name": "Lisa Müller", "points": 920, "is_current_user": False},
        {"rank": 5, "name": "Michael Fischer", "points": 850, "is_current_user": False}
    ]
    
    # Glücks-Bubble Challenge
    bubble_challenge = {
        "current_clicks": 1,
        "required_clicks": 5,
        "reward": 50
    }
    
    return {
        "user_progress": user_progress,
        "revenue": revenue,
        "revenue_history": revenue_history,
        "shop_performance": shop_performance,
        "agent_chat": agent_chat,
        "ranking": ranking,
        "bubble_challenge": bubble_challenge
    }

# Formatierungsfunktionen
def format_revenue(value):
    return f"{value:,.0f} €".replace(",", ".")

def format_percent(value):
    return f"{value}%"

# Navigation
def render_navigation():
    st.markdown('<div style="display: flex; justify-content: space-between; margin-bottom: 20px;">', unsafe_allow_html=True)
    
    # Logo und Titel
    st.markdown('<h1 class="main-header">KI-Cockpit</h1>', unsafe_allow_html=True)
    
    # Benutzer-Avatar
    st.markdown('<div style="display: flex; align-items: center;">'
                '<div style="width: 40px; height: 40px; border-radius: 50%; background-color: #0d6efd; color: white; '
                'display: flex; align-items: center; justify-content: center; margin-right: 10px;">M</div>'
                '<span>Max Mustermann</span>'
                '</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tabs
    tabs = st.tabs([
        "📊 Dashboard", 
        "🎫 Tickets", 
        "🤖 KI-Agent", 
        "🧩 Skill Tree", 
        "📈 Prognose", 
        "👤 Profil"
    ])
    
    return tabs

# Fortschrittsanzeige
def render_progress_section(data):
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header">🏆 Mein Fortschritt</h2>', unsafe_allow_html=True)
        
        # Level und Punkte
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown(f'<div class="level-circle">{data["user_progress"]["level"]}</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'<h3>Level {data["user_progress"]["level"]}: {data["user_progress"]["level_title"]}</h3>', unsafe_allow_html=True)
            st.markdown(f'{data["user_progress"]["current_points"]} von {data["user_progress"]["total_points"]} Punkten', unsafe_allow_html=True)
            
            # Fortschrittsbalken
            progress_value = data["user_progress"]["current_points"] / data["user_progress"]["total_points"]
            st.progress(progress_value)
            
            st.markdown(f'<div style="display: flex; justify-content: space-between;">'
                      f'<span>{data["user_progress"]["current_points"]} Punkte</span>'
                      f'<span>{data["user_progress"]["total_points"]} Punkte</span>'
                      f'</div>', unsafe_allow_html=True)
        
        # Skills
        for skill in data["user_progress"]["skills"]:
            st.markdown(f'<div class="skill-badge">{skill["icon"]} {skill["name"]}</div>', unsafe_allow_html=True)
        
        # Buttons
        col1, col2 = st.columns(2)
        with col1:
            st.button("Punkte einlösen", key="redeem_points", use_container_width=True)
        with col2:
            st.button("Gratis Punkte sichern", key="free_points", use_container_width=True, type="primary")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Umsatz-Übersicht
def render_revenue_section(data):
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header">💶 Umsatz-Übersicht</h2>', unsafe_allow_html=True)
        
        # Filter-Buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.button("Alle Shops", key="all_shops", use_container_width=True, type="primary")
        with col2:
            st.button("Einzelner Shop", key="single_shop", use_container_width=True)
        with col3:
            st.button("Mitarbeiter-Umsatz", key="employee_revenue", use_container_width=True)
        
        # Statistik-Karten
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'<div class="stat-value">{format_revenue(data["revenue"]["total"])}</div>', unsafe_allow_html=True)
            st.markdown('<div class="stat-label">Gesamtumsatz</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'<div class="stat-value">{format_revenue(data["revenue"]["personal"])}</div>', unsafe_allow_html=True)
            st.markdown('<div class="stat-label">Mein Umsatz</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'<div class="stat-value">{format_revenue(data["revenue"]["dsl"])}</div>', unsafe_allow_html=True)
            st.markdown('<div class="stat-label">DSL</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'<div class="stat-value">{format_revenue(data["revenue"]["warranty"])}</div>', unsafe_allow_html=True)
            st.markdown('<div class="stat-label">Wertgarantie</div>', unsafe_allow_html=True)
        
        # Umsatzdiagramm
        df_revenue = pd.DataFrame(data["revenue_history"])
        
        fig = px.line(df_revenue, x="month", y=["total", "personal"], 
                     labels={"value": "Umsatz (€)", "variable": "Kategorie"},
                     color_discrete_map={"total": "#0d6efd", "personal": "#ff9800"})
        
        fig.update_layout(
            legend_title_text="",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=0, r=0, t=30, b=0),
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Shop Performance
def render_shop_performance(data):
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header">🏪 Shop Performance</h2>', unsafe_allow_html=True)
        
        for shop in data["shop_performance"]:
            col1, col2, col3 = st.columns([2, 8, 1])
            
            with col1:
                st.markdown(f'<div>{shop["name"]}</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown(f'<div style="background-color: #f1f3f4; border-radius: 10px; height: 20px; width: 100%;">'
                          f'<div style="background-color: {shop["color"]}; border-radius: 10px; height: 20px; width: {shop["performance"]}%"></div>'
                          f'</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown(f'<div>{format_percent(shop["performance"])}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Glücks-Bubble Challenge
def render_bubble_challenge(data):
    with st.container():
        st.markdown('<div class="bubble-challenge">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 5])
        
        with col1:
            st.markdown('🎁', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<h3>Glücks-Bubble Challenge</h3>', unsafe_allow_html=True)
            st.markdown(f'Klicke 5x und sichere dir Punkte! ({data["bubble_challenge"]["current_clicks"]}/{data["bubble_challenge"]["required_clicks"]})', unsafe_allow_html=True)
        
        if st.button("Klicken", key="bubble_click", use_container_width=True):
            st.session_state.bubble_clicks = st.session_state.get('bubble_clicks', 1) + 1
            if st.session_state.bubble_clicks >= 5:
                st.success(f"Glückwunsch! Du hast {data['bubble_challenge']['reward']} Punkte gewonnen!")
                st.session_state.bubble_clicks = 1
        
        st.markdown('</div>', unsafe_allow_html=True)

# KI-Agent Verkaufschancen
def render_agent_chat(data):
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header">🤖 KI-Agent Verkaufschancen</h2>', unsafe_allow_html=True)
        
        # Chat-Nachrichten
        for message in data["agent_chat"]["messages"]:
            if message["role"] == "agent":
                st.markdown(f'<div class="chat-message agent-message">'
                          f'{message["content"]}'
                          f'<div class="message-time">{message["timestamp"]}</div>'
                          f'</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message user-message">'
                          f'{message["content"]}'
                          f'<div class="message-time">{message["timestamp"]}</div>'
                          f'</div>', unsafe_allow_html=True)
        
        # Eingabefeld
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_input = st.text_input("", placeholder="Schreibe dem KI-Agenten...", key="agent_input")
        
        with col2:
            if st.button("Senden", key="send_message"):
                if user_input:
                    st.session_state.messages = st.session_state.get('messages', data["agent_chat"]["messages"]).copy()
                    
                    # Benutzernachricht hinzufügen
                    st.session_state.messages.append({
                        "role": "user",
                        "content": user_input,
                        "timestamp": "Jetzt"
                    })
                    
                    # Agenten-Antwort simulieren
                    time.sleep(1)
                    st.session_state.messages.append({
                        "role": "agent",
                        "content": f"Ich habe Ihre Anfrage '{user_input}' erhalten und werde sie bearbeiten.",
                        "timestamp": "Jetzt"
                    })
                    
                    st.experimental_rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# Mitarbeiter Ranking
def render_employee_ranking(data):
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-header">👥 Mitarbeiter Ranking</h2>', unsafe_allow_html=True)
        
        for employee in data["ranking"]:
            col1, col2, col3 = st.columns([1, 3, 2])
            
            with col1:
                st.markdown(f'<div class="rank-circle rank-{employee["rank"]}">{employee["rank"]}</div>', unsafe_allow_html=True)
            
            with col2:
                name_style = "font-weight: bold;" if employee["is_current_user"] else ""
                st.markdown(f'<div style="{name_style}">{employee["name"]}</div>'
                          f'<div>{employee["points"]} Punkte</div>', unsafe_allow_html=True)
            
            with col3:
                progress_value = employee["points"] / data["user_progress"]["total_points"]
                st.progress(progress_value)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Hauptfunktion
def main():
    # CSS laden
    load_css()
    
    # Beispieldaten laden
    data = load_sample_data()
    
    # Navigation rendern
    tabs = render_navigation()
    
    # Dashboard-Tab
    with tabs[0]:
        # Fortschrittsanzeige
        render_progress_section(data)
        
        # Umsatz-Übersicht
        render_revenue_section(data)
        
        # Shop Performance
        render_shop_performance(data)
        
        # Glücks-Bubble Challenge
        render_bubble_challenge(data)
        
        # KI-Agent Verkaufschancen
        render_agent_chat(data)
        
        # Mitarbeiter Ranking
        render_employee_ranking(data)
    
    # Andere Tabs (Platzhalter)
    with tabs[1]:
        st.info("Tickets-Bereich wird geladen...")
    
    with tabs[2]:
        st.info("KI-Agent-Bereich wird geladen...")
    
    with tabs[3]:
        st.info("Skill Tree-Bereich wird geladen...")
    
    with tabs[4]:
        st.info("Prognose-Bereich wird geladen...")
    
    with tabs[5]:
        st.info("Profil-Bereich wird geladen...")

if __name__ == "__main__":
    main()
