import streamlit as st
import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from docx import Document

os.environ['GEMINI_API_KEY'] = 'AIzaSyBZfbkPJHyWCk7ELeT0fgDGpl2GPBbVHt4'

genai.configure(api_key = os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel('gemini-pro')

def read_txt_file(uploaded_file):
    return uploaded_file.read().decode('utf-8')

def read_docx_file(uploaded_file):
    doc = Document(uploaded_file)
    return '\n'.join([para.text for para in doc.paragraphs])

def generate_roasting(prompt):
    response = model.generate_content(prompt,
                                    safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,}
                                    )
    return response.text

def process_file(uploaded_file):
    file_type = uploaded_file.name.split('.')[-1]
    
    if file_type == 'txt':
        content = read_txt_file(uploaded_file)
    elif file_type == 'docx':
        content = read_docx_file(uploaded_file)
    else:
        st.error('Unsupported file type')
        return None

    prompt = f'''
    Instruksi: Berikan roast sarkastik terhadap cover letter berikut. Gunakan metafora dan perumpamaan yang tajam untuk mengkritik kekurangan dan kekurangan dalam surat lamaran. Buat dalam bentuk paragraf dan tambahkan beberapa saran untuk cover letter tersebut. Jawab menggunakan bahasa indonesia.

    Cover Letter:
    {content}
    '''

    roasting = generate_roasting(prompt)
    return roasting

# Streamlit UI
st.title('Roasting Your Cover Letter')
st.write('''
    Cara Penggunaan:
    1. Upload file mu (txt / docx)
    2. Siapkan fisik dan mental
    3. Klik submit
''')

uploaded_file = st.file_uploader('Pilih File:', type=['txt', 'docx'])

if st.button('Submit'):
    if uploaded_file is not None:
        output = process_file(uploaded_file)
        if output:
            st.subheader('Response:', divider='gray')
            st.write(output)
    else:
        st.error('Silakan upload file terlebih dahulu!')

st.write('Created by [**Naufal Faiz Nugraha**](https://www.linkedin.com/in/naufal-faiz-nugraha-867534292)')
