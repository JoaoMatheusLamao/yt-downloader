import os

import yt_dlp

# Lista de buscas
nomes = [
    # Anos 90
    "I Will Always Love You - Whitney Houston",
    "My Heart Will Go On - Celine Dion",
    "Nothing Compares 2 U - Sinéad O'Connor",
    "End of the Road - Boyz II Men",
    "Because You Loved Me - Celine Dion",
    "I Don't Want to Miss a Thing - Aerosmith",
    "Kiss from a Rose - Seal",
    "I'll Make Love to You - Boyz II Men",
    "When a Man Loves a Woman - Michael Bolton",
    "More Than Words - Extreme",
    
    # Anos 2000
    "You're Still the One - Shania Twain",
    "We Belong Together - Mariah Carey",
    "Bleeding Love - Leona Lewis",
    "Make You Feel My Love - Adele",
    "Un-break My Heart - Toni Braxton",
    "Beautiful - Christina Aguilera",
    "Everything I Do (I Do It for You) - Bryan Adams",
    "Truly Madly Deeply - Savage Garden",
    "With You - Chris Brown",
    "No One - Alicia Keys",
    
    # Até 2010 (final 2000s)
    "Halo - Beyoncé",
    "Apologize - OneRepublic",
    "Love Story - Taylor Swift",
    "The Scientist - Coldplay",
    "Lucky - Jason Mraz feat. Colbie Caillat",
    "Chasing Cars - Snow Patrol",
    "Fix You - Coldplay",
    "Fallin' - Alicia Keys",
    "You Raise Me Up - Josh Groban",
    "I Don't Want to Miss a Thing - Aerosmith",
    
    # Nacional
    "Mulher de Fases - Raimundos",
    
    
    "Girls Just Want to Have Fun - Cyndi Lauper",
    "Billie Jean - Michael Jackson",
    "Like a Virgin - Madonna",
    "Wake Me Up Before You Go-Go - Wham!",
    "Sweet Dreams (Are Made of This) - Eurythmics",
    "Take On Me - a-ha",
    "Material Girl - Madonna",
    "I Wanna Dance with Somebody - Whitney Houston",
    "Footloose - Kenny Loggins",
    "Thriller - Michael Jackson",
    "Dancing in the Dark - Bruce Springsteen",
    "Every Breath You Take - The Police",
    "Livin' on a Prayer - Bon Jovi",
    "Eye of the Tiger - Survivor",
    "Don't Stop Believin' - Journey",
    "Summer of '69 - Bryan Adams",
    "Uptown Girl - Billy Joel",
    "Come On Eileen - Dexys Midnight Runners",
    "Walk Like an Egyptian - The Bangles",
    "Should I Stay or Should I Go - The Clash",
    "Sweet Child O' Mine - Guns N' Roses",
    "Jump - Van Halen",
    "You Spin Me Round (Like a Record) - Dead or Alive",
    "Take My Breath Away - Berlin",
    "Karma Chameleon - Culture Club",
    "I Melt with You - Modern English",
    "Hungry Like the Wolf - Duran Duran",
    "Tainted Love - Soft Cell",
    "Relax - Frankie Goes to Hollywood",
    "Let's Dance - David Bowie",
    "With or Without You - U2",
    "Jack & Diane - John Mellencamp",
    "Beds Are Burning - Midnight Oil",
    "Invisible Touch - Genesis",
    "The Power of Love - Huey Lewis and the News",
    "Keep on Loving You - REO Speedwagon",
    "Man in the Mirror - Michael Jackson",
    "99 Luftballons - Nena",
    "Borderline - Madonna",
    "I Want to Know What Love Is - Foreigner",
    "Boys Don't Cry - The Cure",
    "Every Rose Has Its Thorn - Poison",
]


PASTA_DESTINO = "downloads"
os.makedirs(PASTA_DESTINO, exist_ok=True)
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
