# -*- coding: utf-8; Mode: Python; indent-tabs-mode: nil; tab-width: 4 -*-

# Copyright (C) 2010 Canonical Ltd.
# Written by Evan Dandrea <evan.dandrea@canonical.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from __future__ import print_function

import os
import subprocess
import sys

from ubiquity import i18n, misc, osextras, plugin, upower


NAME = 'overview'
AFTER = 'usersetup'
WEIGHT = 11
OEM = False


# TODO: This cannot be a non-debconf plugin after all as OEMs may want to
# preseed the 'install updates' and 'install non-free software' options.  So?
# Just db_get them.  No need for any other overhead, surely.  Actually, you
# need the dbfilter for that get.



class PageGtk(plugin.PluginUI):

    plugin_title = 'ubiquity/text/overview_heading_label'

    def __init__(self, controller, *args, **kwargs):
        self.controller = controller
        from gi.repository import Gtk
        builder = Gtk.Builder()
        self.controller.add_builder(builder)
        builder.add_from_file(os.path.join(
            os.environ['UBIQUITY_GLADE'], 'stepOverview.ui'))
        builder.connect_signals(self)
        self.page = builder.get_object('stepPrepare')
        self.langreset = builder.get_object(
            'langreset')
        self.linfo = builder.get_object(
            'linfo')
        self.diskinfo = builder.get_object(
            'diskinfo')
        self.userinfo = builder.get_object(
            'userinfo')
        self.passwdinfo = builder.get_object(
            'passwdinfo')
        self.verifylabel = builder.get_object(
            'verifylabel')
        self.modelcode = builder.get_object('modelcode')
        self.layoutcode = builder.get_object('layoutcode')
        self.keyboardinfo = builder.get_object(
            'keyboardinfo')
        self.partitioninfo = builder.get_object(
            'partitioninfo')
        self.plugin_widgets = self.page

    def set_modelcode(self,modelcode):
        if modelcode:
            self.modelcode.set_text(modelcode)

    def get_modelcode(self):
        return self.modelcode.get_text()
 
    def set_layoutcode(self,layoutcode):
        if layoutcode:
            self.layoutcode.set_text(layoutcode)

    def get_layoutcode(self):
        return self.layoutcode.get_text()

    def set_language_info(self, langinfo):
        if langinfo:
            self.linfo.set_text(langinfo)

    def get_language_info(self):
        return self.linfo.get_text()

    def set_username_info(self, usernameinfo):
        if usernameinfo:
            self.userinfo.set_text(usernameinfo)

    def get_username_info(self):
        return self.userinfo.get_text()

    def set_passwd_info(self, passwordinfo):
        if passwordinfo:
            self.passwdinfo.set_text(passwordinfo)
    
    def get_passwd_info(self):
        return self.passwdinfo.get_text()

    def set_timezone_info(self,timezoneinfo):
        if timezoneinfo:
            self.diskinfo.set_text(timezoneinfo)

    def get_timezone_info(self):
        return self.diskinfo.get_text()

    def get_langreset_info(self):
        return self.langreset.get_active_text()

    def set_keyboard_info(self, keyboardinfo):
        if keyboardinfo:
            self.keyboardinfo.set_text(keyboardinfo)

    def set_partition_info(self, partitioninfo):
        if partitioninfo:
            self.partitioninfo.set_text(partitioninfo)

    def on_inforeset_clicked(self,ubused_widget):
        resetlang=self.get_langreset_info() 
        resettz=self.get_timezone_info()
        resetusername=self.get_username_info()
        resetpasswd=self.get_passwd_info
        self.set_language_info(resetlang)         
        self.verifylabel.hide()
        self.verifylabel.show()

class Page(plugin.Plugin):
    def prepare(self):
 #       if (self.db.get('apt-setup/restricted') == 'false' or
 #               self.db.get('apt-setup/multiverse') == 'false'):
 #           self.ui.set_allow_nonfree(False)
 #       else:
 #           use_nonfree = self.db.get('ubiquity/use_nonfree') == 'true'
 #           self.ui.set_use_nonfree(use_nonfree)
#        user_sure = self.db.get('ubiquity/user_sure') == 'true'
        usernames = self.db.get('passwd/username')
        langinfo = self.db.get('localechooser/languagelist')
        passwordinfo = self.db.get('passwd/user-password')
        timezoneinfo = self.db.get('time/zone')
        keyboardmodel = self.db.get('keyboard-configuration/modelcode')
        keyboardlayout = self.db.get('keyboard-configuration/layoutcode')
       
        if langinfo == 'zh_CN':
            language = "中文"
        else :
            language = "English"
        self.ui.set_language_info(language)
        self.ui.set_username_info(usernames)
        self.ui.set_passwd_info(passwordinfo)
        self.ui.set_timezone_info(timezoneinfo)

        self.ui.set_modelcode(keyboardmodel)
        self.ui.set_layoutcode(keyboardlayout)
        modelcodetext = self.ui.get_modelcode()
        layoutcodetext = self.ui.get_layoutcode()

        if layoutcodetext is 'cn':
            keboardindo = '汉语键盘'
        elif layoutcodetext is 'en':
            keyboardindo = '英语键盘'
        else:
            keyboardindo = '其他键盘'
        self.ui.set_keyboard_info(keyboardindo)
        self.ui.set_partition_info(keyboardlayout)
        
        command = ['/usr/share/ubiquity/simple-plugins', 'prepare2']
        questions = ['ubiquity/user_sure']
        return command, questions

 

    def ok_handler(self):
        languageinfo = self.ui.get_language_info()
        self.preseed_bool('ubiquity/user_sure', True) 
#        self.preseed_bool('ubiquity/use_nonfree', use_nonfree)
#        self.preseed_bool('ubiquity/download_updates', download_updates)
#        if use_nonfree:
#            with misc.raised_privileges():
                # Install ubuntu-restricted-addons.
#                self.preseed_bool('apt-setup/universe', True)
#                self.preseed_bool('apt-setup/multiverse', True)
        plugin.Plugin.ok_handler(self)
