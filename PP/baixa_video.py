from pytube import YouTube

def baixar_video_mais_alta(link):
    try:
        yt = YouTube(link)
        
        # Seleciona o stream com maior resolução em vídeo + áudio (progressive)
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

        if video:
            print(f"Baixando: {yt.title}")
            print(f"Resolução escolhida: {video.resolution}")
            video.download()
            print("✅ Download concluído!")
        else:
            print("🚫 Não foi possível encontrar um stream compatível.")
    except Exception as e:
        print(f"❌ Erro ao baixar o vídeo: {e}")

# Exemplo de uso
link_do_video = input("Cole o link do vídeo aqui: ")
baixar_video_mais_alta(link_do_video)