import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import PyPDF2
import os
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel(
model_name="gemini-1.0-pro")
convo = model.start_chat(history=[])


prompt="""You are a Question Predictor, act as question preparer.You Will perform a pattern analysis 
on given previous questions and syllabus copy if it is available
and predicts the next possible questions to help the students to get Good score in there exams.
The Previous Year qestions are :\n"""

def text_extractor(pdf_file):
    pdf_reader =PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    #st.write(pdf_file.name)
    #st.image(pdf_file,caption="Uploaded PDF")
    text = ""
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

def Question_Predictor(q_text,s_text):
    convo.send_message(prompt+q_text+"\n Syllubus Copy :\n"+s_text)
    response=str(convo.last.text)
    return response


st.title("StudyBot")
st.image("images/studybot.png",width=10,use_column_width=True)

pdf_file = st.file_uploader("Upload Previous Papers (PDF):",type="pdf")

syllabus_copy = st.file_uploader("Uplpoad syllabus Copy here : (Optional)")



if pdf_file is not None:
    q_text = text_extractor(pdf_file)
    if syllabus_copy is not None:
        syllabus_text = text_extractor(syllabus_copy)
    else:
        syllabus_text = "Syllbus Copy is Not Available"
    #st.write(q_text)
    Final_questions = Question_Predictor(q_text,syllabus_text)
    st.markdown("### Expected Questions :")
    st.write(Final_questions)


    

    


        
        
    


