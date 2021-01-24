import pygame
from pygame import mixer
import pickle
from os import path
#запускаем музон сразу с проектом
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()
#ставим фпс
clock = pygame.time.Clock()
fps = 60
#размеры окна
shirina_okna = 1000
visota_okna = 1000
#имя там и тому подобное
screen = pygame.display.set_mode((shirina_okna, visota_okna))
pygame.display.set_caption('ММММММ ФОНК')
#мышь невидима(где же она?)
pygame.mouse.set_visible(False)


#шрефты
shrift = pygame.font.SysFont('Bauhaus 93', 70)
shrift1 = pygame.font.SysFont('Bauhaus 93', 60)
shrift2 = pygame.font.SysFont('Bauhaus 93', 30)


#игровые параметры, значения
razmer = 50
proigrish = 0
osnov_menu = True
uroven = 1
vsego_uroven = 10
stata = 0


#обозначаем цвета
white = (255, 255, 255)
blue = (0, 0, 255)
black = (0, 0, 0)


#загружаем изображения
fon = pygame.image.load('homyak_fon.png')
ponovoi_img = pygame.image.load('zanovo1.png')
nachat_img = pygame.image.load('nachat.png')
fonksila_img = pygame.image.load('fonksila.png')
vihod_img = pygame.image.load('vihod.png')

#ММММММММ ФОНК
pygame.mixer.music.load('я научу играть вас на фортепиано тудудудудудуду.mp3')
pygame.mixer.music.play(-5, 7.3, 10)
pygame.mixer.music.set_volume(0.2)
zvuk_kur = pygame.mixer.Sound('hrust.mp3')
zvuk_kur.set_volume(0.2)
zvuk_prijka = pygame.mixer.Sound('prig.mp3')
zvuk_prijka.set_volume(0.1)
zvuk_kakaya_jalost = pygame.mixer.Sound('jalost.mp3')
zvuk_kakaya_jalost.set_volume(0.)

#функция вывода текста
def risuem_text(text, font, text_col, x, y):
    izobr = font.render(text, True, text_col)
    screen.blit(izobr, (x, y))


#функция для обновления уровня
def peresapusk_urovnya(level):
    igrock.vot_i_pomer(100, visota_okna - 130)
    gruppa_vragi.empty()
    gruppa_platform.empty()
    gruppa_monetki.empty()
    gruppa_lava.empty()
    gruppa_portala.empty()

    #тут мудрим с загрузкой уровня из папки с файлом
    if path.exists(f'level{level}_data'):
        atkroi = open(f'level{level}_data', 'rb')
        dannie_mira = pickle.load(atkroi)
    mir = Mir(dannie_mira)
    #обновили монет ки
    return mir

#отвечает, логично, за кнопки
class Knopka():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
    #рисуем кноп очки
    def otrisovka(self):
        a_kak_eto_nazvat = False

        #чекаем, где мышь(да куда она делась, почему вместо нее хомяк???)
        pos = pygame.mouse.get_pos()

        #проверяем нажатие мыш.... хомяка.
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                a_kak_eto_nazvat = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        #отображаем кноп (линзы в оправе)
        screen.blit(self.image, self.rect)

        return a_kak_eto_nazvat

