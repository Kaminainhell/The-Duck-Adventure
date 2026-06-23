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

#Corredor Geral
CL, CA = 128, 96          # corredor padrão
CL2    = 384              # altura do corredor largo (antes da sala final)

# Sala pequena início
SP_L, SP_A = 512, 384
SP_x = (largura_mundo - SP_L) // 2
SP_y = altura_mundo - SP_A

# Corredor 1 (SP - SG)
C1_x = (largura_mundo - CL) // 2
C1_y = SP_y - CA

# Sala grande
SG_L, SG_A = 1536, 1152
SG_x = (largura_mundo - SG_L) // 2
SG_y = C1_y - SG_A

# Corredor 2 (SG - SM)
C2_x = (largura_mundo - CL) // 2
C2_y = SG_y - CA

# Sala média
SM_L, SM_A = 1024, 768
SM_x = (largura_mundo - SM_L) // 2
SM_y = C2_y - SM_A

# Corredor 3 (SM - SP2)
C3_x = (largura_mundo - CL) // 2
C3_y = SM_y - CA

# Sala pequena 2
SP2_L, SP2_A = 512, 384
SP2_x = (largura_mundo - SP2_L) // 2
SP2_y = C3_y - SP2_A

# Corredor largo (SP2 - SF)
CL_x = (largura_mundo - CL) // 2
CL_y = SP2_y - CL2

# Sala grande final
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
    #Cria muros em torno de uma sala/corredor com aberturas.
    #ab_* = (ini, fim).
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
    #Corredor vertical: só paredes laterais (topo/base abertos para as salas).
    for y in range(cy, cy + ca, AZULEJO):
        muro_group.add(Muro(cx - AZULEJO, y))
        muro_group.add(Muro(cx + cl,   y))

# Sala pequena início — abre topo para C1
paredes(SP_x, SP_y, SP_L, SP_A,
        ab_topo=(C1_x, C1_x + CL))

# Corredor 1
corredor_v(C1_x, C1_y, CL, CA)

# Sala grande — abre base (C1) e topo (C2)
paredes(SG_x, SG_y, SG_L, SG_A,
        ab_base=(C1_x, C1_x + CL),
        ab_topo=(C2_x, C2_x + CL))

# Corredor 2
corredor_v(C2_x, C2_y, CL, CA)

# Sala média — abre base (C2) e topo (C3)
paredes(SM_x, SM_y, SM_L, SM_A,
        ab_base=(C2_x, C2_x + CL),
        ab_topo=(C3_x, C3_x + CL))

# Corredor 3
corredor_v(C3_x, C3_y, CL, CA)

# Sala pequena 2 — abre base (C3) e topo (corredor largo)
paredes(SP2_x, SP2_y, SP2_L, SP2_A,
        ab_base=(C3_x, C3_x + CL),
        ab_topo=(CL_x, CL_x + CL))

# Corredor largo
corredor_v(CL_x, CL_y, CL, CL2)

# Sala grande final — abre base (corredor largo), topo fechado
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
        self.vida        = 300
        self.invensivel  = 0
        self.ataque_timer = 0

Pato_group = pygame.sprite.Group()
pato = Pato()
Pato_group.add(pato)

Galinha_group = pygame.sprite.Group()

