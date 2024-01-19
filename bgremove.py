import streamlit as st
from PIL import Image
from rembg import remove
from io import BytesIO

def removebg(img, remove_objects):
    # Convert the uploaded file to bytes
    img_bytes = img.read()

    # Process the image using removebg with specified removal objects
    output_bytes = remove(img_bytes, target_objects=remove_objects)

    # Return the result as a PIL Image
    return Image.open(BytesIO(output_bytes))

def main():
    st.title("Background Remover App")

    # Upload image
    uploaded_file = st.file_uploader("Choose an image ...", type=["jpg", "jpeg", "png"])

    # Additional options using sidebar
    with st.sidebar:
        st.header("Options")
        # Create a multi-select widget for removal objects
        remove_objects = st.multiselect("Select Objects to Remove", ["Person", "Car", "Background"])
        # You can add more objects to the list as needed

    if uploaded_file is not None:
        # Display uploaded image
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        # Button to remove background
        if st.button("Remove Background"):
            # Check if any objects are selected
            if not remove_objects:
                st.warning("Please select at least one object to remove.")
            else:
                # Process the image
                result = removebg(uploaded_file, remove_objects)

                # Display processed image
                st.image(result, caption="Image with Background Removed", use_column_width=True)

                # Convert the PIL Image to bytes
                result_bytes = BytesIO()
                result.save(result_bytes, format="PNG")
                result_bytes = result_bytes.getvalue()

                # Add download option for the processed image
                download_btn = st.download_button(
                    label="Download Processed Image",
                    data=result_bytes,
                    file_name="processed_image.png",
                    mime="image/png",
                    key="processed_image",
                    help="Click to download the processed image."
                )

if __name__ == "__main__":
    main()
