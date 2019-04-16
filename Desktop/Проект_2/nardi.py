import pygame
import os
from random import choice

pygame.init()
size = 1000, 1000
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Нарды")
color = pygame.Color('white')


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        global posic1
        posic1 = [0]
        global posic2
        posic2 = [0]
        global beliy
        beliy = [0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 2]
        global cherniy
        cherniy = [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 3, 0,
                   5, 0, 0, 0, 0, 0]

    def render(self):
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, color,
                                 (i * self.cell_size + self.left,
                                  j * self.cell_size + self.top,
                                  self.cell_size, self.cell_size), 1)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def hod(self, kletk, cvet):
        if cvet == 0:
            if cherniy[kletk - 2] == 0:
                return True
            else:
                return False
        else:
            if beliy[kletk] == 0:
                return True
            else:
                return False

    def poed(self, kletk, cvet):
        if cvet == 0:
            if cherniy[kletk - 3] == 1:
                posic1[0] += 1
        else:
            if beliy[kletk] == 1:
                return True
            else:
                return False

    def vozvrat(self, kletk, cvet):
        if cvet == 0:
            beliy[kletk - 1] -= 1
            beliy[kletk - 2] += 1
            return (beliy[kletk - 2] - 1)
        else:
            cherniy[kletk - 1] -= 1
            cherniy[kletk] += 1
            return (cherniy[kletk] - 1)

    def spis(self, kletk, a, cvet):
        if a == 0:
            if cvet == 0:
                return (beliy[kletk - 1] - 1)
            else:
                return (cherniy[kletk - 1] - 1)
        else:
            if cvet == 0:
                return (beliy[kletk - 2] + 1)
            else:
                return (cherniy[kletk] + 1)


class Beliy(pygame.sprite.Sprite):
    image = load_image("beliy.png")

    def __init__(self, x, rasp, kletk):
        super().__init__(all_sprites2)
        self.image = Beliy.image
        self.rect = self.image.get_rect()
        self.x = x[0]
        self.y = x[1]
        self.rect.x = self.x
        self.rect.y = self.y
        self.f = False
        self.rasp = rasp
        self.kletk = kletk
        self.perehod = False
        self.cvet = 0
        self.d = False

    def nagat(self, event):
        s = Board.spis(self, self.kletk, 0, self.cvet)
        k = Board.spis(self, self.kletk, 1, self.cvet)
        if self.rect.collidepoint(event.pos):
            if self.rasp == 1:
                if (self.rect.y == (42 + 62 * s)) and (k < 8):
                    self.f = True
            else:
                if (self.rect.y == (910 - 62 * s)) and (k < 8):
                    self.f = True

    def on_board(self, event):
        if self.f:
            self.rect.x = event.pos[0] - 20
            self.rect.y = event.pos[1] - 20

    def otgat(self):
        self.hod_prois = False
        if self.kletk == 13:
            self.rasp = 0
        if self.rasp == 1:
            a = Board.hod(self, self.kletk, self.cvet)
            a1 = self.x - 62
            t = a1 - 61 <= self.rect.x < a1 + 62
            m = 42 <= self.rect.y <= 476
            if t and m and a:
                self.hod_prois = True
                hod = Board.vozvrat(self, self.kletk, self.cvet)
                self.kletk -= 1
                self.x = a1
                if self.kletk == 18:
                    self.x = 394
                self.y = hod * 62 + 42
        else:
            a = Board.hod(self, self.kletk, self.cvet)
            a1 = self.x + 62
            t = a1 - 61 <= self.rect.x < a1 + 62
            m = 538 <= self.rect.y <= 910
            if t and m and a:
                self.hod_prois = True
                hod = Board.vozvrat(self, self.kletk, self.cvet)
                self.kletk -= 1
                self.x = a1
                if self.kletk == 12:
                    self.x -= 62
                elif self.kletk == 6:
                    self.x = 546
                self.y = 910 - hod * 62
            else:
                if self.kletk == 13:
                    self.rasp = 1

        self.rect.topleft = self.x, self.y
        self.f = False

    def game_process(self):
        return self.hod_prois


