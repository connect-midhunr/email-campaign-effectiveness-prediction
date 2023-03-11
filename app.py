import numpy as np
import pandas as pd
import pickle
import streamlit as st

# importing XGBoost model
predictor = pickle.load(open('./models/xgboost_model.pkl', 'rb'))
scaler = pickle.load(open('./models/std_scaler.pkl', 'rb'))

# defining a function to predict campaign effectiveness
def get_prediction(params: dict):
    parameter_df = pd.DataFrame(columns=['Subject_Hotness_Score', 'Total_Past_Communications', 'Word_Count', 'Total_Links_Images', 
                                         'Email_Type_1', 'Email_Source_Type_1', 'Email_Campaign_Type_2', 'Email_Campaign_Type_3'])

    feature_values = []

    # adding subject hotness score, total past communications, word count, total links and total images
    feature_values.append(np.sqrt(params['Subject Hotness Score']))
    feature_values.append(params['Total Past Communications'])
    feature_values.append(params['Word Count'])
    feature_values.append(np.log(params['Total Links'] + params['Total Images']))

    # adding e-mail type
    if params['E-mail Type'] == 1:
        feature_values.append(1)
    else:
        feature_values.append(0)

    # adding e-mail source type
    if params['E-mail Source Type'] == 1:
        feature_values.append(1)
    else:
        feature_values.append(0)

    # adding e-mail campaign type
    if params['E-mail Campaign Type'] == 2:
        feature_values.append(1)
    else:
        feature_values.append(0)

    if params['E-mail Campaign Type'] == 3:
        feature_values.append(1)
    else:
        feature_values.append(0)
    
    parameter_df.loc[0] = feature_values
    
    print()
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    print("-------------------------------------------")
    print()
    print(parameter_df)
    print()
    print("-------------------------------------------")
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    print()
    
    X = parameter_df.replace([np.inf, -np.inf, np.nan], 0)
    X = scaler.transform(X)
    y = predictor.predict(X)

    if y[0] == 2:
        return "E-mail Acknowledged"
    elif y[0] == 1:
        return "E-mail Read"
    else:
        return "E-mail Ignored"

def main():
    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">E-mail Campaign Effectiveness Prediction</h2>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)

    with st.form(key='columns_in_form'):
        c1, c2 = st.columns(2)

        with c1:
            email_type = st.selectbox("E-mail Type", [1, 2])
            subject_hotness_score = st.text_input("Subject Hotness Score", "0.0")
            email_source_type = st.selectbox("E-mail Source Type", [1, 2])
            customer_location = st.selectbox("Customer Location", ['A', 'B', 'C', 'D', 'E', 'F'])
            email_campaign_type = st.selectbox("E-mail Campaign Type", [1, 2, 3])
        
        with c2:
            total_past_communications = st.text_input("Total Past Communications", "0")
            time_email_sent_category = st.selectbox("Time Email Sent Category", [1, 2, 3])
            word_count = st.text_input("Word Count", "0")
            total_links = st.text_input("Total Links", "0")
            total_images = st.text_input("Total Images", "0")
        
        predict = st.form_submit_button("Predict Campaign Effectiveness")

        if predict:
            params = {"E-mail Type" : email_type, "Subject Hotness Score" : float(subject_hotness_score), 
                      "E-mail Source Type" : email_source_type, "Customer Location" : customer_location, 
                      "E-mail Campaign Type": email_campaign_type, "Total Past Communications" : int(total_past_communications), 
                      "Time Email Sent Category" : time_email_sent_category, "Word Count" : int(word_count), 
                      "Total Links" : int(total_links), "Total Images" : int(total_images)}
            st.text_area("Campaign Effectiveness", get_prediction(params))

if __name__ == '__main__':
    main()