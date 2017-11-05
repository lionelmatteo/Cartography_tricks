# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Cartography_tricks
                                 A QGIS plugin
 Do some tricks for a great cartography
                             -------------------
        begin                : 2017-10-13
        copyright            : (C) 2017 by MATTEO Lionel
        email                : matteo@geoazur.unice.fr
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Cartography_tricks class from file Cartography_tricks.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .cartography_tricks import Cartography_tricks
    return Cartography_tricks(iface)
