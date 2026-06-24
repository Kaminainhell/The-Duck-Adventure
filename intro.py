import pygame
import sys

WIDTH = 800
HEIGHT = 600

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

pygame.font.init()
fonte = pygame.font.Font('assets/Fonte/fonte.ttf', 30)



def intro(tela, clock):



    painel = pygame.image.load(
        "assets/Titulo/vaida.png"
    ).convert_alpha()

    # Ajusta o painel para ocupar toda a largura
    painel = pygame.transform.scale(
        painel,
        (WIDTH, 180)
    )

    falas = [
        "Depois de uma longa viagem...",
        "Duck finalmente o que tanto procurava.",
        "Uma masmorra, mas não qualquer masmorra.",
        "Era a masmorra das galinhas.",
        "As galinhas haviam capturado uma princesa",
        "E você, Duck, vai salva-la"
    ]

    fala_atual = 0

    while True:

        tela.fill(PRETO)

        # Painel na parte inferior
        tela.blit(
            painel,
            (0, HEIGHT - painel.get_height())
        )

        # Texto principal
        texto = fonte.render(
            falas[fala_atual],
            True,
            BRANCO
        )

        tela.blit(
            texto,
            (
                40,
                HEIGHT - painel.get_height() + 40
            )
        )

        # Aviso
        aviso = fonte.render(
            "ENTER para continuar",
            True,
            BRANCO
        )

        tela.blit(
            aviso,
            (
                40,
                HEIGHT - 50
            )
        )

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key in (
                    pygame.K_RETURN,
                    pygame.K_SPACE
                ):

                    fala_atual += 1

                    if fala_atual >= len(falas):
                        return

        clock.tick(60)