# serverless-stabledif


Serverless Stable Diffusion 

Use Azure functions to generate images with txt2img using CPU 
It uses the hugging face diffusers library https://github.com/huggingface/diffusers
with Stable Diffusion Model 
Tested with 1.5 model  https://huggingface.co/runwayml/stable-diffusion-v1-5  
but it should works with other versions (1.4, 2.0, 2.1)
 
You have to create an Azure Function application in App service or using Premium Plan because 
Stable Diffusion inference needs something like 7Go ram to create content. 

In your storage account create an Azure File Share to cache models 
And attach an azure file share to you azure function app. 

$resourcegroup=stablediffusion
$namefunc = stablediffusion
$storageaccountname=stablediffusion
$storagekey
az webapp config storage-account add \
--resource-group $resourcegroup \
--name $namefunc \
--custom-id modelsmount \
--storage-type AzureFiles \
--share-name models \
--account-name  $storageaccountname \
--mount-path "/models" \
--access-key $storagekey

Build the docker image push it to an Azure Container Registry and deploy the image to your azure function app

Don't forget to download the diffusers model an put it into the models/stable-diffusion-v1-5 folder into the azure file share. 

And you're ready to generate content by simply put the prompt in an azure queue message 



