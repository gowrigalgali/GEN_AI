
import base64
import streamlit as st
import os
import io
from PIL import Image 
import fitz  
import google.generativeai as genai

genai.configure(api_key="AIzaSyBN2Rv8xddlMd2AEkm3VoJjH9DOV8KRHLQ")

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Extract images from PDF using PyMuPDF
        pdf_bytes = uploaded_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        images = []
        for page in doc:
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append(img)

        # Convert images to bytes
        img_byte_arr = io.BytesIO()
        images[0].save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")


## Streamlit App

st.set_page_config(page_title="ATS Resume Expert")
st.header("ResumeReviewer.ai")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file1 = st.file_uploader("Upload the first resume(PDF)...", type=["pdf"])
uploaded_file2 = st.file_uploader("Upload the second resume(PDF)...", type=["pdf"])

submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("How Can I Improve my Skills")
submit3 = st.button("Percentage match")
submit4 = st.button("Choose candidate")
submit5 = st.button("UpSkill")
submit6 = st.button("Candidate's Domain")
submit7= st.button("Interview questions")


input_prompt1 = """
You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements. Don't generate information outside of the resume just summerize the contents of the resume and tell the strengths and weaknesses of the candidate.
Make sure you take the most appropriate keywords from the resume and keep the content of the summary short, do not confuse between the contents of the resume, keep it accurate.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage. Give percentage matches for skill, communication, experience, leadership, and overall percentage in a tabular format. The table should also include the level of skills, that is average,good and best. 
Give a short description based on the percentage match.
"""

input_prompt4 = """
Given the above candidate resumes, you are supposed choose the best candidate based on match to the job description and tell why you choose the candidate, make sure you
explicitly name the candidate. Make sure the first Word of the response is the Candidates name. 
"""

input_prompt5 = """
Also give a description of why the candidate is choosen and what he/she can bring to the table in terms of the job description in under 50 words. Give percentage matches for skill, communication, experience, leadership, and overall percentage in a tabular format.
"""

input_prompt6 = """
Based on the provided job description provide actual links to course,
Let the output be of this format : 
here are some recommended courses and resources to upskill:
Make sure these links actual are hyperlinked such that the user can visit them 

"""
input_prompt7 = """
You are an experienced HR manager. Your task is to identify the domain or areas in which the resume is best suited for based on their resume given. Include info from the resume why they are good for that domain, Like for example if a candidate has worked with Googel GenAI, he's good for AI etc.stating the fact. 
The ouptut should be in tabluar format as in, like a  table, with a column consisting of related domains and another column consisting of percentage score and the total should add up to a hundered, there also should another column with info from th resume reassuring the percentage given per domain. With the available calculated data construct a pie chart such that it will be easy to understand visually.
"""
input_prompt8="""
You are an experienced interviewer. You have to conduct interview for the given job description. Generate questions based on the job's skills. Make sure the questions are of all types and difficulty levels. Also try to include questions from the topic the candidate has mentioned in his/her given resume.
Ask a max of 10 questions which includes technical and behavioural. For example: If the description requires knowledge in Java then such questions must be asked Core Java:

You are supposed ask only 10 questions don't exceed the limit, also mix up the technical questions and don't just ask difference based ones."""

if submit1:
    if uploaded_file1 is not None:
        pdf_content = input_pdf_setup(uploaded_file1)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file1 is not None:
        pdf_content = input_pdf_setup(uploaded_file1)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit2:
    if uploaded_file1 is not None:
        pdf_content = input_pdf_setup(uploaded_file1)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit4:
    if uploaded_file1 is not None and uploaded_file2 is not None:
        pdf_content1 = input_pdf_setup(uploaded_file1)
        pdf_content2 = input_pdf_setup(uploaded_file2)
        response1 = get_gemini_response(input_prompt4, pdf_content1, input_text)
        response2 = get_gemini_response(input_prompt4, pdf_content2, input_text)
        
        
        if response1 > response2:
            #chosen_candidate = "Candidate from the first resume"
            cand_name = get_gemini_response("Get the candadite name", pdf_content1, input_text)
            st.subheader("Chosen Candidate:")
            st.write(cand_name)
            description = get_gemini_response(input_prompt5,pdf_content1,input_text)
            st.write(description)
        else:
            cand_name = get_gemini_response("What is the candidates name, return just the name please ", pdf_content2, input_text)
            st.subheader("Chosen Candidate:")
            st.write(cand_name)
            description = get_gemini_response(input_prompt5,pdf_content2,input_text)
            st.write(description)
        
    else:
        st.write("Please upload both resumes to compare")

elif submit5:
    if input_text:
        pdf_content = input_pdf_setup(uploaded_file1)
        response = get_gemini_response(input_prompt6, pdf_content, prompt=input_text)
        st.subheader("Recommended Courses and Resources to Upskill:")
        st.write(response)
    else:
        st.write("Please provide the job description to get recommended courses and resources.")
elif submit6:
    if uploaded_file1 is not None:
        pdf_content = input_pdf_setup(uploaded_file1)
        input_text=" "
        response = get_gemini_response(input_prompt7, pdf_content, input_text)
        st.subheader("Candidate's Domain or Areas of Expertise:")
        st.write(response)
    else:
        st.write("Please upload the resume")
elif submit7:
    if uploaded_file1 is not None:
        pdf_content = input_pdf_setup(uploaded_file1)
        input_text=" "
        response = get_gemini_response(input_prompt8, pdf_content, input_text)
        st.subheader("Interview questions based on the job description")
        st.write(response)
    else:
        st.write("Please upload the resume")
