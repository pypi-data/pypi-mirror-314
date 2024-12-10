import os 
from PIL import Image
import torch
from diffusers.utils import load_image, check_min_version
from .controlnet_flux import FluxControlNetModel
from .transformer_flux import FluxTransformer2DModel
from .pipeline_flux_controlnet_inpaint import FluxControlNetInpaintingPipeline
import spaces 
import huggingface_hub

@spaces.GPU()
def process(input_image_editor,
            prompt,
            negative_prompt,
            controlnet_conditioning_scale,
            guidance_scale,
            seed,
            num_inference_steps,
            true_guidance_scale            
            ):
    huggingface_hub.login(os.getenv('HF_TOKEN_FLUX'))

    check_min_version("0.30.2")
    transformer = FluxTransformer2DModel.from_pretrained(
            "black-forest-labs/FLUX.1-dev", subfolder='transformer', torch_dytpe=torch.bfloat16
        )


    # Build pipeline
    controlnet = FluxControlNetModel.from_pretrained("alimama-creative/FLUX.1-dev-Controlnet-Inpainting-Beta", torch_dtype=torch.bfloat16)
    pipe = FluxControlNetInpaintingPipeline.from_pretrained(
        "black-forest-labs/FLUX.1-dev",
        controlnet=controlnet,
        transformer=transformer,
        torch_dtype=torch.bfloat16
    ).to("cuda")
    pipe.transformer.to(torch.bfloat16)
    pipe.controlnet.to(torch.bfloat16)
    image = input_image_editor['background']
    mask = input_image_editor['layers'][0]
    size = (768, 768)
    image_or = image.copy()
    
    image = image.convert("RGB").resize(size)
    mask = mask.convert("RGB").resize(size)
    generator = torch.Generator(device="cuda").manual_seed(seed)
    result = pipe(
    prompt=prompt,
    height=size[1],
    width=size[0],
    control_image=image,
    control_mask=mask,
    num_inference_steps=num_inference_steps,
    generator=generator,
    controlnet_conditioning_scale=controlnet_conditioning_scale,
    guidance_scale=guidance_scale,
    negative_prompt=negative_prompt,
    true_guidance_scale=true_guidance_scale
    ).images[0]

    return result.resize((image_or.size[:2]))

