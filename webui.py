import os
import random

from comfy.sd import load_checkpoint_guess_config

from nodes import (
    VAEDecode,
    KSamplerAdvanced,
    EmptyLatentImage,
    SaveImage,
    CLIPTextEncode,
)

from modules.path import modelfile_path

xl_base_filename = os.path.join(modelfile_path, 'sd_xl_base_1.0.safetensors')
xl_refiner_filename = os.path.join(modelfile_path, 'sd_xl_refiner_1.0.safetensors')

xl_base, xl_base_clip, xl_base_vae, xl_base_clipvision = load_checkpoint_guess_config(xl_base_filename)
del xl_base_clipvision

opCLIPTextEncode = CLIPTextEncode()
opEmptyLatentImage = EmptyLatentImage()
opKSamplerAdvanced = KSamplerAdvanced()

positive_conditions = opCLIPTextEncode.encode(clip=xl_base_clip, text='a handsome man in forest')[0]
negative_conditions = opCLIPTextEncode.encode(clip=xl_base_clip, text='bad, ugly')[0]

initial_latent_image = opEmptyLatentImage.generate(width=1024, height=1536, batch_size=1)[0]

samples = opKSamplerAdvanced.sample(
    add_noise="enable",
    noise_seed=random.randint(1, 2 ** 64),
    steps=25,
    cfg=9,
    sampler_name="euler",
    scheduler="normal",
    start_at_step=0,
    end_at_step=25,
    return_with_leftover_noise="enable",
    model=xl_base,
    positive=positive_conditions,
    negative=negative_conditions,
    latent_image=initial_latent_image,
)

a = 0
