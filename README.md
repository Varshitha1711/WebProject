#  X-Ray Image Enhancement & Noise Removal

A **Streamlit-based Image Processing application** designed to enhance and denoise grayscale **X-ray images**.  

This project demonstrates key **image enhancement techniques** in the **spatial domain**, including **noise reduction**, **contrast enhancement**, and **edge sharpening**, commonly used in **medical imaging** workflows.  

---

## ⚙️ Core Features

###  Noise Removal
- Apply **Median**, **Gaussian**, and **Bilateral filters** to remove random noise.  
- Optional **noise simulation** (Gaussian, Salt & Pepper, Speckle) for testing filter effectiveness.  

###  Contrast Enhancement
- **Histogram Equalization** for global contrast improvement.  
- **CLAHE (Contrast Limited Adaptive Histogram Equalization)** for localized enhancement — ideal for X-rays.  

###  Detail & Edge Enhancement
- **Unsharp Masking** to bring out fine details and improve sharpness without over-enhancing noise.  

###  Preset Medical Enhancement
- One-click **Preset Enhancement** applies an optimized sequence:  
  **Bilateral Filter → CLAHE → Unsharp Mask**  
  This sequence enhances contrast and details while preserving diagnostic features.  

###  Interactive Comparison
- **Side-by-side image display** (Original, Noisy, Enhanced).  
- Supports **real-time adjustments** and **multi-filter combinations**.  

###  Downloadable Results
- Enhanced image can be downloaded instantly for further use or analysis.


##  Project Structure
xray-enhancement/
├── app_streamlit_xray.py       # Main Streamlit application
├── requirements.txt            # Required Python packages
└── README.md                   # Documentation


## 🚀 Getting Started

### 1️ Prerequisites
- Python 3.8+
- pip installed

---

### 2️ Clone the Repository

```bash
git clone <repository-url>
cd xray-enhancement
```

### 3 Install Dependencies
pip install -r requirements.txt

### 4️ Run the Application

streamlit run app_streamlit_xray.py

## Technical Details
### Technologies Used

### Backend

 Python – core image processing
 OpenCV – filtering, histogram equalization, contrast adjustment
 scikit-image – noise modeling and utilities
 Pillow – image I/O

### Frontend

 Streamlit – interactive UI and visualization
 Real-time side-by-side comparison of original and enhanced images
 Allows users to apply multiple filters sequentially or use a preset enhancement

### Image Processing Techniques

Noise Reduction – Median, Gaussian, Bilateral Filters
Contrast Enhancement – Histogram Equalization, CLAHE
Detail Enhancement – Unsharp Masking
Preset Enhancement – Bilateral → CLAHE → Unsharp Mask

## Key Features

Apply multiple filters to X-ray images sequentially or use a preset enhancement
Compare original, noisy, and enhanced images side-by-side
Download enhanced X-ray images
Visual enhancement without metrics, focused on clarity and detail

## Future Enhancements

Add quantitative metrics (PSNR, SSIM) for objective quality assessment
Support batch processing for multiple images
Add presets for different X-ray types and noise levels
Extend support to other medical imaging formats (CT, MRI)