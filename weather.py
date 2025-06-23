import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import requests
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from io import BytesIO
import base64


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)


st.set_page_config(page_title="Weather Analytics Pro", layout="wide", page_icon="⛅")


st.markdown("""
<style>
    /* Main styles */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Sidebar styles */
    .css-1d391kg {
        background-color: #343a40 !important;
        color: white !important;
    }
    
    .sidebar .sidebar-content {
        background-color: #343a40;
    }
    
    
    .card {
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        transition: 0.3s;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        background-color: white;
    }
    
    .card:hover {
        box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
    }
    
  
    .stButton>button {
        border-radius: 20px;
        border: 1px solid #4CAF50;
        background-color: #4CAF50;
        color: white;
        padding: 8px 16px;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: white;
        color: #4CAF50;
    }
    
    
    h1 {
        color: #343a40;
        border-bottom: 2px solid #4CAF50;
        padding-bottom: 10px;
    }
    
    h2 {
        color: #495057;
    }
    
    
    .dataframe {
        border-radius: 10px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.1);
    }
    
    
    .weather-icon {
        font-size: 2rem;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    
    .tab {
        overflow: hidden;
        border: 1px solid #ccc;
        background-color: #f1f1f1;
        border-radius: 10px 10px 0 0;
    }
    
    .tab button {
        background-color: inherit;
        float: left;
        border: none;
        outline: none;
        cursor: pointer;
        padding: 14px 16px;
        transition: 0.3s;
    }
    
    .tab button:hover {
        background-color: #ddd;
    }
    
    .tab button.active {
        background-color: #4CAF50;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


API_KEY = "87965cbbca5d5d20e48a91321593c8b8"
BASE_URL = "https://home.openweathermap.org/api_keys"

sample_data = {
    'date': pd.date_range(start='2023-01-01', end='2023-12-31'),
    'temperature': np.random.randint(-5, 35, size=365),
    'humidity': np.random.randint(30, 90, size=365),
    'precipitation': np.random.uniform(0, 15, size=365).round(1),
    'wind_speed': np.random.uniform(0, 25, size=365).round(1)
}
sample_df = pd.DataFrame(sample_data)


def get_weather_icon(condition):
    icons = {
        'clear': '☀️',
        'clouds': '☁️',
        'rain': '🌧️',
        'snow': '❄️',
        'thunderstorm': '⛈️',
        'drizzle': '🌦️',
        'mist': '🌫️'
    }
    condition = condition.lower()
    for key in icons:
        if key in condition:
            return icons[key]
    return '🌈'


with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: white; margin-bottom: 5px;">⛅ Weather Analytics Pro</h1>
        <p style="color: #adb5bd;">Your comprehensive weather analysis solution</p>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.radio(
        "Navigation",
        ["🌤️ Real-time Weather", "📊 Historical Analysis", "🏙️ Compare Cities", "📈 Generate Report"],
        key="nav"
    )
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #adb5bd; margin-top: 30px;">
        <p>Powered by OpenWeatherMap API</p>
        <p>© 2023 Weather Analytics</p>
    </div>
    """, unsafe_allow_html=True)


