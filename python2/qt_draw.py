#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os
import time
import threading
import random
import copy


class config:

    # 【特等奖、一等奖、二等奖、三等奖、VIP奖】
    # 总个数
    prize_all_num  = [3,3,15,30,200]
    # 每次抽奖个数
    prize_once_num = [1,1,5,10,1]
    # 奖项选择设置对应值
    prize_show_value = "0: 特等奖\n1: 一等奖\n2: 二等奖\n3: 三等奖\n4: VIP奖"
    prize_name = ["特等奖","一等奖","二等奖","三等奖","VIP专项"]
    # 默认设置为 三等奖
    prize_chose_default = 3

    prize_rejoin_default = 4


    # 抽奖人照片集
    person_photo_path = "2019_photo"
    
    # 测试目录
    test_path = "test_photo"

    unkown_photo = 'unkown.png'

    # 大标题名字    
    title_str = "xxxxx2019年会抽奖软件"
    
    
    # 达到两排显示的个数
    show_two_line = 5
    show_x_zone = 0.95
    show_y_single_zone = 0.25


    
    
    # line : 0 就一行 1：有两行，这是第一行，2：有两行，这是第二行
    # y start
    show_y_place_start = [0.2, 0.2, 0.5]
    show_x_place_start = 0.05
    show_name_place = 0.001
    name_size = [140,40]

    show_prize_list_size = [0.6,0.6]

    show_x_y_ratio = 0.75
    show_y_size = [0.5, 0.25, 0.25]




class Photo_class:

    def __init__(self):
        print('Photo')
        self.find_photo('test_photo')


    def read_from_file(self):
        fp = open('config.txt')
        while True:
            line = fp.readline()
            if not line: break
        fp.close

    def find_photo(self, path):
        self.photos = {}
        for file in os.listdir(path):
            print(file)
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                self.photos[self.filter_name(file)] = file_path


    def filter_name(self,filename):
        return filename.split('.')[0]

    



