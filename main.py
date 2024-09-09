import torch
import pickle
import streamlit as st
from PIL import Image

from image_captioning import NIC
from image_captioning import resize_and_normalize_image
from image_captioning import IMAGENET_IMAGE_SIZE, IMAGENET_IMAGE_MEAN, IMAGENET_IMAGE_STD
from assets.config import NUM_LAYERS, HIDDEN_SIZE, EMBED_SIZE, NIC_PATH, VOCAB_PATH


# Title of the app
st.title("Image Caption Generator")

# Instruction for the user
st.write("Upload an image and get a generated caption.")

# Uploading the image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open the image file
    img = Image.open(uploaded_file)

    # Display the image
    st.image(img, caption="Uploaded Image", use_column_width=True)

    # Placeholder for caption generation
    st.write("Generating caption...")

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    with open(VOCAB_PATH, 'rb') as f:
        vocab = pickle.load(f)

    nic = NIC(HIDDEN_SIZE, len(vocab), EMBED_SIZE, NUM_LAYERS).eval()
    nic.load_state_dict(torch.load(NIC_PATH))
    nic = nic.to(device)

    adjusted_img = resize_and_normalize_image(img, IMAGENET_IMAGE_SIZE, IMAGENET_IMAGE_SIZE, IMAGENET_IMAGE_MEAN,
                                              IMAGENET_IMAGE_STD)
    # Move the image to the device
    image_tensor = adjusted_img.to(device)

    # Generate the final caption by generating first the corresponding words ids, and the using the Vocabulary to
    # obtain the words
    sampled_ids = nic.generate_caption(image_tensor)
    sampled_ids = sampled_ids[0].cpu().numpy()

    sampled_caption = []
    for word_id in sampled_ids:
        word = vocab.to_word(word_id)
        sampled_caption.append(word)
        if word == '<<end>>':
            break

    # Show the image and the caption
    sampled_caption = [word for word in sampled_caption if word not in ['<<start>>', '<<end>>']]
    sentence = ' '.join(sampled_caption)

    # Display the generated caption
    st.write(f"Caption: **{sentence}**")

# Footer or additional instructions
st.write("Upload another image to generate a new caption.")
















