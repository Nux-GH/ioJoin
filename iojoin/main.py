#!/usr/bin/kivy
# -*- coding: utf-8 -*-

from .kivy_imports import *
from kivy.app import App

from os.path import expanduser
from os import path
from os import mkdir
from subprocess import check_call, CalledProcessError
from time import sleep

from .ListBox import RV


class FileChooser(ModalView):
    def path_changed(self, a, b, c):
        self.path_label.text = self.file_chooser.path

    def selection_done(self, object, a, b=None):
        if a is not None:
            choosen_path = a[0]
            if path.exists(choosen_path) and not path.isdir(choosen_path):
                self.choosen_files = choosen_path
        self.dismiss()

    def __init__(self, title, start_path=None):
        super().__init__()
        self.choosen_files = None
        self.title = title
        self.size_hint = (0.5, 0.5)

        root = BoxLayout(orientation='vertical')
        title_label = Label(text=title, size=(1, 40), size_hint=(1, None))
        root.add_widget(title_label)
        path_label = Label(text=start_path, size=(1, 40), size_hint=(1, None))
        self.path_label = path_label
        root.add_widget(path_label)
        file_chooser = FileChooserIconView(on_submit=self.selection_done, on_entry_added=self.path_changed)
        file_chooser.title = title
        file_chooser.path = start_path
        self.file_chooser = file_chooser
        root.add_widget(self.file_chooser)

        def ok_button_pressed(arg):
            choosen_path = file_chooser.selection
            if choosen_path is not None and len(choosen_path) > 0:
                self.selection_done(self, choosen_path)
            else:
                self.dismiss()

        button_box = BoxLayout(size=(1, 40), size_hint=(1, None))
        btn_ok = Button(text="OK", on_press=ok_button_pressed)
        btn_no = Button(text="Cancel", on_press=self.dismiss)
        button_box.add_widget(Widget())
        button_box.add_widget(btn_ok)
        button_box.add_widget(btn_no)

        root.add_widget(button_box)
        self.add_widget(root)


class IOMain(App):
    last_pressed = None

    def choose_file(self, argb):
        self.last_pressed = argb
        home = expanduser("~")
        chooser = FileChooser('Select a file...', home)
        chooser.bind(on_dismiss=self._file_selected)
        self.chooser = chooser
        chooser.open()

    def _file_selected(self, args):
        if self.chooser.choosen_files is None:
            return

        if not path.exists('./thumbs'):
            mkdir('./thumbs')
        file_path = self.chooser.choosen_files
        file_name, ext = path.splitext(path.basename(file_path))
        thumb_dest = './thumbs/' + file_name + '_thumb.png'
        thumb_dest = path.abspath(thumb_dest)
        try:
            # pre_command = 'ffmpeg -y -ss 1 -i _in_ -vf select=gt(scene\,0.5) -frames:v 1 -vsync vfr _out_'.split()
            pre_command = 'ffmpeg -y -ss 1 -i _in_ -frames:v 1 _out_'.split()
            command = []
            for c in pre_command:
                if c == '_in_':
                    command.append(file_path)
                elif c == '_out_':
                    command.append(thumb_dest)
                else:
                    command.append(c)

            check_call(command)
        except CalledProcessError as error:
            raise RuntimeError(str(error.output))

        self.last_pressed.child_thumb.source = thumb_dest

    def join_files(self, args):
        self.log('joining')

    def log(self, text):
        self.status_list.add(text)

    def build(self):
        self.root = BoxLayout(orientation='vertical')

        intro_b = Button(text='PRESS TO ADD INTRO', on_press=self.choose_file, pos_hint={'x': 0, 'y': 0})
        self.intro_button = intro_b
        # , source='/home/jrg/Documentos/python/ioPaste/iopaste/test.png')
        intro_thumb = Image(size=(1, 1), pos_hint={'x': 0, 'y': 0})
        self.intro_thumb = intro_thumb
        intro_b.child_thumb = intro_thumb
        intro_layer = FloatLayout()
        intro_layer.add_widget(intro_b)
        intro_layer.add_widget(intro_thumb)

        main_b = Button(text='PRESS TO ADD MAIN VIDEO', on_press=self.choose_file, pos_hint={'x': 0, 'y': 0})
        self.main_button = main_b
        main_thumb = Image(size=(1, 1), pos_hint={'x': 0, 'y': 0})
        self.main_thumb = main_thumb
        main_b.child_thumb = main_thumb
        main_layer = FloatLayout()
        main_layer.add_widget(main_b)
        main_layer.add_widget(main_thumb)

        outro_b = Button(text='PRESS TO ADD OUTRO', on_press=self.choose_file, pos_hint={'x': 0, 'y': 0})
        self.outro_button = outro_b
        outro_thumb = Image(size=(1, 1), pos_hint={'x': 0, 'y': 0})
        self.outro_thumb = outro_thumb
        outro_b.child_thumb = outro_thumb
        outro_layer = FloatLayout()
        outro_layer.add_widget(outro_b)
        outro_layer.add_widget(outro_thumb)

        self.root.add_widget(intro_layer)
        self.root.add_widget(main_layer)
        self.root.add_widget(outro_layer)

        join_layer = BoxLayout(size=(1, 100), size_hint=(1, None))
        # join_button = Button(text='join >>>', on_press=self.join_files, size=(200, 1), size_hint=(None, 1))
        join_button = Button(text='Join >>>', on_press=self.join_files, size=(100, 1), size_hint=(None, 1))

        self.join_button = join_button
        status_list = RV()
        self.status_list = status_list
        join_layer.add_widget(status_list)
        join_layer.add_widget(join_button)

        self.root.add_widget(join_layer)

        # self.label = Label(text="00:00:00", size_hint=(1.0, 1.0), pos_hint={'x': 0.5, 'y': 0})
        # self.label.bind(size=self.label.setter('text_size'))
        # intro_layer.add_widget(self.label)
        return self.root


IOMain().run()