class Galinha(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/Inimigos/Galinha.png")
        self.rect  = self.image.get_rect()
        self.vida  = 1

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
        self.vida  = 2
        self.tempo_recuo = 0

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


# LOOP PRINCIPAL

while rodando:

    # 1. Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pato.ataque_timer = 10

    # 2. Ataque
    if pato.ataque_timer > 0:
        area = pygame.Rect(pato.rect.centerx - 50, pato.rect.centery - 50, 100, 100)
        for g in Galinha_group:
            if area.colliderect(g.rect): g.vida -= 1
        for g in Galo_group:
            if area.colliderect(g.rect): g.vida -= 1
        pato.ataque_timer -= 1

    # 3. Imunidade
    if pato.invensivel > 0:
        pato.invensivel -= 1

    # 4. Movimento pato
    tecla = pygame.key.get_pressed()
    vx = vy = 0
    if tecla[pygame.K_d] or tecla[pygame.K_RIGHT]:  vx =  Velocidade
    if tecla[pygame.K_a] or tecla[pygame.K_LEFT]:   vx = -Velocidade
    if tecla[pygame.K_w] or tecla[pygame.K_UP]:     vy = -Velocidade
    if tecla[pygame.K_s] or tecla[pygame.K_DOWN]:   vy =  Velocidade

    # Colisão parede
    # Salva movimento anterior
    anterior_x, anterior_y = pato.rect.x, pato.rect.y
    pato.rect.x += vx
    pato.rect.y += vy

    for m in muro_group:
        if pato.rect.colliderect(m.rect):
            pato.rect.x, pato.rect.y = anterior_x, anterior_y; break

    for g in Galinha_group:
        if pato.rect.colliderect(g.rect):
            pato.rect.x, pato.rect.y = anterior_x, anterior_y; break

    # Borda do mundo

    pato.rect.left   = max(0, pato.rect.left)
    pato.rect.right  = min(largura_mundo, pato.rect.right)
    pato.rect.top    = max(0, pato.rect.top)
    pato.rect.bottom = min(altura_mundo, pato.rect.bottom)

    # 5. Câmera
    cam_x = max(0, min(pato.rect.centerx - largura // 2, largura_mundo - largura))
    cam_y = max(0, min(pato.rect.centery - altura  // 2, altura_mundo  - altura))

    # 6. Galinhas
    for galinha in Galinha_group:
        if g.vida <= 0: g.kill(); continue              #vida
        dx = pato.rect.centerx - g.rect.centerx         #vetorial para distancia
        dy = pato.rect.centery - g.rect.centery
        dist = (dx**2 + dy**2) ** 0.5
        if dist == 0: continue
        galinha_x, galinha_y = galinha.rect.x, galinha.rect.y       #Guarda posição
        dist_seg = 200
        if dist > dist_seg + 20:
            galinha.rect.x += dx / dist; galinha.rect.y += dy / dist
        elif dist < dist_seg - 20:
            galinha.rect.x -= dx / dist; galinha.rect.y -= dy / dist
        else:
            galinha.rect.x += -dy / dist; galinha.rect.y += dx / dist
        for m in muro_group:
            if galinha.rect.colliderect(m.rect):
                galinha.rect.x, galinha.rect.y = galinha_x, galinha_y; break
        galinha.rect.left   = max(0, g.rect.left)
        galinha.rect.right  = min(largura_mundo, g.rect.right)
        galinha.rect.top    = max(0, g.rect.top)
        galinha.rect.bottom = min(altura_mundo, g.rect.bottom)

    # 7. Galos
    for galo in Galo_group:
        if galo.vida <= 0: galo.kill(); continue            #vida galo
        dx = pato.rect.centerx - galo.rect.centerx          #outra vetorial para distancia
        dy = pato.rect.centery - galo.rect.centery
        dist = (dx**2 + dy**2) ** 0.5
        galo_x, galo_y = galo.rect.x, galo.rect.y           #guarda posição
        if dist > 0:
            if galo.tempo_recuo > 0:
                galo.rect.x -= dx / dist; g.rect.y -= dy / dist
                galo.tempo_recuo -= 1
            else:
                galo.rect.x += dx / dist * 2; galo.rect.y += dy / dist * 2
        for m in muro_group:
            if galo.rect.colliderect(m.rect):
                galo.rect.x, galo.rect.y = galo_x, galo_y; break
        galo.rect.left   = max(0, g.rect.left)
        galo.rect.right  = min(largura_mundo, g.rect.right)
        galo.rect.top    = max(0, g.rect.top)
        galo.rect.bottom = min(altura_mundo, g.rect.bottom)
        if galo.rect.colliderect(pato.rect) and pato.invensivel == 0:
            pato.vida -= 1; pato.invensivel = 60; g.tempo_recuo = 30
            print("Vida:", pato.vida)

    # 8. Ovos
    for ovo in ovo_group:
        ovo.rect.x += ovo.vel_x
        ovo.rect.y += ovo.vel_y
        if pato.rect.colliderect(ovo.rect):
            if pato.invensivel == 0:
                pato.vida -= 1; pato.invensivel = 30
                print("Vida:", pato.vida)
            ovo.kill(); continue
        if (ovo.rect.right < 0 or ovo.rect.left > largura_mundo or
                ovo.rect.bottom < 0 or ovo.rect.top > altura_mundo):
            ovo.kill()

    tempo_ovo += 1
    if tempo_ovo >= 180:
        for g in Galinha_group:
            ovo_group.add(Ovo(g.rect.centerx, g.rect.centery,
                              pato.rect.centerx, pato.rect.centery))
        tempo_ovo = 0

    if pato.vida <= 0:
        rodando = False

    # 9. Renderização
    tela.fill((0, 0, 0))
    tela.blit(chao_surface, (0, 0), (cam_x, cam_y, largura, altura))

    for m in muro_group:
        sx, sy = m.rect.x - cam_x, m.rect.y - cam_y
        if -AZULEJO < sx < largura and -AZULEJO < sy < altura:
            tela.blit(m.image, (sx, sy))

    for s in Galinha_group:
        tela.blit(s.image, (s.rect.x - cam_x, s.rect.y - cam_y))
    for s in Galo_group:
        tela.blit(s.image, (s.rect.x - cam_x, s.rect.y - cam_y))
    for ovo in ovo_group:
        tela.blit(ovo.image, (ovo.rect.x - cam_x, ovo.rect.y - cam_y))

    tela.blit(pato.image, (pato.rect.x - cam_x, pato.rect.y - cam_y))
    tela.blit(fonte.render(f"Vida: {pato.vida}", True, (255, 255, 255)), (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()