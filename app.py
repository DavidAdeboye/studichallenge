import streamlit as st
import os
from dotenv import load_dotenv
from ocr_processor import OCRProcessor
from ai_processor import AIProcessor
from pdf_handler import PDFHandler
import tempfile

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
        with st.spinner("Initializing OCR engines..."):
            ocr_processor = OCRProcessor()
            pdf_handler = PDFHandler()
            ai_processor = AIProcessor()
        
        # Display available engines
        with st.expander("📋 System Information", expanded=False):
            st.write("**Available OCR Engines:**")
            for engine in ocr_processor.available_engines:
                st.write(f"✅ {engine.replace('_', ' ').title()}")
            
            st.write("**Available PDF Conversion Methods:**")
            for method in pdf_handler.conversion_methods:
                st.write(f"✅ {method.replace('_', ' ').title()}")
            
            st.info("💡 The system will automatically use the best available OCR engine for each page.")
    
    except Exception as e:
        st.error(f"❌ Failed to initialize processors: {str(e)}")
        st.info("Please check that all required dependencies are installed. Run the setup script if needed.")
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
                    # Process lecture notes
                    st.info("📄 Extracting text from lecture notes...")
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_lecture:
                        tmp_lecture.write(lecture_notes.read())
                        lecture_images = pdf_handler.convert_pdf_to_images(tmp_lecture.name)
                        lecture_text = ocr_processor.extract_text_from_images(lecture_images)
                    
                    # Process past exam questions
                    st.info("❓ Extracting text from past exam questions...")
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_exam:
                        tmp_exam.write(past_exams.read())
                        exam_images = pdf_handler.convert_pdf_to_images(tmp_exam.name)
                        exam_text = ocr_processor.extract_text_from_images(exam_images)
                    
                    # Generate AI insights
                    st.info("🤖 Generating study materials with AI...")
                    study_materials = ai_processor.generate_study_materials(lecture_text, exam_text)
                    
                    # Display results
                    display_results(study_materials)
                    
                    # Clean up temporary files
                    os.unlink(tmp_lecture.name)
                    os.unlink(tmp_exam.name)
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please upload both lecture notes and past exam questions.")

def display_results(study_materials):
    st.success("✅ Study materials generated successfully!")
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["🔮 Predicted Questions", "🧭 Areas of Concentration", "💡 Study Tips"])
    
    with tab1:
        st.header("🔮 50 Predicted Exam Questions")
        if "predicted_questions" in study_materials:
            for i, question in enumerate(study_materials["predicted_questions"], 1):
                st.write(f"**{i}.** {question}")
        else:
            st.write("No predicted questions generated.")
    
    with tab2:
        st.header("🧭 Areas of Concentration")
        if "areas_of_concentration" in study_materials:
            for area in study_materials["areas_of_concentration"]:
                st.write(f"• {area}")
        else:
            st.write("No areas of concentration identified.")
    
    with tab3:
        st.header("💡 Smart Study Tips")
        if "study_tips" in study_materials:
            for tip in study_materials["study_tips"]:
                st.write(f"• {tip}")
        else:
            st.write("No study tips generated.")

if __name__ == "__main__":
    main()
