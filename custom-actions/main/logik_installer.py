'''Downloads and installs Logik Matchbox collection to specified folder v1.3'''
# Works with Flame 2020 and up
# Written by Michael Vaglienty. Updated June 13th, 2019
# Email: michaelv_2d@hotmail.com - www.pyflame.com

import os

VERSION = 'v1_3'
DOT_VERSION = VERSION.replace('_', '.')

### config setup ###
CONFIG_PATH = '/opt/Autodesk/shared/python/pyFlame/logik_installer_%s/Config' % VERSION
CONFIG_FILE = os.path.join(CONFIG_PATH, 'config')

def load_config_file():
    '''Load config file, create default if none exists'''

    def check_for_config_file():
        '''Check for config file'''

        if not os.path.isdir(CONFIG_PATH):
            print'config folder does not exist, creating folder and config file.'
            os.makedirs(CONFIG_PATH)
            create_default_config_file()
        else:
            if not os.path.isfile(CONFIG_FILE):
                print'config file does not exist, creating new config file.'
                create_default_config_file()

    def create_default_config_file():
        '''Create default config file'''

        config_text = []

        config_text.insert(0, 'Setup values for pyFlame Logik Installer script.')
        config_text.insert(1, 'Install Path:')
        config_text.insert(2, '/opt/Autodesk')

        out_file = open(CONFIG_FILE, 'w')
        for line in config_text:
            print >>out_file, line
        out_file.close()

    check_for_config_file()

    get_config_values = open(CONFIG_FILE, 'r')
    values = get_config_values.read().splitlines()

    install_path = values[2]

    get_config_values.close()

    return install_path

def main_window(selection):
    '''Main install window'''
    from PySide2 import QtWidgets, QtCore

    install_path = load_config_file()

    def browse_button():
        '''Install path browse button'''

        install_path_saved = install_entry.text()

        install_path = str(QtWidgets.QFileDialog.\
                           getExistingDirectory(window, "Select Directory",
                                                install_path_saved,
                                                QtWidgets.QFileDialog.ShowDirsOnly))

        if install_path != '':
            install_entry.setText(install_path)
        else:
            install_entry.setText(install_path_saved)

    def install_button():
        '''Installs matchboxes from logik site'''
        from subprocess import Popen, PIPE
        import urllib
        import time

        def save_config_file():
            '''Save config file'''

            config_text = []

            config_text.insert(0, 'Setup values for pyFlame Logik Installer script.')
            config_text.insert(1, 'Install Path:')
            config_text.insert(2, install_path)

            out_file = open(CONFIG_FILE, 'w')
            for line in config_text:
                print >>out_file, line
            out_file.close()

        def done_window():
            '''Done message window'''

            messgae_box = QtWidgets.QMessageBox()
            messgae_box.setText('<b><center>Logik Matchbox Installed')
            messgae_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
            messgae_box.setIcon(QtWidgets.QMessageBox.Information)
            reply = messgae_box.exec_()

            if reply == QtWidgets.QMessageBox.Ok:
                window.close()

        def error_window():
            '''Error message window'''

            messgae_box = QtWidgets.QMessageBox()
            messgae_box.setText('<b><center>Install Failed')
            messgae_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
            messgae_box.setIcon(QtWidgets.QMessageBox.Warning)

        install_path = install_entry.text()

        save_config_file()

        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.BusyCursor)

        tar_path = '/opt/Autodesk/shared/python/pyFlame/Logik_Installer_%s/MatchboxShaderCollection.tgz' % VERSION

        urllib.urlretrieve('https://logik-matchbook.org/MatchboxShaderCollection.tgz', tar_path)

        command = 'tar -xvpzf /opt/Autodesk/shared/python/pyFlame/Logik_Installer_%s/MatchboxShaderCollection.tgz --strip-components 1 -C %s' % (VERSION, install_path)

        command = command.split(' ', 6)

        Popen(command, stdin=PIPE, stderr=PIPE, universal_newlines=True)

        time.sleep(5)

        QtWidgets.QApplication.restoreOverrideCursor()

        if os.listdir(install_path) != []:
            os.remove(tar_path)
            done_window()
        else:
            error_window()

    def cancel_button():
        '''Close window'''

        window.close()

    window = QtWidgets.QWidget()
    window.setFixedSize(585, 110)
    window.setWindowTitle('pyFlame Logik Installer %s' % DOT_VERSION)
    window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    window.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    install_label = QtWidgets.QLabel('Install Path: ', window)
    install_label.move(20, 20)

    install_entry = QtWidgets.QLineEdit(install_path, window)
    install_entry.move(100, 18)
    install_entry.resize(330, 21)

    install_browse_btn = QtWidgets.QPushButton('Browse', window)
    install_browse_btn.move(445, 17)
    install_browse_btn.resize(100, 24)
    install_browse_btn.clicked.connect(browse_button)

    install_btn = QtWidgets.QPushButton('Install', window)
    install_btn.move(335, 67)
    install_btn.resize(100, 24)
    install_btn.clicked.connect(install_button)

    cancel_btn = QtWidgets.QPushButton('Cancel', window)
    cancel_btn.move(170, 67)
    cancel_btn.resize(100, 24)
    cancel_btn.clicked.connect(cancel_button)

    window.show()

    return window

def get_main_menu_custom_ui_actions():
    '''Main menu custom action'''

    return [
        {
            'name': 'pyFlame',
            'actions': [
                {
                    'name': 'Logik Installer',
                    'execute': main_window,
                    'minimumVersion': '2020'
                }
            ]
        }
    ]
