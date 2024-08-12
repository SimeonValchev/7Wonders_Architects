import random
import wx
import time


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
deck_left = [0] + [10]*6 + [0] * 14
deck_right = [0] + [10] * 14
my_decks = {'cent': deck_cent, 'left': deck_left, 'right': deck_right}

top_cards = {'cent': generate_card(my_decks['cent']), 'left': generate_card(my_decks['left']),
             'right': generate_card(my_decks['right'])}

inv_list = [generate_inv() for i in range(0, 3)]
war = 0
traded_tools = [0] * 3
traded_res = [0] * 6
to_build = -1


class Player:
    def __init__(self, name):
        self.wonder = name
        self.can_build_stage = [0, -1]
        self.wonder_point = [0] * 5
        self.counter_stages = 0

        self.data = [0] * 14
        self.inv = [0] + [0] * 15
        self.score = 0
        self.cat = False
        self.can_use_cat = False

        if name == 'alexandria':
            self.wonder_point = [4, 3, 6, 5, 7]
        elif name == 'babylon':
            self.wonder_point = [3, 0, 5, 5, 7]

        if name == 'rhodes':
            self.can_build_stage[1] = 1
        elif name == 'artemis':
            self.can_build_stage = [0, -1, -1]


at_turn = 0
player = [Player('babylon'), Player('alexandria')]
flags = {'build': 0, 'draw': 1, 'inv': 0}


