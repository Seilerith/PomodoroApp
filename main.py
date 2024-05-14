from kivy.core.window import Window
from kivy.utils import platform
from kivy.lang import Builder
from kivy.clock import Clock

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout

from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.button import MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel


if platform != "android": 
    Window.size = (300, 600)

KV = '''
BoxLayout:
    orientation: 'vertical'
    MDBottomNavigation:
        id: bottom_nav
        selected_color_background: 0, 0, 0, 0
        MDBottomNavigationItem:
            name: 'screen 1'
            text: 'Pomodoro'
            icon: 'timer'
            FloatLayout:
                Image:
                    #source: 'Images/tomato.png'
                    size_hint: None, None
                    size: self.texture_size  # Görsel boyutunu orijinal boyutuyla eşle
                    pos_hint: {'center_x': 0.5, 'center_y': 0.65}  # Ekranın ortasına yerleştirme
                BoxLayout:
                    orientation: 'vertical'
                    spacing: '10dp'
                    padding: '10dp'
                    Widget:  # Ekranın en alt kısmını ayırmak için boş bir widget
                        size_hint_y: None
                        height: dp(0)
                    MDLabel:
                        id: timer_label
                        text: '00:00'
                        pos_hint: {'center_x': 0.5, 'center_y': 0.1}
                        font_size: '35sp'
                        color: 'black'
                        halign: 'center'
                    MDProgressBar:
                        id: progress_bar
                        value: 0
                        size_hint: 1, 0.2
                        color: 255/255, 0/255, 0/255, 1
                        radius: [10, 10]
                        max: 1500  # Pomodoro süresi saniye cinsinden (25 dakika = 1500 saniye)
                    Widget:  # Ekranın en alt kısmını ayırmak için boş bir widget
                        size_hint_y: None
                        height: dp(0)
                    MDLabel:
                        id: note_label
                        text: 'Pomodoro, uzun süre çalışmanızı sağlayan tekniktir.'
                        pos_hint: {'center_x': 0.5, 'center_y': 0.65}
                        font_size: '16sp'
                        md_bg_color: 96/255, 125/255, 139/255, .3
                        size_hint: 1,.3
                        color: 'black'
                        halign: 'center'
                    Widget:  # Ekranın en alt kısmını ayırmak için boş bir widget
                        size_hint_y: None
                        height: dp(50)
                    MDGridLayout:
                        cols: 3
                        padding: [dp(0), dp(0), dp(0), dp(0)]
                        spacing: [dp(2), dp(0)]
                        size_hint_y: None
                        height: self.minimum_height
                        MDIconButton:
                            id: pause_buton
                            size_hint_x: .1
                            icon: "pause"
                            md_bg_color: 245/255, 247/255, 252/255, 1
                            radius: [20]
                            on_release: app.stop_timer()                       
                        MDIconButton:
                            id: pomodoro_buton
                            size_hint_x: .2
                            icon: "play"
                            md_bg_color: 255/255, 50/255, 50/255, 1
                            radius: [20]
                            #on_release: app.start_timer()
                        MDIconButton:
                            id: reset_buton
                            size_hint_x: .1
                            icon: "undo-variant"
                            md_bg_color: 245/255, 247/255, 252/255, 1
                            radius: [20]
                            on_release: app.reset_timer()

                    Widget:  # Ekranın en alt kısmını ayırmak için boş bir widget
                        size_hint_y: None
                        height: dp(10)
        MDBottomNavigationItem:
            name: 'screen 2'
            text: 'To Do'
            icon: 'clipboard-check'
            ScrollView:
                MDList:
                    id: todo_list
                    BoxLayout:
                        size_hint_y: None
                        height: dp(56)
                        padding: dp(8)
                        spacing: dp(8)
                        MDTextField:
                            id: todo_item
                            hint_text: "Görevinizi girin"
                            helper_text_mode: "on_focus"
                            size_hint_x: 0.8
                        MDFillRoundFlatIconButton:
                            text: "Ekle"
                            size_hint_x: 0.2
                            icon: "plus"
                            on_release: app.add_todo_item()

        MDBottomNavigationItem:
            name: 'screen 3'
            text: 'Note'
            icon: 'note'
            ScrollView:
                MDList:
                    id: note_list
                    padding: "10dp", "10dp", "10dp", "100dp"
            BoxLayout:
                orientation: 'vertical'
                spacing: '10dp'
                padding: '10dp'
                MDTextField:
                    id: note_input
                    hint_text: "Notunuzu buraya giriniz"
                    mode: "fill"
                    multiline: True
                    height: "48dp"
                MDFillRoundFlatButton:
                    spacing: '10dp'
                    text: "Ekle"
                    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                    icon: "plus"
                    size_hint_x: 1
                    halign:'center'
                    on_release: app.add_note()

'''

class PomodoroApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_string(KV)
    
    def on_start(self):
        self.todo_list = self.root.ids.todo_list  
        self.timer = 0
        self.PauseKontrol = True
        self.BreakPauseKontrol = True
        self.total_seconds = 0
        self.root.ids.pomodoro_buton.on_release = self.start_timer

    def add_todo_item(self):
        todo_text = self.root.ids.todo_item.text.strip()
        if todo_text:
            todo_container = BoxLayout(size_hint_y=None, height=dp(56), padding=dp(8), spacing=dp(8))
            delete_button = MDIconButton(icon="delete", on_release=self.delete_todo_item)
            todo_item = OneLineListItem(text=todo_text)
            todo_container.add_widget(todo_item)
            todo_container.add_widget(delete_button)

            self.todo_list.add_widget(todo_container)
            self.root.ids.todo_item.text = ""  

    def delete_todo_item(self, instance):
        item_to_remove = instance.parent 
        self.todo_list.remove_widget(item_to_remove)  

    def start_timer(self):
        self.root.ids.pomodoro_buton.disabled = True

        if self.PauseKontrol == True:
            self.pause_timer()

        if not self.timer:
            self.timer = Clock.schedule_interval(self.update_timer, 1)
            self.root.ids.note_label.text = "Pomodoro Başladı."

    def pause_timer(self):
        self.root.ids.pause_buton.on_release = self.stop_timer
        self.root.ids.reset_buton.on_release = self.reset_timer

        self.root.ids.pause_buton.disabled=False
        self.root.ids.reset_buton.disabled=False

        self.root.ids.timer_label.text = '00:00'
        self.root.ids.note_label.text = "Pomodoro Başlıyor."

        self.root.ids.progress_bar.max = 1500
        self.root.ids.progress_bar.color = 255/255, 0/255, 0/255, 1
        self.root.ids.progress_bar.value = 0
        
    def stop_timer(self):
        self.root.ids.pomodoro_buton.disabled = False
        self.PauseKontrol = False
        if self.timer:
            self.timer.cancel()
            self.timer = None

    def reset_timer(self):
        self.stop_timer()
        self.root.ids.timer_label.text = '00:00'
        self.root.ids.note_label.text = "Tekrar Başlıyor."
        self.root.ids.progress_bar.value = 0  

    def update_timer(self, interval):
        timer_label = self.root.ids.timer_label
        timer_text = timer_label.text
        note_label = self.root.ids.note_label
        note_text = note_label.text

        minutes, seconds = map(int, timer_text.split(':'))
        total_seconds = minutes * 60 + seconds
        total_seconds += 1

        if total_seconds <= 1500:  
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            timer_label.text = f"{minutes:02}:{seconds:02}"
            self.root.ids.progress_bar.value = total_seconds  
            if  total_seconds == 1500:
                note_label.text = "Pomodoro Tamamlandı."

                self.root.ids.pomodoro_buton.md_bg_color=50/255,255/255,50/255
                self.root.ids.pause_buton.disabled=True
                self.root.ids.reset_buton.disabled=True

                self.root.ids.reset_buton.on_release = self.break_reset_timer
                self.root.ids.pause_buton.on_release = self.break_stop_timer
                self.root.ids.pomodoro_buton.on_release = self.break_start_timer

                self.BreakPauseKontrol = True
                
        else:
            self.stop_timer()

    def break_start_timer(self):
        self.root.ids.pomodoro_buton.disabled = True
        if self.BreakPauseKontrol == True:
            self.break_pause_timer()
        if not self.timer:
            self.timer = Clock.schedule_interval(self.break_timer, 1)
            self.root.ids.note_label.text = "Mola Başladı."

    def break_stop_timer(self):
        self.root.ids.pomodoro_buton.disabled = False
        self.BreakPauseKontrol = False
        if self.timer:
            self.timer.cancel()
            self.timer = None
        

    def break_pause_timer(self):
        self.root.ids.pause_buton.on_release = self.break_stop_timer
        self.root.ids.reset_buton.on_release = self.break_reset_timer

        self.root.ids.pause_buton.disabled=False
        self.root.ids.reset_buton.disabled=False

        self.root.ids.timer_label.text = '00:00'
        self.root.ids.note_label.text = "Mola başlıyor."

        self.root.ids.progress_bar.max = 300
        self.root.ids.progress_bar.color = 50/255, 255/255, 50/255, 1
        self.root.ids.progress_bar.value = 0

    def break_reset_timer(self):
        self.break_stop_timer()
        self.root.ids.timer_label.text = '00:00'
        self.root.ids.note_label.text = "Tekrar Başlıyor."
        self.root.ids.progress_bar.value = 0
    
    def break_timer(self,interval):
        timer_label = self.root.ids.timer_label
        timer_text = timer_label.text
        note_label = self.root.ids.note_label
        note_text = note_label.text

        minutes, seconds = map(int, timer_text.split(':'))
        total_seconds = minutes * 60 + seconds
        total_seconds += 1

        if total_seconds <= 300:
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            timer_label.text = f"{minutes:02}:{seconds:02}"
            self.root.ids.progress_bar.value = total_seconds
            if  total_seconds == 300:
                note_label.text = "Mola Tamamlandı."

                self.root.ids.pomodoro_buton.md_bg_color=255/255,50/255,50/255
                self.root.ids.pause_buton.disabled=True
                self.root.ids.reset_buton.disabled=True

                self.root.ids.reset_buton.on_release = self.reset_timer
                self.root.ids.pause_buton.on_release = self.stop_timer
                self.root.ids.pomodoro_buton.on_release = self.start_timer

                self.PauseKontrol = True

        else:
            self.break_stop_timer()

    def add_note(self):
        note_text = self.root.ids.note_input.text.strip()
        if note_text:
            note = MDTextField(text=note_text, multiline=True, disabled=True, pos_hint={"center_y": 5})
            self.root.ids.note_list.add_widget(note)
            self.root.ids.note_input.text = ""  
            self.root.ids.note_input.text = ""  

if __name__ == '__main__':
    PomodoroApp().run()
#By ABDULAZİZ_HOCAOĞLU
