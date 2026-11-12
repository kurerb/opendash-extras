"""Monta este repositório a partir da instalação do Herbert: copia as traduções (lang/<código>) e as artes em HD
(assets/ui) que são trabalho dele, e deixa de fora os arquivos originais do jogo e a dublagem PT-BR.

uso: python ferramentas/montar.py   (rodar de novo sempre que as traduções ou as artes mudarem)
"""
import fnmatch
import shutil
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
INSTALACAO = Path(r"F:\Ports e Recomps\Mega Man Legends 2 (OpenDash)")
CODIGO = Path(r"C:\opendash-hd")

# o que vai de cada pacote de idioma
PACOTE_PASTAS = ["msg", "exe", "art"]
PACOTE_ARQUIVOS = ["font.bin", "widths.bin", "charset.bin", "font.txt", "legendas*.tsv"]
# nunca vai: vozes e efeitos (originais do disco americano ou da dublagem), o patch da dublagem, cópias de segurança,
# o manifest.json (caminhos absolutos do computador do Herbert)
NUNCA = ["snd", "snd_restored", "sfx", "*.vcdiff", "manifest.json", "*.bak", "*.antes*", "*.bak-*"]
# pacotes com o texto original do jogo (roteiro americano / japonês): só as legendas
SO_LEGENDAS = {"en", "jp"}

# as artes em HD (assets/ui da pasta de código); a fonte e os textos dos menus vão pelo código (PRs)
ARTES = ["credits", "flags", "title", "dualshock.svg", "language.svg", "options_junction.svg", "hand_fill.png", "hand_edge.png"]
# ainda sem aprovação do Herbert (logo da CAPCOM: marca registrada, decidir antes)
FORA_POR_ENQUANTO = ["capcom_logo.svg"]
# nunca vão (uso pessoal do Herbert: arte oficial, escaneados, imagens baixadas): assets/ui/extras, assets/ui/gallery,
# assets/ui/credits/fundo.png
# russo e chinês tradicional: depois (Herbert, 11/11)
NUNCA += ["c12_*", "c19_*", "zhhk.svg",  # cartões dos créditos com logos de terceiros (漢検) e o da CAPCOM
          "zhhk", "fundo.png", "logo_mml2.png", "logo_rd2.png", "logo_rd2s.png", "capcom_logo.*"]
# também fora: assets/ui/mission (faixas de missão), dualshock.png (origem desconhecida), backdrop_tile.png (arte do
# Doni Arts: só com a permissão dele), assets/ui/extras, assets/ui/gallery


def nunca(nome):
    return any(fnmatch.fnmatch(nome, p) for p in NUNCA)


def copiar(origem, destino):
    if origem.is_dir():
        for f in sorted(origem.rglob("*")):
            if f.is_file() and not any(nunca(p) for p in f.relative_to(origem).parts):
                alvo = destino / f.relative_to(origem)
                alvo.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, alvo)
    elif not nunca(origem.name):
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origem, destino)


def main():
    lang_destino = AQUI / "lang"
    ui_destino = AQUI / "assets" / "ui"
    for d in (lang_destino, ui_destino):
        if d.exists():
            shutil.rmtree(d)
    total = 0
    # as traduções vão no repositório do OpenDash (translations/); aqui só com --com-idiomas
    pacotes = sorted(p for p in (INSTALACAO / "lang").iterdir() if p.is_dir()) if '--com-idiomas' in sys.argv else []
    for pacote in pacotes:
        codigo = pacote.name
        itens = [] if codigo in SO_LEGENDAS else [pacote / n for n in PACOTE_PASTAS]
        for padrao in (["legendas*.tsv"] if codigo in SO_LEGENDAS else PACOTE_ARQUIVOS):
            itens += sorted(pacote.glob(padrao))
        for item in itens:
            if item.exists():
                copiar(item, lang_destino / codigo / item.name)
        n = sum(1 for f in (lang_destino / codigo).rglob("*") if f.is_file()) if (lang_destino / codigo).exists() else 0
        total += n
        print(f"lang/{codigo}: {n} arquivos")
    for nome in ARTES:
        origem = CODIGO / "assets" / "ui" / nome
        if origem.exists():
            copiar(origem, ui_destino / nome)
            print(f"assets/ui/{nome}")
        else:
            print(f"(faltando) assets/ui/{nome}", file=sys.stderr)
    print(f"{total} arquivos de idioma; fora por enquanto: {', '.join(FORA_POR_ENQUANTO)}")


if __name__ == "__main__":
    main()
