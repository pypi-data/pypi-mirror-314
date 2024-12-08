import webbrowser

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QMainWindow,
    QToolBar,
    QHBoxLayout,
    QDialog,
    QWidgetAction,
    QSpinBox,
    QWidget,
    QApplication,
    QSizePolicy,
    QStackedWidget,
    QMenu,
    QSystemTrayIcon,
    QMessageBox,
)

from pyqt_openai import (
    DEFAULT_SHORTCUT_FULL_SCREEN,
    APP_INITIAL_WINDOW_SIZE,
    DEFAULT_APP_NAME,
    DEFAULT_APP_ICON,
    ICON_STACKONTOP,
    ICON_CUSTOMIZE,
    ICON_FULLSCREEN,
    ICON_CLOSE,
    DEFAULT_SHORTCUT_SETTING,
    TRANSPARENT_RANGE,
    TRANSPARENT_INIT_VAL,
    ICON_GITHUB,
    ICON_DISCORD,
    PAYPAL_URL,
    KOFI_URL,
    DISCORD_URL,
    GITHUB_URL,
    DEFAULT_SHORTCUT_FOCUS_MODE,
    ICON_FOCUS_MODE,
    ICON_SETTING,
    DEFAULT_SHORTCUT_SHOW_SECONDARY_TOOLBAR,
    DEFAULT_SHORTCUT_STACK_ON_TOP,
    ICON_PAYPAL,
    ICON_KOFI,
    ICON_PATREON,
    PATREON_URL,
    ICON_UPDATE,
    ICON_SHORTCUT,
)
from pyqt_openai.aboutDialog import AboutDialog
from pyqt_openai.chat_widget.chatMainWidget import ChatMainWidget
from pyqt_openai.config_loader import CONFIG_MANAGER
from pyqt_openai.customizeDialog import CustomizeDialog
from pyqt_openai.dalle_widget.dalleMainWidget import DallEMainWidget
from pyqt_openai.doNotAskAgainDialog import DoNotAskAgainDialog
from pyqt_openai.g4f_image_widget.g4fImageMainWidget import G4FImageMainWidget
from pyqt_openai.lang.translations import LangClass
from pyqt_openai.models import SettingsParamsContainer, CustomizeParamsContainer
from pyqt_openai.replicate_widget.replicateMainWidget import ReplicateMainWidget
from pyqt_openai.settings_dialog.settingsDialog import SettingsDialog
from pyqt_openai.shortcutDialog import ShortcutDialog
from pyqt_openai.updateSoftwareDialog import update_software
from pyqt_openai.util.common import (
    restart_app,
    show_message_box_after_change_to_restart,
    set_auto_start_windows,
    init_llama, set_api_key,
)
from pyqt_openai.widgets.navWidget import NavBar


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__settingsParamContainer = SettingsParamsContainer()
        self.__customizeParamsContainer = CustomizeParamsContainer()

        self.__initContainer(self.__settingsParamContainer)
        self.__initContainer(self.__customizeParamsContainer)

    def __initUi(self):
        self.setWindowTitle(DEFAULT_APP_NAME)

        self.__chatMainWidget = ChatMainWidget(self)
        self.__dallEWidget = DallEMainWidget(self)
        self.__replicateWidget = ReplicateMainWidget(self)
        self.__g4fImageWidget = G4FImageMainWidget(self)

        self.__mainWidget = QStackedWidget()
        self.__mainWidget.addWidget(self.__chatMainWidget)
        self.__mainWidget.addWidget(self.__dallEWidget)
        self.__mainWidget.addWidget(self.__replicateWidget)
        self.__mainWidget.addWidget(self.__g4fImageWidget)

        self.__setActions()
        self.__setMenuBar()
        self.__setTrayMenu()
        self.__setToolBar()

        self.__loadApiKeys()

        self.setCentralWidget(self.__mainWidget)
        self.resize(*APP_INITIAL_WINDOW_SIZE)

        self.__refreshColumns()
        self.__chatMainWidget.refreshCustomizedInformation(
            self.__customizeParamsContainer
        )

    def __loadApiKeys(self):
        set_api_key('OPENAI_API_KEY', CONFIG_MANAGER.get_general_property('OPENAI_API_KEY'))
        set_api_key('REPLICATE_API_KEY', CONFIG_MANAGER.get_general_property('REPLICATE_API_KEY'))
        init_llama()

    def __setActions(self):
        self.__langAction = QAction()

        # menu action
        self.__exitAction = QAction(LangClass.TRANSLATIONS["Exit"], self)
        self.__exitAction.triggered.connect(self.__beforeClose)

        self.__stackAction = QAction(LangClass.TRANSLATIONS["Stack on Top"], self)
        self.__stackAction.setShortcut(DEFAULT_SHORTCUT_STACK_ON_TOP)
        self.__stackAction.setIcon(QIcon(ICON_STACKONTOP))
        self.__stackAction.setCheckable(True)
        self.__stackAction.toggled.connect(self.__stackToggle)

        self.__showSecondaryToolBarAction = QAction(
            LangClass.TRANSLATIONS["Show Secondary Toolbar"], self
        )
        self.__showSecondaryToolBarAction.setShortcut(
            DEFAULT_SHORTCUT_SHOW_SECONDARY_TOOLBAR
        )
        self.__showSecondaryToolBarAction.setCheckable(True)
        self.__showSecondaryToolBarAction.setChecked(
            CONFIG_MANAGER.get_general_property("show_secondary_toolbar")
        )
        self.__showSecondaryToolBarAction.toggled.connect(self.__toggleSecondaryToolBar)

        self.__focusModeAction = QAction(LangClass.TRANSLATIONS["Focus Mode"], self)
        self.__focusModeAction.setShortcut(DEFAULT_SHORTCUT_FOCUS_MODE)
        self.__focusModeAction.setIcon(QIcon(ICON_FOCUS_MODE))
        self.__focusModeAction.setCheckable(True)
        self.__focusModeAction.setChecked(
            CONFIG_MANAGER.get_general_property("focus_mode")
        )
        self.__focusModeAction.triggered.connect(self.__activateFocusMode)

        self.__fullScreenAction = QAction(LangClass.TRANSLATIONS["Full Screen"], self)
        self.__fullScreenAction.setShortcut(DEFAULT_SHORTCUT_FULL_SCREEN)
        self.__fullScreenAction.setIcon(QIcon(ICON_FULLSCREEN))
        self.__fullScreenAction.setCheckable(True)
        self.__fullScreenAction.setChecked(False)
        self.__fullScreenAction.triggered.connect(self.__fullScreenToggle)

        self.__aboutAction = QAction(LangClass.TRANSLATIONS["About..."], self)
        self.__aboutAction.setIcon(QIcon(DEFAULT_APP_ICON))
        self.__aboutAction.triggered.connect(self.__showAboutDialog)

        # TODO LANGAUGE
        self.__checkUpdateAction = QAction(
            LangClass.TRANSLATIONS["Check for Updates..."], self
        )
        self.__checkUpdateAction.setIcon(QIcon(ICON_UPDATE))
        self.__checkUpdateAction.triggered.connect(self.__checkUpdate)

        self.__viewShortcutsAction = QAction(
            LangClass.TRANSLATIONS["View Shortcuts"], self
        )
        self.__viewShortcutsAction.setIcon(QIcon(ICON_SHORTCUT))
        self.__viewShortcutsAction.triggered.connect(self.__showShortcutsDialog)

        self.__githubAction = QAction("Github", self)
        self.__githubAction.setIcon(QIcon(ICON_GITHUB))
        self.__githubAction.triggered.connect(lambda: webbrowser.open(GITHUB_URL))

        self.__discordAction = QAction("Discord", self)
        self.__discordAction.setIcon(QIcon(ICON_DISCORD))
        self.__discordAction.triggered.connect(lambda: webbrowser.open(DISCORD_URL))

        self.__paypalAction = QAction("Paypal", self)
        self.__paypalAction.setIcon(QIcon(ICON_PAYPAL))
        self.__paypalAction.triggered.connect(lambda: webbrowser.open(PAYPAL_URL))

        self.__kofiAction = QAction("Ko-fi ❤", self)
        self.__kofiAction.setIcon(QIcon(ICON_KOFI))
        self.__kofiAction.triggered.connect(lambda: webbrowser.open(KOFI_URL))

        self.__patreonAction = QAction("Patreon", self)
        self.__patreonAction.setIcon(QIcon(ICON_PATREON))
        self.__patreonAction.triggered.connect(lambda: webbrowser.open(PATREON_URL))

        self.__navBar = NavBar()
        self.__navBar.add(LangClass.TRANSLATIONS["Chat"])
        self.__navBar.add("DALL-E")
        self.__navBar.add("Replicate")
        self.__navBar.add("G4F Image")
        self.__navBar.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred
        )
        self.__navBar.itemClicked.connect(self.__aiTypeChanged)

        # Chat is the default widget
        self.__navBar.setActiveButton(0)

        # toolbar action
        self.__chooseAiAction = QWidgetAction(self)
        self.__chooseAiAction.setDefaultWidget(self.__navBar)

        self.__customizeAction = QAction(self)
        self.__customizeAction.setText(LangClass.TRANSLATIONS["Customize"])
        self.__customizeAction.setIcon(QIcon(ICON_CUSTOMIZE))
        self.__customizeAction.triggered.connect(self.__executeCustomizeDialog)

        self.__transparentAction = QWidgetAction(self)
        self.__transparentSpinBox = QSpinBox()
        self.__transparentSpinBox.setRange(*TRANSPARENT_RANGE)
        self.__transparentSpinBox.setValue(TRANSPARENT_INIT_VAL)
        self.__transparentSpinBox.valueChanged.connect(self.__setTransparency)
        self.__transparentSpinBox.setToolTip(
            LangClass.TRANSLATIONS["Set Transparency of Window"]
        )
        self.__transparentSpinBox.setMinimumWidth(100)

        lay = QHBoxLayout()
        lay.addWidget(self.__transparentSpinBox)

        transparencyActionWidget = QWidget(self)
        transparencyActionWidget.setLayout(lay)
        self.__transparentAction.setDefaultWidget(transparencyActionWidget)

        self.__settingsAction = QAction(self)
        self.__settingsAction.setText(LangClass.TRANSLATIONS["Settings"])
        self.__settingsAction.setIcon(QIcon(ICON_SETTING))
        self.__settingsAction.setShortcut(DEFAULT_SHORTCUT_SETTING)
        self.__settingsAction.triggered.connect(self.__showSettingsDialog)

    def __fullScreenToggle(self, f):
        if f:
            self.showFullScreen()
        else:
            self.showNormal()

    def __activateFocusMode(self, f):
        f = not f
        # Toggle GUI
        for i in range(self.__mainWidget.count()):
            currentWidget = self.__mainWidget.widget(i)
            currentWidget.showSecondaryToolBar(f)
            currentWidget.toggleButtons(f)
        self.__toggleSecondaryToolBar(f)

        # Toggle container
        self.__settingsParamContainer.show_secondary_toolbar = f
        CONFIG_MANAGER.set_general_property("focus_mode", not f)

    def __setMenuBar(self):
        menubar = self.menuBar()

        fileMenu = QMenu(LangClass.TRANSLATIONS["File"], self)
        fileMenu.addAction(self.__settingsAction)
        fileMenu.addAction(self.__exitAction)

        viewMenu = QMenu(LangClass.TRANSLATIONS["View"], self)
        viewMenu.addAction(self.__focusModeAction)
        viewMenu.addAction(self.__fullScreenAction)
        viewMenu.addAction(self.__stackAction)
        viewMenu.addAction(self.__showSecondaryToolBarAction)

        helpMenu = QMenu(LangClass.TRANSLATIONS["Help"], self)
        helpMenu.addAction(self.__aboutAction)
        helpMenu.addAction(self.__checkUpdateAction)
        helpMenu.addAction(self.__viewShortcutsAction)
        helpMenu.addAction(self.__githubAction)
        helpMenu.addAction(self.__discordAction)

        donateMenu = QMenu(LangClass.TRANSLATIONS["Donate"], self)
        donateMenu.addAction(self.__paypalAction)
        donateMenu.addAction(self.__kofiAction)
        donateMenu.addAction(self.__patreonAction)

        menubar.addMenu(fileMenu)
        menubar.addMenu(viewMenu)
        menubar.addMenu(helpMenu)
        menubar.addMenu(donateMenu)

    def __setTrayMenu(self):
        # background app
        menu = QMenu()
        app = QApplication.instance()

        action = QAction("Quit", self)
        action.setIcon(QIcon(ICON_CLOSE))

        action.triggered.connect(app.quit)

        menu.addAction(action)

        tray_icon = QSystemTrayIcon(app)
        tray_icon.setIcon(QIcon(DEFAULT_APP_ICON))
        tray_icon.activated.connect(self.__activated)

        tray_icon.setContextMenu(menu)

        tray_icon.show()

    def __activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show()

    def __setToolBar(self):
        self.__toolbar = QToolBar()
        self.__toolbar.addAction(self.__chooseAiAction)
        self.__toolbar.addAction(self.__showSecondaryToolBarAction)
        self.__toolbar.addAction(self.__fullScreenAction)
        self.__toolbar.addAction(self.__stackAction)
        self.__toolbar.addAction(self.__focusModeAction)
        self.__toolbar.addAction(self.__settingsAction)
        self.__toolbar.addAction(self.__checkUpdateAction)
        self.__toolbar.addAction(self.__customizeAction)
        self.__toolbar.addAction(self.__githubAction)
        self.__toolbar.addAction(self.__discordAction)
        self.__toolbar.addAction(self.__paypalAction)
        self.__toolbar.addAction(self.__kofiAction)
        self.__toolbar.addAction(self.__patreonAction)
        self.__toolbar.addAction(self.__aboutAction)
        self.__toolbar.addAction(self.__viewShortcutsAction)
        self.__toolbar.addAction(self.__transparentAction)
        self.__toolbar.setMovable(False)

        self.addToolBar(self.__toolbar)

        # QToolbar's layout can't be set spacing with lay.setSpacing so i've just did this instead
        self.__toolbar.setStyleSheet("QToolBar { spacing: 2px; }")

        for i in range(self.__mainWidget.count()):
            currentWidget = self.__mainWidget.widget(i)
            currentWidget.showSecondaryToolBar(
                self.__settingsParamContainer.show_secondary_toolbar
            )

    def __showAboutDialog(self):
        aboutDialog = AboutDialog(self)
        aboutDialog.exec()

    def __checkUpdate(self):
        update_software()

    def __showShortcutsDialog(self):
        shortcutListWidget = ShortcutDialog(self)
        shortcutListWidget.exec()

    def __stackToggle(self, f):
        if f:
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        else:
            # Qt.WindowType.WindowCloseButtonHint is added to prevent the close button get deactivated
            self.setWindowFlags(
                self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint
                | Qt.WindowType.WindowCloseButtonHint
            )
        self.show()

    def __setTransparency(self, v):
        self.setWindowOpacity(v / 100)

    def __toggleSecondaryToolBar(self, f):
        self.__showSecondaryToolBarAction.setChecked(f)
        self.__mainWidget.currentWidget().showSecondaryToolBar(f)
        self.__settingsParamContainer.show_secondary_toolbar = f

    def __executeCustomizeDialog(self):
        dialog = CustomizeDialog(self.__customizeParamsContainer, parent=self)
        reply = dialog.exec()
        if reply == QDialog.DialogCode.Accepted:
            container = dialog.getParam()
            self.__customizeParamsContainer = container
            self.__refreshContainer(container)
            self.__chatMainWidget.refreshCustomizedInformation(container)

    def __aiTypeChanged(self, i):
        self.__mainWidget.setCurrentIndex(i)
        self.__navBar.setActiveButton(i)
        widget = self.__mainWidget.currentWidget()
        widget.showSecondaryToolBar(
            self.__settingsParamContainer.show_secondary_toolbar
        )

    def __initContainer(self, container):
        """
        Initialize the container with the values in the settings file
        """
        for k, v in container.get_items():
            setattr(container, k, CONFIG_MANAGER.get_general_property(k))
        if isinstance(container, SettingsParamsContainer):
            self.__lang = LangClass.lang_changed(container.lang)
            set_auto_start_windows(container.run_at_startup)

    def __refreshContainer(self, container):
        if isinstance(container, SettingsParamsContainer):
            prev_db = CONFIG_MANAGER.get_general_property("db")
            prev_show_secondary_toolbar = CONFIG_MANAGER.get_general_property(
                "show_secondary_toolbar"
            )
            prev_show_as_markdown = CONFIG_MANAGER.get_general_property(
                "show_as_markdown"
            )
            prev_run_at_startup = CONFIG_MANAGER.get_general_property("run_at_startup")

            for k, v in container.get_items():
                CONFIG_MANAGER.set_general_property(k, v)

            # If db name is changed
            if container.db != prev_db:
                QMessageBox.information(
                    self,
                    LangClass.TRANSLATIONS["Info"],
                    LangClass.TRANSLATIONS[
                        "The name of the reference target database has been changed. The changes will take effect after a restart."
                    ],
                )
            if container.run_at_startup != prev_run_at_startup:
                set_auto_start_windows(container.run_at_startup)
            # If show_secondary_toolbar is changed
            if container.show_secondary_toolbar != prev_show_secondary_toolbar:
                for i in range(self.__mainWidget.count()):
                    currentWidget = self.__mainWidget.widget(i)
                    currentWidget.showSecondaryToolBar(container.show_secondary_toolbar)
            # If properties that require a restart are changed
            if (
                container.lang != self.__lang
                or container.show_as_markdown != prev_show_as_markdown
            ):
                change_list = []
                if container.lang != self.__lang:
                    change_list.append(LangClass.TRANSLATIONS["Language"])
                if container.show_as_markdown != prev_show_as_markdown:
                    change_list.append(LangClass.TRANSLATIONS["Show as Markdown"])
                result = show_message_box_after_change_to_restart(change_list)
                if result == QMessageBox.StandardButton.Yes:
                    restart_app()

        elif isinstance(container, CustomizeParamsContainer):
            prev_font_family = CONFIG_MANAGER.get_general_property("font_family")
            prev_font_size = CONFIG_MANAGER.get_general_property("font_size")

            for k, v in container.get_items():
                CONFIG_MANAGER.set_general_property(k, v)

            if (
                container.font_family != prev_font_family
                or container.font_size != prev_font_size
            ):
                change_list = [
                    LangClass.TRANSLATIONS["Font Change"],
                ]
                result = show_message_box_after_change_to_restart(change_list)
                if result == QMessageBox.StandardButton.Yes:
                    restart_app()

    def __refreshColumns(self):
        self.__chatMainWidget.setColumns(
            self.__settingsParamContainer.chat_column_to_show
        )
        image_column_to_show = self.__settingsParamContainer.image_column_to_show
        if image_column_to_show.__contains__("data"):
            image_column_to_show.remove("data")
        self.__dallEWidget.setColumns(
            self.__settingsParamContainer.image_column_to_show
        )
        self.__replicateWidget.setColumns(
            self.__settingsParamContainer.image_column_to_show
        )

    def __showSettingsDialog(self):
        dialog = SettingsDialog(parent=self)
        reply = dialog.exec()
        if reply == QDialog.DialogCode.Accepted:
            container = dialog.getParam()
            self.__settingsParamContainer = container
            self.__refreshContainer(container)
            self.__refreshColumns()

    def __doNotAskAgainChanged(self, value):
        self.__settingsParamContainer.do_not_ask_again = value
        self.__refreshContainer(self.__settingsParamContainer)

    def __beforeClose(self):
        if self.__settingsParamContainer.do_not_ask_again:
            app = QApplication.instance()
            app.quit()
        else:
            # Show a message box to confirm the exit or cancel or running in the background
            dialog = DoNotAskAgainDialog(
                self.__settingsParamContainer.do_not_ask_again, parent=self
            )
            dialog.doNotAskAgainChanged.connect(self.__doNotAskAgainChanged)
            reply = dialog.exec()
            if dialog.isCancel():
                return True
            else:
                if reply == QDialog.DialogCode.Accepted:
                    app = QApplication.instance()
                    app.quit()
                elif reply == QDialog.DialogCode.Rejected:
                    self.close()

    def closeEvent(self, event):
        f = self.__beforeClose()
        if f:
            event.ignore()
        else:
            return super().closeEvent(event)
