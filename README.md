# AIRi-TV

The  research dissemination system for AIRi. It's made by a fusion of Mixture of Models to converstation based on a research paper, with just 5s of author speech reference, a picture with the author and the article itself.

Made with ❤️ for the Artificial Intelligence Research Institute at the Technical University of Cluj-Napoca.

## SETUP:

IMPORTANT:
Before you continue, make sure you link your HuggingFace account with the machine you work with and ffmpeg installed into your docker container. To use Llama-3.1-8B-Instruct (as used in this repo), request access from Meta for the model checkpoint [here](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct).

### To create all the venvs and meet the requirements of each model and the bash script that does the full generation:


```
git clone https://github.com/davidcombei/AIRi-TV.git
cd AIRi-TV/
mkdir assets/audio/
mkdir assets/video/

conda create -yn llama python==3.11.14
conda activate llama
pip install -r requirements_LLM.txt
conda deactivate 

conda create -yn chatterbox python==3.11
conda activate chatterbox
pip install -r requirements_TTS.txt
conda deactivate 

conda create -yn sadtalker python==3.8
conda activate sadtalker
pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113
conda install -y ffmpeg
pip install -r requirements_VisualModel.txt
conda deactivate 
```

After your venvs are created and ready, you need to get the checkpoints for SadTalker and the enhancer (gfpgan) from [here](https://drive.google.com/drive/folders/1loOFWGCYoBdCn1lRXPqNlBrI3VOcKjGV?usp=sharing).
NOTE: I do not own these checkpoints, these are made in this [Github Repo](https://github.com/OpenTalker/SadTalker)
Move both directories into your cloned git repo and run:
```
mv checkpoints/ VisualModel/SadTalker/
```
Upload your image, audio and article into `assets/` directory.

Final step, run:
```
./run_dissemination.sh assets/your_article.pdf assets/your_image.png assets/your_audio.wav
```
Wait for the system to create your video. The final output will be saved as: `assets/video/articleName_podcast.mp4`.

Enjoy! :)