class Cherniy(pygame.sprite.Sprite):
    image = load_image("cherniy.png")

    def __init__(self, x, rasp, kletk):
        super().__init__(all_sprites3)
        self.image = Cherniy.image
        self.rect = self.image.get_rect()
        self.x = x[0]
        self.y = x[1]
        self.rect.x = self.x
        self.rect.y = self.y
        self.f = False
        self.rasp = rasp
        self.kletk = kletk
        self.cvet = 1

    def nagat(self, event):
        s = Board.spis(self, self.kletk, 0, self.cvet)
        k = Board.spis(self, self.kletk, 1, self.cvet)
        if self.rect.collidepoint(event.pos):
            if self.rasp == 1:
                if (self.rect.y == (42 + 62 * s)) and (k < 8):
                    self.f = True
            else:
                if (self.rect.y == (910 - 62 * s)) and (k < 8):
                    self.f = True

    def on_board(self, event):
        if self.f:
            self.rect.x = event.pos[0] - 20
            self.rect.y = event.pos[1] - 20

    def otgat(self):
        self.hod_prois = False
        if self.kletk == 12:
            self.rasp = 1
        if self.rasp == 1:
            a = Board.hod(self, self.kletk, self.cvet)
            a1 = self.x + 62
            t = a1 - 61 <= self.rect.x < a1 + 62
            m = self.rect.y <= 476
            if t and m and a:
                self.hod_prois = True
                hod = Board.vozvrat(self, self.kletk, self.cvet)
                self.kletk += 1
                self.x = a1
                if self.kletk == 19:
                    self.x = 546
                elif self.kletk == 13:
                    self.x -= 62
                self.y = hod * 62 + 42
            else:
                if self.kletk == 12:
                    self.rasp = 0
        else:
            a = Board.hod(self, self.kletk, self.cvet)
            a1 = self.x - 62
            t = a1 - 61 <= self.rect.x < a1 + 62
            m = 538 <= self.rect.y
            if t and m and a:
                self.hod_prois = True
                hod = Board.vozvrat(self, self.kletk, self.cvet)
                self.kletk += 1
                self.x = a1
                if self.kletk == 7:
                    self.x = 394
                self.y = 910 - hod * 62

        self.rect.topleft = self.x, self.y
        self.f = False

    def game_process(self):
        return self.hod_prois


class arrow(pygame.sprite.Sprite):
    image = load_image("arrow.png")

    def __init__(self):
        super().__init__(all_sprites1)
        self.image = arrow.image
        self.rect = self.image.get_rect()

    def cursor(self, event):
        self.rect.topleft = event.pos


class kubik:
    def __init__(self, a, b, cvet):
        self.a = a
        self.b = b
        self.cvet = cvet

    def brosok(self):
        if self.cvet == 0:
            a1 = 239
            b1 = 302
        else:
            a1 = 701
            b1 = 764
        if self.a == 1:
            pygame.draw.circle(screen, pygame.Color("black"), [a1, 507], 7)

        elif self.a == 2:
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 + 20, 487], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 - 20, 527], 7)

        elif self.a == 3:
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 + 20, 487], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 - 20, 527], 7)
            pygame.draw.circle(screen, pygame.Color("black"), [a1, 507], 7)

        elif self.a == 4:
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 + 20, 487], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 - 20, 527], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 - 20, 487], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 + 20, 527], 7)

        elif self.a == 5:
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 + 20, 487], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 - 20, 527], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 - 20, 487], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 + 20, 527], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1, 507], 7)

        elif self.a == 6:
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 + 20, 487], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 - 20, 527], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 - 20, 487], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 + 20, 527], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 - 20, 507], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [a1 + 20, 507], 7)

        if self.b == 1:
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1, 507], 7)

        elif self.b == 2:
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 - 20, 527], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 + 20, 487], 7)

        elif self.b == 3:
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 - 20, 527], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 + 20, 487], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1, 507], 7)

        elif self.b == 4:
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 - 20, 527], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 + 20, 487], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 + 20, 527], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 - 20, 487], 7)

        elif self.b == 5:
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 - 20, 527], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 + 20, 487], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 + 20, 527], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 - 20, 487], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1, 507], 7)

        elif self.b == 6:
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 - 20, 527], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 + 20, 487], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 + 20, 527], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 - 20, 487], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 - 20, 507], 7)
            pygame.draw.circle(screen, pygame.Color("black"),
                               [b1 + 20, 507], 7)


all_sprites = pygame.sprite.Group()
all_sprites1 = pygame.sprite.Group()
all_sprites2 = pygame.sprite.Group()
all_sprites3 = pygame.sprite.Group()

sprite_image = load_image("pole.jpg")
sprite = pygame.sprite.Sprite(all_sprites)
sprite.image = sprite_image
sprite.rect = sprite.image.get_rect()


