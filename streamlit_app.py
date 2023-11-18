import streamlit as st
import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt

# Load the model
model = joblib.load('xgb_model_final.pkl')

def predict_injury_severity(input_data):
    probability = model.predict_proba(input_data)[:, 1]
    return (probability >= 0.38).astype(int)

def shap_summary_plot(model, input_data):
    explainer = shap.Explainer(model)
    shap_values = explainer.shap_values(input_data)
    plt.figure(figsize=(20, 15))
    shap.summary_plot(shap_values, input_data, show=False)
    plt.tight_layout()
    st.pyplot(plt)

def shap_waterfall_plot(model, input_data):
    # Initialize the SHAP explainer
    explainer = shap.Explainer(model)

    # Generate SHAP values for the input data
    shap_values = explainer(input_data)

    # Check if input_data is a single instance
    if len(input_data) == 1:
        # Display waterfall plot for the first (and only) instance
        plt.figure(figsize=(20, 15))
        shap.plots.waterfall(shap_values[0], show=False)
        plt.tight_layout()
        st.pyplot(plt)
    else:
        st.error("SHAP waterfall plot is only available for individual predictions.")

def main():
    if 'input_df' not in st.session_state:
        st.session_state['input_df'] = pd.DataFrame()

    tab1,tab2,tab3=st.tabs(['Make a Prediction','See SHAP Summary Plot','See Waterfall Plot'])
    with tab1:
    
        with st.form("prediction_form"):
            st.subheader("Check the Following Boxes for YES, Skip for NO:")
            col1,col2=st.columns(2)
            with col1:
            # Your input fields
                inputs1 = {
                    
                    'Vehicle First Impact Location_SIX OCLOCK': st.checkbox('Did the vehicle first impact location occur at six o\'clock of the Vehicle?'),
                    'Vehicle Damage Extent_NO DAMAGE': st.checkbox('Was there no damage to the vehicle?'),
                    'Vehicle Damage Extent_SUPERFICIAL': st.checkbox('Was the vehicle damage superficial?'),
                    'Vehicle Damage Extent_FUNCTIONAL': st.checkbox('Is the Vehicle still functional?'),
                    'Vehicle Second Impact Location_SIX OCLOCK': st.checkbox('Did the vehicle second impact location occur at six o\'clock of the Vehicle?'),
                    'Vehicle Damage Extent_DISABLING': st.checkbox('Was the vehicle damage disabling?'),
                    'Collision Type_SAME DIRECTION SIDESWIPE': st.checkbox('Was the collision a same direction sideswipe?'),
                    'Vehicle Body Type_MOTORCYCLE': st.checkbox('Is it a motorcycle?'),
                    'Vehicle Movement_BACKING': st.checkbox('Was the vehicle backing?'),
                    'Collision Type_SAME DIR REAR END': st.checkbox('Was the collision a same direction rear end?'),
                    'Collision Type_HEAD ON': st.checkbox('Was the collision head on?'),
                    'Vehicle Movement_MOVING CONSTANT SPEED': st.checkbox('Was the vehicle moving at a constant speed?')}
            with col2:
                inputs2={
                    
                    'Vehicle Body Type_SCHOOL BUS': st.checkbox('Is it a school bus?'),
                    'Vehicle Second Impact Location_FOUR OCLOCK': st.checkbox('Did the vehicle second impact location occur at four o\'clock of the Vehicle?'),
                    'Vehicle Body Type_PASSENGER CAR': st.checkbox('Is it a passenger car?'),
                    'Vehicle Second Impact Location_NINE OCLOCK': st.checkbox('Did the vehicle second impact location occur at nine o\'clock of the Vehicle?'),
                    'Collision Type_OTHER': st.checkbox('Check if the collision type was not one of the following: Same Direction Rear End, Same Direction Sideswipe, Head On, Angle, Opposite Direction Sideswipe, Opposite Direction Rear End, Same Movement Angle, Straight Movement Angle'),
                    'Collision Type_STRAIGHT MOVEMENT ANGLE': st.checkbox('Was the collision a straight movement angle?'),
                    'Vehicle First Impact Location_TWELVE OCLOCK': st.checkbox('Did the vehicle first impact location occur at twelve o\'clock of the Vehicle?'),
                    'Vehicle Second Impact Location_TWELVE OCLOCK': st.checkbox('Did the vehicle second impact location occur at twelve o\'clock of the Vehicle?')
         
                }
    
            submit_button = st.form_submit_button("See Level of Emergency")
    
            if submit_button:
                inputs = {**inputs1, **inputs2}  # Combine inputs from both columns
                if submit_button:
                    input_df = pd.DataFrame([inputs])
                    st.session_state['input_df'] = input_df
                    prediction = predict_injury_severity(input_df)

        
        # Use HTML with inline CSS for color styling
                if prediction == 1:
                    severity = '<span style="color: red;">High</span>'
                else:
                    severity = '<span style="color: green;">Low</span>'
    
                st.markdown(f'<p class="big-font">Emergency Level: <b>{severity}</b></p>', unsafe_allow_html=True)
    with tab2:   
            if st.session_state['input_df'].empty:
                st.write("Please make a prediction first.")
            else:
                st.subheader("SHAP Summary Explanation")
                shap_summary_plot(model, st.session_state['input_df'])

    with tab3:

            if st.session_state['input_df'].empty:
                st.write("Please make a prediction first.")
            else:
                st.subheader("SHAP Waterfall Explanation for the Prediction")
                shap_waterfall_plot(model, st.session_state['input_df'])





            
        
if __name__ == '__main__':
    main()
