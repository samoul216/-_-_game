import pygame  # استيراد مكتبة Pygame للتعامل مع الرسومات والتعامل مع الأحداث (مثل الفأرة والزر)

#class زر التحكم
class Button():
    def __init__(self, x, y, image, scale):  # دالة البدء لتحديد خصائص الزر
        width = image.get_width()  # الحصول على عرض الصورة الأصلية
        height = image.get_height()  # الحصول على ارتفاع الصورة الأصلية

        # تغيير حجم الصورة بناءً على المقياس المعطى
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))

        # إنشاء مستطيل يحيط بالصورة لتحديد موقعها وتصادمها
        self.rect = self.image.get_rect()

        # تحديد موقع الزاوية العلوية اليسرى للزر
        self.rect.topleft = (x, y)

        # متغير لتتبع ما إذا تم النقر على الزر أم لا
        self.clicked = False

    def draw(self, surface):  # دالة لرسم الزر على الشاشة
        action = False  # متغير لتحديد إذا كان الزر قد تم الضغط عليه (سيُعاد عند الدالة)

        # الحصول على موقع المؤشر (الفأرة)
        pos = pygame.mouse.get_pos()

        # التحقق إذا كان المؤشر فوق الزر (collidepoint)
        if self.rect.collidepoint(pos):
            # التحقق من الضغط على الزر الأيسر للمؤشر (index 0) ولم يتم النقر سابقًا
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True  # وضع علامة أن الزر قد تم النقر عليه
                action = True  # تم تنفيذ فعل (نقر الزر)

        # التحقق إذا تم تحرير الزر الأيسر
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False  # إعادة المتغير إلى الوضع غير المنقر

        # رسم صورة الزر على الشاشة في الموقع المحدد
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action  # إرجاع ما إذا كان الزر قد تم الضغط عليه (True) أو لا (False)