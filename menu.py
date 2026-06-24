import pygame
import sys

WIDTH = 800
HEIGHT = 600

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CINZA = (150, 150, 150)
azul_claro = (173, 216, 230)

pygame.font.init()

logo = pygame.image.load("assets/titulo/titulo - menu.png")
sobretitulo = pygame.image.load("assets/Titulo/sobretitulo_menu.png")

painel = pygame.image.load("assets/Titulo/vaida.png")
painel = pygame.transform.scale(painel, (160, 64))

fonte_menu = pygame.font.SysFont(None, 48)


def menu(tela, clock):

    opcoes = ["Jogar", "Sair"]
    selecionado = 0

    while True:

        tela.fill(azul_claro)

        # Logo
        tela.blit(
            logo,
            (
                WIDTH // 2 - logo.get_width() // 2,
                50
            )
        )

        # Subtítulo
        tela.blit(
            sobretitulo,
            (
                WIDTH // 2 - sobretitulo.get_width() // 2,
                120
            )
        )

        # Painéis e opções
        for i, opcao in enumerate(opcoes):

            painel_x = WIDTH // 2 - painel.get_width() // 2
            painel_y = 250 + i * 100

            tela.blit(
                painel,
                (painel_x, painel_y)
            )

            cor = BRANCO if i == selecionado else CINZA

            texto = fonte_menu.render(
                opcao,
                True,
                cor
            )

            texto_rect = texto.get_rect(
                center=(
                    painel_x + painel.get_width() // 2,
                    painel_y + painel.get_height() // 2
                )
            )

            tela.blit(texto, texto_rect)

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    selecionado = (selecionado - 1) % len(opcoes)

                if event.key == pygame.K_DOWN:
                    selecionado = (selecionado + 1) % len(opcoes)

                if event.key == pygame.K_RETURN:

                    if selecionado == 0:
                        return 'intro'

                    if selecionado == 1:
                        pygame.quit()
                        sys.exit()

        clock.tick(60)