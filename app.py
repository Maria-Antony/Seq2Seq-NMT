from flask import Flask, request
import numpy as np
import pickle
import pandas as pd
# import flasgger
import streamlit as st 
import torch
import time
from transformers import MBartForConditionalGeneration, MBartTokenizer

app=Flask(__name__)
# Swagger(app)


def predict_text(input_text,tgt_lang):
    
    """Let's Authenticate the Banks Note 
    This is using docstrings for specifications.
    ---
    parameters:  
      - name: input_text
        in: query
        type: sir
        required: true
      - name: tgt_lang
        in: query
        type: str
        required: true
    responses:
        200:
            description: The output values
        
    """
    # input_text=request.args.get("Input string")
    # tgt_lang=request.args.get("Target Language")

    tokenizer = MBartTokenizer.from_pretrained("Maria90/my-mbart-model")
    model = MBartForConditionalGeneration.from_pretrained("Maria90/my-mbart-model",token='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')
    model.load_state_dict(torch.load('/Users/marianivethaantonypushparaj/Desktop/Streamlit-PR/Model_weights_MBart.pth',map_location=torch.device('cpu')),strict=False)

    encoded_en_text = tokenizer(input_text, return_tensors="pt",truncation = True)
    generated_tokens = model.generate(**encoded_en_text,forced_bos_token_id=tokenizer.lang_code_to_id[tgt_lang])
    output_str = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    print(output_str)
    return "translated text: "+ str(output_str).strip("[]").replace("'", "")

def main():
    # st.title("")
    
    base="dark"
    primaryColor="#cb2828"
    backgroundColor="#92867f"
    secondaryBackgroundColor="#4a4a56"

    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">Neural Machine Translation App </h2>
    <h3 style="color:white;text-align:center;">Supports German, Spanish and Dutch</h3>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    int_text = st.text_input("Input Text","Type Here")
    # tgt_lang = st.text_input("Target Language","Type Here")
    result=""
    option = st.selectbox(
    "Language to be Translated",
    ("German", "Dutch", "Spanish"),
    index=None,
    placeholder="Select language...",
)
    if option == 'German':
        tgt_lang = 'de_DE'
    elif option == 'Dutch':
        tgt_lang = 'nl_XX'
    else:
        tgt_lang = 'es_XX'
    
    if st.button("Predict"):
        progress_text = "Operation in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)
        result = predict_text(int_text,tgt_lang)
        percent_complete = 0
        while percent_complete < 100:
            time.sleep(0.01)
            percent_complete += 1
            my_bar.progress(percent_complete, text=progress_text)
        st.success('The output {}'.format(result))

if __name__=='__main__':
    main()