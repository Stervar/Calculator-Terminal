import wx

class MyApp(wx.App):
    def OnInit(self):
        self.frame = wx.Frame(None, title='wxPython Калькулятор', size=(300, 200))
        panel = wx.Panel(self.frame)

        button = wx.Button(panel, label='Нажми меня', pos=(100, 50))
        button.Bind(wx.EVT_BUTTON, self.on_button_click)

        self.frame.Show()
        return True

    def on_button_click(self, event):
        wx.MessageBox('Кнопка нажата!', 'Информация', wx.OK | wx.ICON_INFORMATION)

if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()