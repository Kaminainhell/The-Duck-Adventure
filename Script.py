import pygame
pygame.init()

#  Tela
largura = 800
altura  = 600

#  Mundo
largura_mundo = 4000
altura_mundo  = 6000

AZULEJO = 32

# Assets
chao_azulejo = pygame.image.load("assets/ambiente/Chao2.png")
muro_img  = pygame.image.load("assets/ambiente/muro.png")

tela    = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("pato")
fonte   = pygame.font.SysFont(None, 36)
clock   = pygame.time.Clock()
rodando = True
Velocidade = 5


# LAYOUT  (de baixo para cima)

CL, CA = 128, 96
CL2    = 384

SP_L, SP_A = 512, 384
SP_x = (largura_mundo - SP_L) // 2
SP_y = altura_mundo - SP_A

C1_x = (largura_mundo - CL) // 2
C1_y = SP_y - CA

SG_L, SG_A = 1536, 1152
SG_x = (largura_mundo - SG_L) // 2
SG_y = C1_y - SG_A

C2_x = (largura_mundo - CL) // 2
C2_y = SG_y - CA

SM_L, SM_A = 1024, 768
SM_x = (largura_mundo - SM_L) // 2
SM_y = C2_y - SM_A

C3_x = (largura_mundo - CL) // 2
C3_y = SM_y - CA

SP2_L, SP2_A = 512, 384
SP2_x = (largura_mundo - SP2_L) // 2
SP2_y = C3_y - SP2_A

CL_x = (largura_mundo - CL) // 2
CL_y = SP2_y - CL2

SF_L, SF_A = 1536, 1152
SF_x = (largura_mundo - SF_L) // 2
SF_y = CL_y - SF_A


# CHÃO PRÉ-RENDERIZADO

chao_surface = pygame.Surface((largura_mundo, altura_mundo), pygame.SRCALPHA)
chao_surface.fill((0, 0, 0, 0))

regioes = [
    (SP_x,  SP_y,  SP_L,  SP_A),
    (C1_x,  C1_y,  CL,    CA),
    (SG_x,  SG_y,  SG_L,  SG_A),
    (C2_x,  C2_y,  CL,    CA),
    (SM_x,  SM_y,  SM_L,  SM_A),
    (C3_x,  C3_y,  CL,    CA),
    (SP2_x, SP2_y, SP2_L, SP2_A),
    (CL_x,  CL_y,  CL,    CL2),
    (SF_x,  SF_y,  SF_L,  SF_A),
]

for rx, ry, rw, rh in regioes:
    for x in range(rx, rx + rw, AZULEJO):
        for y in range(ry, ry + rh, AZULEJO):
            chao_surface.blit(chao_azulejo, (x, y))


# MUROS

muro_group = pygame.sprite.Group()

