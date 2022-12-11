import azure.functions as func
import logging
from diffusers import StableDiffusionPipeline
import uuid 

app = func.FunctionApp()

# @app.function_name(name="NewImgTransform")
# @app.queue_trigger(arg_name="msg", queue_name="img-transform",
#                    connection="AzureWebJobsStorage")  
# @app.read_blob(arg_name="obj", path="transform/{idblob}.jpg", connection="AzureWebJobsStorage")
# def img2img(msg: func.QueueMessage,obj: func.InputStream):
#     logging.info('Python queue trigger processed an event: %s',
#                  msg.get_body().decode('utf-8'))

@app.function_name(name="NewImgCreate")
@app.queue_trigger(arg_name="msg", queue_name="img-create",
                   connection="AzureWebJobsStorage")  
def txt2img(msg: func.QueueMessage):
    logging.info('Python queue trigger processed an event: %s',
                msg.get_body().decode('utf-8'))
    
    #pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
    pipe = StableDiffusionPipeline.from_pretrained("/models/models/stable-diffusion-v1-5")
    
    prompt = msg.get_body().decode('utf-8')
    image = pipe(prompt,num_inference_steps=20).images[0]  
    idfile =str(uuid.uuid4())
    image.save(idfile+".png")
    


# Learn more at aka.ms/pythonprogrammingmodel

# Get started by running the following code to create a function using a HTTP trigger.

# @app.function_name(name="HttpTrigger1")
# @app.route(route="hello")
# def test_function(req: func.HttpRequest) -> func.HttpResponse:
#      logging.info('Python HTTP trigger function processed a request.')
# 
#      name = req.params.get('name')
#      if not name:
#         try:
#             req_body = req.get_json()
#         except ValueError:
#             pass
#         else:
#             name = req_body.get('name')
#
#      if name:
#         return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
#      else:
#         return func.HttpResponse(
#              "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
#              status_code=200
#         )