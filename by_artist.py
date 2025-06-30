import os

import yt_dlp

artistas = [
    "Gustavo Lima",
]

PASTA_DESTINO = "downloads"
TEMPO_MAXIMO = 8 * 60  # 8 minutos em segundos
TEMPO_MINIMO = 80  # 80 segundos
PALAVRAS_PROIBIDAS = ["greatest", "hits", "full album", "best of", "the best"]

def eh_compilacao(titulo, duracao):
    titulo_lower = titulo.lower()
    return (
        any(p in titulo_lower for p in PALAVRAS_PROIBIDAS)
        or duracao > TEMPO_MAXIMO
        or duracao < TEMPO_MINIMO
    )

def baixar_top_filtrado(artista):
    print(f"\nBuscando top músicas de: {artista}")
    query = f"ytsearch20:{artista}"

    ydl_opts = {
    'format': 'best',  # garante vídeo + áudio juntos
    'noplaylist': True,
    'outtmpl': os.path.join(PASTA_DESTINO, '%(title)s.%(ext)s'),
    'quiet': True,
    'no_warnings': True,
    }

    musicas_validas = []

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            for entrada in info['entries']:
                if not entrada:
                    continue
                titulo = entrada['title']
                duracao = entrada['duration']
                url = entrada['webpage_url']

                if not eh_compilacao(titulo, duracao):
                    musicas_validas.append(url)
                    print(f"Aceita: {titulo} ({duracao}s)")
                else:
                    print(f"Ignorada: {titulo} ({duracao}s)")

                if len(musicas_validas) == 20:
                    break

        if not musicas_validas:
            print(f"Nenhuma música individual válida encontrada para '{artista}'")
            return

        print(f"Baixando {len(musicas_validas)} músicas...")

        download_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
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

        os.makedirs(PASTA_DESTINO, exist_ok=True)

        with yt_dlp.YoutubeDL(download_opts) as ydl:
            ydl.download(musicas_validas)

        print(f"{len(musicas_validas)} músicas baixadas com sucesso!")

    except Exception as e:
        print(f"Erro ao baixar músicas de '{artista}': {e}")

def main():

    for artista in artistas:
        baixar_top_filtrado(artista)

if __name__ == "__main__":
    main()
