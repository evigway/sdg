from diffusers import DiffusionPipeline
import torch

pipeline = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16)
pipeline.to("cuda")
image = pipeline("Realistic Army tanks from first person view in a marshy terrain faraway").images
print("Number of images:", len(image))
image[0].save("generated_image3.png")