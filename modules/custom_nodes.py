import numpy as np
from PIL import Image
from gfpgan import GFPGANer
from .tools import tensor_to_pil, pil_to_tensor


class GFPGANImage:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "upscale_by": ("FLOAT", {"default": 2, "min": 0.05, "max": 4, "step": 0.05}),
                "bg_upsampler": (['none', 'realesrgan'], ),
                "image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "upscale"
    CATEGORY = "mc_tools/upscaling"

    def upscale(self, upscale_by, bg_upsampler, image):
        if bg_upsampler == 'realesrgan':
            import torch
            if not torch.cuda.is_available():  # CPU
                import warnings
                warnings.warn('The unoptimized RealESRGAN is slow on CPU. We do not use it. '
                              'If you really want to use it, please modify the corresponding codes.')
                background_upsampler = None
            else:
                from basicsr.archs.rrdbnet_arch import RRDBNet
                from realesrgan import RealESRGANer
                model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
                background_upsampler = RealESRGANer(
                    scale=2,
                    model_path='https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth',
                    model=model,
                    tile=400,
                    tile_pad=10,
                    pre_pad=0,
                    half=True)  # need to set False in CPU mode
        else:
            background_upsampler = None

        gan = GFPGANer(model_path="https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth", upscale=upscale_by, bg_upsampler=background_upsampler)
        cropped_faces, restored_faces, restored_img = gan.enhance(np.array(tensor_to_pil(image)))
        tensor = pil_to_tensor(Image.fromarray(restored_img, mode="RGB"))
        return (tensor, )


NODE_MAPPINGS = {
    "MCGFPGANImage": GFPGANImage,
}

NODE_NAME_MAPPINGS = {
    "MCGFPGANImage": "MC-Tools / GFPGAN Image",
}