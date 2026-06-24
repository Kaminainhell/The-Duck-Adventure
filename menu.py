import pygame
import sys
import random

pygame.mixer.init()
pygame.mixer.music.load("assets/Musica/menu_musica-192kbps.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

def menu(tela, clock):

    largura, altura = tela.get_size()

    # Fontes
    fonte_menu = pygame.font.Font("assets/Fonte/fonte.ttf", 44)

    # Assets
    logo = pygame.image.load("assets/Titulo/titulo - menu.png")
    logo = pygame.transform.scale(logo, (768, 128))

    sobretitulo = pygame.image.load("assets/Titulo/sobretitulo_menu.png")

    painel = pygame.image.load("assets/Titulo/vaida.png")
    painel = pygame.transform.scale(painel, (192, 64))

    # Cores
    PRETO      = (  0,   0,   0)
    BRANCO     = (255, 255, 255)
    CINZA      = (150, 150, 150)
    AZUL_CLARO = (173, 216, 230)

    # Overlay escuro semi-transparente
    overlay = pygame.Surface((largura, altura))
    overlay.fill(PRETO)

    # Partículas de neve/luz
    COR_PART = (200, 230, 255)   # azul claríssimo
    particulas = []
    for _ in range(60):
        particulas.append({
            "x":     random.randint(0, largura),
            "y":     random.randint(-altura, 0),
            "vy":    random.uniform(1.5, 4.0),
            "r":     random.randint(3, 9),
            "alpha": random.randint(160, 255),
        })

    # Estado
    opcoes    = ["Jogar", "Sair"]
    selecionado = 0

    fade_alpha = 0       # overlay começa invisível até 120
    FADE_MAX   = 120
    fade_speed = 4

    pulse_tick = 0       # drive do efeito pulsante no logo

    # Loop principal
    while True:
        clock.tick(60)

        # Eventos
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
                        return "intro"
                    if selecionado == 1:
                        pygame.quit()
                        sys.exit()

        # Atualiza partículas
        for p in particulas:
            p["y"] += p["vy"]
            if p["y"] > altura + 20:
                p["y"] = random.randint(-60, -10)
                p["x"] = random.randint(0, largura)

        # Fade-in do overlay
        if fade_alpha < FADE_MAX:
            fade_alpha = min(FADE_MAX, fade_alpha + fade_speed)

        pulse_tick += 1

        # Renderização

        # Fundo azul claro
        tela.fill(AZUL_CLARO)

        # Partículas
        part_surf = pygame.Surface((largura, altura), pygame.SRCALPHA)
        for p in particulas:
            pygame.draw.circle(
                part_surf,
                (COR_PART[0], COR_PART[1], COR_PART[2], p["alpha"]),
                (int(p["x"]), int(p["y"])),
                p["r"],
            )
        tela.blit(part_surf, (0, 0))

        # Overlay escurecido semi-transparente
        overlay.set_alpha(fade_alpha)
        tela.blit(overlay, (0, 0))

        # Logo pulsante
        escala_pulse = 1.0 + 0.015 * abs(
            pygame.math.Vector2(1, 0).rotate(pulse_tick * 2).x
        )
        w_logo = int(logo.get_width()  * escala_pulse)
        h_logo = int(logo.get_height() * escala_pulse)
        logo_scaled = pygame.transform.smoothscale(logo, (w_logo, h_logo))

        # Sombra do logo
        logo_sombra = pygame.transform.smoothscale(logo, (w_logo, h_logo))
        logo_sombra.set_alpha(80)
        tela.blit(
            logo_sombra,
            (largura // 2 - w_logo // 2 + 4, 50 + 4),
        )
        tela.blit(
            logo_scaled,
            (largura // 2 - w_logo // 2, 50),
        )

        # Subtítulo
        tela.blit(
            sobretitulo,
            (largura // 2 - sobretitulo.get_width() // 2, 170),
        )

        # Painéis + opções
        for i, opcao in enumerate(opcoes):
            painel_x = largura  // 2 - painel.get_width()  // 2
            painel_y = 250 + i * 100

            tela.blit(painel, (painel_x, painel_y))

            # Item selecionado pisca
            if i == selecionado:
                if (pulse_tick // 30) % 2 == 0:
                    cor = BRANCO
                else:
                    cor = (220, 220, 100)   # amarelo suave no pulso
            else:
                cor = CINZA

            texto = fonte_menu.render(opcao, True, cor)

            # Sombra do texto
            sombra_texto = fonte_menu.render(opcao, True, PRETO)
            centro_x = painel_x + painel.get_width()  // 2
            centro_y = painel_y + painel.get_height() // 2
            tela.blit(
                sombra_texto,
                sombra_texto.get_rect(center=(centro_x + 2, centro_y + 2)),
            )
            tela.blit(
                texto,
                texto.get_rect(center=(centro_x, centro_y)),
            )

        pygame.display.flip()