class MyFrame(wx.Frame):

    def end_game(self):
        score_0 = player[0].data[6]*2 + player[0].data[7]*3 + player[0].data[13]*3 + player[0].score
        score_1 = player[1].data[6]*2 + player[1].data[7]*3 + player[1].data[13]*3 + player[1].score

        text0 = wx.StaticText(self.panel, label=str(score_0), pos=(100, self.GetSize()[1] - 200 - self.wonder_leftside.GetSize()[1]//3))
        text1 = wx.StaticText(self.panel, label=str(score_1), pos=(self.GetSize()[0] - 450, self.GetSize()[1] - 200 - self.wonder_rightside.GetSize()[1]//3))

        font = text0.GetFont()
        font.SetPointSize(20)
        text0.SetFont(font)
        text1.SetFont(font)

        flags['build'] = -1
        flags['draw'] = -1
        flags['inv'] = -1

    def war_update(self, horns):
        global war
        temp_client = wx.ClientDC(self.panel)
        unupdated_war = war
        war += horns

        # UPDATE VISUAL TOKENS
        for i in range(unupdated_war, min(war, 3)):
            temp_client.DrawBitmap(self.war_icons.GetSubBitmap((0, 0, 75, 75)), 143 + i * 85, 63, True)

        if war >= 3:
            war = 0
            time.sleep(1)

            # CALCULATE WINNER
            p0_war = max(player[0].data[8] + player[0].data[9], 1)
            p1_war = max(player[1].data[8] + player[1].data[9], 1)

            total = 0
            winner = -1
            temp_coords = [0, self.GetSize()[1] - 142]
            if p0_war == p1_war:
                winner = 0
            elif p0_war > p1_war:
                total = 1 + min((p0_war - p1_war) // p1_war, 1)
                temp_coords[0] = 448
                winner = 0
            else:
                total = 1 + min((p1_war - p0_war) // p0_war, 1)
                temp_coords[0] = self.GetSize()[0] - 86
                winner = 1

            # BACKEND UPDATE
            player[winner].data[13] += total
            player[0].data[9] = 0
            player[1].data[9] = 0

            # VISUAL UPDATE
            temp_client.DrawBitmap(self.blank_tile, 448, self.GetSize()[1] - 200)
            temp_client.DrawBitmap(self.blank_tile, self.GetSize()[0] - 86, self.GetSize()[1] - 200)

            if total != 0:
                temp_client.DrawBitmap(self.bonus_icons.GetSubBitmap((0, 0, 58, 58)), temp_coords[0], temp_coords[1])
                if player[winner].data[13] > 1:
                    temp_client.DrawCircle(temp_coords[0] + 50, temp_coords[1] + 50, 10)
                    temp_client.DrawText(str(player[winner].data[13]), temp_coords[0] + 47, temp_coords[1] + 43)

            time.sleep(1)
            # PEACE TOKENS RESET
            for i in range(0, 3):
                temp_client.DrawBitmap(self.war_icons.GetSubBitmap((75, 0, 75, 75)), 143 + i * 85, 63, True)

    def inv_update(self):
        c1 = 0
        c2 = 0
        exert = player[at_turn].data[10:13]
        if exert[0] == exert[1] == exert[2]:
            c1 = exert[0]
        for i in exert:
            c2 += i // 2

        flags['inv'] = max(c1, c2)

    def resource_update(self):
        res_exert = player[at_turn].data[:6]
        count_unique = 0
        count_max_same = 0

        for i in range(5):
            if res_exert[i] > 0:
                count_unique += 1
                count_max_same = max(count_max_same, res_exert[i])

        count_unique += res_exert[5]
        count_max_same += res_exert[5]

        for int in player[at_turn].can_build_stage:
            if int == -1:
                continue

            if ((int == 0 and count_unique >= 2) or
                    (int == 1 and count_max_same >= 2) or
                    (int == 2 and count_unique >= 3) or
                    (int == 3 and count_max_same >= 3) or
                    (int == 4 and count_unique >= 4)):
                flags['build'] = 1
                self.builders[at_turn].Show()

    def builder_click(self):
        global to_build
        global traded_res
        exert = player[at_turn].data[:6]
        self.open_res_dialog(exert)

        # UPDATE PLAYER DATA
        for i in range(6):
            player[at_turn].data[i] -= traded_res[i]

        if player[at_turn].wonder in ['alexandria', 'gizeh']:
            player[at_turn].can_build_stage[0] = to_build + 1
        elif player[at_turn].wonder == 'babylon':
            if to_build < 2:
                player[at_turn].can_build_stage[0] = to_build + 1
            elif to_build == 2:
                player[at_turn].can_build_stage[0] = 3
                player[at_turn].can_build_stage[1] = 4
            else:
                player[at_turn].can_build_stage[player[at_turn].can_build_stage.index(to_build)] = -1

        # RE-DRAW RESOURCES minus TRADED_TOOLS
        tl_client = wx.ClientDC(self.panel)
        tl_client.SetBackground(wx.Brush("WHITE"))
        for i in range(6):
            # UPDATE VISUALS
            tl_client.DrawBitmap(self.blank_tile, 42 + (58 * i) + (at_turn * (self.GetSize()[0] - 532)),
                                 self.GetSize()[1] - 200)
            if player[at_turn].data[i] >= 1:
                tl_client.DrawBitmap(self.icons.GetSubBitmap((58 * i, 0, 58, 58)),
                                     42 + (58 * i) + (at_turn * (self.GetSize()[0] - 532)), self.GetSize()[1] - 200)
                if player[at_turn].data[i] >= 2:
                    tl_client.DrawCircle(42 + (58 * i) + 50 + (at_turn * (self.GetSize()[0] - 532)),
                                         self.GetSize()[1] - 200 + 50, 7)
                    tl_client.DrawText(str(player[at_turn].data[i]),
                                       42 + (58 * i) + 47 + (at_turn * (self.GetSize()[0] - 532)),
                                       self.GetSize()[1] - 200 + 43)

        # DRAW NEW WONDER STAGE
        if at_turn == 0:
            temp_left = self.wonder_leftside.GetSubBitmap((350*(to_build + 1), 315, 350, 315))
            tl_client.DrawBitmap(temp_left, 100, self.GetSize()[1] - 200 - temp_left.GetSize()[1], True)
        else:
            temp_right = self.wonder_rightside.GetSubBitmap((350 * (to_build + 1), 472, 350, 472))
            tl_client.DrawBitmap(temp_right, self.GetSize()[0] - 450, self.GetSize()[1] - 200 - temp_right.GetSize()[1], True)

        # CHECK END GAME
        player[at_turn].counter_stages += 1
        player[at_turn].score += player[at_turn].wonder_point[to_build]
        if player[at_turn].counter_stages == 5:
            self.end_game()
            return False

        flags['build'] = 0
        to_build = -1
        traded_res = [0] * 6
        self.builders[at_turn].Hide()

        self.resource_update()
        self.next_turn_checker()

    def next_turn_checker(self):
        global at_turn
        if list(flags.values()) == [0, 0, 0]:
            at_turn = (at_turn + 1) % 2
            flags['draw'] = 1
            player[at_turn].can_use_cat = player[at_turn].cat

            arrow_painter = wx.ClientDC(self.panel)
            if at_turn == 0:
                arrow_painter.DrawBitmap(self.arr_left, self.GetSize()[0] // 2 - self.arr_left.GetSize()[0] // 2,
                                         self.label.GetPosition()[1] + 50)
            else:
                arrow_painter.DrawBitmap(self.arr_right, self.GetSize()[0] // 2 - self.arr_right.GetSize()[0] // 2,
                                         self.label.GetPosition()[1] + 50)

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
            res_client.DrawCircle(coords[0] + 50, coords[1] + 50, 7)
            res_client.DrawText(str(player[at_turn].data[id - 1]), coords[0] + 47, coords[1] + 43)

        self.resource_update()

    def handle_civil(self, id):
        civ_client = wx.ClientDC(self.panel)
        civ_client.SetBackground(wx.Brush("WHITE"))
        player[at_turn].data[id - 1] += 1

        if id // 8 == 0:
            player[at_turn].cat = True
            player[at_turn].can_use_cat = True

            player[(at_turn + 1) % 2].cat = False

        coords = [0, self.GetSize()[1] - 142]
        if at_turn == 0:
            coords[0] = 216 + 58 * (id // 8)
        else:
            coords[0] = (self.GetSize()[0] - 318) + 58 * (id // 8)

        # CURRENT CHANGE
        civ_client.DrawBitmap(self.icons.GetSubBitmap((58 * (id - 1), 0, 58, 58)), coords[0], coords[1])
        if player[at_turn].data[id - 1] > 1:
            civ_client.DrawCircle(coords[0] + 50, coords[1] + 50, 10)
            civ_client.DrawText(str(player[at_turn].data[id - 1]), coords[0] + 47, coords[1] + 43)

        # TOTAL
        #   icon
        civ_client.DrawBitmap(self.bonus_icons.GetSubBitmap((58, 0, 58, 58)), coords[0] + 58 * (10 - id), coords[1])
        civ_client.DrawCircle(coords[0] + 50 + 58 * (10 - id), coords[1] + 50, 10)
        civ_client.DrawText('Σ', coords[0] + 47 + 58 * (10 - id), coords[1] + 43)
        civ_client.SetPen(wx.TRANSPARENT_PEN)
        #   circle
        civ_client.DrawCircle(coords[0] + 58 * (10 - id) + 29, coords[1] + 29, 15)
        #   sum
        font = wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        civ_client.SetFont(font)
        sum = player[at_turn].data[6] * 2 + player[at_turn].data[7] * 3
        indent_offset = 0
        if sum // 10 >= 1:
            indent_offset = 1
        civ_client.DrawText(str(sum), coords[0] + 58 * (10 - id) + 24 - (indent_offset * 7), coords[1] + 17)
        civ_client.SetPen(wx.Pen("black", 1))

    def handle_war(self, id):
        war_client = wx.ClientDC(self.panel)
        war_client.SetBackground(wx.Brush("WHITE"))

        temp_id = 8 + id // 10
        player[at_turn].data[temp_id] += 1

        # VISUAL UPDATE
        coords = [0, self.GetSize()[1] - 200]
        if at_turn == 0:
            coords[0] = 390 + (58 * (temp_id // 9))
        else:
            coords[0] = (self.GetSize()[0] - 144) + (58 * (temp_id // 9))

        war_client.DrawBitmap(self.icons.GetSubBitmap((58 * (9 - id // 10), 0, 58, 58)), coords[0], coords[1])
        if player[at_turn].data[temp_id] > 1:
            font = wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
            war_client.SetFont(font)
            war_client.DrawText(str(player[at_turn].data[temp_id]), coords[0] + 24, coords[1] + 17)

        # UPDATE WAR TOKENS
        if id // 10 >= 1:
            self.war_update(1 + id // 11)

    def handle_inv(self, id):
        inv_client = wx.ClientDC(self.panel)
        inv_client.SetBackground(wx.Brush("WHITE"))

        player[at_turn].data[id - 2] += 1

        # VISUAL UPDATE
        coords = [0, self.GetSize()[1] - 142]
        if at_turn == 0:
            coords[0] = (58 * (id - 11)) - 16
        else:
            coords[0] = (self.GetSize()[0] - 492) + (58 * (id - 11)) - 58

        inv_client.DrawBitmap(self.icons.GetSubBitmap((58 * (id - 2), 0, 58, 58)), coords[0], coords[1])
        if player[at_turn].data[id - 2] > 1:
            inv_client.DrawCircle(coords[0] + 50, coords[1] + 50, 7)
            inv_client.DrawText(str(player[at_turn].data[id - 2]), coords[0] + 47, coords[1] + 43)

        self.inv_update()

    def tool_update(self):

        # CHECK IF AMBIGUOUS
        exert = player[at_turn].data[10:13]

        if (exert[0] >= 1 and exert[1] >= 1 and exert[2] >= 1) and (exert[0] >= 2 or exert[1] >= 2 or exert[2] >= 2):
            pass  #trigger window
        elif (exert[0] == 0 and exert[1] >= 2 and exert[2] >= 2) or (
                exert[0] >= 2 and exert[1] == 0 and exert[2] >= 2) or (
                exert[0] >= 2 and exert[1] >= 2 and exert[2] == 0):
            pass  #trigger window

        self.open_dialog(exert)

        # RE-DRAW TOOLS minus TRADED_TOOLS
        tl_client = wx.ClientDC(self.panel)
        tl_client.SetBackground(wx.Brush("WHITE"))
        for i in range(3):
            # BACKEND UPDATE
            player[at_turn].data[10 + i] -= traded_tools[i]
            traded_tools[i] = 0

            # UPDATE VISUALS
            tl_client.DrawBitmap(self.blank_tile, 42 + (58 * i) + (at_turn * (self.GetSize()[0] - 532)),
                                 self.GetSize()[1] - 142)
            if player[at_turn].data[10 + i] >= 1:
                tl_client.DrawBitmap(self.icons.GetSubBitmap((580 + 58 * i, 0, 58, 58)),
                                     42 + (58 * i) + (at_turn * (self.GetSize()[0] - 532)), self.GetSize()[1] - 142)
                if player[at_turn].data[10 + i] >= 2:
                    tl_client.DrawCircle(42 + (58 * i) + 50 + (at_turn * (self.GetSize()[0] - 532)),
                                         self.GetSize()[1] - 142 + 50, 7)
                    tl_client.DrawText(str(player[at_turn].data[10 + i]),
                                       42 + (58 * i) + 47 + (at_turn * (self.GetSize()[0] - 532)),
                                       self.GetSize()[1] - 142 + 43)

    def draw_invention(self, event):
        if flags['inv'] < 1:
            return False

        # DETERMINE WHICH BUTTON IS PRESSED
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

        # GIVE INVENTION TO PLAYER
        player[at_turn].inv[inv_list[which_one]] = 1
        player[at_turn].inv[0] += 1

        # GENERATE NEW INVENTION AND UPDATE VISUALS
        dc2 = wx.ClientDC(self.panel)
        dc2.SetBackground(wx.Brush("WHITE"))

        #   VISUALIZE TAKEN INVENTION
        dc2.DrawBitmap(
            self.inv_tokens_small.GetSubBitmap(
                (58 * (inv_list[which_one] % 4), 58 * (inv_list[which_one] // 4), 58, 58)),
            at_turn * (self.GetSize()[0] - 492) + 58 * (player[at_turn].inv[0] - 1), self.GetSize()[1] - 75)

        #   VISUALIZE NEW INVENTION
        inv_list[which_one] = generate_inv()
        dc2.DrawBitmap(
            self.inv_tokens.GetSubBitmap((100 * (inv_list[which_one] % 4), 100 * (inv_list[which_one] // 4), 100, 100)),
            self.GetSize()[0] - 370 + 110 * which_one, 50, True)

        #   UPDATE TOOLS
        self.tool_update()

        flags['inv'] -= 1
        self.next_turn_checker()

    def draw_card(self, which_deck):
        if flags['draw'] <= 0:
            return False

        temp_card = top_cards[which_deck]
        if temp_card <= 6:
            self.handle_resource(temp_card)
        elif temp_card in [7, 8]:
            self.handle_civil(temp_card)
        elif temp_card in [9, 10, 11]:
            self.handle_war(temp_card)
        elif temp_card in [12, 13, 14]:
            self.handle_inv(temp_card)

        # UPDATE VISUALS
        my_decks[which_deck][top_cards[which_deck]] -= 1
        top_cards[which_deck] = generate_card(my_decks[which_deck])
        if which_deck != 'cent':
            self.list_buttons[which_deck].SetBitmap(self.cards.GetSubBitmap((100 * top_cards[which_deck], 0, 100, 148)))
        else:
            player[at_turn].can_use_cat = False
            self.list_buttons[which_deck].SetBitmap(self.cards.GetSubBitmap((0, 0, 100, 148)))

        flags['draw'] -= 1
        self.next_turn_checker()

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

        # AT TURN INIT ARROW
        dc.DrawBitmap(self.arr_left, self.GetSize()[0] // 2 - self.arr_left.GetSize()[0] // 2,
                      self.label.GetPosition()[1] + 50)

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
        self.inv_tokens_small = wx.Bitmap('Assets/progress_smaller.png', wx.BITMAP_TYPE_PNG)
        self.arr_left = wx.Bitmap('Assets/arrow_left.png', wx.BITMAP_TYPE_PNG)
        self.arr_right = wx.Bitmap('Assets/arrow_right.png', wx.BITMAP_TYPE_PNG)
        self.bonus_icons = wx.Bitmap('Assets/bonus_icons.png', wx.BITMAP_TYPE_PNG)
        self.blank_tile = wx.Bitmap('Assets/blank_tile.png', wx.BITMAP_TYPE_PNG)

        #subject to future change
        self.wonder_leftside = wx.Bitmap('Assets/wonder_babylon.png', wx.BITMAP_TYPE_PNG)
        self.wonder_rightside = wx.Bitmap('Assets/wonder_alexandria.png', wx.BITMAP_TYPE_PNG)

        frame_size = self.GetSize()
        # [0] - WIDTH - 1538
        # [1] - HEIGHT - 864

        self.panel = MyPanel(self)
        self.traded_tools = [0, 0, 0]

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
        self.button_cent.Bind(wx.EVT_ENTER_WINDOW, lambda event: self.hover_cent_deck(player[at_turn].cat, True))
        self.button_cent.Bind(wx.EVT_LEAVE_WINDOW, lambda event: self.hover_cent_deck(player[at_turn].cat, False))

        # LABEL 'AT TURN'
        self.label = wx.StaticText(self.panel, label='At turn')
        # FONT SIZE
        font = self.label.GetFont()
        font.SetPointSize(20)
        self.label.SetFont(font)
        # LABEL POSITION
        self.label.SetPosition((frame_size[0] // 2 - self.label.GetSize()[0] // 2, frame_size[1] // 2 - 150))

        # BUILD BUTTON
        button_build_0 = wx.Button(self.panel, label='Build', pos=(42, self.GetSize()[1] - 230))
        button_build_1 = wx.Button(self.panel, label='Build',
                                   pos=(42 + self.GetSize()[0] - 532, self.GetSize()[1] - 230))

        self.builders = [button_build_0, button_build_1]

        button_build_0.SetSize((58, button_build_0.GetSize()[1]))
        button_build_1.SetSize((58, button_build_1.GetSize()[1]))

        button_build_0.Bind(wx.EVT_BUTTON, lambda event: self.builder_click())
        button_build_1.Bind(wx.EVT_BUTTON, lambda event: self.builder_click())

        button_build_0.Hide()
        button_build_1.Hide()

    def open_dialog(self, tools):
        new_panel = SeamlessPanel(self, tools)
        new_panel.ShowModal()
        new_panel.Destroy()

    def open_res_dialog(self, res):
        new_panel = SeamlessResPanel(self, res)
        new_panel.ShowModal()
        new_panel.Destroy()


class SeamlessResPanel(wx.Dialog):

    def __init__(self, parent, res):
        super().__init__(parent, title='Choose what resources to spend', style=wx.NO_BORDER | wx.DEFAULT_DIALOG_STYLE)
        self.res = res

        panel = wx.Panel(self)

        # BUTTONS
        self.icons = wx.Bitmap('Assets/main_icons.png', wx.BITMAP_TYPE_PNG)
        self.buttons = []
        self.nums = []
        for i in range(6):
            btn = wx.BitmapButton(panel, bitmap=self.icons.GetSubBitmap((58 * i, 0, 58, 58)),
                                  pos=(3 + i * 68, 20))
            btn.Bind(wx.EVT_BUTTON, self.on_button_click)
            if res[i] < 1:
                btn.Hide()
                self.nums.append(None)
            else:
                num = wx.StaticText(panel, label=str(self.res[i]),
                                    pos=(i * 68 + btn.GetSize()[0] // 2 + 3, btn.GetSize()[1] + 25))
                self.nums.append(num)
            self.buttons.append(btn)

        # Button to close the dialog
        close_button = wx.Button(panel, size=(self.buttons[1].GetSize()[0], 20), label="Send",
                                 pos=(self.buttons[2].GetPosition()[0] + 5 + self.buttons[3].GetSize()[0] // 2,
                                      self.buttons[1].GetPosition()[0] + 50))
        close_button.Bind(wx.EVT_BUTTON, self.on_send)

        question = wx.StaticText(panel, label='Which stage to build?', pos=(10, self.buttons[1].GetPosition()[0] + 50))

        for i, choice in enumerate(player[at_turn].can_build_stage):
            if choice == -1:
                continue
            temp_rad = wx.RadioButton(panel, name=str(choice), label='Stage ' + str(choice),
                                      pos=(10, self.buttons[1].GetPosition()[0] + 70 + (i * 20)))
            temp_rad.Bind(wx.EVT_RADIOBUTTON, self.radio_click)

        self.SetPosition((400, 300))
        self.SetSize((self.buttons[0].GetSize()[0] * 6 + 56, 300))

    def radio_click(self, event):
        global to_build
        radio = event.GetEventObject()
        name = radio.GetName()
        to_build = int(name)

    def on_button_click(self, event):
        button = event.GetEventObject()
        index = self.buttons.index(button)
        if self.res[index] == 0:
            return False
        self.res[index] -= 1
        traded_res[index] += 1
        self.nums[index].SetLabel(str(self.res[index]))

    def on_send(self, event):
        t = traded_res
        count_unique = 0
        count_max_same = 0

        for i in range(5):
            if t[i] > 0:
                count_unique += 1
                count_max_same = max(count_max_same, t[i])

        count_unique += t[5]
        count_max_same += t[5]

        if ((to_build == 0 and count_unique >= 2) or
                (to_build == 1 and count_max_same >= 2) or
                (to_build == 2 and count_unique >= 3) or
                (to_build == 3 and count_max_same >= 3) or
                (to_build == 4 and count_unique >= 4)):
            self.Close()


class SeamlessPanel(wx.Dialog):

    def __init__(self, parent, tools):
        super().__init__(parent, title='Choose what tools to spend', style=wx.NO_BORDER | wx.DEFAULT_DIALOG_STYLE)
        self.tools = tools
        panel = wx.Panel(self)

        # BUTTONS
        self.icons = wx.Bitmap('Assets/main_icons.png', wx.BITMAP_TYPE_PNG)
        self.buttons = []
        self.nums = []
        for i in range(3):
            btn = wx.BitmapButton(panel, bitmap=self.icons.GetSubBitmap((580 + (58 * i), 0, 58, 58)),
                                  pos=(3 + i * 68, 20))
            btn.Bind(wx.EVT_BUTTON, self.on_button_click)
            if tools[i] < 1:
                btn.Hide()
                self.nums.append(None)
            else:
                num = wx.StaticText(panel, label=str(self.tools[i]),
                                    pos=(i * 68 + btn.GetSize()[0] // 2 + 3, btn.GetSize()[1] + 25))
                self.nums.append(num)
            self.buttons.append(btn)

        # Button to close the dialog
        close_button = wx.Button(panel, size=(self.buttons[1].GetSize()[0], 20), label="Send",
                                 pos=(self.buttons[1].GetPosition()[0], self.buttons[1].GetPosition()[0] + 50))
        close_button.Bind(wx.EVT_BUTTON, self.on_send)

        self.SetPosition((400, 300))
        self.SetSize((self.buttons[0].GetSize()[0] * 3 + 26, 200))

    def on_button_click(self, event):
        button = event.GetEventObject()
        index = self.buttons.index(button)
        if self.tools[index] == 0:
            return False
        self.tools[index] -= 1
        traded_tools[index] += 1
        self.nums[index].SetLabel(str(self.tools[index]))

    def on_send(self, event):
        t = traded_tools
        if (t[0] >= 1 and t[1] >= 1 and t[2] >= 1) or (t[0] >= 2 or t[1] >= 2 or t[2] >= 2):
            self.Close()


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
