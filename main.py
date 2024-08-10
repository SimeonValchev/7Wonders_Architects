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


def next_turn_checker():
    global at_turn
    if list(flags.values()) == [0, 0, 0]:
        at_turn = (at_turn + 1) % 2
        flags['draw'] = 1


# MAIN MAIN MAIN
inventions = [0] + [1] * 15
deck_cent = [0] + [10] * 14
deck_left = [0] + [10] * 14
deck_right = [0] + [10] * 14
my_decks = {'cent': deck_cent, 'left': deck_left, 'right': deck_right}

top_cards = {'cent': generate_card(my_decks['cent']), 'left': generate_card(my_decks['left']),
             'right': generate_card(my_decks['right'])}

inv_list = [generate_inv() for i in range(0, 3)]


class Player:
    def __init__(self):
        self.data = [0] * 13
        self.inv = [0] * 15
        self.score = 0
        self.cat = False


at_turn = 0
player = [Player(), Player()]
flags = {'build': 0, 'draw': 1, 'inv': 0}

class MyFrame(wx.Frame):

    def handle_resource(self, id):
        res_client = wx.ClientDC(self.panel)
        res_client.SetBackground(wx.Brush("WHITE"))
        player[at_turn].data[id - 1] += 1

        coords = [0, self.GetSize()[1] - 200]
        if at_turn == 0:
            coords[0] = (58 * id) - 16
        else:
            coords[0] = (self.GetSize()[0] - 492) + (58 * id) - 58

        res_client.DrawBitmap(self.icons.GetSubBitmap((58 * (id - 1), 0, 58, 58)), coords[0], coords[1])
        if player[at_turn].data[id - 1] > 1:
            res_client.DrawCircle(coords[0] + 50, coords[1] + 50, 10)
            res_client.DrawText(str(player[at_turn].data[id - 1]), coords[0] + 47, coords[1] + 43)

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

        temp_card = top_cards[which_deck]
        if temp_card <= 6:
            self.handle_resource(temp_card)

        # UPDATE DECK
        my_decks[which_deck][top_cards[which_deck]] -= 1
        top_cards[which_deck] = generate_card(my_decks[which_deck])
        self.list_buttons[which_deck].SetBitmap(self.cards.GetSubBitmap((100 * top_cards[which_deck], 0, 100, 148)))

        flags['draw'] -= 1
        next_turn_checker()

    def hover_cent_deck(self, cat, hover):

        if cat:
            if hover:
                self.button_cent.SetBitmap(self.cards.GetSubBitmap((100 * top_cards['cent'], 0, 100, 148)))
            else:
                self.button_cent.SetBitmap(self.cards.GetSubBitmap((0, 0, 100, 148)))

    def OnPaint(self, event):

        # HOLDS THE BITMAPS OF THE INITIAL 3 INVENTIONS
        inv_image_list = [self.inv_tokens.GetSubBitmap((100 * (inv_list[i] % 4), 100 * (inv_list[i] // 4), 100, 100))
                          for i in range(0, 3)]

        # BACKGROUND
        bg_image = wx.Bitmap('Assets/background.png', wx.BITMAP_TYPE_PNG)
        dc = wx.PaintDC(self.panel)
        panel_size = self.panel.GetSize()

        # TILE THE BACKGROUND
        for x in range(0, panel_size.width, bg_image.GetWidth()):
            for y in range(0, panel_size.height, bg_image.GetHeight()):
                dc.DrawBitmap(bg_image, x, y)

        # does nothing? can be removed perhaps?
        dc.SetBackground(wx.Brush("WHITE"))

        # WONDERS
        temp_left = self.wonder_leftside.GetSubBitmap((0, 0, 350, 318))
        temp_right = self.wonder_rightside.GetSubBitmap((0, 0, 350, 472))
        dc.DrawBitmap(temp_left, 100, self.GetSize()[1] - 200 - temp_left.GetSize()[1], True)
        dc.DrawBitmap(temp_right, self.GetSize()[0] - 450, self.GetSize()[1] - 200 - temp_right.GetSize()[1], True)

        # PEACE ICONS
        for i in range(0, 3):
            dc.DrawBitmap(self.war_icons.GetSubBitmap((75, 0, 75, 75)), 143 + i * 85, 63, True)

        # INVENTION TOKENS
        for i, image in enumerate(inv_image_list):
            dc.DrawBitmap(image, self.GetSize()[0] - 370 + 110 * i, 50, True)

        # MYSTERY TOKEN
        dc.DrawBitmap(self.inv_tokens.GetSubBitmap((0, 0, 100, 100)), self.GetSize()[0] - 480, 50, True)

    # DEFINING MAIN FRAME
    def __init__(self, parent, title, decks):
        super(MyFrame, self).__init__(parent, title=title, style=wx.MAXIMIZE)

        # LOADING ASSETS
        quit_image = wx.Bitmap('Assets/ex.png', wx.BITMAP_TYPE_PNG)
        quit_image_hover = wx.Bitmap('Assets/exq.png', wx.BITMAP_TYPE_PNG)
        self.icons = wx.Bitmap('Assets/main_icons.png', wx.BITMAP_TYPE_PNG)
        self.cards = wx.Bitmap('Assets/cards_regular.png', wx.BITMAP_TYPE_PNG)
        self.war_icons = wx.Bitmap('Assets/war_icons.png', wx.BITMAP_TYPE_PNG)
        self.inv_tokens = wx.Bitmap('Assets/progress.png', wx.BITMAP_TYPE_PNG)

        #subject to future change
        self.wonder_leftside = wx.Bitmap('Assets/wonder_babylon.png', wx.BITMAP_TYPE_PNG)
        self.wonder_rightside = wx.Bitmap('Assets/wonder_alexandria.png', wx.BITMAP_TYPE_PNG)

        frame_size = self.GetSize()
        # [0] - WIDTH - 1538
        # [1] - HEIGHT - 864

        self.panel = MyPanel(self)

        #INVENTIONS CLICK
        self.panel.Bind(wx.EVT_LEFT_DOWN, self.draw_invention)

        # BACKGROUND
        self.panel.Bind(wx.EVT_PAINT, self.OnPaint)

        # QUIT BUTTON
        button_quit = wx.BitmapButton(self.panel, bitmap=quit_image, style=wx.NO_BORDER, pos=(frame_size[0] - 30, 0))

        button_quit.Bind(wx.EVT_BUTTON, lambda event: self.Close())
        button_quit.Bind(wx.EVT_ENTER_WINDOW, lambda event: button_quit.SetBitmap(quit_image_hover))
        button_quit.Bind(wx.EVT_LEAVE_WINDOW, lambda event: button_quit.SetBitmap(quit_image))

        # INIT IMAGE for TOP CARDS
        card_images = [self.cards.GetSubBitmap((0, 0, 100, 148))]
        for id in ['left', 'right']:
            card_images.append(self.cards.GetSubBitmap((100 * top_cards[id], 0, 100, 148)))

        # INIT DECK-BUTTONS with TOP CARDS
        self.button_cent = wx.BitmapButton(self.panel, bitmap=card_images[0], style=wx.NO_BORDER,
                                           pos=((frame_size[0] // 2) - 50, 50))
        self.button_left = wx.BitmapButton(self.panel, bitmap=card_images[1], style=wx.NO_BORDER,
                                           pos=((frame_size[0] // 2) - 200, (frame_size[1] // 2) - 25))
        self.button_right = wx.BitmapButton(self.panel, bitmap=card_images[2], style=wx.NO_BORDER,
                                            pos=((frame_size[0] // 2) + 100, (frame_size[1] // 2) - 25))

        self.list_buttons = {'cent': self.button_cent, 'left': self.button_left, 'right': self.button_right}

        # BIND DECK-BUTTONS to FUNCTIONALITY
        self.button_cent.Bind(wx.EVT_BUTTON, lambda event: self.draw_card('cent'))
        self.button_left.Bind(wx.EVT_BUTTON, lambda event: self.draw_card('left'))
        self.button_right.Bind(wx.EVT_BUTTON, lambda event: self.draw_card('right'))

        # BIND HOVERING CENT-DECK for CAT TOTEM FUNCTIONALITY
        self.button_cent.Bind(wx.EVT_ENTER_WINDOW, lambda event: self.hover_cent_deck(True, True))
        self.button_cent.Bind(wx.EVT_LEAVE_WINDOW, lambda event: self.hover_cent_deck(True, False))

        # LABEL TEST
        #self.label = wx.StaticText(self.panel, label='hallo', size=(50,20))


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
