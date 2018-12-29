import pyglet
import requests
import sys
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QApplication
from PyQt5.QtWidgets import QGridLayout, QInputDialog
from PyQt5.QtWidgets import QPushButton, QDesktopWidget, QLineEdit
import csv


#####################################################

def read_save_file():
    """

    Reading saved file, if attempt is success,
    returns True and data, if not returns False

    """
    try:
        file_to_save = open('save_data.csv', "r")
        first_line = file_to_save.readline()
        file_to_save.close()

        data_new = []
        if len(str(first_line)) > 0:
            with open('save_data.csv') as data_csv:
                reader = csv.reader(data_csv)
                for data_list in reader:
                    data_new.append(data_list)

        return [True, data_new]
    except FileNotFoundError:
        return [False, None]


def write_save_file(data_user):
    """

    Writes saved data to user's data

    """
    create_file = open('save_data.csv', "w")
    create_file.close()

    with open('save_data.csv', 'w', newline='\n') as data_csv:
        write = csv.writer(data_csv, delimiter=',')
        write.writerow(data_user)


#####################################################

def get_word_id(word):
    """

    Gets id of the word, returns ids if everything is done, and false if failed

    """

    url = "http://dictionary.skyeng.ru/api/public/v1/words/" \
          "search?_format=json&search={}".format(word)
    response = requests.get(url)
    try:
        ids = response.json()[0]['meanings'][0]['id']
        return ids
    except:
        return None


def get_information_word_format_dict(ids):
    """

    Gets definition and translation of the word
    if everything is done  and returns false if not

    """

    url = "http://dictionary.skyeng.ru/api/public/" \
          "v1/meanings?_format=json&ids={}".format(ids)
    response = requests.get(url)
    # print(len(response.json()))
    # print(response.json())
    if len(response.json()) >= 1:
        return [True, dict(response.json()[0])]
    else:
        return [False, None]


class word_good:
    """

    Made to define word's level

    """

    def __init__(self, word_info):
        print(word_info)
        if word_info[0]:
            self.word_dict = word_info[1]  # Initialising
        else:
            print("Yes")
            self.word_dict = {'difficultyLevel': 'None', "id": 'None'}

    def get_id(self):
        """

        Returns id of the word

        """
        return self.word_dict['id']

    def get_translate(self):
        """

        Returns translation of the word

        """
        return self.word_dict['translation']['text']

    def get_definition(self):
        """

        Returns definition of the word

        """
        return self.word_dict['definition']['text']

    def get_word_soundUrl(self):
        """

        Returns sound url

        """
        return "http:" + self.word_dict['soundUrl']

    def get_word_def_soundUrl(self):
        return "http:" + self.word_dict['definition']['soundUrl']

    def examples_list(self):
        """
            Module that makes list consisting element with pattern
            of word usage and link on audio file
        """
        example_list = []
        for i in self.word_dict['examples']:
            example_list.append((i['text'], i['soundUrl']))
        return example_list

    def level_word(self):
        """

        Detects level of the word, returns name of level


        """
        print(self.word_dict['difficultyLevel'])
        if str(self.word_dict['difficultyLevel']) == "None":
            return "None"
        elif self.word_dict['difficultyLevel'] == 1:
            return 'A1'
        elif self.word_dict['difficultyLevel'] == 2:
            return 'A2'
        elif self.word_dict['difficultyLevel'] == 3:
            return 'B1'
        elif self.word_dict['difficultyLevel'] == 4:
            return 'B2'
        elif self.word_dict['difficultyLevel'] == 5:
            return 'C1'
        elif self.word_dict['difficultyLevel'] == 6:
            return 'C2'


#####################################################
word_know = set()


class person(word_good):
    """

    Made for multiplayer use, make users go to the next level,
    create new users

    """
    global word_know

    def __init__(self):
        self.name = ''
        self.password = ''
        self.level = "A1"
        self.count_word = 0
        self.level_all = [
            "A1",
            "A2",
            "B1",
            "B2",
            "C1",
            "C2"
        ]

    def know(self):
        """

        Prints and returns already known words

        """
        return word_know

    def name(self):
        """

        Prints and returns name

        """
        print(self.name)
        return self.name

    def level(self):
        """

        Prints and returns knowledge level

        """
        print(self.level)
        return self.level

    def level_info(self, level):
        """

        Function that shows number of known words,
        returns average of them

        """
        if level == 'A1':
            return [0, 1500]
        elif level == 'A2':
            return [1500, 2500]
        elif level == 'B1':
            return [2500, 3250]
        elif level == 'B2':
            return [3250, 3750]
        elif level == 'C1':
            return [3750, 4500]
        elif level == 'C2':
            return [4500, 1000000]

    def create_user(self, name, level):
        """

        Add new user to the list of users, namely create new user

        """
        self.name = name
        # self.password = password
        self.level = level
        self.count_word = max(list(self.level_info(self, self.level)))

    def check_up_level(self):
        """

        Make user able to go to the next level, return True if client can go
        to the next level and False if not

        """
        self.count_word = len(list(word_know))
        for i in self.level_all:
            if self.level_info(i)[2] > self.count_word\
                    >= self.level_info(i)[0]:
                self.level = i
                return True
        return False

    def add_vocablure(self, word):
        """

        Easily adding word to known word list

        """
        word_know.add(word)

    def data_user(self):
        """

        Returns list of known words

        """
        return list(word_know)

    def knowledge_checking(self, word):
        """

        Checking word level, returns true if we should add this word to our
        vocabulary and false if not

        """

        word_inf = word_good(
            get_information_word_format_dict(
                get_word_id(word)
            )
        )

        # print(word_inf.level_word(),
        #       word_inf.level_word() == 'None',
        #       word_inf.get_id())

        # ((int(word_inf.level()[1]) + int(word_inf.level()[0] - 'A') * 2) >= (
        # (int(self.level[1])) + int(self.level[0] - 'A') * 2 or
        #     word_inf.get_id() in self.word_know):

        if word_inf.get_id() == 'None':
            return False

        if (word_inf.level_word() == 'None' or
            int(ord(self.level[0]) - ord('A')) * 2 + int(self.level[1]) <= int(
                ord(word_inf.level_word()[0]) -
                ord('A')) * 2 + int(word_inf.level_word()[1])) \
                and not word_inf.get_id() in word_know:
            self.add_vocablure(self, word_inf.get_id())
            return True
        else:
            return False


