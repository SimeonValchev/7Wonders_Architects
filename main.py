import random
import wx


def generate_card(deck):
    rand_int = random.randint(1, 14)
    while deck[rand_int] == 0:
        rand_int = random.randint(1, 14)

    return rand_int


def generate_inv():
    rand_int_inv = random.randint(1, 15)
    while inventions[rand_int_inv] == 0:
        rand_int_inv = random.randint(1, 15)

    inventions[rand_int_inv] = 0
    return rand_int_inv


# MAIN MAIN MAIN
inventions = [0] + [1] * 15
deck_cent = [0] + [10] * 14
deck_left = [0] + [10] * 14
deck_right = [0] + [10] * 14
my_decks = [deck_cent, deck_left, deck_right]

# 0: cent   1: left    2: right
top_cards = [generate_card(my_decks[i]) for i in range(0, 3)]

inv_list = [generate_inv() for i in range(0, 3)]


class Player:
    def __init__(self):
        self.data = [0] * 13
        self.inv = [0] * 15
        self.cat = False


class MyFrame(wx.Frame):

    def draw_invention(self, event):
        x, y = event.GetPosition()
        frame = self.GetSize()
        which_one = -1

        if frame[0] - 480 > x or x > frame[0] - 50 or 50 > y or y > 150:
            return False
        else:
            if frame[0] - 270 > x > frame[0] - 370:
                which_one = 0
            elif frame[0] - 160 > x > frame[0] - 260:
                which_one = 1
            elif frame[0] - 50 > x > frame[0] - 150:
                which_one = 2

        if which_one == -1:
            return False

        inv_list[which_one] = generate_inv()

        dc2 = wx.ClientDC(self.panel)
        dc2.SetBackground(wx.Brush("WHITE"))
        inv_tokens2 = wx.Bitmap('Assets/progress.png', wx.BITMAP_TYPE_PNG)
        dc2.DrawBitmap(
            inv_tokens2.GetSubBitmap((100 * (inv_list[which_one] % 4), 100 * (inv_list[which_one] // 4), 100, 100)),
            self.GetSize()[0] - 370 + 110 * which_one, 50, True)

    def draw_card(self, which_deck):
        deck_index = 0
        if which_deck == 'left':
            deck_index = 1
        elif which_deck == 'right':
            deck_index = 2

        my_decks[deck_index][top_cards[deck_index]] -= 1
        top_cards[deck_index] = generate_card(my_decks[deck_index])
        self.list_buttons[deck_index].SetBitmap(self.cards.GetSubBitmap((100 * top_cards[deck_index], 0, 100, 148)))

    def hover_cent_deck(self, cat, hover):
        if cat:
            if hover:
                self.button_cent.SetBitmap(self.cards.GetSubBitmap((100 * top_cards[0], 0, 100, 148)))
            else:
                self.button_cent.SetBitmap(self.cards.GetSubBitmap((0, 0, 100, 148)))

    def OnPaint(self, event):

        # BASE ICONS
        icons = wx.Bitmap('Assets/main_icons.png', wx.BITMAP_TYPE_PNG)
        peace_icons = wx.Bitmap('Assets/war_icons.png', wx.BITMAP_TYPE_PNG).GetSubBitmap((75, 0, 75, 75))
        inv_tokens = wx.Bitmap('Assets/progress.png', wx.BITMAP_TYPE_PNG)
        inv_image_list = [inv_tokens.GetSubBitmap((100 * (inv_list[i] % 4), 100 * (inv_list[i] // 4), 100, 100)) for i
                          in range(0, 3)]

        # WONDERS
        wonder_leftside = wx.Bitmap('Assets/wonder_babylon.png', wx.BITMAP_TYPE_PNG).GetSubBitmap((0, 0, 350, 318))
        wonder_rightside = wx.Bitmap('Assets/wonder_alexandria.png', wx.BITMAP_TYPE_PNG).GetSubBitmap((0, 0, 350, 472))

        # BACKGROUND
        bg_image = wx.Bitmap('Assets/background.png', wx.BITMAP_TYPE_PNG)
        dc = wx.PaintDC(self.panel)
        panel_size = self.panel.GetSize()

        # Tile the image across the panel
        for x in range(0, panel_size.width, bg_image.GetWidth()):
            for y in range(0, panel_size.height, bg_image.GetHeight()):
                dc.DrawBitmap(bg_image, x, y)

        # PAINTING
        dc.SetBackground(wx.Brush("WHITE"))

        # WONDERS
        dc.DrawBitmap(wonder_leftside, 100, self.GetSize()[1] - 200 - wonder_leftside.GetSize()[1], True)
        dc.DrawBitmap(wonder_rightside, self.GetSize()[0] - 450,
                      self.GetSize()[1] - 200 - wonder_rightside.GetSize()[1], True)

        dc.DrawBitmap(icons, 50, self.GetSize()[1] - 200, True)  #test
        # PEACE ICONS
        for i in range(0, 3):
            dc.DrawBitmap(peace_icons, 143 + i * 85, 63, True)

        # INVENTION TOKENS
        for i, image in enumerate(inv_image_list):
            dc.DrawBitmap(image, self.GetSize()[0] - 370 + 110 * i, 50, True)

        dc.DrawBitmap(wx.Bitmap('Assets/progress.png', wx.BITMAP_TYPE_PNG).GetSubBitmap((0, 0, 100, 100)),
                      self.GetSize()[0] - 480, 50, True)

    def __init__(self, parent, title, decks):
        super(MyFrame, self).__init__(parent, title=title, style=wx.MAXIMIZE)

        frame_size = self.GetSize()
        # [0] - WIDTH - 1538
        # [1] - HEIGHT - 864

        # INIT IMAGE SOURCE for CARDS
        self.cards = wx.Bitmap('Assets/cards_regular.png', wx.BITMAP_TYPE_PNG)

        # INIT IMAGE for TOP CARDS
        card_images = [self.cards.GetSubBitmap((0, 0, 100, 148))]
        for i in range(1, 3):
            card_images.append(self.cards.GetSubBitmap((100 * top_cards[i], 0, 100, 148)))

        self.panel = MyPanel(self)
        #INVENTIONS CLICK
        self.panel.Bind(wx.EVT_LEFT_DOWN, self.draw_invention)

        # BACKGROUND
        self.panel.Bind(wx.EVT_PAINT, self.OnPaint)

        # QUIT BUTTON
        quit_image = wx.Bitmap('Assets/ex.png', wx.BITMAP_TYPE_PNG)
        quit_image_hover = wx.Bitmap('Assets/exq.png', wx.BITMAP_TYPE_PNG)
        button_quit = wx.BitmapButton(self.panel, bitmap=quit_image, style=wx.NO_BORDER, pos=(frame_size[0] - 30, 0))

        button_quit.Bind(wx.EVT_BUTTON, lambda event: self.Close())
        button_quit.Bind(wx.EVT_ENTER_WINDOW, lambda event: button_quit.SetBitmap(quit_image_hover))
        button_quit.Bind(wx.EVT_LEAVE_WINDOW, lambda event: button_quit.SetBitmap(quit_image))

        # INIT DECK-BUTTONS
        self.button_cent = wx.BitmapButton(self.panel, bitmap=card_images[0], style=wx.NO_BORDER,
                                           pos=((frame_size[0] // 2) - 50, 50))
        self.button_left = wx.BitmapButton(self.panel, bitmap=card_images[1], style=wx.NO_BORDER,
                                           pos=((frame_size[0] // 2) - 200, (frame_size[1] // 2) - 25))
        self.button_right = wx.BitmapButton(self.panel, bitmap=card_images[2], style=wx.NO_BORDER,
                                            pos=((frame_size[0] // 2) + 100, (frame_size[1] // 2) - 25))

        self.list_buttons = [self.button_cent, self.button_left, self.button_right]

        # BIND DECK-BUTTONS to FUNCTIONALITY
        self.button_cent.Bind(wx.EVT_BUTTON, lambda event: self.draw_card('cent'))
        self.button_left.Bind(wx.EVT_BUTTON, lambda event: self.draw_card('left'))
        self.button_right.Bind(wx.EVT_BUTTON, lambda event: self.draw_card('right'))

        # BIND HOVERING CENT-DECK for CAT TOTEM FUNCTIONALITY
        self.button_cent.Bind(wx.EVT_ENTER_WINDOW, lambda event: self.hover_cent_deck(True, True))
        self.button_cent.Bind(wx.EVT_LEAVE_WINDOW, lambda event: self.hover_cent_deck(True, False))


class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(parent=None, title="Hello", decks=my_decks)
        frame.ShowFullScreen(True)

        return True


app = MyApp()
app.MainLoop()
