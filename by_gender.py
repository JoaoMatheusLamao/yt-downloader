import os

import yt_dlp

PASTA_DESTINO = "downloads"
TEMPO_MAXIMO = 8 * 60
TEMPO_MINIMO = 80  # 80 segundos
PALAVRAS_PROIBIDAS = ["greatest", "hits", "full album", "best of", "the best"]
ARQUIVO_BAIXADOS = "baixados.txt"

generos = ["internacional anos 90"]

def carregar_baixados():
    if not os.path.isfile(ARQUIVO_BAIXADOS):
        return set()
    with open(ARQUIVO_BAIXADOS, "r", encoding="utf-8") as f:
        return set(linha.strip() for linha in f)

def salvar_baixados(urls):
    with open(ARQUIVO_BAIXADOS, "a", encoding="utf-8") as f:
        for url in urls:
            f.write(url + "\n")

def eh_compilacao(titulo, duracao):
    titulo_lower = titulo.lower()
    return any(p in titulo_lower for p in PALAVRAS_PROIBIDAS) or duracao > TEMPO_MAXIMO or duracao < TEMPO_MINIMO

def baixar_top_50_ignorando_baixados(genero):
    print(f"\nBuscando top 25 músicas do gênero: {genero} (filtrando já baixados)")
    query = f"ytsearch25:{genero}"

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
    }

    baixados = carregar_baixados()
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

                if url in baixados:
                    print(f"Ignorando já baixado: {titulo}")
                    continue

                if not eh_compilacao(titulo, duracao):
                    musicas_validas.append(url)
                    print(f"Aceita: {titulo} ({duracao}s)")
                else:
                    print(f"Ignorada: {titulo} ({duracao}s)")

                if len(musicas_validas) == 25:
                    break

        if not musicas_validas:
            print(f"Nenhuma música válida nova encontrada para o gênero '{genero}'")
            return

        print(f"Baixando {len(musicas_validas)} músicas novas...")

        download_opts = {
            'format': 'best',  # garante vídeo + áudio juntos
            'noplaylist': True,
            'outtmpl': os.path.join(PASTA_DESTINO, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
        }

        os.makedirs(PASTA_DESTINO, exist_ok=True)

        with yt_dlp.YoutubeDL(download_opts) as ydl:
            ydl.download(musicas_validas)

        salvar_baixados(musicas_validas)

        print(f"{len(musicas_validas)} músicas baixadas com sucesso!")

    except Exception as e:
        print(f"Erro ao baixar músicas do gênero '{genero}': {e}")

def main():

    for genero in generos:
        baixar_top_50_ignorando_baixados(genero)

if __name__ == "__main__":
    main()
