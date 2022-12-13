import logging

import azure.functions as func
import logging
from diffusers import StableDiffusionPipeline
import uuid 
import io
from PIL import Image

def main(msg: func.QueueMessage,outputblob:func.Out[func.InputStream]) -> None:
    logging.info('Python queue trigger function processed a queue item: %s',
                 msg.get_body().decode('utf-8'))
    pipe = StableDiffusionPipeline.from_pretrained("/models/models/stable-diffusion-v1-5")
    
    prompt = msg.get_body().decode('utf-8')
    image = pipe(prompt,num_inference_steps=20).images[0]  
    idfile =str(uuid.uuid4())
    dataout = io.BytesIO()

    image.save(dataout,'jpeg')
    dataout.seek(0)
    outputblob.set(dataout)
