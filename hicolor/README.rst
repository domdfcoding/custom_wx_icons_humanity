**************************************
Hicolor/Gnome Icon Theme for wxPython
**************************************

This package provides a wxPython wxArtProvider class with icons from the Hicolor/Gnome Icon Theme.

To use it in your application:

.. code-block:: python

	from wx_icons_hicolor import wxHicolorIconTheme

	class MyApp(wx.App):
		def OnInit(self):
			wx.ArtProvider.Push(wxHicolorIconTheme())
			self.frame = TestFrame(None, wx.ID_ANY)
			self.SetTopWindow(self.frame)
			self.frame.Show()
			return True

And then the icons can be accessed through wx.ArtProvider:

.. code-block:: python

	wx.ArtProvider.GetBitmap('document-new', wx.ART_OTHER, wx.Size(48, 48))

Any `FreeDesktop Icon Theme Specification <https://specifications.freedesktop.org/icon-naming-spec/icon-naming-spec-latest.html>`_ name can be used.

Currently the `Client ID` is not used, so just pass `wx.ART_OTHER`.
