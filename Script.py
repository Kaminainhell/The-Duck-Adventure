import pygame
from menu import menu
from intro import intro


pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("assets/Musica/Musica_fundo-192kbps.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

try:
    pygame.mixer.init()
    print("Mixer iniciado")
except Exception as e:
    print(e)

#  Tela
largura = 800
altura  = 600

#  Mundo
largura_mundo = 4000
altura_mundo  = 6000

AZULEJO = 32

# Assets
chao_azulejo = pygame.image.load("assets/ambiente/Chao2.png")
muro_img     = pygame.image.load("assets/ambiente/muro.png")

tela    = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("pato")
fonte   = pygame.font.SysFont(None, 36)
fonte_p = pygame.font.SysFont(None, 28)
clock   = pygame.time.Clock()
rodando = True
Velocidade = 5

# LAYOUT
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

def paredes(sx, sy, sl, sa, ab_topo=None, ab_base=None, ab_esq=None, ab_dir=None):
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
        muro_group.add(Muro(cx + cl, y))

def bloco_muros(ox, oy, colunas=3, linhas=3):
    for col in range(colunas):
        for lin in range(linhas):
            muro_group.add(Muro(ox + col * AZULEJO, oy + lin * AZULEJO))

paredes(SP_x,  SP_y,  SP_L,  SP_A,  ab_topo=(C1_x, C1_x + CL))
corredor_v(C1_x, C1_y, CL, CA)
paredes(SG_x,  SG_y,  SG_L,  SG_A,  ab_base=(C1_x, C1_x + CL), ab_topo=(C2_x, C2_x + CL))
corredor_v(C2_x, C2_y, CL, CA)
paredes(SM_x,  SM_y,  SM_L,  SM_A,  ab_base=(C2_x, C2_x + CL), ab_topo=(C3_x, C3_x + CL))
corredor_v(C3_x, C3_y, CL, CA)
paredes(SP2_x, SP2_y, SP2_L, SP2_A, ab_base=(C3_x, C3_x + CL), ab_topo=(CL_x, CL_x + CL))
corredor_v(CL_x, CL_y, CL, CL2)
paredes(SF_x,  SF_y,  SF_L,  SF_A,  ab_base=(CL_x, CL_x + CL))

bloco_muros(SG_x,                    SG_y)
bloco_muros(SG_x + SG_L - 3*AZULEJO, SG_y)
bloco_muros(SG_x,                    SG_y + SG_A - 3*AZULEJO)
bloco_muros(SG_x + SG_L - 3*AZULEJO, SG_y + SG_A - 3*AZULEJO)

muro_meio_y = SP_y + SP_A // 2 - AZULEJO // 2
muro_meio_x = SP_x + (SP_L - 384) // 2
for col in range(384 // AZULEJO):
    muro_group.add(Muro(muro_meio_x + col * AZULEJO, muro_meio_y))

# CONSTANTES
KB_PATO            = 10
KB_INIMIGO         = 10
FRICCAO            = 0.75
DIST_ALERTA        = 225
PATROL_RANGE       = 80
ANIM_SPEED         = 12
DASH_FORCA         = 15
DASH_COOLDOWN_NORM = 90
DASH_COOLDOWN_FUR  = 20
DASH_DURACAO       = 8
DASH_POS_INVUL     = 10
FURIA_DURACAO      = 240
FURIA_BONUS_KILLS  = 30
FURIA_VEL_MULT     = 1.5
FURIA_DANO_DASH    = 2
SEQUENCIA_BOOST    = 10
VEL_BOOST_KILLS    = 2
CURA_QUANTIDADE    = 5
DANO_FLASH_DUR     = 8


# SPRITES ─────────────────────────────────────────────────────────────────────

class Pato(pygame.sprite.Sprite):
    img_dir  = pygame.image.load("assets/Pato/pato_direito_1.png")
    img_esq  = pygame.image.load("assets/Pato/pato_esquerdo_1.png")
    walk_dir = [
        pygame.image.load("assets/Pato/pato_direito_2.png"),
        pygame.image.load("assets/Pato/pato_direito_3.png"),
    ]
    walk_esq = [
        pygame.image.load("assets/Pato/pato_esquerdo_2.png"),
        pygame.image.load("assets/Pato/pato_esquerdo_3.png"),
    ]
    atk_dir = pygame.image.load("assets/Pato/pato_kat_dir.png")
    atk_esq = pygame.image.load("assets/Pato/pato_kat_esq.png")

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.img_dir
        self.rect  = self.image.get_rect()
        self.rect.x = SP_x + SP_L // 2
        self.rect.y = SP_y + SP_A

        self.vida            = 10
        self.vida_max        = 10
        self.invensivel      = 0
        self.ataque_timer    = 0
        self.ataque_cooldown = 0
        self.vel_x           = 0.0
        self.vel_y           = 0.0
        self.dash_cooldown   = 0
        self.dash_timer      = 0
        self.dash_vx         = 0.0
        self.dash_vy         = 0.0
        self.ultima_dir_x    = 1
        self.ultima_dir_y    = 0
        self.sequencia_kills = 0
        self.vel_bonus       = 0
        self.furia_carga     = 0
        self.furia_ativa     = False
        self.furia_timer     = 0
        self.facing          = "dir"
        self.anim_frame      = 0
        self.anim_timer      = 0

    def vel_atual(self):
        base = Velocidade + self.vel_bonus
        if self.furia_ativa:
            base = int(base * FURIA_VEL_MULT)
        return base

    def registrar_kill(self):
        self.sequencia_kills += 1
        self.vel_bonus = VEL_BOOST_KILLS if self.sequencia_kills >= SEQUENCIA_BOOST else 0
        self.furia_carga = min(100, self.furia_carga + 8)
        if self.furia_ativa:
            self.furia_timer = min(self.furia_timer + FURIA_BONUS_KILLS, FURIA_DURACAO * 3)

    def tomar_dano(self):
        self.sequencia_kills = 0
        self.vel_bonus       = 0

    def ativar_furia(self):
        if self.furia_carga >= 100 and not self.furia_ativa:
            self.furia_ativa = True
            self.furia_timer = FURIA_DURACAO
            self.furia_carga = 0

    def atualizar_furia(self):
        if self.furia_ativa:
            self.furia_timer -= 1
            if self.furia_timer <= 0:
                self.furia_ativa = False
                self.furia_timer = 0

    def em_dash(self):
        return self.dash_timer > 0

    def atualizar_animacao(self, movendo, atacando):
        if atacando:
            self.image = self.atk_dir if self.facing == "dir" else self.atk_esq
            return
        if movendo:
            self.anim_timer += 1
            if self.anim_timer >= ANIM_SPEED:
                self.anim_timer = 0
                self.anim_frame = (self.anim_frame + 1) % 2
            lista = self.walk_dir if self.facing == "dir" else self.walk_esq
            self.image = lista[self.anim_frame]
        else:
            self.anim_frame = 0
            self.image = self.img_dir if self.facing == "dir" else self.img_esq

Pato_group = pygame.sprite.Group()
pato = Pato()
Pato_group.add(pato)


def aplicar_flash(sprite):
    flash = sprite.image.copy()
    flash.fill((255, 0, 0, 120), special_flags=pygame.BLEND_RGBA_MULT)
    sprite.image = flash


class Galinha(pygame.sprite.Sprite):
    frames_dir = [
        pygame.image.load("assets/Inimigos/galinha/galinha_walk_dir1.png"),
        pygame.image.load("assets/Inimigos/galinha/galinha_walk_dir2.png"),
    ]
    frames_esq = [
        pygame.image.load("assets/Inimigos/galinha/galinha_walk_esq1.png"),
        pygame.image.load("assets/Inimigos/galinha/galinha_walk_esq2.png"),
    ]

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image           = self.frames_dir[0]
        self.rect            = self.image.get_rect()
        self.rect.x          = x
        self.rect.y          = y
        self.vida            = 2
        self.vel_x           = 0.0
        self.vel_y           = 0.0
        self.tempo_recuo     = 0
        self.dano_flash      = 0
        self.patrol_origem_x = x
        self.patrol_dir      = 1
        self.patrol_pausa    = 0
        self.patrol_speed    = 1.2
        self.anim_frame      = 0
        self.anim_timer      = 0
        self.facing          = "dir"

    def atualizar_animacao(self, movendo, dx):
        if dx < 0:   self.facing = "esq"
        elif dx > 0: self.facing = "dir"
        if movendo:
            self.anim_timer += 1
            if self.anim_timer >= ANIM_SPEED:
                self.anim_timer = 0
                self.anim_frame = (self.anim_frame + 1) % 2
        else:
            self.anim_frame = 0
        lista = self.frames_dir if self.facing == "dir" else self.frames_esq
        self.image = lista[self.anim_frame]
        if self.dano_flash > 0:
            aplicar_flash(self)
            self.dano_flash -= 1

Galinha_group = pygame.sprite.Group()
for i in range(3):
    Galinha_group.add(Galinha(SP_x + 60 + i * 130, SP_y + 60))
for i in range(15):
    Galinha_group.add(Galinha(SG_x + 80 + (i % 5) * 260, SG_y + 80 + (i // 5) * 200))
for i in range(10):
    Galinha_group.add(Galinha(SM_x + 80 + (i % 5) * 180, SM_y + 200 + (i // 5) * 200))
for i in range(3):
    Galinha_group.add(Galinha(SP2_x + 40 + (i % 5) * 80, SP2_y + 60 + (i // 5) * 100))
for i in range(15):
    Galinha_group.add(Galinha(SF_x + 80 + (i % 5) * 80, SF_y + 80 + (i // 5) * 100))


class Galo(pygame.sprite.Sprite):
    frames_walk_dir   = [
        pygame.image.load("assets/Inimigos/galo/galo_walk_dir1.png"),
        pygame.image.load("assets/Inimigos/galo/galo_walk_dir2.png"),
    ]
    frames_walk_esq   = [
        pygame.image.load("assets/Inimigos/galo/galo_walk_esq1.png"),
        pygame.image.load("assets/Inimigos/galo/galo_walk_esq2.png"),
    ]
    frames_ataque_dir = [
        pygame.image.load("assets/Inimigos/galo/galo_ataque_dir1.png"),
        pygame.image.load("assets/Inimigos/galo/galo_ataque_dir2.png"),
    ]
    frames_ataque_esq = [
        pygame.image.load("assets/Inimigos/galo/galo_ataque_esq1.png"),
        pygame.image.load("assets/Inimigos/galo/galo_ataque_esq2.png"),
    ]

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image           = self.frames_walk_dir[0]
        self.rect            = self.image.get_rect()
        self.rect.x          = x
        self.rect.y          = y
        self.vida            = 3
        self.tempo_recuo     = 0
        self.dano_flash      = 0
        self.vel_x           = 0.0
        self.vel_y           = 0.0
        self.patrol_origem_x = x
        self.patrol_dir      = 1
        self.patrol_pausa    = 0
        self.patrol_speed    = 1.5
        self.anim_frame      = 0
        self.anim_timer      = 0
        self.facing          = "dir"
        self.atacando        = False

    def atualizar_animacao(self, movendo, dx, atacando):
        if dx < 0:   self.facing = "esq"
        elif dx > 0: self.facing = "dir"
        self.atacando = atacando
        self.anim_timer += 1
        if self.anim_timer >= ANIM_SPEED:
            self.anim_timer = 0
            self.anim_frame = (self.anim_frame + 1) % 2
        if atacando:
            lista = self.frames_ataque_dir if self.facing == "dir" else self.frames_ataque_esq
        else:
            lista = self.frames_walk_dir if self.facing == "dir" else self.frames_walk_esq
            if not movendo: self.anim_frame = 0
        self.image = lista[self.anim_frame]
        if self.dano_flash > 0:
            aplicar_flash(self)
            self.dano_flash -= 1

Galo_group = pygame.sprite.Group()
for i in range(4):
    Galo_group.add(Galo(SP_x + 50 + i * 110, SP_y + 50))
for i in range(25):
    Galo_group.add(Galo(SG_x + 120 + (i % 5) * 260, SG_y + 200 + (i // 5) * 180))
for i in range(20):
    Galo_group.add(Galo(SM_x + 100 + (i % 4) * 220, SM_y + 100 + (i // 4) * 120))
for i in range(2):
    Galo_group.add(Galo(SP2_x + 40 + (i % 4) * 100, SP2_y + 40 + (i // 4) * 80))
for i in range(30):
    Galo_group.add(Galo(SF_x + 40 + (i%4) * 300, SF_y + 40 + (i // 4) * 220))


class Princesa(pygame.sprite.Sprite):
    frames = [
        pygame.image.load("assets/Princesa/princesa_respiro1.png"),
        pygame.image.load("assets/Princesa/princesa_respiro2.png"),
        pygame.image.load("assets/Princesa/princesa_respiro3.png"),
    ]

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image      = self.frames[0]
        self.rect       = self.image.get_rect()
        self.rect.x     = x
        self.rect.y     = y
        self.anim_frame = 0
        self.anim_timer = 0
        self.liberada = False
    def atualizar_animacao(self):
        self.anim_timer += 1
        if self.anim_timer >= 20:
            self.anim_timer = 0
            self.anim_frame = (self.anim_frame + 1) % 3
        self.image = self.frames[self.anim_frame]

Princesa_group = pygame.sprite.Group()
Princesa_group.add(Princesa(SF_x + SF_L - 96, SF_y + SF_A // 2 - 32))


class Cura(pygame.sprite.Sprite):
    img = pygame.image.load("assets/utensilios/cura.png")

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image  = self.img.copy()
        self.rect   = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

cura_group = pygame.sprite.Group()
cura_group.add(Cura(SP2_x + SP2_L // 2 - 16, SP2_y + SP2_A // 2 - 16))


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

ovo_group = pygame.sprite.Group()
tempo_ovo = 0


# HUD ─────────────────────────────────────────────────────────────────────────
def desenhar_barra(surf, x, y, w, h, valor, maximo, cor, cor_fundo=(60, 60, 60)):
    pygame.draw.rect(surf, cor_fundo, (x, y, w, h))
    fill = int(w * max(0, valor) / maximo)
    if fill > 0:
        pygame.draw.rect(surf, cor, (x, y, fill, h))
    pygame.draw.rect(surf, (200, 200, 200), (x, y, w, h), 2)

def desenhar_hud(surf, pato):
    # vida
    bw, bh = 200, 18
    bx, by = 10, 10
    desenhar_barra(surf, bx, by, bw, bh, pato.vida, pato.vida_max, (220, 50, 50))
    vida_txt = fonte_p.render(f"{pato.vida}/{pato.vida_max}", True, (255, 255, 255))
    surf.blit(vida_txt, (bx + bw + 6, by))

    # dash cooldown
    cd_txt = "Dash: PRONTO" if pato.dash_cooldown == 0 else f"Dash: {pato.dash_cooldown}"
    surf.blit(fonte_p.render(cd_txt, True, (180, 220, 255)), (10, 34))

    # fúria (canto superior direito)
    fw, fh = 160, 14
    fx = largura - fw - 10
    fy = 10
    cor_furia = (255, 80, 0) if pato.furia_ativa else (220, 180, 0)
    desenhar_barra(surf, fx, fy, fw, fh,
                   pato.furia_timer if pato.furia_ativa else pato.furia_carga,
                   FURIA_DURACAO   if pato.furia_ativa else 100,
                   cor_furia)
    label = "FÚRIA ATIVA!" if pato.furia_ativa else (
            "FÚRIA PRONTA![Q]" if pato.furia_carga >= 100 else f"Fúria {pato.furia_carga}/100")
    lbl_surf = fonte_p.render(label, True, cor_furia)
    surf.blit(lbl_surf, (largura - lbl_surf.get_width() - 10, fy + fh + 2))

    # sequência (abaixo da fúria, canto direito)
    if pato.sequencia_kills > 0:
        sy_hud = fy + fh + 22
        cor_seq = (0, 220, 80) if pato.sequencia_kills >= SEQUENCIA_BOOST else (80, 180, 255)
        desenhar_barra(surf, fx, sy_hud, fw, 10,
                       min(pato.sequencia_kills, SEQUENCIA_BOOST), SEQUENCIA_BOOST, cor_seq)
        seq_txt = f"Seq: {pato.sequencia_kills}" + ("  +VEL" if pato.sequencia_kills >= SEQUENCIA_BOOST else "")
        st = fonte_p.render(seq_txt, True, cor_seq)
        surf.blit(st, (largura - st.get_width() - 10, sy_hud + 12))

resultado = menu(tela, clock)

if resultado == "intro":
    intro(tela, clock)


# LOOP PRINCIPAL ──────────────────────────────────────────────────────────────
while rodando:

    # 1. Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
        if Princesa.liberada:
            if pato.rect.colliderect(Princesa.rect):
                estado = "dialogo"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                if pato.ataque_cooldown == 0:
                    pato.ataque_timer    = 10
                    pato.ataque_cooldown = 40

            if event.key == pygame.K_SPACE:
                cd = DASH_COOLDOWN_FUR if pato.furia_ativa else DASH_COOLDOWN_NORM
                if pato.dash_cooldown == 0:
                    pato.dash_cooldown = cd
                    pato.dash_timer    = DASH_DURACAO
                    pato.dash_vx       = pato.ultima_dir_x * DASH_FORCA
                    pato.dash_vy       = pato.ultima_dir_y * DASH_FORCA

            if event.key == pygame.K_q:
                pato.ativar_furia()

    # 2. Cooldowns
    if pato.ataque_cooldown > 0: pato.ataque_cooldown -= 1
    if pato.dash_cooldown   > 0: pato.dash_cooldown   -= 1
    pato.atualizar_furia()

    # 2b. Ataque
    if pato.ataque_timer > 0:
        area = pygame.Rect(pato.rect.centerx - 50, pato.rect.centery - 50, 100, 100)
        for galinha in list(Galinha_group):
            if area.colliderect(galinha.rect):
                galinha.vida       -= 1
                galinha.dano_flash  = DANO_FLASH_DUR
                dx = galinha.rect.centerx - pato.rect.centerx
                dy = galinha.rect.centery - pato.rect.centery
                dist = (dx**2 + dy**2) ** 0.5 or 1
                galinha.vel_x = dx / dist * KB_INIMIGO
                galinha.vel_y = dy / dist * KB_INIMIGO
                galinha.tempo_recuo = 15
                if galinha.vida <= 0:
                    galinha.kill(); pato.registrar_kill()
        for galo in list(Galo_group):
            if area.colliderect(galo.rect):
                galo.vida       -= 1
                galo.dano_flash  = DANO_FLASH_DUR
                dx = galo.rect.centerx - pato.rect.centerx
                dy = galo.rect.centery - pato.rect.centery
                dist = (dx**2 + dy**2) ** 0.5 or 1
                galo.vel_x = dx / dist * KB_INIMIGO
                galo.vel_y = dy / dist * KB_INIMIGO
                galo.tempo_recuo = 30
                if galo.vida <= 0:
                    galo.kill(); pato.registrar_kill()
        pato.ataque_timer -= 1

    # 3. Imunidade
    if pato.invensivel > 0: pato.invensivel -= 1

    # 4. Movimento pato
    tecla = pygame.key.get_pressed()
    vx = vy = 0
    spd = pato.vel_atual()
    if tecla[pygame.K_d] or tecla[pygame.K_RIGHT]:  vx =  spd; pato.facing = "dir"
    if tecla[pygame.K_a] or tecla[pygame.K_LEFT]:   vx = -spd; pato.facing = "esq"
    if tecla[pygame.K_w] or tecla[pygame.K_UP]:     vy = -spd
    if tecla[pygame.K_s] or tecla[pygame.K_DOWN]:   vy =  spd

    movendo_pato = vx != 0 or vy != 0
    if movendo_pato:
        mag = (vx**2 + vy**2) ** 0.5
        pato.ultima_dir_x = vx / mag
        pato.ultima_dir_y = vy / mag

    em_dash_agora = pato.dash_timer > 0
    if em_dash_agora:
        vx += pato.dash_vx
        vy += pato.dash_vy
        pato.dash_timer -= 1
        if pato.dash_timer == 0:
            pato.invensivel = max(pato.invensivel, DASH_POS_INVUL)

    vx += pato.vel_x; vy += pato.vel_y
    pato.vel_x *= FRICCAO; pato.vel_y *= FRICCAO
    if abs(pato.vel_x) < 0.1: pato.vel_x = 0
    if abs(pato.vel_y) < 0.1: pato.vel_y = 0

    anterior_x, anterior_y = pato.rect.x, pato.rect.y
    pato.rect.x += vx
    pato.rect.y += vy

    for m in muro_group:
        if pato.rect.colliderect(m.rect):
            pato.rect.x, pato.rect.y = anterior_x, anterior_y
            pato.vel_x = pato.vel_y = 0
            pato.dash_timer = 0
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

    pato.atualizar_animacao(movendo_pato, pato.ataque_timer > 0)

    # dash em fúria — corpo causa dano
    if pato.furia_ativa and em_dash_agora:
        area_dash = pato.rect.inflate(8, 8)
        for galinha in list(Galinha_group):
            if area_dash.colliderect(galinha.rect):
                galinha.vida      -= FURIA_DANO_DASH
                galinha.dano_flash = DANO_FLASH_DUR
                if galinha.vida <= 0:
                    galinha.kill(); pato.registrar_kill()
        for galo in list(Galo_group):
            if area_dash.colliderect(galo.rect):
                galo.vida      -= FURIA_DANO_DASH
                galo.dano_flash = DANO_FLASH_DUR
                if galo.vida <= 0:
                    galo.kill(); pato.registrar_kill()

    # 5. Câmera
    cam_x = max(0, min(pato.rect.centerx - largura // 2, largura_mundo - largura))
    cam_y = max(0, min(pato.rect.centery - altura  // 2, altura_mundo  - altura))

    # 6. Galinhas
    for galinha in Galinha_group:
        if galinha.vida <= 0: galinha.kill(); pato.registrar_kill(); continue
        dx = pato.rect.centerx - galinha.rect.centerx
        dy = pato.rect.centery - galinha.rect.centery
        dist = (dx**2 + dy**2) ** 0.5
        if dist == 0: continue
        galinha_x, galinha_y = galinha.rect.x, galinha.rect.y
        move_dx = 0

        if galinha.tempo_recuo > 0:
            galinha.tempo_recuo -= 1
        elif dist < DIST_ALERTA:
            dist_seg = 100
            if dist >= dist_seg + 30:
                galinha.rect.x += 1 if pygame.time.get_ticks() // 500 % 2 == 0 else -1
                move_dx = dx
            elif dist > dist_seg + 20:
                galinha.rect.x += dx / dist; galinha.rect.y += dy / dist; move_dx = dx
            elif dist < dist_seg - 20:
                galinha.rect.x -= dx / dist; galinha.rect.y -= dy / dist; move_dx = -dx
            else:
                galinha.rect.x += -dy / dist; galinha.rect.y += dx / dist; move_dx = -dy
        else:
            if galinha.patrol_pausa > 0:
                galinha.patrol_pausa -= 1
            else:
                destino = galinha.patrol_origem_x + galinha.patrol_dir * PATROL_RANGE
                diff = destino - galinha.rect.x
                if abs(diff) <= galinha.patrol_speed + 1:
                    galinha.patrol_dir *= -1; galinha.patrol_pausa = 60
                else:
                    galinha.rect.x += galinha.patrol_dir * galinha.patrol_speed
                    move_dx = galinha.patrol_dir

        galinha.rect.x += galinha.vel_x; galinha.rect.y += galinha.vel_y
        galinha.vel_x *= FRICCAO; galinha.vel_y *= FRICCAO
        if abs(galinha.vel_x) < 0.1: galinha.vel_x = 0
        if abs(galinha.vel_y) < 0.1: galinha.vel_y = 0

        for m in muro_group:
            if galinha.rect.colliderect(m.rect):
                galinha.rect.x, galinha.rect.y = galinha_x, galinha_y
                galinha.vel_x = galinha.vel_y = 0; break

        galinha.rect.left   = max(0, galinha.rect.left)
        galinha.rect.right  = min(largura_mundo, galinha.rect.right)
        galinha.rect.top    = max(0, galinha.rect.top)
        galinha.rect.bottom = min(altura_mundo, galinha.rect.bottom)
        movendo = abs(galinha.vel_x) > 0.5 or abs(move_dx) > 0
        galinha.atualizar_animacao(movendo, move_dx if move_dx != 0 else galinha.vel_x)

    # 7. Galos
    for galo in Galo_group:
        if galo.vida <= 0: galo.kill(); pato.registrar_kill(); continue
        dx = pato.rect.centerx - galo.rect.centerx
        dy = pato.rect.centery - galo.rect.centery
        dist = (dx**2 + dy**2) ** 0.5
        galo_x, galo_y = galo.rect.x, galo.rect.y
        move_dx = 0; atacando = False

        if galo.tempo_recuo > 0:
            if dist > 0:
                galo.rect.x -= dx / dist; galo.rect.y -= dy / dist
            galo.tempo_recuo -= 1; move_dx = -dx
        elif dist < DIST_ALERTA:
            if dist > 0:
                galo.rect.x += dx / dist * 2; galo.rect.y += dy / dist * 2
                move_dx = dx
            atacando = galo.rect.colliderect(pato.rect)
        else:
            if galo.patrol_pausa > 0:
                galo.patrol_pausa -= 1
            else:
                destino = galo.patrol_origem_x + galo.patrol_dir * PATROL_RANGE
                diff = destino - galo.rect.x
                if abs(diff) <= galo.patrol_speed + 1:
                    galo.patrol_dir *= -1; galo.patrol_pausa = 60
                else:
                    galo.rect.x += galo.patrol_dir * galo.patrol_speed
                    move_dx = galo.patrol_dir

        galo.rect.x += galo.vel_x; galo.rect.y += galo.vel_y
        galo.vel_x *= FRICCAO; galo.vel_y *= FRICCAO
        if abs(galo.vel_x) < 0.1: galo.vel_x = 0
        if abs(galo.vel_y) < 0.1: galo.vel_y = 0

        for m in muro_group:
            if galo.rect.colliderect(m.rect):
                galo.rect.x, galo.rect.y = galo_x, galo_y
                galo.vel_x = galo.vel_y = 0; break

        galo.rect.left   = max(0, galo.rect.left)
        galo.rect.right  = min(largura_mundo, galo.rect.right)
        galo.rect.top    = max(0, galo.rect.top)
        galo.rect.bottom = min(altura_mundo, galo.rect.bottom)
        movendo = abs(galo.vel_x) > 0.5 or abs(move_dx) > 0
        galo.atualizar_animacao(movendo, move_dx if move_dx != 0 else galo.vel_x, atacando)

        if galo.rect.colliderect(pato.rect) and pato.invensivel == 0 and not pato.em_dash():
            pato.vida -= 1; pato.invensivel = 60
            pato.tomar_dano()
            kx = pato.rect.centerx - galo.rect.centerx
            ky = pato.rect.centery - galo.rect.centery
            kdist = (kx**2 + ky**2) ** 0.5 or 1
            pato.vel_x = kx / kdist * KB_PATO
            pato.vel_y = ky / kdist * KB_PATO
            for g in Galo_group: g.tempo_recuo = 60

    # 8. Ovos
    for ovo in ovo_group:
        ovo.rect.x += ovo.vel_x; ovo.rect.y += ovo.vel_y
        if pato.rect.colliderect(ovo.rect):
            if pato.invensivel == 0 and not pato.em_dash():
                pato.vida -= 1; pato.invensivel = 30
                pato.tomar_dano()
                kx = pato.rect.centerx - ovo.rect.centerx
                ky = pato.rect.centery - ovo.rect.centery
                kdist = (kx**2 + ky**2) ** 0.5 or 1
                pato.vel_x = kx / kdist * KB_PATO
                pato.vel_y = ky / kdist * KB_PATO
            ovo.kill(); continue
        if (ovo.rect.right < 0 or ovo.rect.left > largura_mundo or
                ovo.rect.bottom < 0 or ovo.rect.top > altura_mundo):
            ovo.kill()

    tempo_ovo += 1
    if tempo_ovo >= 150:
        for galinha in Galinha_group:
            dx = pato.rect.centerx - galinha.rect.centerx
            dy = pato.rect.centery - galinha.rect.centery
            dist = (dx**2 + dy**2) ** 0.5
            if dist == 0: continue
            if dist <= 300:
                ovo_group.add(Ovo(galinha.rect.centerx, galinha.rect.centery,
                                  pato.rect.centerx, pato.rect.centery))
        tempo_ovo = 0

    for m in muro_group:
        for ovo in ovo_group:
            if ovo.rect.colliderect(m.rect): ovo.kill()

    # 9. Item de cura
    for cura in list(cura_group):
        if pato.rect.colliderect(cura.rect):
            pato.vida = min(pato.vida_max, pato.vida + CURA_QUANTIDADE)
            cura.kill()

    # 10. Princesa
    for p in Princesa_group: p.atualizar_animacao()

    if pato.vida <= 0: rodando = False

    if len(Galinha_group) == 0 and len(Galo_group) == 0:
        Princesa.liberada = True

    # 11. Renderização
    tela.fill((0, 0, 0))
    tela.blit(chao_surface, (0, 0), (cam_x, cam_y, largura, altura))

    for m in muro_group:
        sx, sy = m.rect.x - cam_x, m.rect.y - cam_y
        if -AZULEJO < sx < largura and -AZULEJO < sy < altura:
            tela.blit(m.image, (sx, sy))

    for c in cura_group:
        tela.blit(c.image, (c.rect.x - cam_x, c.rect.y - cam_y))
    for galinha in Galinha_group:
        tela.blit(galinha.image, (galinha.rect.x - cam_x, galinha.rect.y - cam_y))
    for galo in Galo_group:
        tela.blit(galo.image, (galo.rect.x - cam_x, galo.rect.y - cam_y))
    for ovo in ovo_group:
        tela.blit(ovo.image, (ovo.rect.x - cam_x, ovo.rect.y - cam_y))
    for p in Princesa_group:
        tela.blit(p.image, (p.rect.x - cam_x, p.rect.y - cam_y))

    if pato.em_dash():
        dash_img = pato.image.copy()
        dash_img.fill((100, 180, 255, 80), special_flags=pygame.BLEND_RGBA_ADD)
        tela.blit(dash_img, (pato.rect.x - cam_x, pato.rect.y - cam_y))
    elif pato.invensivel == 0 or (pato.invensivel // 5) % 2 == 0:
        tela.blit(pato.image, (pato.rect.x - cam_x, pato.rect.y - cam_y))

    desenhar_hud(tela, pato)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()