def get_current_weather(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    return data


def send_email(subject, body, to_email):
    from_email = "your_email@example.com"
    password = "your_email_password"
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Error sending email: {e}")
        return False


if page == "🌤️ Real-time Weather":
    st.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <h1 style="margin: 0;">Real-time Weather Data</h1>
        <span class="weather-icon" style="margin-left: 15px;">⛅</span>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            city = st.text_input("Enter city name", "London", key="city_input")
            
            if st.button("Get Weather", key="get_weather"):
                with st.spinner('Fetching weather data...'):
                    weather_data = get_current_weather(city)
                    
                    if weather_data.get('cod') == 200:
                        st.success(f"Weather data fetched for {city}")
                        
                        
                        weather_icon = get_weather_icon(weather_data['weather'][0]['main'])
                        st.markdown(f"""
                        <div class="card" style="padding: 20px; text-align: center;">
                            <h2 style="margin-top: 0;">{city.title()}</h2>
                            <div style="font-size: 4rem; margin: 10px 0;">{weather_icon}</div>
                            <div style="font-size: 3rem; font-weight: bold; margin: 10px 0;">
                                {weather_data['main']['temp']}°C
                            </div>
                            <div style="color: #6c757d; margin-bottom: 10px;">
                                {weather_data['weather'][0]['description'].title()}
                            </div>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                                <div>
                                    <div style="font-size: 0.8rem; color: #6c757d;">Humidity</div>
                                    <div style="font-size: 1.2rem; font-weight: bold;">
                                        {weather_data['main']['humidity']}%
                                    </div>
                                </div>
                                <div>
                                    <div style="font-size: 0.8rem; color: #6c757d;">Wind Speed</div>
                                    <div style="font-size: 1.2rem; font-weight: bold;">
                                        {weather_data['wind']['speed']} m/s
                                    </div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Check for extreme conditions
                        if weather_data['main']['temp'] > 30:
                            st.warning("🔥 High temperature warning! Consider staying hydrated.")
                        elif weather_data['main']['temp'] < 0:
                            st.warning("❄️ Freezing temperature warning! Dress warmly.")
                    else:
                        st.error(f"Error: {weather_data.get('message', 'Unknown error')}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Weather Alerts")
            alert_email = st.text_input("Enter email for alerts", key="alert_email")
            alert_condition = st.selectbox("Alert me when", 
                                        ["Temperature > 30°C", "Temperature < 0°C", "High winds (>20 m/s)"],
                                        key="alert_condition")
            
            if st.button("Set Alert", key="set_alert") and alert_email:
                st.success(f"Weather alert set for {alert_condition} to {alert_email}")
            st.markdown('</div>', unsafe_allow_html=True)


elif page == "📊 Historical Analysis":
    st.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <h1 style="margin: 0;">Historical Weather Analysis</h1>
        <span class="weather-icon" style="margin-left: 15px;">📊</span>
    </div>
    """, unsafe_allow_html=True)
    
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload your weather data (CSV)", type=["csv"], key="data_upload")
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
        else:
            df = sample_df.copy()
            st.info("Using sample data. Upload your own CSV file for analysis.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    if not df.empty:
        
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            min_date = df['date'].min()
            max_date = df['date'].max()
            date_range = st.date_input("Select date range", [min_date, max_date], key="date_range")
            
            if len(date_range) == 2:
                filtered_df = df[(df['date'] >= pd.to_datetime(date_range[0])) & 
                                (df['date'] <= pd.to_datetime(date_range[1]))]
            else:
                filtered_df = df
            st.markdown('</div>', unsafe_allow_html=True)
        
        
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Data Visualization")
            
            tab1, tab2, tab3, tab4 = st.tabs(["Line Chart", "Bar Chart", "Heatmap", "Scatter Plot"])
            
            with tab1:
                fig = px.line(filtered_df, x='date', y='temperature', 
                             title='Temperature Over Time',
                             template='plotly_white')
                st.plotly_chart(fig, use_container_width=True)
                
            with tab2:
                monthly_data = filtered_df.groupby(filtered_df['date'].dt.month).mean()
                fig = px.bar(monthly_data, x=monthly_data.index, y='precipitation', 
                            title='Average Monthly Precipitation',
                            template='plotly_white')
                st.plotly_chart(fig, use_container_width=True)
                
            with tab3:
                numeric_df = filtered_df.select_dtypes(include=[np.number])
                corr = numeric_df.corr()
                fig = px.imshow(corr, text_auto=True, 
                               title='Correlation Heatmap',
                               template='plotly_white')
                st.plotly_chart(fig, use_container_width=True)
                
            with tab4:
                fig = px.scatter(filtered_df, x='temperature', y='humidity', 
                               title='Temperature vs Humidity',
                               template='plotly_white')
                st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Statistical Summary")
            st.dataframe(filtered_df.describe().style.background_gradient(cmap='Blues'))
            st.markdown('</div>', unsafe_allow_html=True)


elif page == "🏙️ Compare Cities":
    st.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <h1 style="margin: 0;">Compare Cities</h1>
        <span class="weather-icon" style="margin-left: 15px;">🏙️</span>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        cities = st.multiselect("Select cities to compare", 
                              ["London", "New York", "Tokyo", "Sydney", "Berlin", "Paris", "Moscow"],
                              default=["London", "New York"],
                              key="city_compare")
        
        if cities:
            weather_data = []
            for city in cities:
                with st.spinner(f'Fetching data for {city}...'):
                    data = get_current_weather(city)
                    if data.get('cod') == 200:
                        weather_data.append({
                            'city': city,
                            'temperature': data['main']['temp'],
                            'humidity': data['main']['humidity'],
                            'wind_speed': data['wind']['speed'],
                            'condition': data['weather'][0]['main'],
                            'icon': get_weather_icon(data['weather'][0]['main'])
                        })
            
            if weather_data:
                compare_df = pd.DataFrame(weather_data)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Current Weather Comparison")
                    # Display as styled table
                    st.dataframe(compare_df[['city', 'temperature', 'humidity', 'wind_speed']]
                                .style
                                .background_gradient(cmap='coolwarm', subset=['temperature'])
                                .background_gradient(cmap='Blues', subset=['humidity'])
                                .background_gradient(cmap='Greens', subset=['wind_speed']))
                
                with col2:
                    st.subheader("Visual Comparison")
                    tab1, tab2 = st.tabs(["Temperature", "Humidity & Wind"])
                    
                    with tab1:
                        fig = px.bar(compare_df, x='city', y='temperature', 
                                    color='temperature',
                                    title='Temperature Comparison (°C)',
                                    template='plotly_white')
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with tab2:
                        fig = px.bar(compare_df, x='city', y=['humidity', 'wind_speed'],
                                    barmode='group',
                                    title='Humidity (%) vs Wind Speed (m/s)',
                                    template='plotly_white')
                        st.plotly_chart(fig, use_container_width=True)
                
                
                st.subheader("Current Conditions")
                cols = st.columns(len(weather_data))
                for idx, city_data in enumerate(weather_data):
                    with cols[idx]:
                        st.markdown(f"""
                        <div style="text-align: center; padding: 10px; border-radius: 10px; 
                                  background-color: #f8f9fa; margin: 5px;">
                            <div style="font-size: 2rem;">{city_data['icon']}</div>
                            <div style="font-weight: bold;">{city_data['city']}</div>
                            <div>{city_data['condition']}</div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.error("Failed to fetch data for selected cities")
        st.markdown('</div>', unsafe_allow_html=True)


elif page == "📈 Generate Report":
    st.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <h1 style="margin: 0;">Weather Reports</h1>
        <span class="weather-icon" style="margin-left: 15px;">📈</span>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        report_type = st.selectbox("Select report type", 
                                 ["Daily Summary", "Monthly Summary", "Extreme Events"],
                                 key="report_type")
        
        if report_type == "Daily Summary":
            st.subheader("Daily Weather Report")
            st.write("This report shows daily weather statistics.")
            
          
            report_df = sample_df.groupby(sample_df['date'].dt.date).agg({
                'temperature': ['mean', 'max', 'min'],
                'humidity': 'mean',
                'precipitation': 'sum'
            })
            st.dataframe(report_df.style.background_gradient(cmap='YlOrRd', subset=[('temperature', 'mean')]))
            
        elif report_type == "Monthly Summary":
            st.subheader("Monthly Weather Report")
            
            
            report_df = sample_df.groupby(sample_df['date'].dt.month_name()).agg({
                'temperature': ['mean', 'max', 'min'],
                'humidity': 'mean',
                'precipitation': 'sum'
            })
            st.dataframe(report_df.style.background_gradient(cmap='YlOrRd', subset=[('temperature', 'mean')]))
            
            
            col1, col2 = st.columns(2)
            with col1:
                fig1 = px.line(report_df['temperature']['mean'], 
                             title='Average Monthly Temperature',
                             template='plotly_white')
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                fig2 = px.bar(report_df['precipitation']['sum'], 
                             title='Total Monthly Precipitation',
                             template='plotly_white')
                st.plotly_chart(fig2, use_container_width=True)
        
        elif report_type == "Extreme Events":
            st.subheader("Extreme Weather Events")
            
            
            high_temp = sample_df[sample_df['temperature'] > 30]
            low_temp = sample_df[sample_df['temperature'] < 0]
            high_precip = sample_df[sample_df['precipitation'] > 10]
            
            tab1, tab2, tab3 = st.tabs(["High Temp", "Low Temp", "High Precipitation"])
            
            with tab1:
                st.write("Days with temperature > 30°C:")
                st.dataframe(high_temp.style.applymap(lambda x: 'background-color: #ffcccc' if x > 30 else ''))
            
            with tab2:
                st.write("Days with temperature < 0°C:")
                st.dataframe(low_temp.style.applymap(lambda x: 'background-color: #ccccff' if x < 0 else ''))
            
            with tab3:
                st.write("Days with precipitation > 10mm:")
                st.dataframe(high_precip.style.applymap(lambda x: 'background-color: #ccffcc' if x > 10 else ''))
        
        
        st.markdown("---")
        st.subheader("Export Report")
        
        if st.button("Download Report as CSV", key="download_csv"):
            csv = sample_df.to_csv(index=False)
            st.download_button(
                label="Click to download",
                data=csv,
                file_name='weather_report.csv',
                mime='text/csv',
                key="download_button"
            )
        
        if st.button("Generate PDF Report", key="generate_pdf"):
            st.warning("PDF generation would require additional libraries like reportlab or weasyprint")
        st.markdown('</div>', unsafe_allow_html=True)


st.markdown("""
<div style="text-align: center; margin-top: 50px; color: #6c757d; font-size: 0.9rem;">
    <p>Weather Analytics Pro - Making weather data understandable since 2023</p>
    <p>For support, contact: support@weatherapp.com</p>
</div>
""", unsafe_allow_html=True)