import os
import copy
import time
from collections import deque

pontos_iniciais = 100
custo_jogada    = 1
custo_dica      = 5

mapa_1 = {
    "nome": "Conserto de Carro (6x6) — Iniciante",
    "arquivo_ranking": "ranking_iniciante.txt",
    "tamanho": 6,
    "suspeitos": [
        {
            "id": "A", "nome": "Antônio", "emoji": "🔴",
            "dica_inicial": "Está próximo a um 🚗",
            "dicas_extras": [
                "Está na metade inferior do mapa (linhas 4–5)",
                "Linha 4, coluna 2 — entre os carros",
            ]
        },
        {
            "id": "B", "nome": "Bruno", "emoji": "🟤",
            "dica_inicial": "Está próximo a um barril de oleo (🔘)",
            "dicas_extras": [
                "Está na linha mais baixa do mapa (linha 5)",
                "Linha 5, coluna 0 — canto inferior esquerdo",
            ]
        },
        {
            "id": "C", "nome": "Cristina", "emoji": "🟣",
            "dica_inicial": "Está próxima a uma cadeira (💺)",
            "dicas_extras": [
                "Está na linha do topo (linha 0)",
                "Linha 0, coluna 1 — ao lado da cadeira",
            ]
        },
        {
            "id": "D", "nome": "Diana", "emoji": "🟡",
            "dica_inicial": "Está próxima a uma estante (📚), mas não há ninguém ao redor",
            "dicas_extras": [
                "Está na metade central-direita (linhas 2–3, colunas 3–5)",
                "Linha 3, coluna 4 — ao lado da estante",
            ]
        },
        {
            "id": "E", "nome": "Eduardo", "emoji": "🟢",
            "dica_inicial": "Está numa área aberta, sem ícone ao lado",
            "dicas_extras": [
                "Está na linha 1, metade direita",
                "Linha 1, coluna 5 — canto superior direito",
            ]
        },
        {
            "id": "V", "nome": "Vitor", "emoji": "💀",
            "dica_inicial": "A VÍTIMA — descubra quem estava sozinho no recinto com ele",
            "dicas_extras": [
                "Está na metade superior-direita (linhas 2–3, colunas 3–5)",
                "Linha 2, coluna 3 — ao lado de uma 📚",
            ]
        },
    ],
    "cenario": [
        ['⬜', '💺', '⬜', '⬜', '⬜', '📚'],
        ['⬜', '⬜', '⬜', '⬜', '⬜', '⬜'],
        ['⬜', '⬜', '⬜', '📚', '💺', '💺'],
        ['⬜', '⬜', '⬜', '⬜', '📚', '📚'],
        ['⬜', '🚗', '🚗', '🔘', '⬜', '⬜'],
        ['⬜', '🔘', '⬜', '🚗', '🚗', '⬜'],
    ],
    "solucao": {
        "C": (0, 1),
        "E": (1, 5),
        "V": (2, 3),
        "D": (3, 4),
        "A": (4, 2),
        "B": (5, 0),
    },
    "culpado": "D",
}

