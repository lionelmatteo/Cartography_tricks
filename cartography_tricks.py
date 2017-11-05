# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Cartography_tricks
                                 A QGIS plugin
 Do some tricks for a great cartography
                              -------------------
        begin                : 2017-10-13
        git sha              : $Format:%H$
        copyright            : (C) 2017 by MATTEO Lionel
        email                : matteo@geoazur.unice.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt
from PyQt4.QtGui import QAction, QIcon
from PyQt4 import QtGui, QtCore
# Initialize Qt resources from file resources.py
import resources
import qgis

# Import the code for the DockWidget
from cartography_tricks_dockwidget import Cartography_tricksDockWidget
import os.path

class TestEclipseItem(QtGui.QGraphicsEllipseItem):
    def __init__(self, parent=None):
        QtGui.QGraphicsPixmapItem.__init__(self, parent)

        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)

        # set move restriction rect for the item
        self.move_restrict_rect = QtCore.QRectF(20, 20, 200, 200)
        # set item's rectangle
        self.setRect(QtCore.QRectF(50, 50, 50, 50))

    def mouseMoveEvent(self, event):
        # check of mouse moved within the restricted area for the item
        if self.move_restrict_rect.contains(event.scenePos()):
            QtGui.QGraphicsEllipseItem.mouseMoveEvent(self, event)

class MainForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        scene = QtGui.QGraphicsScene(-50, -50, 600, 600)

        ellipseItem = TestEclipseItem()
        scene.addItem(ellipseItem)

        view = QtGui.QGraphicsView()
        view.setScene(scene)
        view.setGeometry(QtCore.QRect(0, 0, 400, 200))
        self.setCentralWidget(view)

class Cartography_tricks:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Cartography_tricks_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Cartography Tricks')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Cartography_tricks')
        self.toolbar.setObjectName(u'Cartography_tricks')

        #print "** INITIALIZING Cartography_tricks"

        self.pluginIsActive = False
        self.dockwidget = None


    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Cartography_tricks', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToRasterMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/Cartography_tricks/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Artificial sun'),
            callback=self.run,
            parent=self.iface.mainWindow())

    #--------------------------------------------------------------------------

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        #print "** CLOSING Cartography_tricks"

        # disconnects
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)

        # remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        # Commented next statement since it causes QGIS crashe
        # when closing the docked window:
        # self.dockwidget = None

        self.pluginIsActive = False


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        #print "** UNLOAD Cartography_tricks"

        for action in self.actions:
            self.iface.removePluginRasterMenu(
                self.tr(u'&Cartography Tricks'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    #--------------------------------------------------------------------------
    def state_changed(self, int):
        if self.dockwidget.checkBox.isChecked():
            self.Generate_Hillshade()

    def Layer_List(self):
        self.dockwidget.comboBox.clear()
        layers = self.iface.legendInterface().layers()
        layer_list = []
        for layer in layers:
            layer_list.append(layer.name())
        self.dockwidget.comboBox.addItems(layer_list)

        return layers

    def Get_Selected_layer(self, layers):
        # Identify selected layer by its index
        selectedLayerIndex = self.dockwidget.comboBox.currentIndex()
        selectedLayer = layers[selectedLayerIndex]
        return selectedLayer

    def Edit_Slider(self):
        if self.dockwidget.oAzimuth.value() > 180:
            self.dockwidget.dial.setValue(self.dockwidget.oAzimuth.value()-180)
        else:
            self.dockwidget.dial.setValue(self.dockwidget.oAzimuth.value()+180)
        self.dockwidget.verticalSlider.setValue(self.dockwidget.oAltitude.value())
        self.Generate_Hillshade()

    def Edit_Spinbox(self):
        if self.dockwidget.dial.value() > 180:
            self.dockwidget.oAzimuth.setValue(self.dockwidget.dial.value()-180)
        else:
            self.dockwidget.oAzimuth.setValue(self.dockwidget.dial.value()+180)
        self.dockwidget.oAltitude.setValue(self.dockwidget.verticalSlider.value())
        self.Generate_Hillshade()

    def Generate_Hillshade(self):
        if self.dockwidget.checkBox.isChecked():
            Azimuth = self.dockwidget.oAzimuth.value()
            Altitude = self.dockwidget.oAltitude.value()
            selectedLayer = self.Get_Selected_layer(self.iface.legendInterface().layers())
            selectedLayer.setRenderer(qgis.core.QgsHillshadeRenderer(selectedLayer.renderer(), 1, float(Azimuth), float(Altitude)))
            self.iface.mapCanvas().refreshAllLayers()

    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.pluginIsActive:
            self.pluginIsActive = True

            #print "** STARTING Cartography_tricks"

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget == None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = Cartography_tricksDockWidget()

            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)

            # show the dockwidget
            # TODO: fix to allow choice of dock location
            self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dockwidget)

            self.Layer_List()
            # update the comboBox item list when the current layer change (useful when add a new layer)
            self.iface.legendInterface().currentLayerChanged.connect(self.Layer_List)

            self.dockwidget.checkBox.stateChanged.connect(self.state_changed)
            self.dockwidget.oAzimuth.valueChanged.connect(self.Edit_Slider)
            self.dockwidget.oAltitude.valueChanged.connect(self.Edit_Slider)
            self.dockwidget.dial.valueChanged.connect(self.Edit_Spinbox)
            self.dockwidget.verticalSlider.valueChanged.connect(self.Edit_Spinbox)

            self.dockwidget.show()

