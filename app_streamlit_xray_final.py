# app_streamlit_xray_enhanced_only.py
import streamlit as st
import numpy as np
import cv2
from PIL import Image
from io import BytesIO
from skimage.util import random_noise

# ---------------- Page config ----------------
st.set_page_config(page_title="X-ray Enhancer", layout="wide")
st.markdown("""
<style>
.reportview-container, .main {background-color: #0e1117;}
.stButton>button {background-color:#2563eb;color:white;}
.css-1d391kg {color: #e6eef8;}
.stImage img {border-radius: 6px;}
</style>
""", unsafe_allow_html=True)

st.title(" X-Ray Noise Removal & Enhancement")
st.markdown("Upload a grayscale X-ray, select filters, or use the improved preset for medical-grade enhancement.")

# ---------------- Utility functions ----------------
def normalize01(img):
    img = img.astype(np.float32)
    mn, mx = img.min(), img.max()
    return (img - mn) / (mx - mn + 1e-8)

def to_display_uint8(img_float):
    arr = (np.clip(img_float, 0, 1) * 255).astype(np.uint8)
    return Image.fromarray(arr)

def pil_bytes_from_array(img_pil):
    buf = BytesIO()
    if img_pil.mode != 'RGB':
        img_pil = img_pil.convert("RGB")
    img_pil.save(buf, format="PNG")
    return buf.getvalue()

# ---------------- Filters ----------------
def mean_filter(img):
    src = (img*255).astype(np.uint8)
    res = cv2.blur(src,(3,3))
    return normalize01(res)

def median_filter(img):
    src = (img*255).astype(np.uint8)
    res = cv2.medianBlur(src,3)
    return normalize01(res)

def gaussian_filter(img):
    src = (img*255).astype(np.uint8)
    res = cv2.GaussianBlur(src,(5,5),1)
    return normalize01(res)

def bilateral_filter(img):
    src = (img*255).astype(np.uint8)
    res = cv2.bilateralFilter(src,9,75,75)
    return normalize01(res)

def hist_eq(img):
    src = (img*255).astype(np.uint8)
    res = cv2.equalizeHist(src)
    return normalize01(res)

def clahe_filter(img):
    src = (img*255).astype(np.uint8)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    res = clahe.apply(src)
    return normalize01(res)

def unsharp_mask(img):
    src = (img*255).astype(np.uint8)
    blur = cv2.GaussianBlur(src,(5,5),1)
    sharp = cv2.addWeighted(src,1.5,blur,-0.5,0)
    return normalize01(sharp)

# ---------------- Noise demo ----------------
def add_noise(img, type_="Gaussian"):
    if type_=="Gaussian":
        return random_noise(img, mode='gaussian', var=0.01)
    elif type_=="Salt & Pepper":
        return random_noise(img, mode='s&p', amount=0.01)
    elif type_=="Speckle":
        return random_noise(img, mode='speckle', var=0.01)
    else:
        return img

# ---------------- Upload ----------------
uploaded = st.file_uploader("Upload grayscale X-ray (PNG/JPG)", type=['png','jpg','jpeg'])
use_sample = st.checkbox("Use sample X-ray", value=(uploaded is None))

if use_sample and uploaded is None:
    img_orig = np.tile(np.linspace(0,255,512).astype(np.uint8),(512,1))
else:
    if uploaded is None:
        st.stop()
    img_cv = np.array(Image.open(uploaded).convert("L"))
    img_orig = cv2.resize(img_cv,(512,512))

img_f = normalize01(img_orig)

# ---------------- Sidebar options ----------------
st.sidebar.header("Settings")
mode = st.sidebar.radio("Mode", ["Without Noise","With Noise Demo"])
noise_type = st.sidebar.selectbox("Add Noise (demo only)", ["None","Gaussian","Salt & Pepper","Speckle"])

st.sidebar.subheader("Filters (select multiple or use preset)")
use_preset = st.sidebar.checkbox("Use Improved Preset Enhancement")

if not use_preset:
    do_mean = st.sidebar.checkbox("Mean Filter")
    do_median = st.sidebar.checkbox("Median Filter")
    do_gauss = st.sidebar.checkbox("Gaussian Filter")
    do_bilateral = st.sidebar.checkbox("Bilateral Filter")
    do_hist = st.sidebar.checkbox("Histogram Equalization")
    do_clahe = st.sidebar.checkbox("CLAHE (Adaptive Hist Eq)")
    do_unsharp = st.sidebar.checkbox("Unsharp Mask")
else:
    # Preset sequence: Bilateral -> CLAHE -> Unsharp Mask
    do_mean = do_median = do_gauss = False
    do_bilateral = False
    do_clahe = True
    do_unsharp = True
    do_hist = False

run = st.sidebar.button("Apply Filters")
download_name = st.sidebar.text_input("Download filename", value="enhanced_xray.png")

# ---------------- Processing ----------------
if mode=="With Noise Demo":
    noisy_img = add_noise(img_f, noise_type)
else:
    noisy_img = img_f.copy()

processed = noisy_img.copy()

if run:
    if do_mean: processed = mean_filter(processed)
    if do_median: processed = median_filter(processed)
    if do_gauss: processed = gaussian_filter(processed)
    if do_bilateral: processed = bilateral_filter(processed)
    if do_hist: processed = hist_eq(processed)
    if do_clahe: processed = clahe_filter(processed)
    if do_unsharp: processed = unsharp_mask(processed)
    st.success("Filters applied successfully!")

# ---------------- Display ----------------
cols = st.columns(3 if mode=="With Noise Demo" else 2)
cols[0].image(to_display_uint8(img_f), caption="Original", use_container_width=True)
if mode=="With Noise Demo":
    cols[1].image(to_display_uint8(noisy_img), caption=f"Noisy ({noise_type})", use_container_width=True)
    cols[2].image(to_display_uint8(processed), caption="Processed", use_container_width=True)
else:
    cols[1].image(to_display_uint8(processed), caption="Processed", use_container_width=True)

# ---------------- Download ----------------
buf = pil_bytes_from_array(to_display_uint8(processed))
st.download_button("Download Enhanced Image", data=buf, file_name=download_name, mime="image/png")
