import streamlit as st

# Set page configuration
st.set_page_config(page_title="Ziqi Gao - Master's Student at UW", page_icon="🎓", layout="wide")

# Use columns to create a more engaging layout
col1, col2 = st.columns([1, 3])

# In the smaller column, add personal image and contact information in the sidebar style
with col1:
    st.image("img/ziqi.jpg", caption="Ziqi Gao", width=200)
    st.header("Contact Information 📬")
    st.write("Email: gzq@uw.edu")
    st.write("LinkedIn: [Ziqi Gao LinkedIn Page](https://www.linkedin.com/in/ziqi-gao-b86493297/)")
    st.write("GitHub: [Ziqi Gao's GitHub](https://github.com/uwGZQ)")

# In the larger column, add the main content
with col2:
    st.title("Ziqi Gao's Self-Introduction 🌟")

    # Basic Information
    st.header("Basic Information 📖")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Name")
        st.write("Ziqi Gao")
        st.subheader("Position")
        st.write("Master's Student in Data Science at Tsinghua University and Technology Innovation at University of Washington") 
    with col2:
        st.subheader("Location")
        st.write("Seattle, WA, United States")
    
    # Education Background
    st.header("Education Background 🏫")
    edu_data = [
        # {"Degree": "Bachelor's", "Major": "Computer Science and Technology", "Institution": "BUPT", "Year": "2018-2022"},
        {"Degree": "Master's", "Major": "Data Science and Information Technology", "Institution": "Tsinghua University", "Year": "2022-present"},
        {"Degree": "Master's", "Major": "Technology Innovation (Robotics)", "Institution": "University of Washington", "Year": "2023-present"},
    ]
    st.table(edu_data)

    # Research Directions
    st.header("Research Directions 🔍")
    st.markdown("""
    - **Research Area 1**: Multi-modal machine learning 🧠
    - **Research Area 2**: Human-Computer Interaction 👨‍💻
    - **Research Area 3**: Computer Vision 👁
    """)

    # Projects
    st.header("Research Projects 💼")
    projects = [
        "MMTSA: [\[Paper\]](https://ubicomplab.cs.washington.edu/pdfs/mmtsa.pdf) [\[GitHub\]](https://github.com/THU-CS-PI-LAB/MMTSA) - This paper proposes an efficient multimodal neural architecture for HAR using an RGB camera and IMUs called Multimodal Temporal Segment Attention Network (MMTSA).",
        "Eye gaze-enhanced Human activity Recognition: - This project aims to improve the accuracy of human activity recognition by incorporating eye gaze information.",
    ]
    for project in projects:
        st.markdown(f"- {project}")

    # Hobbies and Interests
    st.header("Hobbies and Interests 🎈")
    col1, col2 = st.columns(2)
    with col1:
        st.header("Hobbies")
        st.markdown("""
        - Basketball 🏀
        - Music 🎵
        - Chess ♟️       
        """)
    with col2:
        st.header("Interests")
        st.markdown("""
        - Poetry 📝
        - Traveling ✈️
        - R&B 🎶
        """)