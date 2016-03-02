#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

import json
import curses
import random
import locale

locale.setlocale(locale.LC_ALL, '')

titles = [
"""
                           
|''||''|  ||
   ||    ...    ....
   ||     ||  .|   ''
   ||     ||  ||
  .||.   .||.  '|...'


|''||''|
   ||     ....     ....
   ||    '' .||  .|   ''
   ||    .|' ||  ||
  .||.   '|..'|'  '|...'


|''||''|                 .|.
   ||      ...     ....  |||
   ||    .|  '|. .|...|| '|'
   ||    ||   || ||       |
  .||.    '|..|'  '|...'  .
                         '|'
""",
"""
                               
_/_/_/_/_/  _/
   _/            _/_/_/
  _/      _/  _/
 _/      _/  _/
_/      _/    _/_/_/
_/_/_/_/_/
   _/      _/_/_/    _/_/_/
  _/    _/    _/  _/
 _/    _/    _/  _/
_/      _/_/_/    _/_/_/
_/_/_/_/_/                    _/
   _/      _/_/      _/_/    _/
  _/    _/    _/  _/_/_/_/  _/
 _/    _/    _/  _/
_/      _/_/      _/_/_/  _/

""",
"""
                         
TTTTTTT iii
  TTT         cccc
  TTT   iii cc
  TTT   iii cc
  TTT   iii  ccccc

TTTTTTT
  TTT     aa aa   cccc
  TTT    aa aaa cc
  TTT   aa  aaa cc
  TTT    aaa aa  ccccc

TTTTTTT               !!!
  TTT    oooo    eee  !!!
  TTT   oo  oo ee   e !!!
  TTT   oo  oo eeeee
  TTT    oooo   eeeee !!!
""",
]

# TODO introduce tic tac toe library and use actual game state
game_state = json.loads(open("./fixture.json").read())

# set up global variables
board_size = game_state["board"]["size"]
origin_x = 0
origin_y = 0
border_width = 1
square_size = 9
tile_size = square_size + border_width
total_board_size = square_size * board_size + (border_width * board_size)

# establish color palette indices
title_colors = 1
border_colors = 2
player_one_colors = 3
player_two_colors = 4

def main(screen):
  verify(screen)
  configure(screen)
  show_title(screen)
  game_loop(screen)

class NotEnoughRoomException(Exception):
  pass

def column_width(string):
  # assumes the first column of the image is the widest
  # FIXME returns unreasonably large values for title strings
  first_newline = string.find("\n")
  if first_newline != -1:
    return first_newline
  else:
    return len(string)

def centered_x(screen, string):
  screen_width = width(screen)
  diff = screen_width - len(string)
  if diff < 0:
    raise NotEnoughRoomException("%s > %s"%(len(string),screen_width))
  return diff // 2

def show_title(screen):
  screen.clear()
  screen.attron(curses.color_pair(border_colors))
  for x in range(0,width(screen)):
    screen.addch(0,x,' ')
  message = "   Press Any Key To Continue   "
  screen.addstr(0,centered_x(screen,message),message, curses.A_BOLD)
  screen.attron(curses.color_pair(title_colors))
  title = random.choice(titles)
  first_line = title.split("\n")[1]
  current_line = 0
  for line in title.split("\n"):
    current_line += 1
    screen.addstr(current_line,centered_x(screen,first_line),line)
  any_key = screen.getch()

def game_loop(screen):
  while True:
    render_board(screen)
    key_pressed = screen.getch()
    if key_pressed == ord('q'):
      break
    if key_pressed == curses.KEY_MOUSE:
      _, y, x, __, click_type = curses.getmouse()
      raise Exception(x//tile_size,y//tile_size)

def render_board(screen):
  screen.clear()
  draw_top_bar(screen)
  draw_game_board(screen)

def draw_border(screen,y,x):
  screen.attron(curses.color_pair(border_colors))
  screen.addch(y,x,' ')

def draw_tile(screen,y,x):
  x_index = x // tile_size
  y_index = y // tile_size
  # TODO refer to actual game state via presenter
  if x_index is 1 and y_index is 1:
    screen.attron(curses.color_pair(player_one_colors))
    screen.addstr(y,x,u'X'.encode('utf-8'))
  if x_index is 2 and y_index is 2:
    screen.attron(curses.color_pair(player_two_colors))
    screen.addstr(y,x,u'O'.encode('utf-8'))

def draw_game_board(screen):
  positions = range(1,total_board_size)
  for x in positions:
    for y in positions:
      if (x % tile_size is 0 or y % tile_size is 0):
        draw_border(screen,y,x)
      else:
        draw_tile(screen,y,x)

def draw_top_bar(screen):
  # draw background
#  color_attrs = [curses.color_pair(player_one_colors), curses.color_pair(player_two_colors)]
#  for x in range(1,width(screen)):
#    screen.attron(color_attrs[x%2])
#    screen.addstr(0,x," ")
  # write player names
  screen.attron(curses.color_pair(player_one_colors))
  # TODO refer to actual game state via presenter
  screen.addstr(0,0,u"Φιλοκτήτης is \"X\"".encode('utf-8'))
  matz = "Beatrice is \"O\""
  player_two_name = matz.encode('utf-8')
  player_two_index = width(screen) - len(matz)
  screen.attron(curses.color_pair(player_two_colors))
  screen.addstr(0,player_two_index,player_two_name)

def width(screen):
  height, width = screen.getmaxyx()
  return width

def height(screen):
  height, width = screen.getmaxyx()
  return height

def verify(screen):
  window_size = screen.getmaxyx()
  assert (window_size[0] >= total_board_size) \
    and (window_size[1] >= total_board_size), \
    "Terminal must be at least %sx%s characters"%(total_board_size,total_board_size)
  assert curses.has_colors(), "This game requires a color terminal."

def configure(screen):
  title_foreground = random.choice([curses.COLOR_WHITE,curses.COLOR_CYAN,curses.COLOR_MAGENTA,curses.COLOR_YELLOW,curses.COLOR_GREEN,curses.COLOR_RED])
  curses.init_pair(title_colors, title_foreground, curses.COLOR_BLACK)
  curses.init_pair(border_colors, curses.COLOR_BLACK, curses.COLOR_WHITE)
  curses.init_pair(player_one_colors, curses.COLOR_BLACK, curses.COLOR_CYAN)
  curses.init_pair(player_two_colors, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
  curses.curs_set(0) # hide cursor
  curses.mousemask(1) # enable mouse support

if __name__ == '__main__':
  # TODO prompt for player names and symbols
  # TODO prompt for human versus AI players
  curses.wrapper(main)
  print "Thanks for playing!"
