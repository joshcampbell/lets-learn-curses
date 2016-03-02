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
standard_colors = 1
border_colors = 2
player_one_colors = 3
player_two_colors = 4

def main(screen):
  assert curses.has_colors(), "This game requires a color terminal."
  curses.init_pair(standard_colors, curses.COLOR_WHITE, curses.COLOR_BLACK)
  curses.init_pair(border_colors, curses.COLOR_BLACK, curses.COLOR_WHITE)
  curses.init_pair(player_one_colors, curses.COLOR_BLACK, curses.COLOR_RED)
  curses.init_pair(player_two_colors, curses.COLOR_WHITE, curses.COLOR_BLUE)
  curses.curs_set(0)
  curses.mousemask(1)
  show_title(screen)
  game_loop(screen)

def show_title(screen):
  screen.attron(curses.color_pair(standard_colors))
  screen.clear()
  title = random.choice(titles)
  screen.addstr(0,0,title)
  any_key = screen.getch()

def game_loop(screen):
  while True:
    render_board(screen,game_state)
    key_pressed = screen.getch()
    if key_pressed == ord('q'):
      break
    if key_pressed == curses.KEY_MOUSE:
      _, y, x, __, click_type = curses.getmouse()
      raise Exception(x//tile_size,y//tile_size)

def render_board(screen,game_state):
  screen.clear()
  # draw a grid
  window_size = screen.getmaxyx()
  assert (window_size[0] >= total_board_size) \
         and (window_size[1] >= total_board_size), \
         "Terminal must be at least %sx%s characters"%(total_board_size,total_board_size)
  # draw top bar
  color_attrs = [curses.color_pair(player_one_colors), curses.color_pair(player_two_colors)]
  chars = ["\\","/"]
  for x in range(1,total_board_size):
    screen.attron(color_attrs[x%2])
    screen.addstr(0,x,chars[x%2])
  # write player names on the top bar
  screen.attron(curses.color_pair(player_one_colors))
  screen.addstr(0,0,u"Φιλοκτήτης".encode('utf-8'))
  player_two_name = u"米爾".encode('utf-8')
  player_two_index = total_board_size - len(player_two_name)
  screen.attron(curses.color_pair(player_two_colors))
  screen.addstr(0,player_two_index,player_two_name)
  # iterate over the entire board
  board_range = range(1,total_board_size)
  for x in board_range:
    for y in board_range:
      if (x % tile_size is 0 or y % tile_size is 0):
        # this is a border
        screen.attron(curses.color_pair(border_colors))
        screen.addch(y,x,' ')
      else:
        # this is inside a tile
        x_index = x // tile_size
        y_index = y // tile_size
        if x_index is 1 and y_index is 1:
          screen.attron(curses.color_pair(player_one_colors))
          screen.addch(y,x,'X')
        if x_index is 2 and y_index is 2:
          screen.attron(curses.color_pair(player_two_colors))
          screen.addch(y,x,'O')

if __name__ == '__main__':
  curses.wrapper(main)
  print "Thanks for playing!"
