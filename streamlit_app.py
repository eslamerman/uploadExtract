import streamlit as st
import boto3
import os

# Streamlit app title
st.title("File Upload to S3")

# Get AWS credentials from Streamlit secrets
aws_access_key_id = st.secrets["aws"]["aws_access_key_id"]
aws_secret_access_key = st.secrets["aws"]["aws_secret_access_key"]
bucket_name = st.secrets["aws"]["bucket_name"]  # Add bucket name to secrets

# File uploader
uploaded_file = st.file_uploader("Choose a file", type=["txt", "csv", "jpg", "png", "pdf"]) # Allow various file types


if uploaded_file is not None:
    # Create boto3 session
    try:
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        s3 = session.resource('s3')
        st.write("Session Created")

        # Upload file to S3
        try:
            # Use uploaded filename directly for the S3 key
            s3.meta.client.upload_fileobj(uploaded_file, bucket_name, uploaded_file.name) 

            st.success(f"File '{uploaded_file.name}' uploaded successfully to S3 bucket '{bucket_name}'")


            # [Optional] Display download link (pre-signed URL)
            url = s3.meta.client.generate_presigned_url(
                ClientMethod='get_object', 
                Params={'Bucket': bucket_name, 'Key': uploaded_file.name},
                ExpiresIn=3600  # URL expires in 1 hour
            )
         #  st.markdown(f"[Download Link]({url})")



        except ClientError as e:  # Handle specific S3 errors
            st.error(f"Error uploading file: {e}")
        except Exception as e:  # Handle other potential errors
            st.error(f"An unexpected error occurred: {e}")


    except Exception as e: # Handle boto3 session creation errors
        st.error(f"Error creating boto3 session: {e}")
