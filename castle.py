#import libraries
import pygame  # استيراد مكتبة Pygame للتعامل مع الرسومات واللعبة
import math    # استيراد مكتبة الرياضيات (للحسابات مثل الزوايا)
import random  # لتوليد أرقام عشوائية (مثل اختيار نوع العدو)
import os      # للتعامل مع الملفات (مثل قراءة high score من ملف)
from enemy import Enemy  # استيراد كلاس Enemy من ملف enemy.py
import button   # استيراد وحدة الأزرار
from pygame import mixer
#initialise pygame
pygame.init()  # تهيئة مكتبة pygame
mixer.init() #تهيئة مكتبة mixer 
#game window
SCREEN_WIDTH = 800     # عرض الشاشة
SCREEN_HEIGHT = 600    # ارتفاع الشاشة

#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # إنشاء نافذة اللعبة
pygame.display.set_caption('Castle Defender')  # تحديد عنوان النافذة
clock = pygame.time.Clock()  # لضبط عدد الإطارات في الثانية
FPS = 60  # عدد الإطارات في الثانية

#define game variables
level = 1  # المستوى الحالي
high_score = 0  # أعلى نتيجة تم تحقيقها
level_difficulty = 0  # صعوبة المستوى الحالي
target_difficulty = 1000  # الصعوبة المستهدفة لهذا المستوى
DIFFICULTY_MULTIPLIER = 1.1  # مضاعف الصعوبة بين المستويات
game_over = False  # حالة اللعبة (انتهت أم لا)
next_level = False  # هل اكتمل المستوى الحالي؟
ENEMY_TIMER = 1000  # الزمن بين ظهور الأعداء (بالميلي ثانية)
last_enemy = pygame.time.get_ticks()  # وقت آخر ظهور لعدو
enemies_alive = 0  # عدد الأعداء الذين لا يزالون أحياء
max_towers = 4  # الحد الأقصى للأبراج التي يمكن بناؤها
TOWER_COST = 5000  # تكلفة بناء برج واحد

# مواقع وضع الأبراج على الشاشة
tower_positions = [
[SCREEN_WIDTH - 250, SCREEN_HEIGHT - 200],
[SCREEN_WIDTH - 200, SCREEN_HEIGHT - 150],
[SCREEN_WIDTH - 150, SCREEN_HEIGHT - 150],
[SCREEN_WIDTH - 100, SCREEN_HEIGHT - 150],
]

#load high score
if os.path.exists('score.txt'):  # إذا كان الملف موجودًا
    with open('score.txt', 'r') as file:  # افتح الملف للقراءة
        high_score = int(file.read())  # اقرأ الـ high score

#define colours
WHITE = (255, 255, 255)  # تعريف اللون الأبيض
GREY = (100, 100, 100)   # تعريف اللون الرمادي

#define font
font = pygame.font.SysFont('Futura', 30)  # خط نصي بحجم 30
font_60 = pygame.font.SysFont('Futura', 60)  # خط نصي بحجم 60

