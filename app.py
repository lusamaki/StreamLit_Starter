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
# not yet working ( flag emojis are not being shown)

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
} # service providers and mobile money for some test countries
# we can input more data manually as we test more countries 
# and see what providers and mobile money services they have
# later install a package that has this data for all countries but for now we will just use these few as examples

# ------------------ BUTTON ACTION ------------------
if st.button("🔍 Detect Country"):
    if not number:# if the input field is empty
        st.warning("Please enter a phone number first.")
    else:
        try:#
            parsed = phonenumbers.parse(number)# parse the number using phonenumbers library
            country = geocoder.description_for_number(parsed, "en")# get the country name from the parsed number
            country_code = phonenumbers.region_code_for_number(parsed)# get the country code (e.g., KE for Kenya) from the parsed number

            if not country:# if the country name is not found, show a warning
                st.warning("Country not found. Check the number format.")
            else:
                flag = get_flag(country_code)

                # 🎉 SUCCESS + BALLOONS
                st.success(f"🌍 This number is from: {country} {flag}")#output country name.
                st.balloons()# show balloons animation on success

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

        except:# if there is an error in parsing the number (e.g., invalid format), show an error message
            st.error("❌ Invalid phone number. Use format like +254...")