#####################################################


class Example(QWidget, person, word_good):
    def __init__(self):
        super().__init__()
        self.chose_user = "A1"
        self.name_music = ""
        self.user = person  # Initialising
        self.word_gd = []
        self.initUI()

    def initUI(self):
        self.setGeometry(400, 400, 400, 400)
        self.setWindowTitle('Translate')  # Window settings
        self.center()

        grid = QGridLayout()
        self.setLayout(grid)

        names = [
            'Введите уровень знаний',
        ]
        #####################################################
        self.button_level = QPushButton(self)
        self.button_level.setText(names[0])  # Button for user's level
        grid.addWidget(self.button_level, 1, 1)  #
        #####################################################

        self.button_input_text = QPushButton(self)
        # Text for processing input button
        self.button_input_text.setText("Ввод текста")
        grid.addWidget(self.button_input_text, 1, 0)

        #####################################################

        self.label = QLabel(self)  # Obviously label

        #####################################################

        self.button_show = QPushButton(self)
        self.button_show.setText("Результат")  # Button for showing result
        grid.addWidget(self.button_show, 1, 2)

        #####################################################
        self.button_level.clicked.connect(self.run)
        self.button_input_text.clicked.connect(self.input)
        # Handler of pressed buttons
        self.button_show.clicked.connect(self.show_dict)
        grid.addWidget(self.label, 0, 1)
        self.show()

        # print(self.run())

    def show_dict(self):
        """

        Shows word, defenition and translation
        of it from string that we got before

        """
        s = ""
        for i in self.word_gd:
            s += str(i[0]) + ': ' + str(i[1]) + ': ' + str(i[2]) + '\n'

        txt, okBtnPressed = QInputDialog.getMultiLineText(
            self,
            "Output",
            'Output',
            s
        )

    def run(self):
        """

        User's menu for defining starting level of client

        """
        self.chose_user, okBtnPressed = QInputDialog.getItem(
            self,
            "Выберите ваш уровеньзнания английского",
            "Выберите ваш уровеньзнания английского",
            (
                'A1 - beginner ',
                'A2 - elementary',
                'B1 - pre-intermediate',
                'B2 - intermediate',
                'C1 - upper-intermediate',
                'C2 - advanced'
            ),
            1,
            False
        )
        self.chose_user = self.chose_user[:2]

        name, okBtnPressed_2 = QInputDialog.getText(
            self,
            "Введите имя",
            "Как тебя зовут?",
            False
        )
        self.user.create_user(person, name, self.chose_user)

        print(self.user.level, self.user.name)

        return [self.chose_user, self.user.name]
        #####################################################
        # self.name_music = "beep"
        #
        # self.play = QPushButton("проиграть произношение слова", self)
        # self.play.resize(self.play.sizeHint())
        # self.play.move(100, 330)
        # self.play.clicked.connect(self.play_music())

    def input(self):
        """

        Indicate processing of the introduced text, shows success of handling

        """
        # text, okBtnPressed_3 = QInputDialog.getText(
        #     self,
        #     "Ввод текста",
        #     "Введите текст?",
        #     False
        # )
        self.label.setText("обработка не сделана")
        text, okBtnPressed_3 = \
            QInputDialog.getMultiLineText(
                self,
                "QInputDialog.getMultiLineText()",
                "Input:"
            )

        text_new = ''
        for i in text.split():
            h = ''
            for j in i.strip():
                if j not in 'qwertyuiopasdfghjklzxcvbnm' \
                            'QWERTYUIOPASDFGHJKLZXCVBNM' \
                            'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ' \
                            'йцукенгшщзхъэждлорпавыфячсмитьбю' \
                            '1234567890':
                    h = h + ' '
                else:
                    h = h + j
            text_new = text_new + ' ' + h

        text = set(text_new.split())
        for i in text:
            if self.user.knowledge_checking(self.user, i):
                id = get_word_id(i)
                word = get_information_word_format_dict(id)
                wrd = word_good(word)
                self.word_gd.append([i, wrd.get_translate(),
                                     wrd.get_definition()])

        self.label.setText("обработка сделана")
        write_save_file(list(self.user.data_user(self)))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        #####################################################
    def get_voice(self, voice_link, name):
        """

        Gets link of the audio file of the word if it is not none

        """
        voice = requests.get(voice_link)
        self.name_music = name
        file_name = '{}.ogg'.format(name)

        if voice is not None:
            with open(file_name, 'wb') as file:
                file.write(bytes(voice.content))

    def play_music(self):
        """

        Playing recieved audio file

        """
        song = pyglet.resource.media('{}.wav'.format(self.name_music),
                                     streaming=False)
        song.play()
        pyglet.app.run()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