sashkab1 = Beliy((84, 42), 1, 13)
sashkab2 = Beliy((84, 104), 1, 13)
sashkab3 = Beliy((84, 166), 1, 13)
sashkab4 = Beliy((84, 228), 1, 13)
sashkab5 = Beliy((84, 290), 1, 13)
sashkab6 = Beliy((332, 910), 0, 8)
sashkab7 = Beliy((332, 848), 0, 8)
sashkab8 = Beliy((332, 786), 0, 8)
sashkab9 = Beliy((546, 910), 0, 6)
sashkab10 = Beliy((546, 848), 0, 6)
sashkab11 = Beliy((546, 786), 0, 6)
sashkab12 = Beliy((546, 724), 0, 6)
sashkab13 = Beliy((546, 662), 0, 6)
sashkab14 = Beliy((856, 42), 1, 24)
sashkab15 = Beliy((856, 104), 1, 24)
sashkac1 = Cherniy((84, 910), 0, 12)
sashkac2 = Cherniy((84, 848), 0, 12)
sashkac3 = Cherniy((84, 786), 0, 12)
sashkac4 = Cherniy((84, 724), 0, 12)
sashkac5 = Cherniy((84, 662), 0, 12)
sashkac6 = Cherniy((332, 42), 1, 17)
sashkac7 = Cherniy((332, 104), 1, 17)
sashkac8 = Cherniy((332, 166), 1, 17)
sashkac9 = Cherniy((546, 42), 1, 19)
sashkac10 = Cherniy((546, 104), 1, 19)
sashkac11 = Cherniy((546, 166), 1, 19)
sashkac12 = Cherniy((546, 228), 1, 19)
sashkac13 = Cherniy((546, 290), 1, 19)
sashkac14 = Cherniy((856, 910), 0, 1)
sashkac15 = Cherniy((856, 848), 0, 1)
dvor = Board(6, 15)
dvor.set_view(84, 42, 62)
dom = Board(6, 15)
dom.set_view(546, 42, 62)
zone = Board(1, 15)
zone.set_view(472, 42, 62)
konec = Board(1, 15)
konec.set_view(934, 42, 62)
cursor = arrow()
kub1 = choice((1, 2, 3, 4, 5, 6))
kub2 = choice((1, 2, 3, 4, 5, 6))
cvet = 0
kub = kubik(kub1, kub2, cvet)
nomer_hoda = 1
font = pygame.font.Font('freesansbold.ttf', 50)
orig_surf = font.render('Ход белых', True, (255, 255, 255))
txt_surf = orig_surf.copy()
alpha_surf = pygame.Surface(txt_surf.get_size(),
                            pygame.SRCALPHA)
alpha = 255
hod_prois = False

pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0),
                        (0, 0, 0, 0, 0, 0, 0, 0))

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if nomer_hoda % 2 == 1:
                for k in all_sprites2:
                    k.nagat(event)
            else:
                for k in all_sprites3:
                    k.nagat(event)
        if event.type == pygame.MOUSEMOTION:
            for i in all_sprites1:
                i.cursor(event)

            for k in all_sprites2:
                k.on_board(event)

            for k in all_sprites3:
                k.on_board(event)
        if event.type == pygame.MOUSEBUTTONUP:
            for k in all_sprites2:
                k.otgat()
                hod_prois += k.game_process()
                kub1 = choice((1, 2, 3, 4, 5, 6))
                kub2 = choice((1, 2, 3, 4, 5, 6))

            for k in all_sprites3:
                k.otgat()
                hod_prois += k.game_process()
                kub1 = choice((1, 2, 3, 4, 5, 6))
                kub2 = choice((1, 2, 3, 4, 5, 6))
            if hod_prois >= 1:
                if nomer_hoda % 2 == 1:
                    font = pygame.font.Font('freesansbold.ttf', 50)
                    orig_surf = font.render('Ход чёрных', True, (0, 0, 0))
                    txt_surf = orig_surf.copy()
                    alpha_surf = pygame.Surface(txt_surf.get_size(),
                                                pygame.SRCALPHA)
                    alpha = 255

                    cvet = 1
                else:
                    cvet = 0
                    font = pygame.font.Font('freesansbold.ttf', 50)
                    orig_surf = font.render('Ход белых', True, (255, 255, 255))
                    txt_surf = orig_surf.copy()
                    alpha_surf = pygame.Surface(txt_surf.get_size(),
                                                pygame.SRCALPHA)
                    alpha = 255

                kub = kubik(kub1, kub2, cvet)
    if hod_prois >= 1:
        nomer_hoda += 1
        hod_prois = False
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    all_sprites.update()
    all_sprites2.draw(screen)
    all_sprites2.update()
    all_sprites3.draw(screen)
    all_sprites3.update()
    if nomer_hoda % 2 == 1:
        pygame.draw.rect(screen, pygame.Color('white'), (208, 476, 62, 62), 0)
        pygame.draw.rect(screen, pygame.Color('white'), (271, 476, 62, 62), 0)
        if alpha > 0:
            alpha = max(alpha-4, 0)
            txt_surf = orig_surf.copy()
            alpha_surf.fill((255, 255, 255, alpha))
            txt_surf.blit(alpha_surf, (0, 0),
                          special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(txt_surf, (363, 476))
    else:
        pygame.draw.rect(screen, pygame.Color('white'), (670, 476, 62, 62), 0)
        pygame.draw.rect(screen, pygame.Color('white'), (733, 476, 62, 62), 0)
        if alpha > 0:
            alpha = max(alpha-4, 0)
            txt_surf = orig_surf.copy()
            alpha_surf.fill((255, 255, 255, alpha))
            txt_surf.blit(alpha_surf, (0, 0),
                          special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(txt_surf, (363, 476))
    kub.brosok()
    if pygame.mouse.get_focused():
        all_sprites1.draw(screen)
        all_sprites1.update()
    pygame.display.flip()
    clock.tick(30)
pygame.quit()
