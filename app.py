import streamlit as st
from PIL import Image
from image_analysis import analyze_image
from utils.roi_calculator import calculate_roi

st.set_page_config(page_title="Solar Rooftop Analyzer", layout="centered")
st.title("☀️ Solar Rooftop Analysis Tool")
st.markdown("Upload a rooftop image to get solar panel recommendations and ROI.")

uploaded_image = st.file_uploader("Upload Satellite Rooftop Image", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    image = Image.open(uploaded_image).convert("RGB")
    st.image(image, caption="Uploaded Rooftop", use_column_width=True)

    st.write("Analyzing rooftop...")

    try:
        # 1. Analyze the image (area, usable area, panel count)
        rooftop_data = analyze_image(image)

        st.subheader("📊 Rooftop Analysis Summary")
        st.write(f"**Estimated Rooftop Area:** {rooftop_data['area_m2']} m²")
        st.write(f"**Estimated Usable Area:** {rooftop_data['usable_area_m2']} m²")
        st.write(f"**Estimated Panel Count:** {rooftop_data['panel_count']} panels")

        # 2. Calculate ROI
        roi_data = calculate_roi(rooftop_data['panel_count'])

        st.subheader("💰 ROI & Cost Estimate")
        st.write(f"**Total Installation Cost:** ₹{roi_data['installation_cost']:,}")
        st.write(f"**Estimated Annual Generation:** {roi_data['annual_generation']} kWh")
        st.write(f"**Estimated Annual Savings:** ₹{roi_data['annual_savings']:,}")
        st.write(f"**Estimated Payback Period:** {roi_data['payback_years']} years")

    except Exception as e:
        st.error(f"Something went wrong: {e}")
