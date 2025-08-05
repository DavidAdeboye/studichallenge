import streamlit as st
import os
import tempfile
from dotenv import load_dotenv
from simple_ocr_processor import SimpleOCRProcessor
from ai_processor import AIProcessor

# Load environment variables
load_dotenv()

def main():
    st.set_page_config(
        page_title="Study Buddy - AI Exam Prep",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 Study Buddy - AI Exam Preparation")
    st.markdown("Upload your lecture notes and past exam questions to get AI-powered study insights!")
    
    # Initialize processors
    try:
        with st.spinner("Initializing OCR engine..."):
            ocr_processor = SimpleOCRProcessor()
            ai_processor = AIProcessor()
        
        # Display system information
        with st.expander("📋 System Information", expanded=False):
            st.write("**OCR Engine:** ImageMagick + Tesseract")
            st.info("💡 Using reliable ImageMagick preprocessing with Tesseract OCR for maximum accuracy.")
    
    except Exception as e:
        st.error(f"❌ Failed to initialize processors: {str(e)}")
        st.info("Please check that ImageMagick and Tesseract are installed and added to PATH.")
        return
    
    # Create two columns for file uploads
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Lecture Notes")
        lecture_notes = st.file_uploader(
            "Upload your lecture notes (PDF)",
            type=['pdf'],
            key="lecture_notes"
        )
    
    with col2:
        st.subheader("❓ Past Exam Questions")
        past_exams = st.file_uploader(
            "Upload past exam questions (PDF)",
            type=['pdf'],
            key="past_exams"
        )
    
    if st.button("🚀 Generate Study Materials", type="primary"):
        if lecture_notes and past_exams:
            with st.spinner("Processing your files... This may take a few minutes."):
                try:
                    # Create progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Process lecture notes
                    status_text.text("📄 Extracting text from lecture notes...")
                    progress_bar.progress(10)
                    
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_lecture:
                        tmp_lecture.write(lecture_notes.read())
                        lecture_text = ocr_processor.extract_text_from_pdf(tmp_lecture.name)
                    
                    progress_bar.progress(40)
                    
                    # Process past exam questions
                    status_text.text("❓ Extracting text from past exam questions...")
                    
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_exam:
                        tmp_exam.write(past_exams.read())
                        exam_text = ocr_processor.extract_text_from_pdf(tmp_exam.name)
                    
                    progress_bar.progress(70)
                    
                    # Generate AI insights
                    status_text.text("🤖 Generating study materials with AI...")
                    study_materials = ai_processor.generate_study_materials(lecture_text, exam_text)
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Processing complete!")
                    
                    # Display results
                    display_results(study_materials)
                    
                    # Clean up temporary files
                    os.unlink(tmp_lecture.name)
                    os.unlink(tmp_exam.name)
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    import traceback
                    with st.expander("🔍 Error Details"):
                        st.code(traceback.format_exc())
        else:
            st.warning("Please upload both lecture notes and past exam questions.")

def display_results(study_materials):
    st.success("✅ Study materials generated successfully!")
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["🔮 Predicted Questions", "🧭 Areas of Concentration", "💡 Study Tips"])
    
    with tab1:
        st.header("🔮 50 Predicted Exam Questions")
        if "predicted_questions" in study_materials and study_materials["predicted_questions"]:
            for i, question in enumerate(study_materials["predicted_questions"], 1):
                st.write(f"**{i}.** {question}")
        else:
            st.write("No predicted questions generated.")
    
    with tab2:
        st.header("🧭 Areas of Concentration")
        if "areas_of_concentration" in study_materials and study_materials["areas_of_concentration"]:
            for area in study_materials["areas_of_concentration"]:
                st.write(f"• {area}")
        else:
            st.write("No areas of concentration identified.")
    
    with tab3:
        st.header("💡 Smart Study Tips")
        if "study_tips" in study_materials and study_materials["study_tips"]:
            for tip in study_materials["study_tips"]:
                st.write(f"• {tip}")
        else:
            st.write("No study tips generated.")

if __name__ == "__main__":
    main()
