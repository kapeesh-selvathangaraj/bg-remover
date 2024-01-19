import streamlit as st
from PIL import Image
from rembg import remove
from io import BytesIO
from bokeh.models import ColumnDataSource, FreehandDrawTool
from bokeh.plotting import figure
from bokeh.io import show

def removebg(img, mask):
    # Convert the uploaded file to bytes
    img_bytes = img.read()

    # Process the image using removebg with a mask
    output_bytes = remove(img_bytes, target_mask=mask)

    # Return the result as a PIL Image
    return Image.open(BytesIO(output_bytes))

def main():
    st.title("Background Remover App")

    # Upload image
    uploaded_file = st.file_uploader("Choose an image ...", type=["jpg", "jpeg", "png"])

    # Additional options using sidebar
    with st.sidebar:
        st.header("Options")

    if uploaded_file is not None:
        # Display uploaded image
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        # Create Bokeh plot for drawing
        plot = figure(width=400, height=400, title="Draw a mask to select object")
        plot.axis.visible = False

        # Create a ColumnDataSource for drawing tool
        source = ColumnDataSource(data=dict(image=[], x=[], y=[]))
        plot.image_url(url=[uploaded_file], x=0, y=0, w=1, h=1, source=source)

        # Add FreehandDrawTool to the plot
        draw_tool = FreehandDrawTool(renderers=[plot], num_objects=1)
        plot.add_tools(draw_tool)
        plot.toolbar.active_drag = draw_tool

        # Display the Bokeh plot
        st.bokeh_chart(plot, use_container_width=True)

        # Button to remove background
        if st.button("Remove Background"):
            try:
                # Get the drawn mask from the Bokeh plot
                mask = source.data['image'][0] if source.data['image'] else None

                if mask is None:
                    st.warning("Please draw a mask to select the object.")
                else:
                    # Process the image
                    result = removebg(uploaded_file, mask)

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

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
