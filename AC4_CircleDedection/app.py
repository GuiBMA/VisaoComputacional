# Circle Detection Streamlit App – Shape Number Pipeline
import cv2
import numpy as np
import streamlit as st
from PIL import Image

def load_image(uploaded_file):
    """Convert the uploaded file to an OpenCV BGR ndarray."""
    img = Image.open(uploaded_file).convert("RGB")
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def detect_circles_hough(gray: np.ndarray, *, dp: float, min_dist: int,
                           param1: int, param2: int, min_r: int, max_r: int):
    """Standard Hough-Gradient detection."""
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=dp, minDist=min_dist,
                               param1=param1, param2=param2,
                               minRadius=min_r, maxRadius=max_r)
    return [] if circles is None else np.round(circles[0]).astype(int)

def detect_circles_contours(mask: np.ndarray, *, circ_thresh: float):
    """Contour based circle detection using circularity (shape number)."""
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    out = []
    for cnt in cnts:
        peri = cv2.arcLength(cnt, True)
        if peri == 0:
            continue
        area = cv2.contourArea(cnt)
        circularity = 4 * np.pi * area / (peri ** 2)  # shape number metric
        if circularity >= circ_thresh:
            (x, y), r = cv2.minEnclosingCircle(cnt)
            out.append((int(x), int(y), int(r)))
    return out

# Streamlit Front‑End
st.set_page_config(page_title="Circle Detection", layout="wide")
st.title("Circle Detection - Shape Number Pipeline")

uploaded = st.file_uploader("Upload image", type=["jpg", "jpeg", "png", "bmp"])
mode = st.sidebar.selectbox("Detection mode", ("Hough Transform", "Binary Mask (Shape Number)"))

if uploaded:
    bgr = load_image(uploaded)
    disp = bgr.copy()
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

    if mode == "Hough Transform":
        st.sidebar.markdown("### Hough Parameters")
        dp = st.sidebar.slider("dp (inv. accumulator ratio)", 1.0, 3.0, 1.2, 0.1)
        min_dist = st.sidebar.slider("minDist (px)", 10, 500, 30, 5)
        p1 = st.sidebar.slider("Canny param1", 50, 300, 100, 5)
        p2 = st.sidebar.slider("Accumulator param2", 10, 300, 30, 5)
        r_min = st.sidebar.slider("minRadius", 0, 500, 0, 1)
        r_max = st.sidebar.slider("maxRadius", 0, 1000, 0, 1)

        circles = detect_circles_hough(gray, dp=dp, min_dist=min_dist,
                                        param1=p1, param2=p2,
                                        min_r=r_min, max_r=r_max)
    else:
        st.sidebar.markdown("### Binary Mask Parameters")
        thresh_val = st.sidebar.slider("Threshold (0 for Otsu)", 0, 255, 0, 1)
        circ_thr = st.sidebar.slider("Circularity threshold", 0.0, 1.0, 0.80, 0.01)

        if thresh_val == 0:
            _, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        else:
            _, mask = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY_INV)

        circles = detect_circles_contours(mask, circ_thresh=circ_thr)
        with st.expander("Binary mask preview"):
            st.image(mask, clamp=True, channels="GRAY")

    for idx, (x, y, r) in enumerate(circles, 1):
        cv2.circle(disp, (x, y), r, (0, 255, 0), 2)
        cv2.circle(disp, (x, y), 2, (0, 0, 255), 3)
        cv2.putText(disp, str(idx), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (255, 0, 0), 2, cv2.LINE_AA)

    st.subheader(f"Detected circles: {len(circles)}")
    st.image(cv2.cvtColor(disp, cv2.COLOR_BGR2RGB), use_column_width=True)

    # Export results
    with st.expander("Download results"):
        if st.button("Download annotated image"):
            success, encoded_img = cv2.imencode(".png", disp)
            if success:
                st.download_button("Download PNG", encoded_img.tobytes(), file_name="circles.png")
