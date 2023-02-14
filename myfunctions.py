from pytube import YouTube
from pathlib import Path,PurePath
import os

#sim, essa parte do codigo ta muito bagunçada
#sim, eu vou arrumar e estrutura um dia
#não, eu não sei que dia é esse


#funções auxiliares
def change_extension(nome_arq, substituicoes):
    path = Path(nome_arq)
    if path.suffix in substituicoes: # se a extensão deve ser substituída
        return path.with_suffix(substituicoes[path.suffix]).name
    return nome_arq

def delete_FileOnDir(path):
    lista=os.listdir(path)
    for item in lista:
        os.remove(os.path.join(path,item))
    pass

def create_dir(id,user,dirname):
    #cria pasta
    if user == None:
        user='Desconhecido'
    path=os.path.join(os.path.expanduser('~'),"Documents","Server","Temp",f"{id} @{user}",dirname)
    if not os.path.isdir(path):
        os.makedirs(path)
    
    return path


#funções principais 
###########################BAIXAR COISA DO YOUTUBE
def info_media(link):
    yt=YouTube(link)
    info={
        'title':yt.title,
        'duration':yt.length,
        'author':yt.author
    }

    return info

def download_audio(user,id,link):
    #create dir
    path=create_dir(id,user,'audio')
    #Download Audio | baixa o audio em formato mp4
    mp4_audio = YouTube(link).streams.get_audio_only().download(path)
    #Change to .mp4 to .mp3
    audio_path=PurePath(mp4_audio) 
    audio_path=str(audio_path.with_suffix('.mp3'))
    os.rename(mp4_audio,audio_path)

    return audio_path

def download_video(user,id,link):
    #create dir
    path_video=create_dir(id,user,'video')
    #Download Video
    mp4_video = YouTube(link).streams.get_highest_resolution().download(path_video)
    audio_path=PurePath(mp4_video) 
    audio_path=str(audio_path.with_suffix('.mp4'))

    return mp4_video
    

