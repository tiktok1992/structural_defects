import streamlit as st
import google.generativeai as genai
from PIL import Image
import datetime as dt
import os
from dotenv import load_dotenv 

load_dotenv()#activate api key

# Configure the model
key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-2.5-flash-lite')


# Upload and show image
st.sidebar.title(':red[UPLOAD YOUR IMAGE HERE]')
uploaded_image = st.sidebar.file_uploader('Here',type=['jpeg','jpg','png'])
if uploaded_image:
    image = Image.open(uploaded_image)
    st.sidebar.subheader(':blue[UPLOADED IMAGE]')
    st.sidebar.image(image)

# Create main page
st.title(':orange[STRUCTURAL DEFFECTS] : :green[AI assisted structural defect identifier in construction business]')
tips ='''To use the application folow the steps below:
* Upload the image
* Click on the button to generate summary
* Click download to save the report generated'''
st.write(tips)
rep_title = st.text_input('Report Title :',None)
prep_by = st.text_input('Report Prepared by :',None)
prep_for = st.text_input('Report Prepared for :',None)

prompt = f'''Assume you are a structural engineer. The user has has provided an image
of a structure. You need to identify the strucutural defects in the image and genarate
a report. The report should contain the following:

It should start with the title, prepared by and prepared for details. Provided by the user.
use {rep_title} as title, {prep_by} as prepared by, {prep_for} as prepred for the same.
Also mention the current date from {dt.datetime.now().date()}.

* Identify and classify the defect for eg: crack, spalling, corrosion, honeycombing, etc.
* There could more than one defects in the image. Identify all the defects seperately.
* For each defect identified, provide a short description of the defect and its potential impact on the structure.
* For each measure the severity of the defect as low, medium or high. Also mention if the defect is inevitable or avoidable.
* Also mention the time before this defect leads to permament damage to the structure.
* provide a shot term and long solution anlong with their estimated cost (in INR) and time to implement.
* What precuationary measures can be taken to avoid such defects in future.
* The report generated should be in the word format.
* Show the data in bullet points and tabular format wherever possible.
* Make sure that the report does not exceeds 3 pages.'''

if st.button('Generate Report'):
    if uploaded_image is None:
        st.error('Please upload an image first.')
    else:
        with st.spinner('Generating Report...'):
            response = model.generate_content([prompt,image],generation_config={"temperature":0.2})
            st.write(response.text)

        st.download_button(
            label='Download Report',
            data=response.text,
            file_name='structural_defect_report.txt',
            mime="text/plain")