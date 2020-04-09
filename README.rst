****************
custom_wx_icons
****************

.. image:: https://travis-ci.com/domdfcoding/custom_wx_icons.svg?branch=master
    :target: https://travis-ci.com/domdfcoding/custom_wx_icons
    :alt: Build Status
.. image:: https://readthedocs.org/projects/custom_wx_icons/badge/?version=latest
    :target: https://custom_wx_icons.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

This repository contains a collection of freedesktop-esque icon themes for wxPython.
Each theme provides a custom wx.ArtProvider class that allows the icons to be accessed using icon names from the `FreeDesktop Icon Theme Specification <https://specifications.freedesktop.org/icon-naming-spec/icon-naming-spec-latest.html>`_.

+----------------------+------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------+
|wx_icons_hicolor      | This is the base theme for all other themes.                                       | .. image:: https://img.shields.io/pypi/v/wx_icons_hicolor.svg                           |
|                      | It is based on the                                                                 |    :target: https://pypi.org/project/wx_icons_hicolor/                                  |
|                      | `gnome-icon-theme <https://launchpad.net/gnome-icon-theme>`_.                      |    :alt: PyPI                                                                           |
|                      |                                                                                    | .. image:: https://img.shields.io/pypi/pyversions/wx_icons_hicolor.svg                  |
|                      |                                                                                    |    :target: https://pypi.org/project/wx_icons_hicolor/                                  |
|                      |                                                                                    |    :alt: PyPI - Python Version                                                          |
|                      |                                                                                    | .. image:: https://img.shields.io/pypi/l/wx_icons_hicolor.svg                           |
|                      |                                                                                    |    :target: https://github.com/domdfcoding/custom_wx_icons/blob/master/hicolor/LICENSE  |
|                      |                                                                                    |    :alt: PyPI - License                                                                 |
+----------------------+------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------+
|wx_icons_adwaita      | This theme is based on the                                                         | .. image:: https://img.shields.io/pypi/v/wx_icons_adwaita.svg                           |
|                      | `Adwaita icon theme <https://github.com/GNOME/adwaita-icon-theme>`_                |    :target: https://pypi.org/project/wx_icons_adwaita/                                  |
|                      | version 3.28.                                                                      |    :alt: PyPI                                                                           |
|                      |                                                                                    | .. image:: https://img.shields.io/pypi/pyversions/wx_icons_adwaita.svg                  |
|                      |                                                                                    |    :target: https://pypi.org/project/wx_icons_adwaita/                                  |
|                      |                                                                                    |    :alt: PyPI - Python Version                                                          |
|                      |                                                                                    | .. image:: https://img.shields.io/pypi/l/wx_icons_adwaita.svg                           |
|                      |                                                                                    |    :target: https://github.com/domdfcoding/custom_wx_icons/blob/master/adwaita/LICENSE  |
|                      |                                                                                    |    :alt: PyPI - License                                                                 |
+----------------------+------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------+
|wx_icons_humanity     | This theme is based on the                                                         | .. image:: https://img.shields.io/pypi/v/wx_icons_humanity.svg                          |
|                      | `Humanity icon theme <https://launchpad.net/ubuntu/+source/humanity-icon-theme>`_  |    :target: https://pypi.org/project/wx_icons_humanity/                                 |
|                      | version 0.6.15.                                                                    |    :alt: PyPI                                                                           |
|                      | It also includes the Humanity_Dark theme                                           | .. image:: https://img.shields.io/pypi/pyversions/wx_icons_humanity.svg                 |
|                      |                                                                                    |    :target: https://pypi.org/project/wx_icons_humanity/                                 |
|                      |                                                                                    |    :alt: PyPI - Python Version                                                          |
|                      |                                                                                    | .. image:: https://img.shields.io/pypi/l/wx_icons_humanity.svg                          |
|                      |                                                                                    |    :target: https://github.com/domdfcoding/custom_wx_icons/blob/master/humanity/LICENSE |
|                      |                                                                                    |    :alt: PyPI - License                                                                 |
+----------------------+------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------+
|wx_icons_suru         | This theme is based on the                                                         | .. image:: https://img.shields.io/pypi/v/wx_icons_suru.svg                              |
|                      | `Suru icon theme <https://github.com/ubuntu/yaru/blob/master/icons>`_              |    :target: https://pypi.org/project/wx_icons_suru/                                     |
|                      | version 20.04.4.                                                                   |    :alt: PyPI                                                                           |
|                      |                                                                                    | .. image:: https://img.shields.io/pypi/pyversions/wx_icons_suru.svg                     |
|                      |                                                                                    |    :target: https://pypi.org/project/wx_icons_suru/                                     |
|                      |                                                                                    |    :alt: PyPI - Python Version                                                          |
|                      |                                                                                    | .. image:: https://img.shields.io/pypi/l/wx_icons_suru.svg                              |
|                      |                                                                                    |    :target: https://github.com/domdfcoding/custom_wx_icons/blob/master/suru/LICENSE     |
|                      |                                                                                    |    :alt: PyPI - License                                                                 |
+----------------------+------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------+
|wx_icons_tango        | This theme is based on public domain icons from the Tango Desktop Project          | .. image:: https://img.shields.io/pypi/v/wx_icons_tango.svg                             |
|                      |                                                                                    |    :target: https://pypi.org/project/wx_icons_tango/                                    |
|                      |                                                                                    |    :alt: PyPI                                                                           |
|                      |                                                                                    | .. image:: https://img.shields.io/pypi/pyversions/wx_icons_tango.svg                    |
|                      |                                                                                    |    :target: https://pypi.org/project/wx_icons_tango/                                    |
|                      |                                                                                    |    :alt: PyPI - Python Version                                                          |
|                      |                                                                                    | .. image:: https://img.shields.io/pypi/l/wx_icons_tango.svg                             |
|                      |                                                                                    |    :target: https://github.com/domdfcoding/custom_wx_icons/blob/master/tango/LICENSE    |
|                      |                                                                                    |    :alt: PyPI - License                                                                 |
+----------------------+------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------+

.. .. image:: https://coveralls.io/repos/github/domdfcoding/custom_wx_icons/badge.svg?branch=master
    :target: https://coveralls.io/github/domdfcoding/custom_wx_icons?branch=master
    :alt: Coverage

The individual themes contain instructions on how to use them in your program.