#تحميل الصوت في اللعبة
pygame.mixer.music.load('C:/Users/samo/OneDrive/Desktop/game.py/audio/music2.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)
shot_fx = pygame.mixer.Sound('C:/Users/samo/OneDrive/Desktop/game.py/audio/shot.wav')
shot_fx.set_volume(0.9)
grenade_fx = pygame.mixer.Sound('C:/Users/samo/OneDrive/Desktop/game.py/audio/grenade.wav')
grenade_fx.set_volume(1.5)
jump_fx = pygame.mixer.Sound('C:/Users/samo/OneDrive/Desktop/game.py/audio/jump.wav')
jump_fx.set_volume(0.9)

#load images
bg = pygame.image.load('C:/Users/samo/OneDrive/Desktop/game.py/img/bg.png').convert_alpha()  # تحميل خلفية اللعبة

#castle
castle_img_100 = pygame.image.load('C:/Users/samo/OneDrive/Desktop/game.py/img/castle/castle_100.png').convert_alpha()  # القلعة بصحتها الكاملة
castle_img_50 = pygame.image.load('C:/Users/samo/OneDrive/Desktop/game.py/img/castle/castle_50.png').convert_alpha()    # القلعة بنسبة 50% من الصحة
castle_img_25 = pygame.image.load('C:/Users/samo/OneDrive/Desktop/game.py/img/castle/castle_25.png').convert_alpha()    # القلعة بنسبة 25% من الصحة

#tower
tower_img_100 = pygame.image.load('C:/Users/samo/OneDrive/Desktop/game.py/img/tower/tower_100.png').convert_alpha()  # البرج بصحته الكاملة
tower_img_50 = pygame.image.load('C:/Users/samo/OneDrive/Desktop/game.py/img/tower/tower_50.png').convert_alpha()    # البرج بنسبة 50%
tower_img_25 = pygame.image.load('C:/Users/samo/OneDrive/Desktop/game.py/img/tower/tower_25.png').convert_alpha()    # البرج بنسبة 25%

#bullet image
bullet_img = pygame.image.load('C:/Users/samo/OneDrive/Desktop/game.py/img/bullet.png').convert_alpha()  # تحميل صورة الرصاصة
b_w = bullet_img.get_width()  # الحصول على العرض
b_h = bullet_img.get_height()  # الحصول على الارتفاع
bullet_img = pygame.transform.scale(bullet_img, (int(b_w * 0.075), int(b_h * 0.075)))  # تصغير حجم الرصاصة

#load enemies
enemy_animations = []  # قائمة تحتوي على جميع الرسوم المتحركة للأعداء
enemy_types = ['knight', 'goblin', 'purple_goblin', 'red_goblin']  # أنواع الأعداء
enemy_health = [75, 100, 125, 150]  # صحة كل نوع من الأعداء
animation_types = ['walk', 'attack', 'death']  # أنواع الحركات

for enemy in enemy_types:
    animation_list = []
    for animation in animation_types:
        temp_list = []
        num_of_frames = 20  # عدد الإطارات لكل نوع من الحركات
        for i in range(num_of_frames):
            img = pygame.image.load(f"C:/Users/samo/OneDrive/Desktop/game.py/img/enemies/{enemy}/{animation}/{i}.png").convert_alpha()
            e_w = img.get_width()
            e_h = img.get_height()
            img = pygame.transform.scale(img, (int(e_w * 0.2), int(e_h * 0.2)))  # تصغير الصورة
            temp_list.append(img)
        animation_list.append(temp_list)
    enemy_animations.append(animation_list)

#button images
repair_img = pygame.image.load('C:/Users/samo/OneDrive/Desktop/game.py/img/repair.png').convert_alpha()  # صورة زر الإصلاح
armour_img = pygame.image.load('C:/Users/samo/OneDrive/Desktop/game.py/img/armour.png').convert_alpha()  # صورة زر الدروع

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#function for displaying status
def show_info():
    draw_text('Money: ' + str(castle.money), font, GREY, 10, 10)
    draw_text('Score: ' + str(castle.score), font, GREY, 180, 10)
    draw_text('High Score: ' + str(high_score), font, GREY, 180, 30)
    draw_text('Level: ' + str(level), font, GREY, SCREEN_WIDTH // 2, 10)
    draw_text('Health: ' + str(castle.health) + " / " + str(castle.max_health), font, GREY, SCREEN_WIDTH - 230, SCREEN_HEIGHT - 50)
    draw_text('1000', font, GREY, SCREEN_WIDTH - 220 , 70)
    draw_text(str(TOWER_COST), font, GREY, SCREEN_WIDTH - 150, 70)
    draw_text('500', font, GREY, SCREEN_WIDTH - 70 , 70)

# كلاس القلعة
class Castle():
    def __init__(self, image100, image50, image25, x, y, scale):
        self.health = 1000  # صحة القلعة الابتدائية
        self.max_health = self.health  # أقصى صحة يمكن أن تصل إليها القلعة
        self.fired = False  # متغير لمعرفة إذا تم إطلاق النار مؤخرًا
        self.money = 0  # المال المتاح للقلعة
        self.score = 0  # النقاط التي جمعها اللاعب

        # حساب الأبعاد من الصورة الأساسية (بصحة 100%)
        width = image100.get_width()
        height = image100.get_height()

        # تغيير حجم الصور بناءً على المقياس المعطى
        self.image100 = pygame.transform.scale(image100, (int(width * scale), int(height * scale)))
        self.image50 = pygame.transform.scale(image50, (int(width * scale), int(height * scale)))
        self.image25 = pygame.transform.scale(image25, (int(width * scale), int(height * scale)))

        # إنشاء مستطيل لتحديد موقع القلعة
        self.rect = self.image100.get_rect()
        self.rect.x = x  # تحديد الموقع الأفقي للقلعة
        self.rect.y = y  # تحديد الموقع الرأسي للقلعة

    def shoot(self):
        pos = pygame.mouse.get_pos()  # الحصول على موقع المؤشر
        x_dist = pos[0] - self.rect.midleft[0]  # المسافة الأفقية بين المؤشر والقلعة
        y_dist = -(pos[1] - self.rect.midleft[1])  # المسافة الرأسية (عكس محور Y في Pygame)

        # حساب الزاوية التي يجب أن تطلق فيها الرصاصة
        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        # التحقق من الضغط على زر الفأرة الأيسر، وعدم وجود إطلاق سابق، وأن يكون المؤشر فوق الشاشة
        if pygame.mouse.get_pressed()[0] and self.fired == False and pos[1] > 70:
            self.fired = True  # وضع علامة أن إطلاق قد حدث
            bullet = Bullet(bullet_img, self.rect.midleft[0], self.rect.midleft[1], self.angle)  # إنشاء رصاصة جديدة
            bullet_group.add(bullet)  # إضافة الرصاصة إلى مجموعة الرصاصات

        # إعادة ضبط حالة الإطلاق عند تحرير زر الفأرة
        if pygame.mouse.get_pressed()[0] == False:
            self.fired = False

    def draw(self):
        # اختيار الصورة المناسبة بناءً على صحة القلعة
        if self.health <= 250:
            self.image = self.image25
        elif self.health <= 500:
            self.image = self.image50
        else:
            self.image = self.image100

        # رسم القلعة على الشاشة
        screen.blit(self.image, self.rect)

    def repair(self):
        # إصلاح القلعة إذا كان هناك ما يكفي من المال ولم تصل الصحة إلى الحد الأقصى
        if self.money >= 1000 and self.health < self.max_health:
            self.health += 500  # زيادة الصحة
            self.money -= 1000  # خصم المال

            # التأكد من ألا تتجاوز الصحة الحد الأقصى
            if castle.health > castle.max_health:
                castle.health = castle.max_health

    def armour(self):
        # زيادة الحد الأقصى للصحة إذا كان هناك ما يكفي من المال
        if self.money >= 500:
            self.max_health += 250  # زيادة الحد الأقصى للصحة
            self.money -= 500  # خصم المال

# كلاس البرج
class Tower(pygame.sprite.Sprite):
    def __init__(self, image100, image50, image25, x, y, scale):
        pygame.sprite.Sprite.__init__(self)  # تهيئة كائن Sprite

        self.got_target = False  # هل يوجد هدف محدد لهذا البرج؟
        self.angle = 0  # زاوية اتجاه البرج
        self.last_shot = pygame.time.get_ticks()  # وقت آخر طلقة

        # تحميل وتحجيم الصور الثلاثة (100%, 50%, 25%)
        width = image100.get_width()
        height = image100.get_height()
        self.image100 = pygame.transform.scale(image100, (int(width * scale), int(height * scale)))
        self.image50 = pygame.transform.scale(image50, (int(width * scale), int(height * scale)))
        self.image25 = pygame.transform.scale(image25, (int(width * scale), int(height * scale)))

        # تحديد الصورة الافتراضية
        self.image = self.image100

        # المستطيل الذي يمثل موقع البرج
        self.rect = self.image100.get_rect()
        self.rect.x = x  # تحديد الموقع الأفقي للبرج
        self.rect.y = y  # تحديد الموقع الرأسي للبرج

    def update(self, enemy_group):
        self.got_target = False  # إعادة ضبط الهدف

        # البحث عن أول عدو لا يزال حيًا ليكون الهدف
        for e in enemy_group:
            if e.alive:
                target_x, target_y = e.rect.midbottom  # موقع العدو
                self.got_target = True  # تم العثور على هدف
                break  # الخروج من الحلقة

        # إذا كان هناك هدف، نحسب الزاوية ونطلق النار
        if self.got_target:
            x_dist = target_x - self.rect.midleft[0]  # المسافة الأفقية
            y_dist = -(target_y - self.rect.midleft[1])  # المسافة الرأسية

            # حساب الزاوية بالدرجات
            self.angle = math.degrees(math.atan2(y_dist, x_dist))

            shot_cooldown = 1000  # فترة الانتظار بين الطلقات (بالميلي ثانية)

            # التحقق مما إذا مر الزمن الكافي لإطلاق النار
            if pygame.time.get_ticks() - self.last_shot > shot_cooldown:
                self.last_shot = pygame.time.get_ticks()  # تحديث وقت آخر إطلاق
                bullet = Bullet(bullet_img, self.rect.midleft[0], self.rect.midleft[1], self.angle)  # إنشاء رصاصة
                bullet_group.add(bullet)  # إضافتها إلى مجموعة الرصاصات

        # تحديث شكل البرج بناءً على صحة القلعة
        if castle.health <= 250:
            self.image = self.image25
        elif castle.health <= 500:
            self.image = self.image50
        else:
            self.image = self.image100
#bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)  # تهيئة كائن الـ Sprite

        self.image = image  # الصورة التي تم تعيينها للرصاصة
        self.rect = self.image.get_rect()  # المستطيل الذي يمثل موقع الرصاصة

        self.rect.x = x  # تحديد موقع x للرصاصة
        self.rect.y = y  # تحديد موقع y للرصاصة

        self.angle = math.radians(angle)  # تحويل الزاوية من درجات إلى راديان
        self.speed = 10  # سرعة الرصاصة

        # حساب الحركة الأفقية (dx) والرأسية (dy) بناءً على الزاوية
        self.dx = math.cos(self.angle) * self.speed  # الحركة الأفقية
        self.dy = -(math.sin(self.angle) * self.speed)  # الحركة الرأسية (سالبة لأن المحور Y معاكس)

    def update(self):  # تحديث موقع الرصاصة كل إطار
        # التحقق إذا خرجت الرصاصة خارج الشاشة
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()  # إزالة الرصاصة من المجموعة إذا خرجت

        # تحديث الموقع بناءً على dx و dy
        self.rect.x += self.dx
        self.rect.y += self.dy


class Crosshair():
    def __init__(self, scale):  # دالة الإنشاء
        # تحميل صورة العلامة (الهدف)
        image = pygame.image.load('C:/Users/samo/OneDrive/Desktop/game.py/img/crosshair.png').convert_alpha()

        # الحصول على عرض وارتفاع الصورة
        width = image.get_width()
        height = image.get_height()

        # تغيير حجم الصورة بناءً على المقياس المعطى
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))

        # المستطيل الذي يمثل موقع العلامة
        self.rect = self.image.get_rect()

        # إخفاء مؤشر الفأرة الافتراضي
        pygame.mouse.set_visible(False)

    def draw(self):  # دالة لرسم العلامة
        mx, my = pygame.mouse.get_pos()  # الحصول على موقع المؤشر
        self.rect.center = (mx, my)  # وضع مركز العلامة في مكان المؤشر
        screen.blit(self.image, self.rect)  # رسم العلامة على الشاشة


