import streamlit as st
from PIL import Image
import base64
import boto3
import io
import json

GENERATE_TEXT_MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"

GENERATE_IMAGE_MODEL_ID = "stability.stable-diffusion-xl-v1"
MAX_SEED = 4294967295
DEFAULT_SEED = 42

STYLES_MAP = {
    "3D Model": "3d-model",
    "Analog Film": "analog-film",
    "Anime": "anime",
    "Cinematic": "cinematic",
    "Comic Book": "comic-book",
    "Digital Art": "digital-art",
    "Enhance": "enhance",
    "Fantasy Art": "fantasy-art",
    "Isometric": "isometric",
    "Line Art": "line-art",
    "Low Poly": "low-poly",
    "Modeling Compound": "modeling-compound",
    "Neon Punk": "neon-punk",
    "Origami": "origami",
    "Photographic": "photographic",
    "Pixel Art": "pixel-art",
    "Tile Texture": "tile-texture",
    "None": "None",
}

NEGATIVE_PROMPTS = [
    "bad anatomy", "distorted", "blurry",
    "pixelated", "dull", "unclear",
    "poorly rendered",
    "poorly Rendered face",
    "poorly drawn face",
    "poor facial details",
    "poorly drawn hands",
    "poorly rendered hands",
    "low resolution",
    "Images cut out at the top, left, right, bottom.",
    "bad composition",
    "mutated body parts",
    "blurry image",
    "disfigured",
    "oversaturated",
    "bad anatomy",
    "deformed body features",
]

#セッションを取得する. ~/aws/credentials, ~/aws/configの内容を取得している.
boto3_session = boto3.Session(profile_name = "bedrock_prof", region_name = "us-east-1")

#Bedrock-runtime サービスクライアントを取得する
bedrock = boto3_session.client(service_name = "bedrock-runtime")

def generate_text(text_prompt):
    prompt_config = {
        "system": "あなたはユーザーからの入力内容に沿った画像をStable Diffusionで生成するためのプロンプトを作成するAIアシスタントです。あなたの回答文ではStable Diffusionに与えるためのプロンプトのみ出力し、それ以外の文章は出力しないでください。",
         "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": text_prompt
                    }
                ]
            }
        ],
        "max_tokens": 2000,
        "temperature": 1,
        "top_p": 0.999,
        "top_k": 250,
        "stop_sequences":["\\n\\nHuman:"],
        "anthropic_version": "bedrock-2023-05-31"
    }
    body = json.dumps(prompt_config)
    accept = "application/json"
    content_type = "application/json"
    response = bedrock.invoke_model(
        body = body, modelId = GENERATE_TEXT_MODEL_ID, accept = accept, contentType = content_type
    )
    response_body = json.loads(response.get("body").read())
    generated_text = response_body.get("content")[0].get("text")
    return generated_text

@st.cache_data(show_spinner = False)
def generate_image(image_prompt, style, seed = DEFAULT_SEED):
    prompt_config = {
        "text_prompts": [
            {
                "text": image_prompt,
                "weight": 1
            }
        ],
        "cfg_scale": 10,
        "seed": seed,
        "steps": 50,
        "width": 512,
        "height": 512,
        "style_preset": style,
        "negative_prompts": NEGATIVE_PROMPTS,
    }
    body = json.dumps(prompt_config)
    accept = "application/json"
    content_type = "application/json"
    response = bedrock.invoke_model(
        body = body, modelId = GENERATE_IMAGE_MODEL_ID, accept = accept, contentType = content_type
    )
    response_body = json.loads(response.get("body").read())
    
    image_bytes = response_body.get("artifacts")[0].get("base64")
    image_data = base64.b64decode(image_bytes.encode())
    st.session_state['image_data'] = image_data
    return image_data
    
@st.cache_data
def get_image(image_data):
    return Image.open(io.BytesIO(image_data))

if __name__ == "__main__":
    st.title("Stable Diffusionで画像生成")
    
    with st.sidebar:
        #SelectBox
        style_key = st.sidebar.selectbox(
            "画像のスタイルを選択",
            STYLES_MAP.keys(),
            index=0
            )
        
        seed = st.sidebar.slider(
            "Seed",
            min_value = 0,
            value = DEFAULT_SEED,
            max_value = MAX_SEED,
            step = 1,
        )
        
    prompt = st.text_input("プロンプトを入力してください")
    if not prompt:
        st.warning("プロンプトを入力してください")
        st.stop()
        
    if st.button("画像生成", type = "primary"):
        if len(prompt) > 0:
            st.markdown(f"""
                        画像生成中・・・(プロンプト={prompt})
                        """)
            
            #Create a spinner to show the image is being generated
            with st.spinner("画像生成中・・・"):
                generated_text = generate_text(prompt)
                
                style = STYLES_MAP[style_key]
                print("Generate image with Style:{} with Seed:{} and Prompt: {}".format(
                    style_key, seed, generated_text))
                image_data = generate_image(
                    image_prompt = generated_text, style = style, seed = seed)
                st.success("画像生成完了")
    if st.session_state.get("image_data", None):
        image = get_image(st.session_state.image_data)
        st.image(image)