class Muro(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = muro_img.convert_alpha()
        self.rect  = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def paredes(sx, sy, sl, sa,
            ab_topo=None, ab_base=None,
            ab_esq=None,  ab_dir=None):
    for x in range(sx - AZULEJO, sx + sl + AZULEJO, AZULEJO):
        if ab_topo is None or not (ab_topo[0] <= x < ab_topo[1]):
            muro_group.add(Muro(x, sy - AZULEJO))
        if ab_base is None or not (ab_base[0] <= x < ab_base[1]):
            muro_group.add(Muro(x, sy + sa))
    for y in range(sy, sy + sa, AZULEJO):
        if ab_esq is None or not (ab_esq[0] <= y < ab_esq[1]):
            muro_group.add(Muro(sx - AZULEJO, y))
        if ab_dir is None or not (ab_dir[0] <= y < ab_dir[1]):
            muro_group.add(Muro(sx + sl, y))

def corredor_v(cx, cy, cl, ca):
    for y in range(cy, cy + ca, AZULEJO):
        muro_group.add(Muro(cx - AZULEJO, y))
        muro_group.add(Muro(cx + cl,   y))

paredes(SP_x, SP_y, SP_L, SP_A,
        ab_topo=(C1_x, C1_x + CL))
corredor_v(C1_x, C1_y, CL, CA)
paredes(SG_x, SG_y, SG_L, SG_A,
        ab_base=(C1_x, C1_x + CL),
        ab_topo=(C2_x, C2_x + CL))
corredor_v(C2_x, C2_y, CL, CA)
paredes(SM_x, SM_y, SM_L, SM_A,
        ab_base=(C2_x, C2_x + CL),
        ab_topo=(C3_x, C3_x + CL))
corredor_v(C3_x, C3_y, CL, CA)
paredes(SP2_x, SP2_y, SP2_L, SP2_A,
        ab_base=(C3_x, C3_x + CL),
        ab_topo=(CL_x, CL_x + CL))
corredor_v(CL_x, CL_y, CL, CL2)
paredes(SF_x, SF_y, SF_L, SF_A,
        ab_base=(CL_x, CL_x + CL))


# SPRITES

class Pato(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/Pato/Pato2.png")
        self.rect  = self.image.get_rect()
        self.rect.x = SP_x + SP_L // 2
        self.rect.y = SP_y + SP_A // 2
        self.vida         = 300
        self.invensivel   = 0
        self.ataque_timer = 0
        self.tempo_recuo  = 0
        self.vel_x        = 0.0   # knockback
        self.vel_y        = 0.0

Pato_group = pygame.sprite.Group()
pato = Pato()
Pato_group.add(pato)

Galinha_group = pygame.sprite.Group()

class Galinha(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/Inimigos/Galinha.png")
        self.rect  = self.image.get_rect()
        self.vida        = 1
        self.vel_x       = 0.0   # knockback
        self.vel_y       = 0.0
        self.tempo_recuo = 0

for i in range(5):
    galinha = Galinha()
    galinha.rect.x = SP_x + 50 + i * 80
    galinha.rect.y = SP_y + 100
    Galinha_group.add(galinha)

Galo_group = pygame.sprite.Group()

class Galo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/Inimigos/Galo.png")
        self.rect  = self.image.get_rect()
        self.vida        = 2
        self.tempo_recuo = 0
        self.vel_x       = 0.0   # knockback
        self.vel_y       = 0.0

for i in range(3):
    galo = Galo()
    galo.rect.x = SP_x + 100 + i * 120
    galo.rect.y = SP_y + 250
    Galo_group.add(galo)

ovo_group = pygame.sprite.Group()

class Ovo(pygame.sprite.Sprite):
    def __init__(self, x, y, alvo_x, alvo_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/OVO/Ovo2.png")
        self.rect  = self.image.get_rect()
        self.rect.center = (x, y)
        dx, dy = alvo_x - x, alvo_y - y
        dist = (dx**2 + dy**2) ** 0.5
        self.vel_x = dx / dist * 4
        self.vel_y = dy / dist * 4

tempo_ovo = 0

# Força dos knockbacks
KB_PATO    = 8    # força ao pato (galo/ovo → pato)
KB_INIMIGO = 10   # força nos inimigos (pato → galinha/galo)
FRICCAO    = 0.75 # decaimento por frame


# LOOP PRINCIPAL

while rodando:

    # 1. Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pato.ataque_timer = 10

    # 2. Ataque — dano + knockback nos inimigos
    if pato.ataque_timer > 0:
        area = pygame.Rect(pato.rect.centerx - 50, pato.rect.centery - 50, 100, 100)
        for galinha in Galinha_group:
            if area.colliderect(galinha.rect):
                galinha.vida -= 1
                # knockback da galinha para longe do pato
                dx = galinha.rect.centerx - pato.rect.centerx
                dy = galinha.rect.centery - pato.rect.centery
                dist = (dx**2 + dy**2) ** 0.5 or 1
                galinha.vel_x = dx / dist * KB_INIMIGO
                galinha.vel_y = dy / dist * KB_INIMIGO
                galinha.tempo_recuo = 15
        for galo in Galo_group:
            if area.colliderect(galo.rect):
                galo.vida -= 1
                # knockback do galo para longe do pato
                dx = galo.rect.centerx - pato.rect.centerx
                dy = galo.rect.centery - pato.rect.centery
                dist = (dx**2 + dy**2) ** 0.5 or 1
                galo.vel_x = dx / dist * KB_INIMIGO
                galo.vel_y = dy / dist * KB_INIMIGO
                galo.tempo_recuo = 30
        pato.ataque_timer -= 1

    # 3. Imunidade
    if pato.invensivel > 0:
        pato.invensivel -= 1

    # 4. Movimento pato (input + knockback)
    tecla = pygame.key.get_pressed()
    vx = vy = 0
    if tecla[pygame.K_d] or tecla[pygame.K_RIGHT]:  vx =  Velocidade
    if tecla[pygame.K_a] or tecla[pygame.K_LEFT]:   vx = -Velocidade
    if tecla[pygame.K_w] or tecla[pygame.K_UP]:     vy = -Velocidade
    if tecla[pygame.K_s] or tecla[pygame.K_DOWN]:   vy =  Velocidade

    # soma input + knockback
    vx += pato.vel_x
    vy += pato.vel_y
    pato.vel_x *= FRICCAO
    pato.vel_y *= FRICCAO
    if abs(pato.vel_x) < 0.1: pato.vel_x = 0
    if abs(pato.vel_y) < 0.1: pato.vel_y = 0

    anterior_x, anterior_y = pato.rect.x, pato.rect.y
    pato.rect.x += vx
    pato.rect.y += vy

    for m in muro_group:
        if pato.rect.colliderect(m.rect):
            pato.rect.x, pato.rect.y = anterior_x, anterior_y
            pato.vel_x = pato.vel_y = 0
            break

    for galinha in Galinha_group:
        if pato.rect.colliderect(galinha.rect):
            pato.rect.x, pato.rect.y = anterior_x, anterior_y
            pato.vel_x = pato.vel_y = 0
            break

    pato.rect.left   = max(0, pato.rect.left)
    pato.rect.right  = min(largura_mundo, pato.rect.right)
    pato.rect.top    = max(0, pato.rect.top)
    pato.rect.bottom = min(altura_mundo, pato.rect.bottom)

    # 5. Câmera
    cam_x = max(0, min(pato.rect.centerx - largura // 2, largura_mundo - largura))
    cam_y = max(0, min(pato.rect.centery - altura  // 2, altura_mundo  - altura))

    # 6. Galinhas
    for galinha in Galinha_group:
        if galinha.vida <= 0: galinha.kill(); continue

        dx = pato.rect.centerx - galinha.rect.centerx
        dy = pato.rect.centery - galinha.rect.centery
        dist = (dx**2 + dy**2) ** 0.5
        if dist == 0: continue

        galinha_x, galinha_y = galinha.rect.x, galinha.rect.y
        dist_seg = 100

        # movimento de orbita/fuga (só quando não está em knockback)
        if galinha.tempo_recuo <= 0:
            if dist >= dist_seg + 30:
                galinha.rect.x += 1 if pygame.time.get_ticks() // 500 % 2 == 0 else -1
            elif dist > dist_seg + 20:
                galinha.rect.x += dx / dist
                galinha.rect.y += dy / dist
            elif dist < dist_seg - 20:
                galinha.rect.x -= dx / dist
                galinha.rect.y -= dy / dist
            else:
                galinha.rect.x += -dy / dist
                galinha.rect.y += dx / dist
        else:
            galinha.tempo_recuo -= 1

        # aplica knockback
        galinha.rect.x += galinha.vel_x
        galinha.rect.y += galinha.vel_y
        galinha.vel_x *= FRICCAO
        galinha.vel_y *= FRICCAO
        if abs(galinha.vel_x) < 0.1: galinha.vel_x = 0
        if abs(galinha.vel_y) < 0.1: galinha.vel_y = 0

        for m in muro_group:
            if galinha.rect.colliderect(m.rect):
                galinha.rect.x, galinha.rect.y = galinha_x, galinha_y
                galinha.vel_x = galinha.vel_y = 0
                break
        galinha.rect.left   = max(0, galinha.rect.left)
        galinha.rect.right  = min(largura_mundo, galinha.rect.right)
        galinha.rect.top    = max(0, galinha.rect.top)
        galinha.rect.bottom = min(altura_mundo, galinha.rect.bottom)

    # 7. Galo
    for galo in Galo_group:
        if galo.vida <= 0: galo.kill(); continue

        dx = pato.rect.centerx - galo.rect.centerx
        dy = pato.rect.centery - galo.rect.centery
        dist = (dx**2 + dy**2) ** 0.5
        galo_x, galo_y = galo.rect.x, galo.rect.y

        if dist > 0:
            if galo.tempo_recuo > 0:
                # movimento de recuo (IA) — separado do knockback físico
                galo.rect.x -= dx / dist
                galo.rect.y -= dy / dist
                galo.tempo_recuo -= 1
            else:
                galo.rect.x += dx / dist * 2
                galo.rect.y += dy / dist * 2

        # aplica knockback físico
        galo.rect.x += galo.vel_x
        galo.rect.y += galo.vel_y
        galo.vel_x *= FRICCAO
        galo.vel_y *= FRICCAO
        if abs(galo.vel_x) < 0.1: galo.vel_x = 0
        if abs(galo.vel_y) < 0.1: galo.vel_y = 0

        for m in muro_group:
            if galo.rect.colliderect(m.rect):
                galo.rect.x, galo.rect.y = galo_x, galo_y
                galo.vel_x = galo.vel_y = 0
                break

        galo.rect.left   = max(0, galo.rect.left)
        galo.rect.right  = min(largura_mundo, galo.rect.right)
        galo.rect.top    = max(0, galo.rect.top)
        galo.rect.bottom = min(altura_mundo, galo.rect.bottom)

        # colisão com pato — dano + knockback no pato
        if galo.rect.colliderect(pato.rect) and pato.invensivel == 0:
            pato.vida -= 1
            pato.invensivel = 60
            # vetor pato ← galo
            kx = pato.rect.centerx - galo.rect.centerx
            ky = pato.rect.centery - galo.rect.centery
            kdist = (kx**2 + ky**2) ** 0.5 or 1
            pato.vel_x = kx / kdist * KB_PATO
            pato.vel_y = ky / kdist * KB_PATO
            for g in Galo_group:
                g.tempo_recuo = 60
            print("Vida:", pato.vida)

    # 8. Ovos
    for ovo in ovo_group:
        ovo.rect.x += ovo.vel_x
        ovo.rect.y += ovo.vel_y
        if pato.rect.colliderect(ovo.rect):
            if pato.invensivel == 0:
                pato.vida -= 1
                pato.invensivel = 30
                # knockback na direção do ovo
                kx = pato.rect.centerx - ovo.rect.centerx
                ky = pato.rect.centery - ovo.rect.centery
                kdist = (kx**2 + ky**2) ** 0.5 or 1
                pato.vel_x = kx / kdist * KB_PATO
                pato.vel_y = ky / kdist * KB_PATO
                print("Vida:", pato.vida)
            ovo.kill(); continue
        if (ovo.rect.right < 0 or ovo.rect.left > largura_mundo or
                ovo.rect.bottom < 0 or ovo.rect.top > altura_mundo):
            ovo.kill()

    tempo_ovo += 1
    if tempo_ovo >= 150:
        for galinha in Galinha_group:
            dx = pato.rect.centerx - galinha.rect.centerx
            dy = pato.rect.centery - galinha.rect.centery
            dist = (dx ** 2 + dy ** 2) ** 0.5
            if dist == 0: continue
            if dist <= 300:
                ovo_group.add(Ovo(galinha.rect.centerx, galinha.rect.centery,
                                  pato.rect.centerx, pato.rect.centery))
        tempo_ovo = 0

    for m in muro_group:
        for ovo in ovo_group:
            if ovo.rect.colliderect(m.rect):
                ovo.kill()

    if pato.vida <= 0:
        rodando = False

    # 9. Renderização
    tela.fill((0, 0, 0))
    tela.blit(chao_surface, (0, 0), (cam_x, cam_y, largura, altura))

    for m in muro_group:
        sx, sy = m.rect.x - cam_x, m.rect.y - cam_y
        if -AZULEJO < sx < largura and -AZULEJO < sy < altura:
            tela.blit(m.image, (sx, sy))

    for galinha in Galinha_group:
        tela.blit(galinha.image, (galinha.rect.x - cam_x, galinha.rect.y - cam_y))
    for galo in Galo_group:
        tela.blit(galo.image, (galo.rect.x - cam_x, galo.rect.y - cam_y))
    for ovo in ovo_group:
        tela.blit(ovo.image, (ovo.rect.x - cam_x, ovo.rect.y - cam_y))

    tela.blit(pato.image, (pato.rect.x - cam_x, pato.rect.y - cam_y))
    tela.blit(fonte.render(f"Vida: {pato.vida}", True, (255, 255, 255)), (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()