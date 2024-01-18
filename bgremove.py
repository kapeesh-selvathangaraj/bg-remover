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

if __name__ == "__main__":
    main()