# إنشاء القلعة
castle = Castle(castle_img_100, castle_img_50, castle_img_25, SCREEN_WIDTH - 250, SCREEN_HEIGHT - 300, 0.2)

# إنشاء العلامة (Crosshair)
crosshair = Crosshair(0.025)

# إنشاء الأزرار
repair_button = button.Button(SCREEN_WIDTH - 220, 10, repair_img, 0.5)  # زر الإصلاح
tower_button = button.Button(SCREEN_WIDTH - 140, 10, tower_img_100, 0.1)  # زر بناء البرج
armour_button = button.Button(SCREEN_WIDTH - 75, 10, armour_img, 1.5)  # زر الدروع

# إنشاء مجموعات لعناصر اللعبة
tower_group = pygame.sprite.Group()  # مجموعة الأبراج
bullet_group = pygame.sprite.Group()  # مجموعة الرصاصات
enemy_group = pygame.sprite.Group()  # مجموعة الأعداء


# حلقة اللعبة الرئيسية
run = True  # متغير للتحكم في استمرارية الحلقة
while run:  # بداية الحلقة
    clock.tick(FPS)  # ضبط عدد الإطارات في الثانية

    if game_over == False:  # إذا كانت اللعبة لا تزال جارية
        screen.blit(bg, (0, 0))  # رسم الخلفية

        castle.draw()  # رسم القلعة
        castle.shoot()  # إطلاق النار من القلعة

        tower_group.draw(screen)  # رسم الأبراج
        tower_group.update(enemy_group)  # تحديث حالة الأبراج

        crosshair.draw()  # رسم العلامة (الهدف)

        bullet_group.update()  # تحديث الرصاصات
        bullet_group.draw(screen)  # رسم الرصاصات

        enemy_group.update(screen, castle, bullet_group)  # تحديث الأعداء

        show_info()  # عرض المعلومات (النقاط، المال، الصحة...)

        # رسم الأزرار والتعامل مع الضغط عليها
        if repair_button.draw(screen):  # إذا تم الضغط على زر الإصلاح
            jump_fx.play()
            castle.repair()  # إصلاح القلعة

        if tower_button.draw(screen):  # إذا تم الضغط على زر بناء برج
            jump_fx.play()
            if castle.money >= TOWER_COST and len(tower_group) < max_towers:  # التحقق من المال والموقع
                tower = Tower(
                    tower_img_100,
                    tower_img_50,
                    tower_img_25,
                    tower_positions[len(tower_group)][0],  # تحديد موقع البرج الجديد
                    tower_positions[len(tower_group)][1],
                    0.2
                )
                tower_group.add(tower)  # إضافة البرج للمجموعة
                castle.money -= TOWER_COST  # خصم تكلفة البرج

        if armour_button.draw(screen):  # إذا تم الضغط على زر الدروع
            jump_fx.play()
            castle.armour()  # زيادة صحة القلعة

        # إنشاء الأعداء
        if level_difficulty < target_difficulty:  # إذا لم يتم الوصول إلى الصعوبة المستهدفة
            if pygame.time.get_ticks() - last_enemy > ENEMY_TIMER:  # التحقق من مرور الوقت المطلوب
                e = random.randint(0, len(enemy_types) -1)  # اختيار نوع عدو عشوائي
                enemy = Enemy(enemy_health[e], enemy_animations[e], -100, SCREEN_HEIGHT - 100, 1)  # إنشاء العدو
                enemy_group.add(enemy)  # إضافته للمجموعة
                last_enemy = pygame.time.get_ticks()  # تحديث وقت آخر ظهور لعدو
                level_difficulty += enemy_health[e]  # زيادة الصعوبة

        enemies_alive = 0  # عدد الأعداء الذين لا يزالون أحياء
        for e in enemy_group:  # التحقق من حالة كل عدو
            if e.alive == True:
                enemies_alive += 1  # زيادة العدد إذا كان العدو حيًا

        if enemies_alive == 0 and next_level == False and level_difficulty >= target_difficulty:  # إذا تم قتل جميع الأعداء
            next_level = True  # الاستعداد للانتقال للمستوى التالي
            level_reset_time = pygame.time.get_ticks()  # تسجيل وقت انتهاء المستوى الحالي

        if next_level == True:  # إذا كان يجب الانتقال للمستوى التالي
            draw_text('LEVEL COMPLETE!', font_60, WHITE, 200, 300)  # عرض رسالة المستوى اكتمل

            if castle.score > high_score:  # التحقق إذا كانت النقاط أعلى من الـ high score
                high_score = castle.score  # تحديث high score
                with open('score.txt', 'w') as file:  # حفظ القيمة في ملف
                    file.write(str(high_score))

            if pygame.time.get_ticks() - level_reset_time > 1500:  # بعد 1.5 ثانية
                next_level = False  # إعادة المتغيرات
                level += 1  # زيادة المستوى
                last_enemy = pygame.time.get_ticks()  # إعادة ضبط توقيت العدو
                target_difficulty *= DIFFICULTY_MULTIPLIER  # زيادة الصعوبة
                level_difficulty = 1  # إعادة الصعوبة إلى الصفر
                enemy_group.empty()  # إزالة الأعداء من المجموعة

        if castle.health <= 0:  # إذا فقدت القلعة كل صحتها
            grenade_fx.play()
            game_over = True  # إنهاء اللعبة

    else:  # إذا انتهت اللعبة
        draw_text('GAME OVER!', font, GREY, 300, 300)  # عرض رسالة "انتهت اللعبة"
        draw_text('PRESS "A" TO PLAY AGAIN!', font, GREY, 250, 360)  # تعليمات لإعادة اللعبة

        pygame.mouse.set_visible(True)  # إظهار مؤشر الفأرة

        key = pygame.key.get_pressed()  # التحقق إذا تم الضغط على مفتاح
        if key[pygame.K_a]:  # إذا تم الضغط على "A"
            # إعادة ضبط المتغيرات
            game_over = False
            level = 1
            target_difficulty = 1000
            level_difficulty = 0
            last_enemy = pygame.time.get_ticks()
            enemy_group.empty()
            tower_group.empty()
            castle.score = 0
            castle.health = 1000
            castle.max_health = castle.health
            castle.money = 0
            pygame.mouse.set_visible(False)  # إخفاء المؤشر مجددًا

    # معالجة الأحداث مثل الضغط على زر الخروج
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # إذا تم الضغط على زر الإغلاق
            run = False  # إنهاء الحلقة

    # تحديث شاشة العرض
    pygame.display.update()

# إنهاء Pygame
pygame.quit()







#1. نظام الرسوم المتحركة (Animation System)	استخدام animation_list + frame_index لتشغيل تسلسل صور العدو (2/5)
#2. تأخير الهجوم (Cooldown System) انتظار 1000ms بين كل ضربة عدو باستخدام pygame.time.get_ticks() (2/5)
#3. تصادم بالفأرة للأزرار (Mouse Collision)	استخدام get_rect() و collidepoint() للتفاعل مع الأزرار (2/5)
#4. إدارة الأعداء عشوائياً (Random Spawning)	توليد أعداء بأنواع مختلفة باستخدام random.choice() (1/5)
#5. تحكم في مستوى اللعبة (Level Difficulty)	تغيير عدد الأعداء حسب المستوى باستخدام عدّاد level_difficulty (2/5)
#6. إدارة الصوت باستخدام mixer	تحميل وتشغيل مؤثرات صوتية وموسيقى بالخلفية (1/5)
#7. خوارزمية تتبع ذكي (ذُكرناها يدويًا)	حساب المسافة بين اللاعب والعدو لتحديد إذا كان العدو يهجم (3/5)
#Алгоритм (AI: Расстояние до игрока)
