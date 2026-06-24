import pygame
import sys


def game_over(tela, clock):

    largura, altura = tela.get_size()

    # Fontes
    fonte_titulo = pygame.font.Font("assets/Fonte/fonte.ttf", 96)
    fonte_sub    = pygame.font.Font("assets/Fonte/fonte.ttf", 42)
    fonte_dica   = pygame.font.Font("assets/Fonte/fonte.ttf", 30)

    # Cores
    VERMELHO_ESC  = (180,  20,  20)
    VERMELHO_BRIL = (255,  60,  60)
    BRANCO        = (255, 255, 255)
    CINZA         = (140, 140, 140)
    PRETO         = (  0,   0,   0)

    # Overlay escuro semi-transparente
    overlay = pygame.Surface((largura, altura))
    overlay.fill(PRETO)

    # Partículas de sangue simples
    import random
    particulas = []
    for _ in range(60):
        particulas.append({
            "x": random.randint(0, largura),
            "y": random.randint(-altura, 0),
            "vy": random.uniform(1.5, 4.0),
            "r": random.randint(3, 9),
            "alpha": random.randint(160, 255),
        })

    # Animação de entrada (fade-in)
    fade_alpha  = 0
    fade_speed  = 4          # quanto sobe por frame
    pulse_tick  = 0          # para o título pulsar

    rodando = True
    while rodando:
        dt = clock.tick(60)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "reiniciar"
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        #Atualiza partículas
        for p in particulas:
            p["y"] += p["vy"]
            if p["y"] > altura + 20:
                p["y"] = random.randint(-60, -10)
                p["x"] = random.randint(0, largura)

        # Fade in
        if fade_alpha < 210:
            fade_alpha = min(210, fade_alpha + fade_speed)

        pulse_tick += 1

        #Renderização
        tela.fill(PRETO)

        # Partículas (gotas vermelhas)
        part_surf = pygame.Surface((largura, altura), pygame.SRCALPHA)
        for p in particulas:
            pygame.draw.circle(
                part_surf,
                (VERMELHO_ESC[0], VERMELHO_ESC[1], VERMELHO_ESC[2], p["alpha"]),
                (int(p["x"]), int(p["y"])),
                p["r"],
            )
        tela.blit(part_surf, (0, 0))

        # Overlay escurecido
        overlay.set_alpha(fade_alpha)
        tela.blit(overlay, (0, 0))

        # Título pulsante
        escala_pulse = 1.0 + 0.03 * abs(pygame.math.Vector2(1, 0).rotate(pulse_tick * 2).x)
        titulo_base  = fonte_titulo.render("GAME OVER", True, VERMELHO_BRIL)
        w  = int(titulo_base.get_width()  * escala_pulse)
        h  = int(titulo_base.get_height() * escala_pulse)
        titulo_surf  = pygame.transform.smoothscale(titulo_base, (w, h))

        # Sombra do título
        sombra = fonte_titulo.render("GAME OVER", True, (60, 0, 0))
        tela.blit(sombra, (largura // 2 - sombra.get_width() // 2 + 4,
                            altura  // 2 - sombra.get_height() // 2 - 60 + 4))
        tela.blit(titulo_surf, (largura // 2 - w // 2,
                                 altura  // 2 - h // 2 - 60))

        # Subtítulo
        sub = fonte_sub.render("O pato caiu em batalha...", True, BRANCO)
        tela.blit(sub, (largura // 2 - sub.get_width() // 2, altura // 2 + 20))

        # Dicas piscantes
        if (pulse_tick // 40) % 2 == 0:
            dica_r = fonte_dica.render("[ R ]  Tentar novamente", True, (220, 220, 100))
            tela.blit(dica_r, (largura // 2 - dica_r.get_width() // 2, altura // 2 + 80))

            dica_e = fonte_dica.render("[ ESC ]  Sair", True, CINZA)
            tela.blit(dica_e, (largura // 2 - dica_e.get_width() // 2, altura // 2 + 115))

        pygame.display.flip()

    return "sair"