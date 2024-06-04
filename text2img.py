from openai import OpenAI
from PIL import Image
import openai
import torch
import io
import base64
class DALLEModel:
    def __init__(self, ckpt: dict = {"imagecap_model":"gpt-4o","txt2img_model":"dall-e-3","api-key":"your-api-key","quality":"standard","size":"1024x1024"}, precision = torch.float16, device = torch.device("cuda")):
        if isinstance(ckpt["api-key"], str):
            self.client = OpenAI(api_key=ckpt["api-key"], base_url="https://openai.ianchen.io/v1")
        elif isinstance(ckpt["api-key"], list):
            self.client = [OpenAI(api_key=c,  base_url="https://openai.ianchen.io/v1") for c in ckpt["api-key"]]
        else:
            raise ValueError("Invalid API Key")
        
        # Must be one of 256x256, 512x512, or 1024x1024 for dall-e-2. Must be one of 1024x1024, 1792x1024, or 1024x1792 for dall-e-3 models.
        if ckpt["txt2img_model"] == 'dall-e-2':
            assert ckpt["size"] in ['256x256', '512x512', '1024x1024']
        elif ckpt["txt2img_model"] == 'dall-e-3':
            assert ckpt["quality"] in ['standard', 'hd']
            assert ckpt["size"] in ['1024x1024', '1792x1024', '1024x1792']
        self.txt2img_model = ckpt["txt2img_model"]
        self.imagecap_model = ckpt["imagecap_model"]
        self.completion_images = 0
        # self.cache_path = ckpt['cache_path']
        self.size = ckpt["size"]
        self.price = 0.0
        if self.txt2img_model == "dall-e-3":
            self.quality = ckpt["quality"]
        else:
            self.quality = None
            
    def _get_caption(self, client, image, text, is_url = True):
        if not is_url:
            base64_image = self.encode_image(image)
            try:
                response = client.chat.completions.create(
                    model=self.imagecap_model,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": f"{text}"},
                                {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}",
                                    "detail": "auto"
                                },
                                },
                            ],
                        }
                    ],
                    max_tokens=300,
                )
            except openai.OpenAIError as e:
                raise e
        else:
            try:
                response = client.chat.completions.create(
                    model=self.imagecap_model,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": f"{text}"},
                                {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"{image}",
                                    "detail": "auto"
                                },
                                },
                            ],
                        }
                    ],
                    max_tokens=300,
                )
            except openai.OpenAIError as e:
                raise e
        return response.choices[0].message.content
        
        
        
        
    def _get_response(self, client, prompt):
        while True:
            try:
                if self.txt2img_model == "dall-e-2":
                    response = client.images.generate(model=self.txt2img_model,
                                                    prompt=prompt,
                                                    size=self.size,
                                                    response_format="b64_json",
                                                    n=1,
                                                    )
                else:
                    response = client.images.generate(model=self.txt2img_model,
                                                    prompt=prompt,
                                                    size=self.size,
                                                    quality=self.quality,
                                                    response_format="b64_json",
                                                    n=1,
                                                    )
            except openai.OpenAIError as e:
                if e.code == "sanitizer_server_error":
                    continue
                else:
                    raise e
            break
        return response

    def get_cost(self):
        return self.price

    def _cost(self,n,quality,size,model):
        if model == "dall-e-3":
            if quality == "standard":
                if size == "1024x1024":
                    return 0.04 * n
                else:
                    return 0.08 * n
            else:
                if size == "1024x1024":
                    return 0.08 * n
                else:
                    return 0.12 * n
        elif model == "dall-e-2":
            if size == "256x256":
                return 0.016 * n
            elif size == "512x512":
                return 0.018 * n
            else:
                return 0.02 * n

    def text2img(self, prompt):
        if isinstance(self.client, list):
            pointer = 0
            client = self.client[pointer]
            try:
                response = self._get_response(client,prompt)
            except openai.RateLimitError as e:
                if pointer < len(self.client) - 1:
                    pointer += 1
                    client = self.client[pointer]
                    response = self._get_response(client, prompt)
                else:
                    raise e
        else:
            response = self._get_response(self.client, prompt)
        self.completion_images += len(response.data)
        self.price += self._cost(len(response.data),self.quality,self.size,self.txt2img_model)
        import base64
        from io import BytesIO
        decoded_bytes_list = [base64.b64decode(response.data[i].b64_json) for i in range(len(response.data))]
        img = [Image.open(BytesIO(decoded_bytes_list[i])) for i in range(len(response.data))]
        return img[0]
    def image_caption(self, image, prompt, is_url = True):
        if not is_url:
            image = self.encode_image(image)
        if isinstance(self.client, list):
            pointer = 0
            client = self.client[pointer]
            try:
                response = self._get_caption(client, image, prompt, is_url)
            except openai.RateLimitError as e:
                if pointer < len(self.client) - 1:
                    pointer += 1
                    client = self.client[pointer]
                    response = self._get_caption(client, image, prompt, is_url)
                else:
                    raise e
        else:
            response = self._get_caption(self.client, image, prompt, is_url)
        return response
    
    
    @staticmethod
    def encode_image(image_input, is_base64: bool = False):
        import base64
        import io
        import numpy as np
        if is_base64:
            return image_input
        if isinstance(image_input, str):
            # Input is a file path
            with open(image_input, "rb") as image_file:
                image_data = image_file.read()
        elif isinstance(image_input, Image.Image):
            # Input is a PIL Image
            buffered = io.BytesIO()
            image_input.save(buffered, format="PNG")
            image_data = buffered.getvalue()
        elif isinstance(image_input, bytes):
            # Input is bytes
            image_data = image_input
        elif isinstance(image_input, np.ndarray):
            # Input is a NumPy array
            image = Image.fromarray(image_input.astype('uint8'))
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            image_data = buffered.getvalue()
        elif isinstance(image_input, torch.Tensor):
            # Input is a PyTorch tensor
            image = image_input.permute(1, 2, 0).numpy()  # Assuming the tensor shape is (C, H, W)
            image = Image.fromarray((image * 255).astype('uint8'))
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            image_data = buffered.getvalue()
        else:
            raise ValueError("Unsupported image input type")

        return base64.b64encode(image_data).decode("utf-8")


  