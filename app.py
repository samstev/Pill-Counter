import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("🧮 Thyronorm Tablet Counter")

uploaded_file = st.file_uploader("📷 Upload image of tablets in ziplock (top view)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(image)

    st.image(image, caption="Uploaded Image", use_column_width=True)

    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    # Adaptive threshold (better than edge detection for your lighting)
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY_INV, 11, 2
    )

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    tablet_contours = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 300 < area < 2000:  # Adjust based on tablet size in your photos
            perimeter = cv2.arcLength(cnt, True)
            circularity = 4 * np.pi * (area / (perimeter ** 2)) if perimeter != 0 else 0
            if circularity > 0.7:  # Closer to 1 = more circular
                tablet_contours.append(cnt)

    output = img_np.copy()
    cv2.drawContours(output, tablet_contours, -1, (0, 255, 0), 2)

    count = len(tablet_contours)
    st.image(output, caption=f"Detected {count} tablets", use_column_width=True)
    st.success(f"✅ Total tablets counted: {count}")
