import streamlit as st
import cv2
import numpy as np
from PIL import Image
from datetime import datetime

st.title("📦 Thyronorm Tablet Counter - Ziplock Cover")

uploaded_file = st.file_uploader("📷 Upload a clear image of tablets in the ziplock cover", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)

    st.image(image, caption="Uploaded Image", use_column_width=True)

    st.subheader("🔍 Counting Tablets...")

    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    gray = cv2.medianBlur(gray, 5)

    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=20,
        param1=50,
        param2=30,
        minRadius=10,
        maxRadius=35
    )

    if circles is not None:
        circles = np.uint16(np.around(circles))
        count = len(circles[0])

        output_img = image_np.copy()

        for i in circles[0, :]:
            cv2.circle(output_img, (i[0], i[1]), i[2], (0, 255, 0), 2)
            cv2.circle(output_img, (i[0], i[1]), 2, (0, 0, 255), 3)

        st.image(output_img, caption=f"Detected {count} tablets", use_column_width=True)
        st.success(f"✅ Total Tablets Counted: {count}")

        if st.button("🖨️ Generate Dispensing Label"):
            now = datetime.now().strftime("%d-%m-%Y %I:%M %p")
            st.text_area("📋 Label Preview", 
                         f"THYRONORM DISPENSING LABEL\n"
                         f"Tablets Counted: {count}\n"
                         f"Date: {now}\n"
                         f"Packed by: ___________", height=120)
    else:
        st.error("⚠️ No tablets detected. Use clear photo, no glare or blur.")
