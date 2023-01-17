import torch
import torchvision.transforms as T
import requests
from PIL import Image
from diffusers import StableDiffusionDepth2ImgPipeline, StableDiffusionImageVariationPipeline

# def tensor_toimg(tensor):
#     """transrorm tensor to pil img"""
#     # define a transform to convert a tensor to PIL image
#     transform = T.ToPILImage()
#     #StableDiffusionDepth2ImgPipeline.decode_latents()
#     # convert the tensor to PIL image using above transform
#     img = transform(tensor)

#     return img

# def decode_img_latents(latents):
#     latents = 1 / 0.18215 * latents

#     with torch.no_grad():
#     imgs =  vae.decode(latents)

#     imgs = (imgs / 2 + 0.5).clamp(0, 1)
#     imgs = imgs.detach().cpu().permute(0, 2, 3, 1).numpy()
#     imgs = (imgs * 255).round().astype('uint8')
#     pil_images = [Image.fromarray(image) for image in imgs]
#     return pil_images

#pipe = StableDiffusionDepth2ImgPipeline.from_pretrained(
#    "stabilityai/stable-diffusion-2-depth",
    #torch_dtype=torch.float16,
#)

#pipe.to("cpu")

def tensortoi(latent):
    img=pipe.decode_latents(latent)
    img=pipe.numpy_to_pil(img)
    return img[0]

url = "http://images.cocodataset.org/val2017/000000039769.jpg"
init_image = Image.open(requests.get(url, stream=True).raw)
#
prompt = "two tigers"
n_propmt = "bad, deformed, ugly, bad anotomy"
intermediatesteps =[]
image = pipe(prompt=prompt, image=init_image, negative_prompt=n_propmt, strength=0.7,callback=lambda  step, timestep, latents: intermediatesteps.append(tensortoi(latents))).images[0]

steps= list(map(lambda step: pipe.numpy_to_pil(pipe.decode_latents(step)),intermediatesteps))

image.save("two_tigers.png")
#intermediatesteps.append(image)
#init_image.save("out2.gif", save_all=True, append_images=intermediatesteps, duration=100, loop=0)


pipevar = StableDiffusionImageVariationPipeline.from_pretrained("lambdalabs/sd-image-variations-diffusers",revision="v2.0",torch_dtype=torch.float16,)
tform = T.Compose([
    T.ToTensor(),
    T.Resize(
        (224, 224),
        interpolation=T.InterpolationMode.BICUBIC,
        antialias=False,
        ),
    T.Normalize(
      [0.48145466, 0.4578275, 0.40821073],
      [0.26862954, 0.26130258, 0.27577711]),
])
#inp = tform(image).to("cuda").unsqueeze(0)
inp = tform(init_image).unsqueeze(0)

out = pipevar(inp,num_images_per_prompt=120,num_inference_steps=35, guidance_scale=3)
#out["images"][0].save("result.jpg")
init_image.save("result.gif", save_all=True, append_images=out["images"], duration=120, loop=0)
#pipevar.to("cuda")