class prize_class:

    person_size = [182, 176]
    window_size = [1920, 1080]

    once_show_place = []
    once_name_place = []
 
    #show_zone = 0.95
    #show_start = [0.05, 0.2]

    hit_all_list = {0:[],1:[], 2:[], 3:[], 4:[]}

    show_place = []
    name_place = []
    show_list = []
    now_choice_prize = None
    prize_num = None
    VIP = False

    def __init__(self,w,h):
        self.VIP = False
        self.now_choice_prize = config.prize_chose_default
        self.set_window_size(w,h)
        self.photo = Photo_class()
        self.photo_dic = self.photo.photos
        self.join_person = self.photo.photos.keys()
        self.VIP_person = copy.deepcopy(self.join_person)
        print self.join_person
        self.init_prize()


    def init_prize(self):
        self.prize_num = config.prize_once_num[config.prize_chose_default]
        self.show_list = []
        self.show_place = []
        self.init_show()
        self.init_once_show_place()

    def set_window_size(self,w,h):
        self.window_size[0] = w
        self.window_size[1] = h
        print("update window_size: ", self.window_size)

    def init_show(self):
        self.show_list = []
        for i in range(self.prize_num):
            self.show_list.append(config.unkown_photo.decode('GB2312'))
        self.get_show_and_name_place()
        print("init:",self.prize_num, " show:", self.show_list)

    def calc_show_place(self, calc_list, line):
        place_all = []
        name_all = []
        number = len(calc_list)
        x_zone_sigle = (config.show_x_zone *  self.window_size[0]) / number
        new_start = config.show_x_place_start *  self.window_size[0]

        photo_new = self.person_size[0] / 2
        for i in range(number):
            center_place = new_start + (x_zone_sigle / 2)
            new_place = [(center_place - photo_new), config.show_y_place_start[line] *  self.window_size[1]]
            place_all.append(new_place)

            y_name_zone  = config.show_name_place * self.window_size[1]
            name_place = [(center_place - (config.name_size[0] /2)) , (y_name_zone + new_place[1] + self.person_size[1])]
            name_all.append(name_place)

            new_start += x_zone_sigle
        return place_all, name_all

    def calc_once_show_place(self):
        size = self.photo_size_calc(0)
        x_zone_sigle = (config.show_x_zone *  self.window_size[0])
        new_start = config.show_x_place_start *  self.window_size[0]
        new_place = 0.0
        photo_new = size[0] / 2
        center_place = new_start + (x_zone_sigle / 2)
        place_all = [(center_place - photo_new), config.show_y_place_start[0] *  self.window_size[1]]

        y_name_zone  = config.show_name_place * self.window_size[1]
        name_all = [(center_place - (config.name_size[0] /2)) , (y_name_zone + place_all[1] + size[1])]

        return place_all, name_all

    def person_size_recalc(self, line):
        self.person_size[1] = self.window_size[1] * config.show_y_size[line]
        self.person_size[0] = config.show_x_y_ratio * self.person_size[1]
        print("update photo size: ", self.person_size)

    def photo_size_calc(self, line):
        y = self.window_size[1] * config.show_y_size[line]
        x = config.show_x_y_ratio * y
        return [x,y]

    def init_once_show_place(self):
        show , name = self.calc_once_show_place()
        self.once_show_place = show
        self.once_name_place = name



    def get_show_and_name_place(self):
        self.show_place = []
        self.name_place = []
        number = min(len(self.show_list), self.prize_num)
        if number >= config.show_two_line :
            self.person_size_recalc(1)
            first_number = number / 2
            list1,name1 = self.calc_show_place(self.show_list[:first_number], 1)
            list2,name2 = self.calc_show_place(self.show_list[first_number:], 2)
            self.show_place = list1+list2
            self.name_place = name1+name2
            
        else:
            self.person_size_recalc(0)  
            self.show_place, self.name_place = self.calc_show_place(self.show_list, 0)
        #print(self.show_place )
        #print(self.name_place )

    def add_hit_prize(self):
        self.show_list = []
        we_need_list = self.get_person_list()
        random.shuffle(we_need_list)
        for i in range(self.prize_num):
            if len(we_need_list) <= i : break
            self.show_list.append(self.photo.photos[we_need_list[i]].decode('GB2312'))
        if not self.show_list: return
        self.get_show_and_name_place()
        #print("now show:", self.show_list)

    def getplace(self, place):
        p_x =  (float)(self.window_size[0]) * place[0]
        p_y =  (float)(self.window_size[1]) * place[1]
        return [p_x, p_y]

    def get_person_list(self):
        if self.VIP == True:
            return self.VIP_person
        else:
            return self.join_person

    def add_once_show_prize(self):
        we_need_list = self.get_person_list()
        random.shuffle(we_need_list)
        return self.photo.photos[we_need_list[0]].decode('GB2312'),0

    def add_hit_prize_real(self):
        self.show_list = []
        remove_index = []
        we_need_list = self.get_person_list()
        random.shuffle(we_need_list)
        for i in range(self.prize_num):
            if len(we_need_list) <= i : break
            self.show_list.append(self.photo.photos[we_need_list[i]].decode('GB2312'))
            remove_index.append(we_need_list[i])
            #self.join_person.remove(self.join_person[i])
        if not self.show_list: return
        self.get_show_and_name_place()
        print("now hit show:", self.show_list)
        #for rm in remove_index:
        #    we_need_list.remove(rm)
        return we_need_list, remove_index

    def set_new_prize(self, value):
        self.VIP = False
        if value == config.prize_rejoin_default:
            self.VIP = True
        self.prize_num = config.prize_once_num[value]
        self.now_choice_prize = value

    def file_name_filter(self, filename):
        new = filename.replace('\\', '/')
        res =  new.split('.')[0]
        return res.split('/')[-1]

    def out_result_file(self, list):
        fp = open('hit_prize_list.txt', 'a+')
        for file in list:
            name = self.file_name_filter(file)
            fp.write('\n')
            str_w = str(self.now_choice_prize) + " add " + name
            fp.write(str_w)
            self.hit_all_list[self.now_choice_prize].append(name)
        fp.close()

    def remove_hit(self, value):
        now_list = self.get_person_list()
        file = now_list[value]

        fp = open('hit_prize_list.txt', 'a+')
        name = self.file_name_filter(file)
        fp.write('\n')
        str_w = str(self.now_choice_prize) + " add " + name
        fp.write(str_w)
        self.hit_all_list[self.now_choice_prize].append(name)
        fp.close()

        now_list.remove(file)

