#Установка параметров экрана
from kivy.config import Config
Config.set("graphics", "resizable", 1)
Config.set("graphics", "width", "360")
Config.set("graphics", "height", "640")

#Импортирование модулей
from kivy.lang.builder import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty
from kivymd.uix.dialog import MDDialog


class kipia_cals(MDScreen):
#Обьекты из окна Шкала сигнал
    fiz_min = ObjectProperty(None)
    fiz_max = ObjectProperty(None)
    out_min = ObjectProperty(None)
    out_max = ObjectProperty(None)
    fiz_value = ObjectProperty(None)
    out_value = ObjectProperty(None)
    otv = ObjectProperty(None)

#Обьеты из экрана контрольных точек
    d_max = ObjectProperty(None)
    d_min = ObjectProperty(None)
    first_point = ObjectProperty(None)
    last_point = ObjectProperty(None)
    pnt_value = ObjectProperty(None)
    btn_pnt = ObjectProperty(None)
    
#Обьекты из экрана с переводом давлений
    pa = ObjectProperty(None)
    kpa = ObjectProperty(None)
    mpa = ObjectProperty(None)
    kg = ObjectProperty(None)
    bar = ObjectProperty(None)
    psi = ObjectProperty(None)
    atm = ObjectProperty(None)
    mm_Hg = ObjectProperty(None)
    mm_H_2_O = ObjectProperty(None)

  
#Функция расчета выходного сигнала
    def fiz_in_inpt(self):
        #Исходное состояние полей ввода
        self.fiz_value.icon_left = ""
        self.fiz_value.helper_text = ""
        self.fiz_value.error = False
        
        #Фоормула расчета выходного сигнала
        self.out_value.text  = str(round(((float(self.fiz_value.text)-float(self.fiz_min.text))/(float(self.fiz_max.text) - float(self.fiz_min.text)))*(float(self.out_max.text) 
                                        - float(self.out_min.text))+float(self.out_min.text), 2))
        
        #Изменение цвета и появление иконки у текстового поля если расчеты выходят за пределы указанные в диапазонах
        if (float(self.out_value.text) > float(self.out_max.text)) or (float(self.out_value.text) < float(self.out_min.text)):
            self.out_value.icon_left = "alert-circle"
            self.out_value.helper_text = "Выход за диапазон"
            self.out_value.error = True
        else:
            self.out_value.icon_left = ""
            self.out_value.helper_text = ""
            self.out_value.error = False
    
#Функция расчета входной величины в зависимости от выходной
    def inpt_in_fiz(self):

        #Исходное состояние полей ввода
        self.out_value.icon_left = ""
        self.out_value.helper_text = ""
        self.out_value.error = False

        #Фоормула расчета входной величины
        self.fiz_value.text  = str(round(((float(self.out_value.text)-float(self.out_min.text))/(float(self.out_max.text) - float(self.out_min.text)))*(float(self.fiz_max.text) 
                                        - float(self.fiz_min.text))+float(self.fiz_min.text), 2))
                                        
         #Изменение цвета и появление иконки у текстового поля если расчеты выходят за пределы указанные в диапазонах         
        if (float(self.fiz_value.text) > float(self.fiz_max.text)) or (float(self.fiz_value.text) < float(self.fiz_min.text)):
            self.fiz_value.icon_left = "alert-circle"
            self.fiz_value.helper_text = "Выход за диапазон"
            self.fiz_value.error = True
        else:
            self.fiz_value.icon_left = ""
            self.fiz_value.helper_text = ""
            self.fiz_value.error = False
    
#Расчет контрольных точек   
    def pnt(self):
        dialog = None
        #Расчет шага диапазона
        pnt_prc = 100/(float(self.pnt_value.text)-1)
        
        #Список с процентами диапазона
        lst_prc = []
        #Список с фактическими значениями
        lst_pnt = []

        #Добавление значения первой точки в %
        lst_prc.append(float(self.first_point.text))
        
        #Сумма процентов
        prc = pnt_prc
        
        #Цикл заполнения списка значениями процентов диапазона
        for _ in range(1,int(self.pnt_value.text)-1,1):
            lst_prc.append(round(prc,1))
            prc+=pnt_prc
        
        #Добавление последней точки
        lst_prc.append(float(self.last_point.text))

        #Цикл расчета контрольных точек
        for i in lst_prc:
            t = round(float(self.d_min.text)+(float(self.d_max.text)-float(self.d_min.text))*(i/100),1)
            lst_pnt.append(t)
        txt = ""
        for i in range(1, len(lst_pnt)+1,1):
            txt += f"{str(i)}. {str(lst_prc[i-1])}% - {str(lst_pnt[i-1])}\n"

        if not dialog:
            dialog = MDDialog (
            title='Контрольные точки:',
            text = txt,
            type='custom',
            )
        dialog.open()

#Функция перевода давлений
    def pressure(self, *press):
        #Коэфиценты для перевода Па во все давления
        kef=[1, 0.001, 0.000001, 0.00001, 0.00001, 0.00014504, 0.00000987, 0.00750064, 0.101971]
        
        #Получение введенного давления и коэфицента для перевода в Па 
        var_kpa = float(press[0])*float(press[1])

        lst_pressure = []
        
        #Заполнения списка расчетными значениями давления
        for i in kef:
            lst_pressure.append(round(var_kpa*i, 4))

        #Передача значений давления в текстовые поля
        self.pa.text = str(lst_pressure[0])
        self.kpa.text = str(lst_pressure[1])
        self.mpa.text = str(lst_pressure[2])
        self.kg.text = str(lst_pressure[3])
        self.bar.text = str(lst_pressure[4])
        self.psi.text = str(lst_pressure[5])
        self.atm.text = str(lst_pressure[6])
        self.mm_Hg.text = str(lst_pressure[7])
        self.mm_H_2_O.text = str(lst_pressure[8])
     
        
class kipia(MDApp):
    def build(self):
        Kipia_cals = kipia_cals()
        return Kipia_cals

kipia().run() 