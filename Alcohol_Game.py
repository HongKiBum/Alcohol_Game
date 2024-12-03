import os
import re
import random
from difflib import SequenceMatcher
import speech_recognition as sr
from tkinter import Tk, Label, Button, filedialog

class total_game:
    def __init__(self):
        pass
    def initialize_gui(self, root, width, height, bg_color):
        root.title("어려운 문장 발음 평가 프로그램")
        root.geometry(f"{width}x{height}")
        root.configure(bg=bg_color)

        return root


    def create_label(self, root, text, font, bg, fg, pady=0, wraplength=None, justify=None):
        label = Label(root, text=text, font=font, bg=bg, fg=fg, wraplength=wraplength, justify=justify)
        label.pack(pady=pady)
        return label


    def create_button(self, root, text, command, font, bg, fg, activebackground, width, height, pady=0):
        button = Button(
            root, text=text, command=command, font=font, bg=bg, fg=fg,
            activebackground=activebackground, relief="flat", width=width, height=height
        )
        button.pack(pady=pady)
        return button


    def select_sentence(self, sentences, sentence_label):
        selected_sentence = random.choice(sentences)
        sentence_label.config(text=selected_sentence)
        return selected_sentence


    def similar_sound_correction(self, word):
        replacements = {
            "쟝": "장",
            "깡": "강",
            "도로록": "도로룩",
            "두루룩": "두루륵",
            "홑겹": "홀겹",
            "겹홑": "겹홀",
            "창살": "창쌀",
            "단풍잎": "단퐁잎",
            "토끼통": "토끼톳",
            "쇠창살": "쇠쌍살",
            "철창살": "쓸창살",
            "공장장": "공쨍장"
        }
        for key, value in replacements.items():
            word = word.replace(key, value)
        return word


    def evaluate_pronunciation(self, correct_text, recorded_text):
        correct_words = re.findall(r'\S+', correct_text)
        recorded_words = re.findall(r'\S+', recorded_text)

        total_ratio = 0
        word_count = min(len(correct_words), len(recorded_words))
        detailed_results = []

        for correct_word, recorded_word in zip(correct_words, recorded_words):
            corrected_recorded_word = similar_sound_correction(recorded_word)
            ratio = SequenceMatcher(None, correct_word, corrected_recorded_word).ratio()
            detailed_results.append((correct_word, corrected_recorded_word, ratio))
            total_ratio += ratio

        avg_ratio = total_ratio / word_count if word_count > 0 else 0
        avg_percentage = avg_ratio * 100

        if avg_ratio > 0.9:
            result = "정확"
        elif avg_ratio > 0.7:
            result = "조금 틀림"
        else:
            result = "많이 틀림"

        return result, avg_percentage, detailed_results


    def recognize_audio(self, file_path):
        recognizer = sr.Recognizer()
        audio_file = sr.AudioFile(file_path)

        with audio_file as source:
            audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data, language='ko-KR')
            return text
        except sr.UnknownValueError:
            return "음성을 인식할 수 없습니다."
        except sr.RequestError:
            return "서비스에 접근할 수 없습니다."


    def analyze_pronunciation(self, correct_text, audio_file, result_label):
        recorded_text = recognize_audio(audio_file)
        print(f"녹음된 텍스트: {recorded_text}")

        result, avg_percentage, _ = evaluate_pronunciation(correct_text, recorded_text)
        print(f"발음 정확도: {result} (평균 유사도: {avg_percentage:.2f}%)")

        result_label.config(text=f"발음 정확도: {result} ({avg_percentage:.2f}%)")


    def upload_audio(self, selected_sentence, result_label):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;*.mp3")])
        if file_path:
            self.analyze_pronunciation(selected_sentence, file_path, result_label)


    def pronunciation_app(self):
        # Initialize GUI
        root = Tk()
        root = self.initialize_gui(root, width=800, height=500, bg_color="#FFFFFF")

        # Sentences for evaluation
        sentences = [
            "도토리가 문을 도로록, 드르륵, 두루룩 열었는가?",
            "우리집 옆집 앞집 뒤창살은 홑겹창살이고 우리집 뒷집 앞집 옆창살은 겹홑창살이다.",
            "한양양장점 옆에 한영양장점 한영양장점 옆에 한양양장점",
            "청단풍잎 홍단풍잎 흑단풍잎 백단풍잎",
            "작은 토끼 토끼통 옆에는 큰 토끼 토끼 통이 있고 큰 토끼 토끼통 옆에는 작은 토끼 토끼 통이 있다.",
            "생각이란 생각하면 생각할수록 생각나는 것이 생각이므로 생각하지 않는 생각이 좋은 생각이라 생각한다.",
            "앞뜰에 있는 말뚝이 말 맬 말뚝이냐 말 못맬 말뚝이냐",
            "경찰청 쇠창살 외철창살 검찰청 쇠창살 쌍철창살",
            "간장 공장 공장장은 강 공장장이고 된장 공장 공장장은 장 공장장이다."
        ]

        # GUI Elements
        label = self.create_label(
            root, "랜덤 문장을 읽어보세요!", font=("Arial", 18), bg="#FFFFFF", fg="#333333", pady=20
        )

        sentence_label = self.create_label(
            root, "", font=("Arial", 14), bg="#FFFFFF", fg="#333333", pady=20, wraplength=700, justify="center"
        )

        result_label = self.create_label(
            root, "", font=("Arial", 14), bg="#FFFFFF", fg="#333333", pady=30
        )

        def select_sentence_callback():
            nonlocal selected_sentence
            selected_sentence = self.select_sentence(sentences, sentence_label)

        def upload_audio_callback():
            self.upload_audio(selected_sentence, result_label)

        select_button = self.create_button(
            root, "누르면 랜덤한 문장이 나와요!", select_sentence_callback,
            font=("Arial", 14), bg="#87CEEB", fg="white",
            activebackground="#B0E0E6", width=23, height=2, pady=10
        )

        upload_button = self.create_button(
            root, "오디오 파일 업로드", upload_audio_callback,
            font=("Arial", 14), bg="#87CEEB", fg="white",
            activebackground="#B0E0E6", width=15, height=2, pady=10
        )

        # Initialize selected_sentence variable
        selected_sentence = ""

        root.mainloop()


