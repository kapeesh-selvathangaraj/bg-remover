import streamlit as st
from PIL import Image
from rembg import remove
from io import BytesIO

def removebg(img):
    # Convert the uploaded file to bytes
    img_bytes = img.read()

    # Process the image using removebg
    output_bytes = remove(img_bytes)

    # Return the result as a PIL Image
    return Image.open(BytesIO(output_bytes))

def main():
    st.title("Background Remover App")
    uploaded_file = st.file_uploader("Choose an image ...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        if st.button("Remove Background"):
            result = removebg(uploaded_file)
            st.image(result, caption="Image with Background Removed", use_column_width=True)

            # Add download option for the processed image
            download_btn = st.button("Download Processed Image")
            if download_btn:
                # Save the processed image to a BytesIO buffer
                result_bytesio = BytesIO()
                result.save(result_bytesio, format="PNG")
                result_bytes = result_bytesio.getvalue()

                # Create a download link
                st.download_button(
                    label="Download Processed Image",
                    data=result_bytes,
                    file_name="processed_image.png",
                    mime="image/png",
                )

if __name__ == "__main__":
    main()
