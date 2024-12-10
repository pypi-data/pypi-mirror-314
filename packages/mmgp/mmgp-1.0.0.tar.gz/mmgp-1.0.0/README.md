**------------------ Memory Management for the GPU Poor by DeepBeepMeep ------------------**

This module contains multiples optimisations so that models such as Flux (and derived), Mochi, CogView, HunyuanVideo, ...  run smoothly on a 24 GB GPU limited card 
This a replacement for the accelerate library that should in theory manage offloading, but doesn't work properly with models that are loaded / unloaded several times in a pipe (eg VAE) 

Requirements:
- GPU: RTX 3090/ RTX 4090
- RAM: minimum 48 GB, recommended 64 GB 

It is almost plug and play and just needs to be invoked from the main app just after the model pipeline has been created.
1) First make sure that the pipeline explictly loads the models in the CPU device 
  for instance: pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-schnell", torch_dtype=torch.bfloat16).to("cpu")
2) Once every potential Lora has been loaded and merged, add the following lines:
  from mmgp import offload
  offload.me(pipe)
If you don't have enough RAM you may disable RAM pinning but model switching option pinInRAM= False
Sometime there isn't an explicit pipe object as each submodel is loaded separately in the main app. If this is the case, you need to create a dictionary that manually maps all the models^.

For instance :
for flux derived models: pipe = { "text_encoder": clip, "text_encoder_2": t5, "transformer": model, "vae":ae }
for mochi: pipe = { "text_encoder": self.text_encoder, "transformer": self.dit, "vae":self.decoder }

Please note that there should be always one model whose Id is 'transformer'. It is corresponds to the main image / video model which usually needs to be quantized (this is done by default)

Becareful, lots of models uses the T5 XXL as a text encoder. However, quite often their corresponding pipeline configuratons points at the official Google T5 XXL repository 
where there is a huge 40GB model to download and load. It is cumbersorme as it is a 32 bits model and contains the decoder part of T5 that is not used. 
I suggest you use instead one of the 16 bits encoder only version available around, for instance:
text_encoder_2 = T5EncoderModel.from_pretrained("black-forest-labs/FLUX.1-dev", subfolder="text_encoder_2", torch_dtype=torch.float16)

You are free to use my code as long you give me proper credits. You may contact me on twitter @deepbeepmeep

Credits 
-------
Huggingface / accelerate for the hooking examples
Huggingface / quanto for their very useful quantizer
gau-nernst for his Pinnig RAM examples