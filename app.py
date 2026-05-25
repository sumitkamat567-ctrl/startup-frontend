import streamlit as st
import requests

st.set_page_config(
    page_title="Startup Success Predictor",
    page_icon="🚀",
    layout="centered"
)

# PREMIUM CSS
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}

.main-container {
    background: rgba(255,255,255,0.05);
    padding: 40px;
    border-radius: 28px;
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 0 40px rgba(0,0,0,0.4);
    margin-top: 30px;
}

.title {
    text-align: center;
    font-size: 52px;
    font-weight: 700;
    background: linear-gradient(to right, #00F5A0, #00D9F5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    color: #94A3B8;
    margin-bottom: 40px;
    font-size: 18px;
}

.stNumberInput label,
.stSelectbox label {
    color: white !important;
    font-weight: 500;
}

.stTextInput input,
.stNumberInput input {
    background-color: rgba(255,255,255,0.06) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
    padding: 12px !important;
}

div[data-baseweb="select"] > div {
    background-color: rgba(255,255,255,0.06) !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: white !important;
}

.stButton > button {
    width: 100%;
    height: 60px;
    border-radius: 18px;
    border: none;
    background: linear-gradient(90deg, #00F5A0, #00D9F5);
    color: #0F172A;
    font-size: 20px;
    font-weight: 700;
    transition: 0.3s ease;
    margin-top: 20px;
}

.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 25px rgba(0,245,160,0.5);
}

.result-success {
    padding: 20px;
    border-radius: 18px;
    background: rgba(0,255,140,0.1);
    border: 1px solid rgba(0,255,140,0.3);
    text-align: center;
    font-size: 28px;
    font-weight: 600;
    margin-top: 30px;
}

.result-fail {
    padding: 20px;
    border-radius: 18px;
    background: rgba(255,0,80,0.1);
    border: 1px solid rgba(255,0,80,0.3);
    text-align: center;
    font-size: 28px;
    font-weight: 600;
    margin-top: 30px;
}

</style>
""", unsafe_allow_html=True)

# MAIN CONTAINER
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.markdown(
    '<div class="title">🚀 Startup Success Predictor</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-powered startup success prediction system</div>',
    unsafe_allow_html=True
)

# INPUTS
amount_log = st.number_input("Funding Amount (log)", value=15.0)

col1, col2 = st.columns(2)

with col1:
    year = st.number_input("Year", value=2023)

with col2:
    month = st.number_input("Month", value=5)

num_investors = st.number_input("Number of Investors", value=3)

has_top_vc = st.selectbox(
    "Top VC Present?",
    [0, 1],
    format_func=lambda x: "Yes" if x == 1 else "No"
)

# CITY OPTIONS
city = st.selectbox(
    "Select City",
    [
        "Ahmedabad",
        "Bangalore",
        "Chennai",
        "Coimbatore",
        "Delhi",
        "Goa",
        "Gurgaon",
        "Hyderabad",
        "Indore",
        "Jaipur",
        "Kanpur",
        "Kochi",
        "Kolkata",
        "Mumbai",
        "Noida",
        "Pune",
        "Surat"
    ]
)

# SUBVERTICAL OPTIONS
subvertical = st.selectbox(
    "Select SubVertical",
    [
        "AI",
        "Analytics",
        "Automobile",
        "Beauty",
        "Cloud Computing",
        "Consumer Internet",
        "Content",
        "Delivery",
        "E-commerce",
        "EdTech",
        "Enterprise Software",
        "Fashion",
        "FinTech",
        "Fitness",
        "Food Delivery",
        "FoodTech",
        "Gaming",
        "HealthTech",
        "Hospitality",
        "Insurance",
        "IoT",
        "Logistics",
        "Marketplace",
        "Mobile",
        "Payments",
        "Real Estate",
        "Recruitment",
        "Ride Sharing",
        "Robotics",
        "SaaS",
        "Security",
        "Social Network",
        "Sports",
        "Technology",
        "Travel",
        "TravelTech"
    ]
)

# INDUSTRY OPTIONS
industry = st.selectbox(
    "Select Industry",
    [
        "Advertising",
        "Agriculture",
        "Automobile",
        "Banking",
        "Construction",
        "Consumer Goods",
        "E-commerce",
        "Education",
        "Electronics",
        "Energy",
        "Entertainment",
        "Fashion",
        "Finance",
        "Food",
        "Gaming",
        "Healthcare",
        "Hospitality",
        "Insurance",
        "IT Services",
        "Logistics",
        "Manufacturing",
        "Media",
        "Real Estate",
        "Retail",
        "Software",
        "Sports",
        "Technology",
        "Telecommunications",
        "Transportation",
        "Travel"
    ]
)

# PREDICT BUTTON
if st.button("Predict Startup Success"):

    with st.spinner("Analyzing startup ecosystem..."):

        url = "https://startup-api-v2.onrender.com/predict"

        params = {
            "amount_log": amount_log,
            "year": year,
            "month": month,
            "num_investors": num_investors,
            "has_top_vc": has_top_vc,
            "City": city,
            "SubVertical": subvertical,
            "Industry": industry
        }

        response = requests.post(url, params=params)

        result = response.json()

        if "prediction" in result:

            prediction = result["prediction"]

            if prediction == 1:
                st.markdown(
                    '<div class="result-success">✅ Startup Likely To SUCCEED</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    '<div class="result-fail">❌ Startup Likely To FAIL</div>',
                    unsafe_allow_html=True
                )

        else:
            st.error("Prediction failed.")
            st.write(result)

st.markdown('</div>', unsafe_allow_html=True)