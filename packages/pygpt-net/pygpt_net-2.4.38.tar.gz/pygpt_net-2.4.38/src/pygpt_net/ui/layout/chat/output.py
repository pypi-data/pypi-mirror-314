#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2024.11.18 00:00:00                  #
# ================================================== #

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QCheckBox, QWidget, QSizePolicy, QPushButton, \
    QGridLayout, QSpacerItem, QWidgetItem, QLayout

from pygpt_net.ui.widget.audio.output import AudioOutput
from pygpt_net.ui.widget.element.labels import ChatStatusLabel, IconLabel, HelpLabel
from pygpt_net.ui.widget.tabs.output import OutputTabs
from pygpt_net.ui.widget.anims.loader import Loader, Loading

from .explorer import Explorer
from .input import Input
from .calendar import Calendar
from .painter import Painter

from pygpt_net.utils import trans
import pygpt_net.icons_rc


class Output:
    def __init__(self, window=None):
        """
        Chat output UI

        :param window: Window instance
        """
        self.window = window
        self.explorer = Explorer(window)
        self.input = Input(window)
        self.calendar = Calendar(window)
        self.painter = Painter(window)

    def setup(self) -> QWidget:
        """
        Setup output

        :return: QWidget
        """
        # tabs
        self.window.ui.tabs['output'] = OutputTabs(self.window)

        # Create the [+] button
        plus_button = QPushButton(QIcon(":/icons/add.svg"), "")
        plus_button.setFixedSize(30, 25)
        plus_button.setFlat(True)
        plus_button.clicked.connect(self.window.controller.ui.tabs.new_tab)
        plus_button.setObjectName('tab-add')
        plus_button.setProperty('tabAdd', True)
        plus_button.setToolTip(trans('action.tab.add.chat'))

        # Add the button to the top right corner of the tab bar
        self.window.ui.tabs['output'].setCornerWidget(plus_button, corner=Qt.TopRightCorner)

        # create empty tabs
        self.window.ui.nodes['output'] = {}
        self.window.ui.nodes['output_plain'] = {}

        # connect signals
        self.window.ui.tabs['output'].currentChanged.connect(
            self.window.controller.ui.tabs.on_tab_changed
        )
        self.window.ui.tabs['output'].tabBarClicked.connect(
            self.window.controller.ui.tabs.on_tab_clicked
        )
        self.window.ui.tabs['output'].tabBarDoubleClicked.connect(
            self.window.controller.ui.tabs.on_tab_dbl_clicked
        )
        self.window.ui.tabs['output'].tabCloseRequested.connect(
            self.window.controller.ui.tabs.on_tab_closed
        )

        # tab bar signals
        self.window.ui.tabs['output'].tabBar().tabMoved.connect(
            self.window.controller.ui.tabs.on_tab_moved
        )

        layout = QVBoxLayout()
        layout.addWidget(self.window.ui.tabs['output'])
        layout.addLayout(self.setup_bottom())
        layout.setContentsMargins(0, 5, 0, 0)

        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def setup_bottom(self) -> QHBoxLayout:
        """
        Setup bottom status bar

        :return: QHBoxLayout
        """
        # video capture icon
        self.window.ui.nodes['icon.video.capture'] = IconLabel(":/icons/webcam.svg")
        self.window.ui.nodes['icon.video.capture'].setToolTip(trans("icon.video.capture"))
        self.window.ui.nodes['icon.video.capture'].clicked.connect(
            lambda:self.window.controller.camera.toggle_capture()
        )

        # audio output icon
        self.window.ui.nodes['icon.audio.output'] = IconLabel(":/icons/volume.svg")
        self.window.ui.nodes['icon.audio.output'].setToolTip(trans("icon.audio.output"))
        self.window.ui.nodes['icon.audio.output'].clicked.connect(
            lambda: self.window.controller.plugins.toggle('audio_output')
        )

        # audio input icon
        self.window.ui.nodes['icon.audio.input'] = IconLabel(":/icons/mic.svg")
        self.window.ui.nodes['icon.audio.input'].setToolTip(trans("icon.audio.input"))
        self.window.ui.nodes['icon.audio.input'].clicked.connect(
            lambda: self.window.controller.plugins.toggle('audio_input')
        )

        # interpreter icon
        self.window.ui.nodes['icon.interpreter'] = IconLabel(":/icons/code.svg")
        self.window.ui.nodes['icon.interpreter'].setToolTip("Python Code Interpreter")
        self.window.ui.nodes['icon.interpreter'].clicked.connect(
            lambda: self.window.tools.get("interpreter").toggle()
        )

        # indexer icon
        self.window.ui.nodes['icon.indexer'] = IconLabel(":/icons/db.svg")
        self.window.ui.nodes['icon.indexer'].setToolTip("Indexer")
        self.window.ui.nodes['icon.indexer'].clicked.connect(
            lambda: self.window.tools.get("indexer").toggle()
        )

        # mode
        self.window.ui.nodes['chat.label'] = ChatStatusLabel("")
        self.window.ui.nodes['chat.label'].setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.window.ui.nodes['chat.label'].setWordWrap(False)

        # model
        self.window.ui.nodes['chat.model'] = ChatStatusLabel("")
        self.window.ui.nodes['chat.model'].setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.window.ui.nodes['chat.model'].setWordWrap(False)

        # plugins
        self.window.ui.nodes['chat.plugins'] = ChatStatusLabel("")
        self.window.ui.nodes['chat.plugins'].setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # timestamp
        self.window.ui.nodes['output.timestamp'] = QCheckBox(trans('output.timestamp'))
        self.window.ui.nodes['output.timestamp'].stateChanged.connect(
            lambda: self.window.controller.chat.common.toggle_timestamp(
                self.window.ui.nodes['output.timestamp'].isChecked())
        )

        # plain text
        self.window.ui.nodes['output.raw'] = QCheckBox(trans('output.raw'))
        self.window.ui.nodes['output.raw'].clicked.connect(
            lambda: self.window.controller.chat.common.toggle_raw(
                self.window.ui.nodes['output.raw'].isChecked())
        )

        """
        # edit icons
        self.window.ui.nodes['output.edit'] = QCheckBox(trans('output.edit'))
        self.window.ui.nodes['output.edit'].clicked.connect(
            lambda: self.window.controller.chat.common.toggle_edit_icons(
                self.window.ui.nodes['output.edit'].isChecked())
        )
        """

        # tokens
        self.window.ui.nodes['prompt.context'] = ChatStatusLabel("")
        self.window.ui.nodes['prompt.context'].setToolTip(trans('tip.tokens.ctx'))
        self.window.ui.nodes['prompt.context'].setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # plugin audio output addon
        self.window.ui.plugin_addon['audio.output'] = AudioOutput(self.window)

        # schedule
        self.window.ui.plugin_addon['schedule'] = ChatStatusLabel("")

        opts_layout = QHBoxLayout()
        # opts_layout.setSpacing(2)  #
        opts_layout.setContentsMargins(0, 0, 0, 0)
        opts_layout.addWidget(self.window.ui.nodes['output.timestamp'])
        # opts_layout.addWidget(self.window.ui.nodes['output.edit'])
        opts_layout.addWidget(self.window.ui.nodes['output.raw'])
        opts_layout.setAlignment(Qt.AlignLeft)

        left_layout = QHBoxLayout()
        left_layout.addLayout(opts_layout)
        left_layout.setContentsMargins(0, 0, 0, 0)

        right_layout = QHBoxLayout()
        right_layout.addWidget(self.window.ui.nodes['icon.video.capture'])
        right_layout.addWidget(self.window.ui.nodes['icon.audio.input'])
        right_layout.addWidget(self.window.ui.nodes['icon.audio.output'])
        right_layout.addWidget(self.window.ui.nodes['icon.interpreter'])
        right_layout.addWidget(self.window.ui.nodes['icon.indexer'])
        right_layout.addWidget(self.window.ui.plugin_addon['schedule'])
        right_layout.addWidget(QLabel(" "))
        right_layout.addWidget(self.window.ui.nodes['chat.plugins'])
        right_layout.addWidget(QLabel(" "))
        right_layout.addWidget(self.window.ui.nodes['chat.label'])
        right_layout.addWidget(QLabel("  "))
        right_layout.addWidget(self.window.ui.nodes['chat.model'])
        right_layout.addWidget(QLabel("  "))
        right_layout.addWidget(self.window.ui.nodes['prompt.context'])
        right_layout.setContentsMargins(0, 0, 0, 0)

        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        right_widget = QWidget()
        right_widget.setLayout(right_layout)

        self.window.ui.nodes['anim.loading'] = Loading()
        self.window.ui.nodes['anim.loading'].hide()

        grid = QGridLayout()

        left_layout = QHBoxLayout()
        left_layout.addWidget(left_widget)
        left_layout.addStretch(1)
        left_layout.setContentsMargins(0, 0, 0, 0)

        center_layout = QHBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(self.window.ui.nodes['anim.loading'])
        center_layout.addStretch()
        center_layout.setContentsMargins(0, 0, 0, 0)

        right_layout = QHBoxLayout()
        right_layout.addStretch(1)
        right_layout.addWidget(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)

        grid.addLayout(left_layout, 0, 0)
        grid.addLayout(center_layout, 0, 1, alignment=Qt.AlignCenter)
        grid.addLayout(right_layout, 0, 2, alignment=Qt.AlignRight)
        grid.setContentsMargins(0, 0, 0, 0)

        self.window.ui.nodes['chat.footer'] = QWidget()
        self.window.ui.nodes['chat.footer'].setLayout(grid)

        bottom_layout = QVBoxLayout()
        bottom_layout.addWidget(self.window.ui.nodes['chat.footer'])
        bottom_layout.setContentsMargins(2, 0, 2, 0)
        return bottom_layout

    def set_fixed_size_policy(self, layout):
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if isinstance(item, QWidgetItem):
                widget = item.widget()
                if widget:
                    widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            elif isinstance(item, QLayout):
                self.set_fixed_size_policy(item)