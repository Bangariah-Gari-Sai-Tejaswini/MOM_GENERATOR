import google.generativeai as genai
import os
import streamlit as st
from pdfextractor import text_extractor
from docxextractor import text_extractor_docx
from imageextractor import extract_image

key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key = key)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

#load file
st.sidebar.title(':orange[Upload your MOM notes here]')
st.sidebar.subheader("Only Upload images,pdf and docx")
user_file = st.sidebar.file_uploader('Upload your file',['pdf','docx','png','jpg','jpeg'])
if user_file:
    if user_file.type == 'application/pdf':
        user_text = text_extractor(user_file)
    elif user_file.type  == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        user_text = text_extractor_docx(user_file)
    elif user_file.type in ['image/jpg','image/jpeg','image/png']:
        user_text = extract_image(user_file)
    else:
        st.sidebar.write('Upload correct file format')

# if user_file:
#     st.write(user_text)
st.title(':blue[Minutes of Meeting]: :green[AI Assisted MOM Generator in a standardized form \
for meeting notes]')
tips = '''
Tips to use this app:
* Upload ur meeting in sidebar(image,pdf,docx)
* Click on generate MOM and get standardized MOM's
'''
st.write(tips)
if st.button('Generate MOM'):
    if user_text is None:
        st.error('Text is not generated')
    else:
        with st.spinner('Processing your data...'):
            prompt = f'''
 Assume you are an expert in creating minutes of meeting. User has provided
 notes of meeting in text format.
 Using this data you need to create a standardized minutes of meeting for the user.
 The data provided by user os as follows
 {user_text}
 Keep format strictly as mentioned below.
 Title : Title of meetinf
 Heading : Meeting Agenda
 Subheading : Nmae of attendees(if attendees name is not there keep it as NA)
 Subheading : date and place of meeeting
 (place means name of conference/meeting in online)
 Body : The body must follow the following sequence of points

 * Key points discussed
 * Highlights any decision that has been finalized
 * Actionable Items to perform
 * Additional Notes
 * Any deadline that has been discussed
 * Any next meeting date that has been discussed
 * 2 to 3 line of summary
 * use bullet points abd highlight or bold important keywords such that context os clear
 * generate the output in such a way that it can be copied and pasted in word
'''
            response = model.generate_content(prompt)
            st.write(response.text)

            st.download_button(label = 'Click to download',
                               data = response.text,
                               file_name = 'MOM.txt',
                               mime = 'text/plain'
                               )