mapa_2 = {
    "nome": "O Jardim do Quintal (9x9) — Intermediário",
    "arquivo_ranking": "ranking_intermediario.txt",
    "tamanho": 9,
    "suspeitos": [
        {
            "id": "C", "nome": "Caryn", "emoji": "🟣",
            "dica_inicial": "Está próxima a uma arvore (🌲)",
            "dicas_extras": [
                "Está na linha do topo (linha 0)",
                "Linha 0, coluna 1 — ao lado da arvore",
            ]
        },
        {
            "id": "G", "nome": "Gilbert", "emoji": "🔶",
            "dica_inicial": "Está próximo a uma flor (🌸)",
            "dicas_extras": [
                "Está na linha 1, metade direita",
                "Linha 1, coluna 8 — canto superior direito",
            ]
        },
        {
            "id": "B", "nome": "Bruce", "emoji": "🟤",
            "dica_inicial": "Está encostado na parede esquerda (coluna 0)",
            "dicas_extras": [
                "Está na metade superior (linhas 0–3)",
                "Linha 2, coluna 0 — parede esquerda",
            ]
        },
        {
            "id": "E", "nome": "Elyse", "emoji": "🟢",
            "dica_inicial": "Está próxima a uma cadeira (💺)",
            "dicas_extras": [
                "Está na metade central (linhas 3–5)",
                "Linha 3, coluna 5 — próxima à cadeira (💺) da linha 4",
            ]
        },
        {
            "id": "H", "nome": "Holden", "emoji": "🔷",
            "dica_inicial": "Não está próximo a nenhum ícone",
            "dicas_extras": [
                "Está na linha central do mapa (linha 4)",
                "Linha 4, coluna 3 — área aberta central",
            ]
        },
        {
            "id": "A", "nome": "Aaron", "emoji": "🔵",
            "dica_inicial": "Está na metade inferior do mapa (linhas 5–8)",
            "dicas_extras": [
                "Está na metade central (colunas 3–6)",
                "Linha 5, coluna 4 — área aberta",
            ]
        },
        {
            "id": "F", "nome": "Franklin", "emoji": "🟠",
            "dica_inicial": "Está próximo a uma estante (📚)",
            "dicas_extras": [
                "Está na metade inferior (linhas 6–8)",
                "Linha 6, coluna 2 — próximo à estante (📚) da linha 6",
            ]
        },
        {
            "id": "D", "nome": "Denise", "emoji": "🟡",
            "dica_inicial": "Está na metade inferior do mapa (linhas 6–8)",
            "dicas_extras": [
                "Está na metade direita (colunas 5–8)",
                "Linha 7, coluna 6 — área aberta",
            ]
        },
        {
            "id": "V", "nome": "Violet", "emoji": "💀",
            "dica_inicial": "A VÍTIMA — descubra quem estava sozinho no recinto com ela",
            "dicas_extras": [
                "Está na linha mais baixa (linha 8), metade direita",
                "Linha 8, coluna 7 — ao lado de uma estante (📚)",
            ]
        },
    ],
    "cenario": [
        ['⬜', '🌲', '⬜', '⬜', '💧', '⬜', '🌲', '⬜', '🌸'],
        ['⬜', '⬜', '⬜', '💧', '💧', '⬜', '⬜', '⬜', '🌸'],
        ['⬜', '⬜', '💧', '💧', '⬜', '🌲', '⬜', '⬜', '⬜'],
        ['📚', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '🌸', '⬜'],
        ['⬜', '⬜', '⬜', '⬜', '⬜', '💺', '⬜', '⬜', '💺'],
        ['⬜', '🌸', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜'],
        ['⬜', '⬜', '⬜', '📚', '🎵', '📚', '⬜', '⬜', '⬜'],
        ['⬜', '⬜', '⬜', '⬜', '🟫', '⬜', '⬜', '⬜', '⬜'],
        ['💺', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '📚', '⬜'],
    ],
    "solucao": {
        "C": (0, 1),
        "G": (1, 8),
        "B": (2, 0),
        "E": (3, 5),
        "H": (4, 3),
        "A": (5, 4),
        "F": (6, 2),
        "D": (7, 6),
        "V": (8, 7),
    },
    "culpado": "D",
}

mapa_3 = {
    "nome": "O Jardim Botanico (12x12) — Avançado",
    "arquivo_ranking": "ranking_avancado.txt",
    "tamanho": 12,
    "suspeitos": [
        {
            "id": "C", "nome": "Caio", "emoji": "🟤",
            "dica_inicial": "Estava ao lado de uma mesa (🟫)",
            "dicas_extras": [
                "Está na area de Informacoes (linha 0, colunas 6–7)",
                "Linha 0, coluna 6 — ao lado da mesa",
            ]
        },
        {
            "id": "A", "nome": "Ana", "emoji": "🔴",
            "dica_inicial": "Estava uma linha abaixo da area de Informacoes",
            "dicas_extras": [
                "Está na linha 1, metade direita",
                "Linha 1, coluna 9 — caminho livre",
            ]
        },
        {
            "id": "D", "nome": "Daniela", "emoji": "🟢",
            "dica_inicial": "Estava num caminho (⬜), estava sozinha",
            "dicas_extras": [
                "Está na metade superior (linhas 2–3)",
                "Linha 2, coluna 2 — caminho livre do Arboreto",
            ]
        },
        {
            "id": "B", "nome": "Bruna", "emoji": "🟡",
            "dica_inicial": "Estava sentada numa cadeira (💺) no Arboreto",
            "dicas_extras": [
                "Está na linha 3, metade esquerda",
                "Linha 3, coluna 0 — proximo à cadeira (💺) da coluna 2",
            ]
        },
        {
            "id": "G", "nome": "Guilherme", "emoji": "🔶",
            "dica_inicial": "Estava ao lado de um bonsai (🌿)",
            "dicas_extras": [
                "Está na linha 4, metade esquerda",
                "Linha 4, coluna 1 — ao lado do bonsai (🌿) na coluna 3",
            ]
        },
        {
            "id": "F", "nome": "Filipe", "emoji": "🟠",
            "dica_inicial": "Estava sozinho, sem nenhum icone ao redor",
            "dicas_extras": [
                "Está na linha 5, metade direita",
                "Linha 5, coluna 8 — area aberta sem icones",
            ]
        },
        {
            "id": "E", "nome": "Eduarda", "emoji": "🔵",
            "dica_inicial": "Estava sentada numa cadeira (💺), sozinha com um homem",
            "dicas_extras": [
                "Está na linha 6, metade esquerda",
                "Linha 6, coluna 3 — area do Gazebo",
            ]
        },
        {
            "id": "H", "nome": "Harlow", "emoji": "🔷",
            "dica_inicial": "Estava ao lado de um arbusto (🌵)",
            "dicas_extras": [
                "Está na linha 7, metade central",
                "Linha 7, coluna 4 — ao lado do arbusto (🌸)",
            ]
        },
        {
            "id": "J", "nome": "Joss", "emoji": "🔸",
            "dica_inicial": "Estava ao lado de uma vitoria-regia (🌸)",
            "dicas_extras": [
                "Está na linha 8, metade direita",
                "Linha 8, coluna 7 — ao lado da vitoria-regia (🌸)",
            ]
        },
        {
            "id": "K", "nome": "Karina", "emoji": "🔹",
            "dica_inicial": "Estava ao lado de um cacto (🌵)",
            "dicas_extras": [
                "Está na linha 9, metade central",
                "Linha 9, coluna 5 — ao lado da vitoria-regia/cacto (🌸)",
            ]
        },
        {
            "id": "I", "nome": "Ines", "emoji": "🟣",
            "dica_inicial": "Estava numa area aberta, estava sozinha",
            "dicas_extras": [
                "Está na linha 10, metade direita",
                "Linha 10, coluna 10 — area de Descanso",
            ]
        },
        {
            "id": "V", "nome": "Veronica", "emoji": "💀",
            "dica_inicial": "A VITIMA — descubra quem estava sozinho no recinto com ela",
            "dicas_extras": [
                "Está na linha mais baixa (linha 11)",
                "Linha 11, coluna 11 — canto inferior direito",
            ]
        },
    ],

    "cenario": [
        ['🌲', '🌲', '🌲', '🌲', '⬜', '⬜', '🟫', '🟫', '💺', '💺', '🌲', '🌲'],
        ['🌲', '🌲', '🌲', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '🌲', '🌲'],
        ['🌲', '🌲', '⬜', '⬜', '⬜', '⬜', '🌲', '⬜', '⬜', '💺', '🌲', '🌲'],
        ['⬜', '⬜', '💺', '⬜', '⬜', '⬜', '🌲', '⬜', '⬜', '⬜', '🌲', '🌲'],
        ['⬜', '⬜', '⬜', '🌿', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '🌲', '🌲'],
        ['⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '🌵', '🌵', '🌲'],
        ['⬜', '💺', '⬜', '⬜', '⬜', '⬜', '🌸', '🌸', '🌵', '🌵', '🌲', '🌲'],
        ['💺', '⬜', '⬜', '🌸', '🌸', '🌸', '🌸', '💧', '💧', '🌵', '🌲', '🌲'],
        ['⬜', '⬜', '🌵', '🌸', '🌵', '🌸', '⬜', '🌸', '💧', '💧', '⬜', '⬜'],
        ['🌵', '🌵', '🌵', '⬜', '⬜', '🌸', '⬜', '💧', '💧', '⬜', '⬜', '⬜'],
        ['⬜', '⬜', '🌵', '⬜', '⬜', '⬜', '⬜', '⬜', '💺', '💺', '⬜', '⬜'],
        ['⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜'],
    ],
    "solucao": {
        "C": (0,  6),
        "A": (1,  9),
        "D": (2,  2),
        "B": (3,  0),
        "G": (4,  1),
        "F": (5,  8),
        "E": (6,  3),
        "H": (7,  4),
        "J": (8,  7),
        "K": (9,  5),
        "I": (10, 10),
        "V": (11, 11),
    },
    "culpado": "E",
}

mapas = [mapa_1, mapa_2, mapa_3]


def exibir_ranking(arquivo, mapa_nome):
    print(f"\n  🏆 --- RANKING: {mapa_nome} ---")
    if not os.path.exists(arquivo):
        print("  [Ranking vazio. Seja o primeiro detetive!]")
        print("  " + "-" * 36)
        return

    ranking = []
    with open(arquivo, "r", encoding="utf-8") as f:
        blocos = f.read().split("\n\n")
        for bloco in blocos:
            if not bloco.strip():
                continue
            linhas = bloco.strip().split("\n")
            if len(linhas) >= 3:
                nome = linhas[0][7:-1].strip()
                pts = linhas[1][9:-1].strip()
                seg = linhas[2][8:-1].strip().rstrip("s").strip()
                ranking.append({"nome": nome, "pontos": int(pts), "tempo": int(seg)})

    ranking.sort(key=lambda x: (-x["pontos"], x["tempo"]))
    for i, d in enumerate(ranking[:5], 1):
        print(f"  {i}.")
        print(f"     Nome - {d['nome']};")
        print(f"     Pontos - {d['pontos']};")
        print(f"     Tempo - {d['tempo']}s;")
    print("  " + "-" * 36)


def salvar_pontuacao(nome, pontos, tempo, arquivo):
    registros = {}
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            blocos = f.read().split("\n\n")
            for bloco in blocos:
                if not bloco.strip():
                    continue
                linhas = bloco.strip().split("\n")
                if len(linhas) >= 3:
                    n = linhas[0][7:-1].strip()
                    p = linhas[1][9:-1].strip()
                    s = linhas[2][8:-1].strip().rstrip("s").strip()
                    registros[n] = (int(p), int(s))

    atual = registros.get(nome)
    if atual is None or pontos > atual[0] or (pontos == atual[0] and tempo < atual[1]):
        registros[nome] = (pontos, tempo)

    with open(arquivo, "w", encoding="utf-8") as f:
        for n, (p, s) in registros.items():
            f.write(f"Nome - {n};\n")
            f.write(f"Pontos - {p};\n")
            f.write(f"Tempo - {s}s;\n\n")


def renderizar_celula(i, j, tabuleiro, cenario):
    celula = tabuleiro[i][j]
    icone  = celula if celula is not None else cenario[i][j]
    return f" {icone} "


def exibir_tabuleiro(tabuleiro, cenario, tamanho, nome, pontos, mapa_nome, tempo=0):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"  🔍 {mapa_nome}")
    print(f"  👤 {nome.upper()}  |  ⭐ {pontos} pontos  |  ⏱️  {tempo}s\n")

    print("    " + "".join(f" {j}  " for j in range(tamanho)))
    print("   +" + "----" * tamanho + "+")
    for i in range(tamanho):
        linha_str = f" {i} |"
        for j in range(tamanho):
            linha_str += renderizar_celula(i, j, tabuleiro, cenario)
        print(linha_str + " |")
    print("   +" + "----" * tamanho + "+")


def exibir_suspeitos(suspeitos, dicas_extras_reveladas):
    print("\n  --- SUSPEITOS ---")
    for s in suspeitos:
        extras_usadas = dicas_extras_reveladas.get(s["id"], 0)
        extras_total  = len(s["dicas_extras"])
        status = f"[+{extras_usadas}/{extras_total} extras]"
        print(f"  [{s['id']}] {s['emoji']} {s['nome'].ljust(10)} {status}  {s['dica_inicial']}")
        for i in range(extras_usadas):
            print(f"            {'':10}  └ {s['dicas_extras'][i]}")
    print(f"\n  [H <ID>] Pedir dica extra  (−{custo_dica} pontos)  ex: H A")


def revelar_dica(id_suspeito, suspeitos, dicas_extras_reveladas, pontos):
    info = next((s for s in suspeitos if s["id"] == id_suspeito), None)

    if info is None:
        ids_validos = [s["id"] for s in suspeitos]
        print(f"  ID inválido. Use um destes: {ids_validos}")
        return pontos

    extras_usadas = dicas_extras_reveladas.get(id_suspeito, 0)

    if extras_usadas >= len(info["dicas_extras"]):
        print(f"  Todas as dicas extras de {info['nome']} já foram reveladas!")
        return pontos

    dicas_extras_reveladas[id_suspeito] = extras_usadas + 1
    pontos = max(0, pontos - custo_dica)
    dica   = info["dicas_extras"][extras_usadas]
    print(f"\n  Dica extra {extras_usadas + 1}/2 para {info['emoji']} {info['nome']}:")
    print(f"     \"{dica}\"")
    print(f"  (−{custo_dica} pontos)")
    return pontos


def verificar_vitoria(tabuleiro, suspeitos, solucao):
    for s in suspeitos:
        l, c = solucao[s["id"]]
        if tabuleiro[l][c] != s["emoji"]:
            return False
    return True


def errados_no_tabuleiro(tabuleiro, suspeitos, solucao):
    errados = []
    for s in suspeitos:
        l, c = solucao[s["id"]]
        if tabuleiro[l][c] != s["emoji"]:
            errados.append(s)
    return errados


def anunciar_encerramento(nome, pontos, tempo, mapa, tabuleiro):
    errados = errados_no_tabuleiro(tabuleiro, mapa["suspeitos"], mapa["solucao"])
    if not errados:
        anunciar_vitoria(nome, pontos, tempo, mapa)
        return True

    print("\n" + "=" * 48)
    print("  Caso encerrado sem solução.")
    print("=" * 48)
    print(f"  Detetive : {nome}")
    print(f"  Pontuação: {pontos} pontos")
    print(f"  Tempo    : {tempo}s")
    print(f"\n  Os seguintes suspeitos estavam na posição errada:")
    for s in errados:
        print(f"    [{s['id']}] {s['emoji']} {s['nome']}")
    print("=" * 48)
    
def anunciar_vitoria(nome, pontos, tempo, mapa):
    culpado_id = mapa["culpado"]
    culpado    = next(s for s in mapa["suspeitos"] if s["id"] == culpado_id)
    print("\n" + "=" * 48)
    print("🎉   CASO ENCERRADO COM SUCESSO!   🎉")
    print("=" * 48)
    print(f"  Mapa     : {mapa['nome']}")
    print(f"  Detetive : {nome}")
    print(f"  Pontuação: {pontos} pontos")
    print(f"  Tempo    : {tempo}s")
    print(f"\n  O culpado e {culpado['emoji']} {culpado['nome']}!")
    print(f"     Estava na célula ao lado da vitima.")
    print("=" * 48)


def selecionar_mapa():
    print("\n  ----------------------------------------")
    print("  |      🔍  BEM-VINDO AO MURDOKU  🔍    |")
    print("  ----------------------------------------\n")
    print("  Escolha o nível:\n")
    for i, mapa in enumerate(mapas, 1):
        print(f"    [{i}] {mapa['nome']}")
    print()
    while True:
        escolha = input("  >> ").strip()
        if escolha.isdigit() and 1 <= int(escolha) <= len(mapas):
            return mapas[int(escolha) - 1]
        else:
            print(f"  Digite um número entre 1 e {len(mapas)}.")


def murdoku():
    mapa         = selecionar_mapa()
    nome_usuario = input("\n  Digite seu nome de detetive: ").strip() or "Anônimo"

    tamanho             = mapa["tamanho"]
    suspeitos           = mapa["suspeitos"]
    cenario             = mapa["cenario"]
    solucao             = mapa["solucao"]
    mapa_nome           = mapa["nome"]
    arquivo_ranking     = mapa["arquivo_ranking"]

    tabuleiro              = [[None for _ in range(tamanho)] for _ in range(tamanho)]
    historico              = deque()
    dicas_extras_reveladas = {}
    pontos                 = pontos_iniciais
    inicio                 = time.time()
    jogo_ativo             = True

    while jogo_ativo:
        tempo = int(time.time() - inicio)
        exibir_tabuleiro(tabuleiro, cenario, tamanho, nome_usuario, pontos, mapa_nome, tempo)
        exibir_suspeitos(suspeitos, dicas_extras_reveladas)

        print(f"\n  COMANDOS:")
        print(f"    [L C ID]   Posicionar suspeito   ex: 4 1 A  (−{custo_jogada} ponto)")
        print(f"    [X L C]    Remover suspeito       ex: X 4 1")
        print(f"    [H ID]     Pedir dica extra       ex: H A   (−{custo_dica} pontos)")
        print(f"    [U]        Desfazer última jogada")
        print(f"    [R]        Ver ranking deste mapa")
        print(f"    [F]        Finalizar e salvar")

        entrada = input("\n  >> ").upper().split()

        if not entrada:
            continue

        comando = entrada[0]

        if comando == 'U':
            if historico:
                tabuleiro = historico.pop()
                print("  Jogada desfeita!")
            else:
                print("  Nada para desfazer!")
            input("  Pressione Enter...")
            continue

        if comando == 'R':
            exibir_ranking(arquivo_ranking, mapa_nome)
            input("  Pressione Enter...")
            continue

        if comando == 'H':
            if len(entrada) < 2:
                print("  Informe o ID do suspeito. Ex: H A")
            else:
                pontos = revelar_dica(entrada[1], suspeitos, dicas_extras_reveladas, pontos)
            input("  Pressione Enter...")
            continue

        if comando == 'F':
            tempo = int(time.time() - inicio)
            resolvido = anunciar_encerramento(nome_usuario, pontos, tempo, mapa, tabuleiro)
            if resolvido:
                salvar_pontuacao(nome_usuario, pontos, tempo, arquivo_ranking)
            exibir_ranking(arquivo_ranking, mapa_nome)
            jogo_ativo = False
            break

        if comando == 'X':
            if len(entrada) < 3:
                print("  Informe linha e coluna. Ex: X 4 1")
                input("  Pressione Enter...")
                continue
            try:
                l, c = int(entrada[1]), int(entrada[2])
                if not (0 <= l < tamanho and 0 <= c < tamanho):
                    print(f"  Linha e coluna devem estar entre 0 e {tamanho - 1}.")
                elif tabuleiro[l][c] is None:
                    print("  Essa célula ja esta vazia.")
                else:
                    historico.append(copy.deepcopy(tabuleiro))
                    removido = tabuleiro[l][c]
                    tabuleiro[l][c] = None
                    print(f"  {removido} removido da posicao ({l}, {c}).")
            except ValueError:
                print("  Use apenas numeros para linha e coluna.")
            input("  Pressione Enter...")
            continue

        elif len(entrada) == 3:
            try:
                l, c        = int(entrada[0]), int(entrada[1])
                id_suspeito = entrada[2]

                if not (0 <= l < tamanho and 0 <= c < tamanho):
                    print(f"  Linha e coluna devem estar entre 0 e {tamanho - 1}.")
                    input("  Pressione Enter...")
                    continue

                info = next((s for s in suspeitos if s["id"] == id_suspeito), None)
                if info is None:
                    print(f"  ID invalido. Use: {[s['id'] for s in suspeitos]}")
                    input("  Pressione Enter...")
                    continue

                if tabuleiro[l][c] is not None:
                    print(f"  A posicao ({l}, {c}) ja tem {tabuleiro[l][c]}.")
                    if input("  Substituir? [S/N] >> ").upper().strip() != 'S':
                        print("  Jogada cancelada.")
                        input("  Pressione Enter...")
                        continue

                historico.append(copy.deepcopy(tabuleiro))
                tabuleiro[l][c] = info["emoji"]
                pontos = max(0, pontos - custo_jogada)

                if verificar_vitoria(tabuleiro, suspeitos, solucao):
                    tempo = int(time.time() - inicio)
                    exibir_tabuleiro(tabuleiro, cenario, tamanho, nome_usuario, pontos, mapa_nome, tempo)
                    anunciar_vitoria(nome_usuario, pontos, tempo, mapa)
                    salvar_pontuacao(nome_usuario, pontos, tempo, arquivo_ranking)
                    exibir_ranking(arquivo_ranking, mapa_nome)
                    jogo_ativo = False

            except ValueError:
                print("  Use apenas numeros para linha e coluna.")
                input("  Pressione Enter...")

        else:
            print("  Comando não reconhecido.")
            input("  Pressione Enter...")


if __name__ == "__main__":
    murdoku()