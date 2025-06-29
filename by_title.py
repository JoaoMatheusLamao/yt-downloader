import os

import yt_dlp

# Lista de buscas
nomes = [
    "creep",
]

PASTA_DESTINO = "downloads"
os.makedirs(PASTA_DESTINO, exist_ok=True)
TEMPO_MAXIMO = 8 * 60  # 8 minutos em segundos
PALAVRAS_PROIBIDAS = ["greatest", "hits", "full album", "best of", "the best"]

def eh_compilacao(titulo, duracao):
    titulo_lower = titulo.lower()
    return (
        any(p in titulo_lower for p in PALAVRAS_PROIBIDAS)
        or duracao > TEMPO_MAXIMO
    )


def buscar_e_baixar(nome):
    print(f"\nBuscando: {nome}")
    query = f"ytsearch1:{nome}"

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'outtmpl': os.path.join(PASTA_DESTINO, '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            video_info = info['entries'][0]  # Primeiro resultado da busca

            titulo = video_info['title']
            url = video_info['webpage_url']
            titulo = video_info['title']
            duracao = video_info['duration']
            
            print(f"Título: {titulo}")
            print(f"URL: {url}")

            if  eh_compilacao(titulo, duracao):
                return


            # Agora baixa
            ydl.download([url])
            print(f"Baixado com sucesso!")

    except Exception as e:
        print(f"Erro ao baixar '{nome}': {e}")

# Executa a busca e download
for nome in nomes:
    buscar_e_baixar(nome)
