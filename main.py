import streamlit as st
from instagrapi import Client
from PIL import Image

import requests
import os
import io


"""
TODO:
1.     
"""


def insta_crawling(ID, PW):
    cl = Client()
    cl.login(ID, PW)

    user_id = cl.user_id_from_username("jaeu8021")
    state_text.text("Feed searching...")

    medias = cl.user_medias(int(user_id), 9)
    folder = "test-folder"
    createDirectory(folder)
    state_text.text("Saving Image....")
    for m in medias:
        try:
            print(cl.photo_download(m.pk, folder))
        except AssertionError:
            pass
    
    state_text.text("Crawling finished!")
            

def photo_download(c, pk, folder):
    media = c.media_info(pk)
    assert media.media_type == 1, "Must been photo"
    filename = "{username}_{media_pk}".format(
            username=media.user.username, media_pk=pk
        )
    
    p = os.path.join(folder, filename + '.jpg')
    
    response = requests.get(media.thumbnail_url, stream=True, timeout=c.request_timeout)
    response.raise_for_status()

    image = Image.open(io.BytesIO(response.content))
    image.show()
    with open(p, "wb") as f:
        f.write(response.content)
    
    return p


def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")


st.title('AI color grader')
st.subheader('Find the filter that best fits your Instagram feed!')
# uploaded_files = st.file_uploader(label="Choose image(s)...",
#                                   type=['jpeg', 'png', 'jpg', 'heic'],
#                                   label_visibility='visible',
#                                   accept_multiple_files=True)
st.latex(r"C := \bigcap_{n = 0}^{\infty} C_n")

# crawled = []
# # Check if the user has uploaded any files
# if uploaded_files or crawled:
#     # Create an empty list to store the images
#     images = []

#     # Loop through each uploaded file and append the opened image to the list
#     for file in uploaded_files:
#         image = Image.open(file)
#         images.append(image)

#     # Calculate the number of rows and columns needed to display the images in a 3x3 grid
#     num_images = len(images)
#     num_rows = (num_images + 2) // 3
#     num_cols = min(num_images, 3)

#     # Set the desired width and height of the images in the grid
#     image_width = 200

#     # Loop through each row and column to display the images in a grid
#     for i in range(num_rows):
#         cols = st.columns(num_cols)
#         for j in range(num_cols):
#             index = i * 3 + j
#             if index < num_images:
#                 cols[j].image(
#                     images[index],
#                     caption=f"{uploaded_files[index].name}",
#                     width=image_width)
#     # center_button = st.container()
#     # with center_button:
#     #     st.button("Process Images", text_align='center')
#     if st.button("Process Images!"):
#         st.write("Images are processed")


# else:
#     # If no files were uploaded, display a message
#     st.write("Please upload one or more image files.")

# insta_id = st.text_input("Put your Instagram ID here!")
# insta_pwd = st.text_input('Put your Instagram password here!')
# Instagram crawling button

state_text = st.text("Ready to Crawl.")
if st.button("Crawling Instagram"):
    state_text.text("Crawling started..")
    insta_crawling("jaeu8021", "kvoid2824#")    


#id = "leessunj"
#pwd = "Ilsj08282!"
