import boto3
import json
import base64

#セッションを取得する. ~/aws/credentials, ~/aws/configの内容を取得している.
boto3_session = boto3.Session(profile_name = "bedrock_prof", region_name = "us-east-1")

#Bedrock-runtime サービスクライアントを取得する
bedrock = boto3_session.client(service_name = "bedrock-runtime")

def generate_text(text_prompt):
    content_text = f"\n\nHuman: Stable Diffusionで以下の内容に沿った画像を生成するためのプロンプトを作成してください。\
        なお、あなたの回答文ではStable Diffusionに与えるためのプロンプトのみ出力し、それ以外の文章は出力しないでください。\
        \n\n{text_prompt}"
    prompt_config = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": content_text}
                ]
            }
        ],
        "max_tokens": 500,
        "temperature": 0.8,
        "top_p": 0.999,
        "top_k": 250,
        "stop_sequences":["\\n\\nHuman:"],
        "anthropic_version": "bedrock-2023-05-31"
    }
    body = json.dumps(prompt_config)

    model_id = "anthropic.claude-3-haiku-20240307-v1:0"
    accept = "application/json"
    content_type = "application/json"
    
    response = bedrock.invoke_model(
        body = body, modelId = model_id, accept = accept, contentType = content_type
    )
    response_body = json.loads(response.get("body").read())
    generated_text = response_body.get("content")[0].get("text")
    return generated_text

def generate_image(image_prompt):
    prompt_config = {
        "text_prompts": [
            {
                "text": image_prompt,
                "weight": 1
            }
        ],
        "cfg_scale": 10,
        "seed": 0,
        "steps": 50,
        "width": 512,
        "height": 512,
        "style_preset": "comic-book"
    }
    body = json.dumps(prompt_config)
    
    model_id = "stability.stable-diffusion-xl-v1"
    accept = "application/json"
    content_type = "application/json"
    
    response = bedrock.invoke_model(
        body = body, modelId = model_id, accept = accept, contentType = content_type
    )
    response_body = json.loads(response.get("body").read())
    print(response_body['result'])
    
    base64_image = response_body.get("artifacts")[0].get("base64")
    base64_bytes = base64_image.encode('ascii')
    generated_image_bytes = base64.b64decode(base64_bytes)
    
    return generated_image_bytes

if __name__ == "__main__":
    decoded_image_file = r"generated_image.png"
    
    # ユーザーからのキーボード入力を受け付ける
    prompt = input("画像生成のためのプロンプトを入力してください: ")
    generated_text = generate_text(prompt)
    #Claude 3で生成されたプロンプトを表示
    print(generated_text)
    
    generated_image_bytes = generate_image(generated_text)
    with open(decoded_image_file, "wb") as image_file:
        image_file.write(generated_image_bytes)