#щтош, вот и класс, (ставь класс) отвечающий за игрока(дада, он огромный)
class Igrock():
    def __init__(self, x, y):
        self.vot_i_pomer(x, y)
    #переменные нужные для ходьбы
    def update(self, igra_okonchena):
        po_iksu = 0
        po_igreky = 0
        dvijenie = 5
        eshe = 20
        #пишем движение при нажатии на кнопки
        if igra_okonchena == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.prijok == False and self.v_vozduhe == False:
                zvuk_prijka.play()
                self.po_igreku = -15
                self.prijok = True
            if key[pygame.K_SPACE] == False:
                self.prijok = False
            if key[pygame.K_LEFT]:
                po_iksu -= 5
                self.peremennaya_dlya_ismeneniya += 1
                self.dada = -1
            if key[pygame.K_RIGHT]:
                po_iksu += 5
                self.peremennaya_dlya_ismeneniya += 1
                self.dada = 1
                #изменяем при нажатии налево картин очку
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.peremennaya_dlya_ismeneniya = 0
                self.da = 0
                if self.dada == 1:
                    self.kartinka = self.napravo[self.da]
                if self.dada == -1:
                    self.kartinka = self.nalevo[self.da]


            #изменение картинки при повороте в др. сторону
            if self.peremennaya_dlya_ismeneniya > dvijenie:
                self.peremennaya_dlya_ismeneniya = 0
                self.da += 1
                if self.da >= len(self.napravo):
                    self.da = 0
                if self.dada == 1:
                    self.kartinka = self.napravo[self.da]
                if self.dada == -1:
                    self.kartinka = self.nalevo[self.da]


            #gravity - это трек у Architects такой, крутой кста
            self.po_igreku += 1
            if self.po_igreku > 10:
                self.po_igreku = 10
            po_igreky += self.po_igreku

            #столкновения просто, в прыжке, и в падении
            self.v_vozduhe = True
            for tile in mir.spisok_s_lvl:
                if tile[1].colliderect(self.rect.x + po_iksu, self.rect.y, self.shirina, self.visota):
                    po_iksu = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + po_igreky, self.shirina, self.visota):
                    if self.po_igreku < 0:
                        po_igreky = tile[1].bottom - self.rect.top
                        self.po_igreku = 0
                    #не падай, если падать некуда ://
                    elif self.po_igreku >= 0:
                        po_igreky = tile[1].top - self.rect.bottom
                        self.po_igreku = 0
                        self.v_vozduhe = False


            #столкновения с врогами
            if pygame.sprite.spritecollide(self, gruppa_vragi, False):
                igra_okonchena = -1
                zvuk_kakaya_jalost.play()

            #с чем же?
            if pygame.sprite.spritecollide(self, gruppa_lava, False):
                igra_okonchena = -1
                zvuk_kakaya_jalost.play()

            #выход.
            if pygame.sprite.spritecollide(self, gruppa_portala, False):
                igra_okonchena = 1


            #платформы.
            for platformochki in gruppa_platform:
                if platformochki.rect.colliderect(self.rect.x + po_iksu, self.rect.y, self.shirina, self.visota):
                    po_iksu = 0
                if platformochki.rect.colliderect(self.rect.x, self.rect.y + po_igreky, self.shirina, self.visota):
                    #если на платформе
                    if abs((self.rect.top + po_igreky) - platformochki.rect.bottom) < eshe:
                        self.po_igreku = 0
                        po_igreky = platformochki.rect.bottom - self.rect.top
                    elif abs((self.rect.bottom + po_igreky) - platformochki.rect.top) < eshe:
                        self.rect.bottom = platformochki.rect.top - 1
                        self.v_vozduhe = False
                        po_igreky = 0
                    if platformochki.move_x != 0:
                        self.rect.x += platformochki.move_direction


            #обновите позицию шаурмы кто нибудь...
            self.rect.x += po_iksu
            self.rect.y += po_igreky

        #КАКАЯ ЖАААААЛОСТЬ, ТЫ ВЫЛЕТАЕШЬ, ДРУЖОК, СИ Ю НЕКСТ ГЕЙМ, ДО ВСТРЕЧИ В ДРУГОМ ЛОББИ!!!!!!
        elif igra_okonchena == -1:
            self.kartinka = self.kartinka_pomer
            risuem_text('КАКАЯ ЖАЛОСТЬ, ТЫ ПРОИГРАЛ ДРУЖОК!', shrift1, black, 30, 450)

        #давайте рисовать
        screen.blit(self.kartinka, self.rect)

        return igra_okonchena

    #вдруг кто умрет в моей элементарной игре, надо же дать второй шанс и показать грустную шаурму, чтобы не повадно было умирать
    def vot_i_pomer(self, x, y):
        self.napravo = []
        self.nalevo = []
        self.da = 0
        self.peremennaya_dlya_ismeneniya = 0
        for num in range(1, 5):
            napravo = pygame.image.load('shava1.png')
            napravo = pygame.transform.scale(napravo, (40, 80))
            nalevo = pygame.transform.flip(napravo, True, False)
            self.napravo.append(napravo)
            self.nalevo.append(nalevo)
        self.kartinka_pomer = pygame.image.load('shavadead.png')
        self.kartinka = self.napravo[self.da]
        self.rect = self.kartinka.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.shirina = self.kartinka.get_width()
        self.visota = self.kartinka.get_height()
        self.po_igreku = 0
        self.prijok = False
        self.dada = 0
        self.v_vozduhe = True


