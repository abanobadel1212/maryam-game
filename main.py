from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from plyer import tts
import random

def speak_now(text):
    try:
        tts.speak(text)
    except:
        pass

def stop_speech():
    try:
        tts.stop()
    except:
        pass

class MaryamQuizApp(App):
    def build(self):
        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        self.current_section = ""
        self.current_player = ""
        self.question_index = 0
        self.score = 0
        self.questions_list = []
        
        # متغيرات قسم التحدي (VS)
        self.vs_question_index = 0
        self.vs_scores = {"Kevin": 0, "Irene": 0}
        self.vs_questions_list = []
        self.vs_turn = "Kevin"
        
        # متغيرات قسم الفوازير
        self.riddle_index = 0
        self.riddle_score = 0
        self.riddles_list = []
        
        self.show_main_menu()
        return self.main_layout

    def clear_screen(self):
        stop_speech() # إسكات أي صوت قديم عند تغيير الشاشة
        self.main_layout.clear_widgets()

    def show_main_menu(self):
        self.clear_screen()
        
        lbl = Label(text="Maryam 3M App - Main Menu", font_size='20sp', halign='center')
        self.main_layout.add_widget(lbl)
        
        sections = [
            ("1. Sports & Math Section", "Sports"),
            ("2. Religion Section", "Religion"),
            ("3. VS Competition (Kevin vs Irene)", "VS"),
            ("4. Riddles & Games", "Games")
        ]
        
        for text_btn, sec_type in sections:
            btn = Button(text=text_btn, size_hint=(1, 0.15), background_color=(0.2, 0.4, 0.7, 1))
            btn.bind(on_press=lambda x, s=sec_type: self.handle_section_click(s))
            self.main_layout.add_widget(btn)
            
        speak_now("أهلاً بكم في تطبيق مريم ثري أم. اختر القسم يا بطل")

    def handle_section_click(self, sec_type):
        if sec_type in ["Sports", "Religion"]:
            self.choose_player_for_section(sec_type)
        elif sec_type == "VS":
            self.start_vs_competition()
        elif sec_type == "Games":
            self.start_easy_games()

    def choose_player_for_section(self, sec_name):
        self.clear_screen()
        self.current_section = sec_name
        
        lbl = Label(text=f"Who is playing in {sec_name}?\nChoose Player:", font_size='22sp', halign='center')
        self.main_layout.add_widget(lbl)
        
        speak_now("مين اللي هيبدأ اللعبة، كيفين ولا إيريني؟")
        
        for player in ["Kevin", "Irene"]:
            btn = Button(text=player, size_hint=(1, 0.25), background_color=(0.3, 0.6, 0.3, 1))
            btn.bind(on_press=lambda x, p=player: self.init_game_session(p))
            self.main_layout.add_widget(btn)

    def generate_dynamic_questions(self, section):
        questions = []
        for i in range(1, 31):
            if section == "Sports":
                if i <= 10:
                    num1 = random.randint(1, 10)
                    num2 = random.randint(1, 5)
                    ans = num1 + num2
                    q_text = f"Question ({i}): {num1} + {num2}?"
                    voice_text = f"السؤال رقم {i}: كم ناتج {num1} زائد {num2}"
                elif i <= 20:
                    num1 = random.randint(10, 30)
                    num2 = random.randint(5, 15)
                    ans = num1 + num2
                    q_text = f"Question ({i}): {num1} + {num2}?"
                    voice_text = f"السؤال رقم {i}: كم ناتج {num1} زائد {num2}"
                else:
                    num1 = random.randint(20, 50)
                    num2 = random.randint(10, 25)
                    ans = abs(num1 - num2)
                    q_text = f"Question ({i}): {num1} - {num2}?"
                    voice_text = f"السؤال رقم {i}: كم ناتج طرح {num1} ناقص {num2}"
            else:
                religion_pool_easy = [
                    {"q": "كم عدد أصابع اليد الواحدة؟", "ans": "5", "voice": "كم عدد أصابع اليد الواحدة؟", "opts": ["5", "10", "4"]},
                    {"q": "من هو أول شخص تم خلقه؟", "ans": "آدم", "voice": "من هو أبو البشر أول شخص تم خلقه؟", "opts": ["آدم", "نوح", "داود"]},
                    {"q": "في أي مدينة وُلد السيد المسيح؟", "ans": "بيت لحم", "voice": "في أي مدينة وُلد السيد المسيح؟", "opts": ["بيت لحم", "القدس", "الناصرة"]}
                ]
                religion_pool_med = [
                    {"q": "كم عدد أيام الخلق في الخليقة؟", "ans": "6", "voice": "كم عدد أيام الخلق؟", "opts": ["6", "7", "5"]},
                    {"q": "من هو البطل الذي بني الفلك العظيم؟", "ans": "نوح", "voice": "من هو النبي الذي بني الفلك؟", "opts": ["نوح", "موسى", "إبراهيم"]}
                ]
                religion_pool_hard = [
                    {"q": "ما هو اسم الجبل الذي تسلمه عليه الوصايا؟", "ans": "سيناء", "voice": "ما هو اسم جبل سيناء الذي تسلمت عليه الوصايا؟", "opts": ["سيناء", "الزيتون", "المقطم"]},
                    {"q": "من هو النبي الذي صعد للسماء في مركبة نار؟", "ans": "إيليا", "voice": "من هو النبي الذي صعد إلى السماء حياً؟", "opts": ["إيليا", "أخنوخ", "موسى"]}
                ]
                
                if i <= 10:
                    r_item = random.choice(religion_pool_easy)
                elif i <= 20:
                    r_item = random.choice(religion_pool_med)
                else:
                    r_item = random.choice(religion_pool_hard)
                
                ans = r_item["ans"]
                q_text = f"Question ({i}): {r_item['q']}"
                voice_text = f"السؤال رقم {i}: {r_item['voice']}"
                options = r_item["opts"][:]
                random.shuffle(options)
                
                questions.append({
                    "question": q_text,
                    "voice": voice_text,
                    "options": options,
                    "answer": str(ans)
                })
                continue
            
            correct_ans = str(ans)
            options = [correct_ans, str(ans + 2), str(abs(ans - 3) if ans >= 3 else ans + 4)]
            random.shuffle(options)
            
            questions.append({
                "question": q_text,
                "voice": voice_text,
                "options": options,
                "answer": correct_ans
            })
        return questions

    def init_game_session(self, player):
        self.current_player = player
        self.question_index = 0
        self.score = 0
        self.questions_list = self.generate_dynamic_questions(self.current_section)
        self.show_question()

    def show_question(self):
        self.clear_screen()
        
        if self.question_index >= len(self.questions_list):
            self.show_final_score()
            return

        q_data = self.questions_list[self.question_index]
        
        q_display = (f"Player: {self.current_player}\n"
                     f"Question ({self.question_index + 1} / {len(self.questions_list)})\n\n"
                     f"Listen to the voice question!")
        
        lbl = Label(text=q_display, font_size='18sp', halign='center')
        self.main_layout.add_widget(lbl)
        
        options_voice = f"الاختيارات هي: {q_data['options'][0]}، أو {q_data['options'][1]}، أو {q_data['options'][2]}"
        speak_now(f"{q_data['voice']}. {options_voice}")

        for ans in q_data["options"]:
            btn = Button(text=ans, size_hint=(1, 0.15), background_color=(0.25, 0.5, 0.7, 1))
            btn.bind(on_press=lambda instance, a=ans: self.check_answer(a))
            self.main_layout.add_widget(btn)

    def check_answer(self, selected_ans):
        stop_speech() # قطع الصوت القديم فور الضغط على الإجابة
        q_data = self.questions_list[self.question_index]
        ar_player = "كيفين" if self.current_player == "Kevin" else "إيريني"
        
        self.clear_screen()
        
        if selected_ans == q_data["answer"]:
            self.score += 1
            msg = f"Awesome {ar_player}! Correct!"
            voice_msg = f"عاش يا {ar_player}، إجابة صحيحة!"
        else:
            msg = f"Not quite, {ar_player}!"
            voice_msg = f"معليش يا {ar_player} الإجابة خطأ"
            
        lbl = Label(text=msg, font_size='22sp', halign='center')
        self.main_layout.add_widget(lbl)
        speak_now(voice_msg)
        
        btn_next = Button(text="Next Question", size_hint=(1, 0.3), background_color=(0.3, 0.6, 0.3, 1))
        self.question_index += 1
        btn_next.bind(on_press=lambda x: self.show_question())
        self.main_layout.add_widget(btn_next)

    def show_final_score(self):
        ar_player = "كيفين" if self.current_player == "Kevin" else "إيريني"
        msg = (f"Game Over, {ar_player}!\n"
               f"Your Score: {self.score} / {len(self.questions_list)}\n"
               f"Mama Mary & Papa Abanoub are super proud!")
        voice_msg = f"انتهت اللعبة يا {ar_player}! مجموع درجاتك هو {self.score} من {len(self.questions_list)}. ماما مريم وبابا أبانوب فخورين بيك!"
        
        lbl = Label(text=msg, font_size='18sp', halign='center')
        self.main_layout.add_widget(lbl)
        speak_now(voice_msg)
        
        btn_back = Button(text="Back to Menu", size_hint=(1, 0.3), background_color=(0.7, 0.3, 0.3, 1))
        btn_back.bind(on_press=lambda x: self.show_main_menu())
        self.main_layout.add_widget(btn_back)

    # ==================== قسم التحدي VS ====================
    def start_vs_competition(self):
        self.vs_question_index = 0
        self.vs_scores = {"Kevin": 0, "Irene": 0}
        self.vs_turn = "Kevin"
        self.vs_questions_list = self.generate_dynamic_questions("Sports")
        self.show_vs_question()

    def show_vs_question(self):
        self.clear_screen()
        
        if self.vs_question_index >= len(self.vs_questions_list):
            self.show_vs_final_score()
            return

        q_data = self.vs_questions_list[self.vs_question_index]
        ar_turn = "كيفين" if self.vs_turn == "Kevin" else "إيريني"
        
        q_display = (f"VS COMPETITION\n"
                     f"Turn: {self.vs_turn} | Q ({self.vs_question_index + 1} / {len(self.vs_questions_list)})\n\n"
                     f"Listen to the battle question!")
        
        lbl = Label(text=q_display, font_size='17sp', halign='center')
        self.main_layout.add_widget(lbl)
        
        options_voice = f"الاختيارات هي: {q_data['options'][0]}، أو {q_data['options'][1]}، أو {q_data['options'][2]}"
        speak_now(f"دور البطل {ar_turn}. {q_data['voice']}. {options_voice}")

        for ans in q_data["options"]:
            btn = Button(text=ans, size_hint=(1, 0.15), background_color=(0.2, 0.5, 0.5, 1))
            btn.bind(on_press=lambda instance, a=ans: self.check_vs_answer(a))
            self.main_layout.add_widget(btn)

    def check_vs_answer(self, selected_ans):
        stop_speech() # قطع الصوت القديم فور الإجابة في التحدي
        q_data = self.vs_questions_list[self.vs_question_index]
        ar_turn = "كيفين" if self.vs_turn == "Kevin" else "إيريني"
        
        self.clear_screen()
        
        if selected_ans == q_data["answer"]:
            self.vs_scores[self.vs_turn] += 1
            msg = f"Great hit, {ar_turn}!"
            voice_msg = f"إجابة صحيحة يا {ar_turn}!"
        else:
            msg = f"Missed, {ar_turn}!"
            voice_msg = f"للأسف يا {ar_turn} لم تكن صحيحة"
            
        lbl = Label(text=msg, font_size='22sp', halign='center')
        self.main_layout.add_widget(lbl)
        speak_now(voice_msg)
        
        self.vs_turn = "Irene" if self.vs_turn == "Kevin" else "Kevin"
        self.vs_question_index += 1
        
        btn_next = Button(text="Next Turn", size_hint=(1, 0.3), background_color=(0.3, 0.6, 0.3, 1))
        btn_next.bind(on_press=lambda x: self.show_vs_question())
        self.main_layout.add_widget(btn_next)

    def show_vs_final_score(self):
        k_score = self.vs_scores["Kevin"]
        i_score = self.vs_scores["Irene"]
        
        if k_score > i_score:
            winner_msg = "Winner: Kevin!"
            voice_winner = "البطل الفائز هو كيفين!"
        elif i_score > k_score:
            winner_msg = "Winner: Irene!"
            voice_winner = "البطلة الفائزة هي إيريني!"
        else:
            winner_msg = "It's a Tie!"
            voice_winner = "تعادل بين الأبطال!"

        msg = (f"Competition Finished!\n"
               f"Kevin: {k_score} | Irene: {i_score}\n"
               f"{winner_msg}\nMama Mary & Papa Abanoub salute you!")
        voice_msg = f"انتهت المسابقة! درجات كيفين هي {k_score}، ودرجات إيريني هي {i_score}. {winner_msg}. بابا أبانوب وماما مريم فخورين بيكم!"
        
        lbl = Label(text=msg, font_size='17sp', halign='center')
        self.main_layout.add_widget(lbl)
        speak_now(voice_msg)
        
        btn_back = Button(text="Back to Menu", size_hint=(1, 0.3), background_color=(0.7, 0.3, 0.3, 1))
        btn_back.bind(on_press=lambda x: self.show_main_menu())
        self.main_layout.add_widget(btn_back)

    # ==================== قسم الفوازير والألعاب ====================
    def start_easy_games(self):
        self.riddle_index = 0
        self.riddle_score = 0
        
        riddles_pool_easy = [
            {"q": "ما هو الحيوان الذي أسمه على لونه؟", "ans": "الأسد", "opts": ["الأسد", "الفيل", "الزرافة"]},
            {"q": "بابه مشدود ومالهوش مفتاح، تفتحه إيه؟", "ans": "البطيخة", "opts": ["البطيخة", "الدولاب", "الشنطة"]},
            {"q": "شيء يقرصك ولا تراه؟", "ans": "البرد", "opts": ["البرد", "البعوض", "الريح"]},
            {"q": "ما هو البيت الذي ليس فيه أبواب ولا أوض؟", "ans": "بيت الشعر", "opts": ["بيت الشعر", "الخيمة", "الكهف"]},
            {"q": "ما هو الشيء الذي كلما أخذت منه كبر؟", "ans": "الحفرة", "opts": ["الحفرة", "الجبل", "النهر"]},
            {"q": "ما هو الشيء الذي يمشي بلا رجلين ولا يدخل إلا باذنين؟", "ans": "الصوت", "opts": ["الصوت", "الرياح", "السحاب"]},
            {"q": "له عين واحدة ولكن لا يرى بها فما هو؟", "ans": "الإبرة", "opts": ["الإبرة", "القفل", "المفتاح"]},
            {"q": "من هو الكائن الذي يكسو الناس ويظل عارياً؟", "ans": "الإبرة", "opts": ["الإبرة", "المقص", "الشجرة"]},
            {"q": "ما هو الشيء الذي يتكلم جميع لغات العالم؟", "ans": "صدى الصوت", "opts": ["صدى الصوت", "الراديو", "التلفزيون"]},
            {"q": "ما هو الشيء الذي يحميك من الشمس ويحترق هو؟", "ans": "الشمعة", "opts": ["الشمعة", "الشمسية", "القبعة"]}
        ]
        
        riddles_pool_med = [
            {"q": "ما هو الشيء الذي له أربع أرجل ولا يستطيع المشي؟", "ans": "الترابيزة", "opts": ["الترابيزة", "الكلب", "القطة"]},
            {"q": "يتحرك بدون قدمين ويطير بدون جناحين فما هو؟", "ans": "السحاب", "opts": ["السحاب", "الطائر", "السمكة"]},
            {"q": "ما هو الشيء الذي كلما زاد نقص؟", "ans": "العمر", "opts": ["العمر", "المال", "الشجر"]},
            {"q": "ما هو الشيء الموجود في وسط العاصمة؟", "ans": "حرف الواو", "opts": ["حرف الواو", "الشارع", "النهر"]},
            {"q": "يولد كبير ويموت صغير فما هو؟", "ans": "الشمعة", "opts": ["الشمعة", "الإنسان", "الشجر"]}
        ]

        riddles_pool_hard = [
            {"q": "ما هو الشيء الذي إذا أكلته كله تستفيد، وإذا أكلت نصفه مت؟", "ans": "السمسم", "opts": ["السمسم", "التفاح", "الخبز"]},
            {"q": "ما هو الشيء الذي تذبحه وتبكي عليه؟", "ans": "البصل", "opts": ["البصل", "العصفور", "الخروف"]},
            {"q": "أنت تراني في الظلام ولكن لا تراني في النور، فمن أنا؟", "ans": "الظل", "opts": ["الظل", "النجم", "القمر"]}
        ]

        constructed_list = []
        for i in range(1, 31):
            if i <= 10:
                item = random.choice(riddles_pool_easy)
            elif i <= 20:
                item = random.choice(riddles_pool_med)
            else:
                item = random.choice(riddles_pool_hard)
            
            constructed_list.append({
                "q": item["q"],
                "ans": item["ans"],
                "opts": item["opts"]
            })

        self.riddles_list = constructed_list
        self.show_riddle()

    def show_riddle(self):
        self.clear_screen()
        
        if self.riddle_index >= len(self.riddles_list):
            self.show_riddle_final_score()
            return

        r_data = self.riddles_list[self.riddle_index]
        
        q_display = (f"Riddles Challenge\n"
                     f"Question ({self.riddle_index + 1} / {len(self.riddles_list)})\n\n"
                     f"Listen to the riddle!")
        
        lbl = Label(text=q_display, font_size='18sp', halign='center')
        self.main_layout.add_widget(lbl)
        
        options = r_data["opts"][:]
        random.shuffle(options)
        
        options_voice = f"الاختيارات هي: {options[0]}، أو {options[1]}، أو {options[2]}"
        speak_now(f"فزورة رقم {self.riddle_index + 1}: {r_data['q']}. {options_voice}")

        for opt in options:
            btn = Button(text=opt, size_hint=(1, 0.15), background_color=(0.8, 0.4, 0.2, 1))
            btn.bind(on_press=lambda instance, o=opt: self.check_riddle_answer(o))
            self.main_layout.add_widget(btn)

    def check_riddle_answer(self, selected_ans):
        stop_speech() # قطع الصوت القديم فور الإجابة في الفوازير
        r_data = self.riddles_list[self.riddle_index]
        self.clear_screen()
        
        if selected_ans == r_data["ans"]:
            self.riddle_score += 1
            msg = "Brilliant! Correct Answer!"
            voice_msg = "برافو عليك، إجابة صحيحة وذكية!"
        else:
            msg = f"Wrong! Correct was: {r_data['ans']}"
            voice_msg = f"للأسف إجابة خاطئة، الإجابة الصحيحة هي {r_data['ans']}"
            
        lbl = Label(text=msg, font_size='20sp', halign='center')
        self.main_layout.add_widget(lbl)
        speak_now(voice_msg)
        
        self.riddle_index += 1
        btn_next = Button(text="Next Riddle", size_hint=(1, 0.3), background_color=(0.3, 0.6, 0.3, 1))
        btn_next.bind(on_press=lambda x: self.show_riddle())
        self.main_layout.add_widget(btn_next)

    def show_riddle_final_score(self):
        msg = (f"Riddles Game Finished!\n"
               f"Your Score: {self.riddle_score} / {len(self.riddles_list)}\n"
               f"Mama Mary & Papa Abanoub are so proud of you!")
        voice_msg = f"خلصت الفوازير يا أبطال! درجتكم هي {self.riddle_score} من {len(self.riddles_list)}. ماما مريم وبابا أبانوب فخورين بيكم جداً!"
        
        lbl = Label(text=msg, font_size='18sp', halign='center')
        self.main_layout.add_widget(lbl)
        speak_now(voice_msg)
        
        btn_back = Button(text="Back to Menu", size_hint=(1, 0.3), background_color=(0.7, 0.3, 0.3, 1))
        btn_back.bind(on_press=lambda x: self.show_main_menu())
        self.main_layout.add_widget(btn_back)

if __name__ == '__main__':
    MaryamQuizApp().run()
