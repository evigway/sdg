from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
import torch

repo_id = "stabilityai/stable-diffusion-2-base"
pipe = DiffusionPipeline.from_pretrained(repo_id, torch_dtype=torch.float16, variant="fp16")

pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe = pipe.to("cuda")

prompt = "Military tank being constructed magically"
image = pipe(prompt, num_inference_steps=25).images[0]
image.save('output/tank_image_icon.png')

# import torch
# from diffusers import StableDiffusion3Pipeline
#
# pipe = StableDiffusion3Pipeline.from_pretrained("stabilityai/stable-diffusion-2", torch_dtype=torch.float16)
# pipe.to("cuda")
#
# image = pipe(
#     prompt="Realistic Army tanks from first person view in a marshy terrain faraway",
#     negative_prompt="",
#     num_inference_steps=28,
#     height=512,
#     width=512,
#     guidance_scale=7.0,
# ).images[0]
#
# image.save("tank_image_4.png")