#класс хелло ворлд
class Mir():
    def __init__(self, soderjimoe):
        self.spisok_s_lvl = []

        #картинки травки(осуждаю) и земельки
        kart_zemlya = pygame.image.load('zemelka.png')
        kart_travka = pygame.image.load('grassyy.png')
        #ВОТ ТУТ ИНТЕРЕСНО!!! мы считываем кодировку уровня с папки проекта, и если там 1 - блок земли, 2 - травы и так далее, как я обозначил
        perem = 0
        for zagr_urov in soderjimoe:
            esh_perem = 0
            for oboznach in zagr_urov:
                if oboznach == 1:
                    kartinka = pygame.transform.scale(kart_zemlya, (razmer, razmer))
                    img_rect = kartinka.get_rect()
                    img_rect.x = esh_perem * razmer
                    img_rect.y = perem * razmer
                    oboznach = (kartinka, img_rect)
                    self.spisok_s_lvl.append(oboznach)
                if oboznach == 2:
                    kartinka = pygame.transform.scale(kart_travka, (razmer, razmer))
                    img_rect = kartinka.get_rect()
                    img_rect.x = esh_perem * razmer
                    img_rect.y = perem * razmer
                    oboznach = (kartinka, img_rect)
                    self.spisok_s_lvl.append(oboznach)
                if oboznach == 3:
                    blob = Vrag1(esh_perem * razmer, perem * razmer + 15)
                    gruppa_vragi.add(blob)
                if oboznach == 4:
                    platform = Platform(esh_perem * razmer, perem * razmer, 1, 0)
                    gruppa_platform.add(platform)
                if oboznach == 5:
                    platform = Platform(esh_perem * razmer, perem * razmer, 0, 1)
                    gruppa_platform.add(platform)
                if oboznach == 6:
                    lava = Lava(esh_perem * razmer, perem * razmer + (razmer // 2))
                    gruppa_lava.add(lava)
                if oboznach == 7:
                    coin = Kurochki(esh_perem * razmer + (razmer // 2), perem * razmer + (razmer // 2))
                    gruppa_monetki.add(coin)
                if oboznach == 8:
                    exit = Portal(esh_perem * razmer, perem * razmer)
                    gruppa_portala.add(exit)
                if oboznach == 9:
                    vrag2 = Vrag2(esh_perem * razmer, perem * razmer + 15)
                    gruppa_vragi.add(vrag2)
                if oboznach == 10:
                    homa = Homa(esh_perem * razmer, perem * razmer)
                    gruppa_vragi.add(homa)
                esh_perem += 1
            perem += 1

    #опять таки, отрисовали все
    def draw(self):
        for tile in self.spisok_s_lvl:
            screen.blit(tile[0], tile[1])


#прописываем класс врагов: картинки там, движения и тому подобное
class Vrag1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('drug.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.dvijeniya = 0

    def update(self):
        self.rect.x += self.move_direction
        self.dvijeniya += 1
        if abs(self.dvijeniya) > 50:
            self.move_direction *= -1
            self.dvijeniya *= -1

class Vrag2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('drug.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.dvijeniya = 0

    def update(self):
        self.rect.x += self.move_direction
        self.dvijeniya += 1
        if abs(self.dvijeniya) > 410:
            self.move_direction *= -1
            self.dvijeniya *= -1

#прописываем двигающуюся платформу
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('oblachko.png')
        self.image = pygame.transform.scale(img, (razmer, razmer // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.move_y = move_y


    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1




#ну что же это может быть?
class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('лава.png')
        self.image = pygame.transform.scale(img, (razmer, razmer // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Homa(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('homyakbez1.png')
        self.image = pygame.transform.scale(img, (razmer, razmer))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#прописываем монетки
class Kurochki(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        izobr = pygame.image.load('nyam.png')
        self.image = pygame.transform.scale(izobr, (razmer // 2, razmer // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

#прописываем выход, скучно ме
class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        izobr = pygame.image.load('homyakbez1.png')
        self.image = pygame.transform.scale(izobr, (razmer, razmer))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


#позиция игрока
igrock = Igrock(100, visota_okna - 130)
#присвоим переменным значение спрайт группы (фигово обьяснил, но сам я понял)
gruppa_vragi = pygame.sprite.Group()
gruppa_platform = pygame.sprite.Group()
gruppa_lava = pygame.sprite.Group()
gruppa_monetki = pygame.sprite.Group()
gruppa_portala = pygame.sprite.Group()
gruppa_vragi2 = pygame.sprite.Group()
gruppa_homa = pygame.sprite.Group()


#загружаем уровни(если существуют)
if path.exists(f'level{uroven}_data'):
    pickle_in = open(f'level{uroven}_data', 'rb')
    dannie_mira = pickle.load(pickle_in)
mir = Mir(dannie_mira)


#ну опять таки, создаем кнопки
knopka_zanovo = Knopka(350, 600, ponovoi_img)
start_button = Knopka(shirina_okna // 2 - 350, visota_okna // 2, nachat_img)
exit_button = Knopka(shirina_okna // 2 + 150, visota_okna // 2, vihod_img)
fonksila_button = Knopka(100, 200, fonksila_img)
#ОСНОВНОЙ ЦИКЛ ПРОГИ ЬЪЬЪЪЬЪЬЪЬЪЬЬЬЪЬЬЬЬЬЪЪЪ!!!!!!!
always = True
while always:
    #проверка фпс
    clock.tick(fps)
    #отображаем фон(не к((()
    screen.blit(fon, (0, 0))
    #привязываем кнопки к функции начала и выхода
    if osnov_menu == True:
        if exit_button.otrisovka():
            always = False
        if start_button.otrisovka():
            osnov_menu = False
        if fonksila_button.otrisovka():
            osnov_menu = False
    else:
        mir.draw()
        #пока играем, отображаем снизу курочек собрано, ведем отсчет кур очек и выводим на экран
        if proigrish == 0:
            gruppa_vragi.update()
            gruppa_platform.update()
            if pygame.sprite.spritecollide(igrock, gruppa_monetki, True):
                stata += 1
                zvuk_kur.play()
                if stata >= 6:
                    risuem_text('а ты лучше, чем я думал', shrift1, black, 50, 450)
            risuem_text('курочек собрано: ' + str(stata), shrift2, white, 10, 970)
        #ВСЕЕЕ ОТОБРАЗИИИТЬ
        gruppa_vragi.draw(screen)
        gruppa_platform.draw(screen)
        gruppa_lava.draw(screen)
        gruppa_monetki.draw(screen)
        gruppa_portala.draw(screen)

        proigrish = igrock.update(proigrish)

        #если помер дед максим(999((9(( по новой
        if proigrish == -1:
            if knopka_zanovo.otrisovka():
                dannie_mira = []
                mir = peresapusk_urovnya(uroven)
                proigrish = 0
                stata = 0
        #если чел крутой и прошел уровень
        if proigrish == 1:
            #прибавляем 1 и запускаем следующий по нумерации
            uroven += 1
            if uroven <= vsego_uroven:
                dannie_mira = []
                mir = peresapusk_urovnya(uroven)
                proigrish = 0
                #ЕСЛИ ВСЕ ПРОШЕЛ, ТО НЕ ЗАВИДУЕМ ЭТОМУ ИНДИВИДУ
            else:
                risuem_text('КРУТОЙ ЧЕЛ, СКИЛЛОВЫЙ', shrift, black, 200, visota_okna // 2)
                if knopka_zanovo.otrisovka():
                    uroven = 1
                    #и опять после прохождения можно обновить
                    dannie_mira = []
                    mir = peresapusk_urovnya(uroven)
                    proigrish = 0
                    stata = 0
    #превращаем мышь(вжжжух!) в хомяка
    if pygame.mouse.get_focused():
        pos = pygame.mouse.get_pos()
        mish = pygame.image.load('homyakbez1.png')
        screen.blit(mish, (pos[0], pos[1]))
    # ну как бы если выход, то выход
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            always = False
    #обновляем
    pygame.display.update()
#выходим(99((
pygame.quit()