class MyApp(QWidget):
    
    btn_sty = "QPushButton{color:black}""QPushButton{background-color:yellow}""QPushButton{border:2px}""QPushButton{border-radius:20px}""QPushButton{padding:20px 40px}"
    btn_font = QFont("微软雅黑",20,QFont.Bold)
    win_size = [300, 30, 1000, 1000]

    once_name_show = None
    once_photo_show = None
    once_scroll_start = False
    scroll_temp = None
    now_scroll_number = 0

    persons_lb = []
    names_lb = []
    prize = None

    desktop = None
    screen_height = None
    screen_width = None
    screenRect = None

    title_show = None
    title_p_show = None

    main_p = None
    main_layout = None

    start_btn = None
    show_btn = None
    chose_btn = None
    show_history = False

    show_lable = None


    def __init__(self):
        super(MyApp,self).__init__()
        self.init_get_size()
        self.init_param()
        self.init_ui()

    def init_param(self):
        self.prize = prize_class(self.screen_width, self.screen_height)


    def init_ui(self):
        self.init_windowtile()
        self.init_mainwindow()
        self.init_text()
        self.init_button()
        self.init_show_photo()
        self.init_widget()
        self.init_scroll_show()

    def init_get_size(self):
        self.desktop = QApplication.desktop()
        self. screenRect = self.desktop.screenGeometry()
        self.screen_height = self.screenRect.height()
        self.screen_width = self.screenRect.width()
        print(self.screen_height," : ", self.screen_width)


    def init_windowtile(self):
        self.setWindowTitle("2019年年会")
        self.move_center()

    def init_text(self):
        self.title_show = QLabel(self)
        self.title_show.setText(config.title_str)
        self.title_show.setFont(QFont("Roman times",30,QFont.Bold))
        self.title_show.setStyleSheet("color:red")
        self.title_show.setScaledContents(True)
        #self.title_show.setAlignment(Qt.AlignCenter)
        self.title_show.resize(900,40)
        place = self.prize.getplace([0.4,0.01])
        self.title_show.move(place[0], place[1])

        self.title_p_show = QLabel(self)
        self.title_p_show.setText('三等奖')
        self.title_p_show.setFont(QFont("Roman times",30,QFont.Bold))
        self.title_p_show.setStyleSheet("color:red")
        self.title_p_show.setScaledContents(True)
        self.title_p_show.resize(200,40)
        place = self.prize.getplace([0.5,0.05])
        self.title_p_show.move(place[0], place[1])



    def init_mainwindow(self):
        self.main_p = QPalette()
        self.main_p.setBrush(self.backgroundRole(),QBrush(QPixmap("beijing2.jpg")))
        #self.main_p.setScaledContents(True)
        self.setPalette(self.main_p)

    def init_button(self):
        self.start_btn = QPushButton("PyQt5 Button", self)
        #self.start_btn = QAbstractButton("PyQt5 Button", self)
        self.start_btn.setText("长按开始第" + str(self.now_scroll_number + 1) + "个")
        self.start_btn.setAutoRepeatDelay(0.01)
        self.start_btn.setAutoRepeat(True)
        #self.start_btn.setCheckable(True)
        self.start_btn.clicked.connect(self.btn_start_once)
        #self.start_btn.pressed.connect(self.btn_start)
        self.start_btn.released.connect(self.btn_hit_once)
        #self.start_btn.move(100, 70)
        self.start_btn.setStyleSheet(self.btn_sty)
        self.start_btn.setFont(self.btn_font)


        self.show_btn = QPushButton("PyQt5 Button2", self)
        self.show_history = False
        self.show_btn.setText("显示历史中奖")
        self.show_btn.clicked.connect(self.btn_show)
        #self.start_btn.move(100, 70)
        self.show_btn.setStyleSheet(self.btn_sty)
        self.show_btn.setFont(self.btn_font)

        self.chose_btn = QPushButton("PyQt5 Button2", self)
        self.chose_btn.setText("选择奖项")
        self.chose_btn.clicked.connect(self.chose_show)
        #self.start_btn.move(100, 70)
        self.chose_btn.setStyleSheet(self.btn_sty)
        self.chose_btn.setFont(self.btn_font)


    def init_scroll_show(self):
        person_size = self.prize.photo_size_calc(0)

        label_ph = QLabel(self)
        #label_ph.setToolTip(name)
        label_ph.setPalette(self.scale_image_once(config.unkown_photo.decode('GB2312')))
        label_ph.setAlignment(Qt.AlignCenter)
        label_ph.setScaledContents(True)
        label_ph.setAutoFillBackground(True)
        label_ph.setFont(self.btn_font)
        label_ph.resize(person_size[0], person_size[1])
        place = self.prize.once_show_place

        self.once_photo_show = label_ph
        self.once_photo_show.move(place[0], place[1])

        label_nm = QLabel(self)
        label_nm.setText("不知道是谁")
        label_nm.setFont(QFont("微软雅黑", 20, QFont.Bold))
        label_nm.setStyleSheet("color:yellow")
        label_nm.setAlignment(Qt.AlignCenter)
        label_nm.setScaledContents(True)
        label_nm.resize(config.name_size[0], config.name_size[1])
        place = self.prize.once_name_place

        self.once_name_show = label_nm
        self.once_name_show.move(place[0], place[1])

        self.once_photo_show.hide()
        self.once_name_show.hide()


    def btn_show(self):
        print("this is show start")
        if not self.show_history:
            self.show_now_hit_prize()
            self.show_history = True
            self.show_btn.setText("显示当前中奖")
        else:
            if self.show_lable:
                 self.show_lable.deleteLater()
                 self.show_lable = None
            self.show_photo(True)
            self.show_history = False
            self.show_btn.setText("显示历史中奖")

    def create_prize_list_show(self):
        self.show_lable = QLabel(self)
        #self.show_lable.setText(name)
        self.show_lable.setWordWrap(True)
        self.show_lable.setFont(QFont("微软雅黑",25,QFont.Bold))
        self.show_lable.setStyleSheet("color:black")
        self.show_lable.setScaledContents(True)
        self.show_lable.resize(config.show_prize_list_size[0]*self.screen_width,config.show_prize_list_size[1]*self.screen_height)
        self.show_lable.move(self.screen_width*0.3, self.screen_height*0.3)

    def show_now_hit_prize(self):
        self.show_photo(False)
        time.sleep(0.01)
        self.create_prize_list_show()
        str_show = ""
        #VIP奖
        str_show += self.add_show_str(4)
        str_show += self.add_show_str(0)
        str_show += self.add_show_str(1)
        str_show += self.add_show_str(2)
        str_show += self.add_show_str(3)

        self.show_lable.setText(str_show)
        self.show_lable.show()

    def add_show_str(self, value):
        str_now = " \n"
        str_now += config.prize_name[value]
        str_now += " : "
        for name in self.prize.hit_all_list[value]:
            str_now += name   ##.encode("UTF8")
            str_now += " "
        str_now += " \n"
        return str_now


    def scale_image(self,filename):
        p_pal = QPalette()
        img = QImage(filename)
        size = QSize(self.prize.person_size[0], self.prize.person_size[1])
        p_pal.setBrush(self.backgroundRole(), QBrush(QPixmap.fromImage(img.scaled(size, Qt.IgnoreAspectRatio))))
        return p_pal

    def scale_image_once(self, filename):
        person_size = self.prize.photo_size_calc(0)
        p_pal = QPalette()
        img = QImage(filename)
        size = QSize(person_size[0], person_size[1])
        p_pal.setBrush(self.backgroundRole(), QBrush(QPixmap.fromImage(img.scaled(size, Qt.IgnoreAspectRatio))))
        return p_pal

    def create_lable_name(self, name, i):
        label_nm = QLabel(self)
        label_nm.setText(name)
        label_nm.setFont(QFont("微软雅黑",20,QFont.Bold))
        label_nm.setStyleSheet("color:yellow")
        label_nm.setScaledContents(True)
        label_nm.resize(config.name_size[0],config.name_size[1])
        place = self.prize.name_place[i]
        label_nm.move(place[0], place[1])
        return label_nm

    def create_lable_photo(self, file, name, i):
        label_ph = QLabel(self)
        label_ph.setToolTip(name)
        label_ph.setPalette(self.scale_image(file))
        label_ph.setAlignment(Qt.AlignCenter)
        label_ph.setScaledContents(True)
        label_ph.setAutoFillBackground(True)
        label_ph.setFont(self.btn_font)
        label_ph.resize(self.prize.person_size[0],self.prize.person_size[1])
        place = self.prize.show_place[i]
        label_ph.move(place[0], place[1])
        return label_ph

    def init_show_photo(self):
        self.persons_lb = []
        self.names_lb = []
        for i in range(len(self.prize.show_list)):
            self.persons_lb.append(self.create_lable_photo(self.prize.show_list[i], '不知道是谁', i))
            self.names_lb.append(self.create_lable_name('不知道是谁', i))

    def reset_show_photo(self):
        self.clear_photo()
        time.sleep(0.1)
        self.prize.init_show()
        for i in range(len(self.prize.show_list)):
            self.persons_lb.append(self.create_lable_photo(self.prize.show_list[i], '不知道是谁', i))
            self.names_lb.append(self.create_lable_name('不知道是谁', i))
            self.persons_lb[i].show()
            self.names_lb[i].show()

    def show_photo_now_no_create(self):
        time.sleep(0.02)
        if not self.prize.show_list:
            self.show_no_person_msg()
        for i in range(len(self.prize.show_list)):
            name = self.file_name_filter(self.prize.show_list[i])
            self.persons_lb[i].setPalette(self.scale_image(self.prize.show_list[i]))
            self.names_lb[i].setText(name)
            #self.persons_lb[i].show()
            #self.names_lb[i].show()
        self.update()

    def init_widget(self):
        self.main_layout = QHBoxLayout()

        self.main_layout.addWidget(self.chose_btn, 1, Qt.AlignLeft | Qt.AlignBottom)
        self.main_layout.addWidget(self.start_btn, 1, Qt.AlignCenter | Qt.AlignBottom)
        self.main_layout.addWidget(self.show_btn, 1, Qt.AlignRight | Qt.AlignBottom)

        self.main_layout.setSpacing(1)
        self.setGeometry(self.win_size[0], self.win_size[1], self.win_size[2], self.win_size[3])

        self.setLayout(self.main_layout)



    def btn_hit(self):
        print("show the hit list...")
        time.sleep(0.1)
        if self.start_btn.isDown():
            print("--------still")
            return
        print("**************")
        list, rm_index_list = self.prize.add_hit_prize_real()

        if len(self.prize.show_list) == len(self.persons_lb):
            self.show_photo_now_no_create()
        else:
            self.show_photo_now()

        time.sleep(0.2)
        res = QMessageBox.question(self, "抽奖完毕",   "请确认是否认同此次抽奖", QMessageBox.Yes | QMessageBox.No)
        if res== QMessageBox.Yes:
            for rm in rm_index_list:
                list.remove(rm)
            self.prize.out_result_file(rm_index_list)

    def btn_hit_once(self):

        time.sleep(0.1)
        if self.start_btn.isDown():
            #print("--------still")
            return
        print("**************")
        if len(self.prize.join_person) == 0:
            self.show_no_person_msg()
            self.start_btn.setText("本次抽奖结束")
            return

        if not self.once_scroll_start:
            return
        time.sleep(0.2)
        res = QMessageBox.question(self, "抽奖完毕",   "请确认是否认同此次抽奖", QMessageBox.Yes | QMessageBox.No)
        if res== QMessageBox.Yes:
            self.add_to_hit_list(self.scroll_temp[0])
            self.prize.remove_hit(self.scroll_temp[1])
            if len(self.prize.show_list) != len(self.persons_lb):
                self.show_photo_now()
            self.reshow_photo_show(True)

        if self.prize.prize_num == self.now_scroll_number:
            self.start_btn.setText("本次抽奖结束")
        else:
            self.start_btn.setText("长按开始第" + str(self.now_scroll_number+1) + "个")

    def add_to_hit_list(self, file):
        name = self.file_name_filter(file)
        self.persons_lb[self.now_scroll_number].setPalette(self.scale_image(file))
        self.names_lb[self.now_scroll_number].setText(name)
        self.now_scroll_number += 1
            

    def btn_start(self):
        print("this is btn start")
        if not self.start_btn.isDown():
            print("--------out ")
            self.start_btn.setText("开始")
            return
        self.start_btn.setText("滚动中")

        self.prize.add_hit_prize()

        if len(self.prize.show_list) == len(self.persons_lb):
            self.show_photo_now_no_create()
        else:
            self.show_photo_now()

    def btn_start_once(self):

        if not self.start_btn.isDown():
            print("------scroll--out ")
            return
        if len(self.prize.join_person) == 0:
            return
        if self.prize.prize_num == self.now_scroll_number:
            self.start_btn.setText("本次抽奖结束")
            now_prize_name = str(config.prize_name[self.prize.now_choice_prize])
            res = QMessageBox.question(self, "抽奖完毕", "是否继续抽"+now_prize_name, QMessageBox.Yes | QMessageBox.No)
            if res == QMessageBox.Yes:
                self.reset_show_photo()
                self.now_scroll_number = 0
                self.start_btn.setText("长按开始第" + str(self.now_scroll_number+1) + "个")
            return

        self.start_btn.setText("滚动中")

        self.reshow_photo_show(False)

        file, vale = self.prize.add_once_show_prize()
        self.once_photo_show.setPalette(self.scale_image_once(file))
        name = self.file_name_filter(file)
        self.once_name_show.setText(name)

        self.scroll_temp = [file, vale]

        self.update()

    def reshow_photo_show(self, show_enable):
        if show_enable and self.once_scroll_start == True:
            self.once_photo_show.hide()
            self.once_name_show.hide()
            self.show_photo(True)
            self.update()
            self.once_scroll_start = False
        elif show_enable == False and self.once_scroll_start == False:
            self.show_photo(False)
            self.once_photo_show.show()
            self.once_name_show.show()
            self.update()
            self.once_scroll_start = True
        #self.update()

    def show_photo(self, enable):
        if enable:
            for photo in self.persons_lb:
                photo.show()
            for name in self.names_lb:
                name.show()
        else:
            for photo in self.persons_lb:
                photo.hide()
            for name in self.names_lb:
                name.hide()


    def chose_show(self):
        print("chose prize...")
        value, ok = QInputDialog.getDouble(self, "请输入选择奖项", config.prize_show_value, self.prize.now_choice_prize, 0, len(config.prize_show_value), 0)
        print(int(value))
        if self.prize.now_choice_prize == int(value) and self.prize.prize_num != self.now_scroll_number:
            return
        self.prize.set_new_prize(int(value))
        str_prize=config.prize_name[int(value)]
        self.title_p_show.setText(str_prize)
        self.reset_show_photo()
        self.now_scroll_number = 0
        self.start_btn.setText("长按开始第" + str(self.now_scroll_number + 1) + "个")


    def clear_photo(self):
        for person in self.persons_lb:
            person.deleteLater()
        for name in self.names_lb:
            name.deleteLater()

        self.persons_lb = []
        self.names_lb = []

    def file_name_filter(self, filename):
        new = filename.replace('\\', '/')
        res =  new.split('.')[0]
        return res.split('/')[-1]

    def show_no_person_msg(self):
        QMessageBox.information(self, "!", "所有人都已经抽奖完")

    def show_photo_now(self):

        time.sleep(0.01)
        if not self.prize.show_list:
            self.show_no_person_msg()
        #self.persons_lb = []
        for i in range(len(self.prize.show_list)):
            name = self.file_name_filter(self.prize.show_list[i])
            self.persons_lb.append(self.create_lable_photo(self.prize.show_list[i], name, i))
            self.names_lb.append(self.create_lable_name(name, i))
            self.persons_lb[i].show()
            self.names_lb[i].show()

    def move_center(self):
        m = self.frameGeometry()
        w = QDesktopWidget().availableGeometry()
        w_center = w.center()
        m.moveCenter(w_center)
        self.move(m.topLeft())


def main():
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()