import streamlit as st
import phonenumbers
from phonenumbers import geocoder
import pycountry
import emoji

# ---------- CUSTOM STYLE ----------
st.markdown("""
<style>
.main {
    background: linear-gradient(to right, #4facfe, #00f2fe);
}

/* Big title */
.big-title {
    font-size: 48px;
    font-weight: bold;
    color: white;
}

/* Subtitle */
.subtitle {
    font-size: 20px;
    color: white;
    margin-bottom: 20px;
}

/* Button style */
div.stButton > button {
    background-color: white;
    color: #007BFF;
    font-size: 18px;
    border-radius: 10px;
    padding: 10px 24px;
}
</style>
""", unsafe_allow_html=True)

  

# ------------------ TITLE ------------------
st.title("📱 Phone Number Country Detector")

# ------------------ INPUT ------------------
number = st.text_input("Enter phone number with country code (e.g., +254...)")

# ------------------ FLAG FUNCTION ------------------
def get_flag(country_code):
    try:
        country = pycountry.countries.get(alpha_2=country_code)
        if country:
            return emoji.emojize(f":flag_{country.alpha_2.lower()}:")
    except:
        return ""
    return ""

# ------------------ COUNTRY DATA ------------------
country_data = {
    "KE": {
        "providers": ["Safaricom", "Airtel Kenya", "Telkom Kenya"],
        "mobile_money": ["M-Pesa", "Airtel Money"]
    },
    "SE": {
        "providers": ["Telia", "Tele2", "Telenor"],
        "mobile_money": []
    },
    "CD": {
        "providers": ["Vodacom", "Airtel DRC", "Orange"],
        "mobile_money": ["M-Pesa", "Airtel Money", "Orange Money"]
    }
}

# ------------------ BUTTON ACTION ------------------
if st.button("🔍 Detect Country"):
    if not number:
        st.warning("Please enter a phone number first.")
    else:
        try:
            parsed = phonenumbers.parse(number)
            country = geocoder.description_for_number(parsed, "en")
            country_code = phonenumbers.region_code_for_number(parsed)

            if not country:
                st.warning("Country not found. Check the number format.")
            else:
                flag = get_flag(country_code)

                # 🎉 SUCCESS + BALLOONS
                st.success(f"🌍 This number is from: {country} {flag}")
                st.balloons()

                # 📡 PROVIDERS
                if country_code in country_data:
                    data = country_data[country_code]

                    st.subheader("📡 Network Providers")
                    for p in data["providers"]:
                        st.write(f"- {p}")

                    # 💰 MOBILE MONEY
                    st.subheader("💰 Mobile Money")
                    if data["mobile_money"]:
                        for m in data["mobile_money"]:
                            st.write(f"- {m}")
                    else:
                        st.write("No major mobile money services")

                else:
                    st.info("No additional data available for this country yet.")

        except:
            st.error("❌ Invalid phone number. Use format like +254...")