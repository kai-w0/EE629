#!/usr/bin/env python
#encoding: UTF-8

'''
NetEase Menu
'''

import curses
import locale
import sys
import os
import json
import time
import webbrowser
from api import NetEase
from player import Player
from ui import Ui

home = os.path.expanduser("~")
if os.path.isdir(home + '/netease-musicbox') is False:
    os.mkdir(home+'/netease-musicbox')

locale.setlocale(locale.LC_ALL, "")
code = locale.getpreferredencoding()   

# carousel x in [left, right]
carousel = lambda left, right, x: left if (x>right) else (right if x<left else x)

shortcut = [
    ['j', 'Down      ', '下移'],
    ['k', 'Up        ', '上移'],
    ['h', 'Back      ', '后退'],
    ['l', 'Forward   ', '前进'],
    ['u', 'Prev page ', '上一页'],
    ['d', 'Next page ', '下一页'],
    ['f', 'Search    ', '快速搜索'],
    ['[', 'Prev song ', '上一曲'],
    [']', 'Next song ', '下一曲'],
    [' ', 'Play/Pause', '播放/暂停'],
    ['m', 'Menu      ', '主菜单'],
    ['p', 'Present   ', '当前播放列表'],
    ['a', 'Add       ', '添加曲目到打碟'],
    ['z', 'DJ list   ', '打碟列表'],
    ['s', 'Star      ', '添加到收藏'],
    ['c', 'Collection', '收藏列表'],
    ['r', 'Remove    ', '删除当前条目'],
    ['q', 'Quit      ', '退出']
]


class Menu:
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('UTF-8')
        self.datatype = 'main'
        self.title = 'NetEase'
        self.datalist = ['Ranking List', 'Artists', 'New Albums', 'Selected Playlists', 'My Lists', 'DJ', 'Discs', 'Collections', 'Search', 'Help']
        self.offset = 0
        self.index = 0
        self.presentsongs = []
        self.player = Player()
        self.ui = Ui()
        self.netease = NetEase()
        self.screen = curses.initscr()
        self.screen.keypad(1)
        self.step = 10
        self.stack = []
        self.djstack = []
        self.userid = None
        self.username = None
        try:
            sfile = file(home + "/netease-musicbox/flavor.json",'r')
            data = json.loads(sfile.read())
            self.collection = data['collection']
            self.account = data['account']
            sfile.close()
        except:
            self.collection = []        
            self.account = {}

    def start(self):
        self.ui.build_menu(self.datatype, self.title, self.datalist, self.offset, self.index, self.step)
        self.stack.append([self.datatype, self.title, self.datalist, self.offset, self.index])
        while True:
            datatype = self.datatype
            title = self.title
            datalist = self.datalist
            offset = self.offset
            idx = index = self.index
            step = self.step
            stack = self.stack
            djstack = self.djstack
            key = self.screen.getch()
            self.ui.screen.refresh()

            # quit
            if key == ord('q'):
                break

            # up
            elif key == ord('k'):
                self.index = carousel(offset, min( len(datalist), offset + step) - 1, idx-1 )

            # down
            elif key == ord('j'):
                self.index = carousel(offset, min( len(datalist), offset + step) - 1, idx+1 )

            # up page
            elif key == ord('u'):
                if offset == 0:
                    continue
                self.offset -= step

                # e.g. 23 - 10 = 13 --> 10
                self.index = (index-step)//step*step

            # down page
            elif key == ord('d'):
                if offset + step >= len( datalist ):
                    continue
                self.offset += step

                # e.g. 23 + 10 = 33 --> 30
                self.index = (index+step)//step*step

            # forward
            elif key == ord('l') or key == 10:
                if self.datatype == 'songs' or self.datatype == 'djchannels' or self.datatype == 'help':
                    continue
                self.ui.build_loading()
                self.dispatch_enter(idx)
                self.index = 0
                self.offset = 0    

            # backward
            elif key == ord('h'):
                # if not main menu
                if len(self.stack) == 1:
                    continue
                up = stack.pop()
                self.datatype = up[0]
                self.title = up[1]
                self.datalist = up[2]
                self.offset = up[3]
                self.index = up[4]

            # search
            elif key == ord('f'):
                self.search()

            # play next
            elif key == ord(']'):
                self.player.next()
                time.sleep(0.1)

            # play previous
            elif key == ord('['):
                self.player.prev()
                time.sleep(0.1)

            # play, stop
            elif key == ord(' '):
                if datatype == 'songs':
                    self.presentsongs = ['songs', title, datalist, offset, index]
                elif datatype == 'djchannels':
                    self.presentsongs = ['djchannels', title, datalist, offset, index]
                self.player.play(datatype, datalist, idx)
                time.sleep(0.1)

            # current list
            elif key == ord('p'):
                if len(self.presentsongs) == 0:
                    continue
                self.stack.append( [datatype, title, datalist, offset, index] )
                self.datatype = self.presentsongs[0]
                self.title = self.presentsongs[1]
                self.datalist = self.presentsongs[2]
                self.offset = self.presentsongs[3]
                self.index = self.presentsongs[4]

            # add to discs
            elif key == ord('a'):
                if datatype == 'songs' and len(datalist) != 0:
                    self.djstack.append( datalist[idx] )
                elif datatype == 'artists':
                    pass

            # load discs
            elif key == ord('z'):
                self.stack.append( [datatype, title, datalist, offset, index] )
                self.datatype = 'songs'
                self.title = 'NetEase > discs'
                self.datalist = self.djstack
                self.offset = 0
                self.index = 0

            # add to collections
            elif key == ord('s'):
                if (datatype == 'songs' or datatype == 'djchannels') and len(datalist) != 0:
                    self.collection.append( datalist[idx] )

            # load collections
            elif key == ord('c'):
                self.stack.append( [datatype, title, datalist, offset, index] )
                self.datatype = 'songs'
                self.title = '网易云音乐 > 收藏'
                self.datalist = self.collection
                self.offset = 0
                self.index = 0

            # remove
            elif key == ord('r'):
                if datatype != 'main' and len(datalist) != 0:
                    self.datalist.pop(idx)
                    self.index = carousel(offset, min( len(datalist), offset + step) - 1, idx )

            elif key == ord('m'):
                if datatype != 'main':
                    self.stack.append( [datatype, title, datalist, offset, index] )
                    self.datatype = self.stack[0][0]
                    self.title = self.stack[0][1]
                    self.datalist = self.stack[0][2]
                    self.offset = 0
                    self.index = 0                    

            elif key == ord('g'):
                if datatype == 'help':
                    webbrowser.open_new_tab('https://github.com/vellow/NetEase-MusicBox')

            self.ui.build_menu(self.datatype, self.title, self.datalist, self.offset, self.index, self.step)


        self.player.stop()
        sfile = file(home + "/netease-musicbox/flavor.json", 'w')
        data = {
            'account': self.account,
            'collection': self.collection
        }
        sfile.write(json.dumps(data))
        sfile.close()
        curses.endwin()

    def dispatch_enter(self, idx):
        # The end of stack
        netease = self.netease
        datatype = self.datatype
        title = self.title
        datalist = self.datalist
        offset = self.offset
        index = self.index
        self.stack.append( [datatype, title, datalist, offset, index])

        if datatype == 'main':
            self.choice_channel(idx) 

        # artists
        elif datatype == 'artists':
            artist_id = datalist[idx]['artist_id']
            songs = netease.artists(artist_id)         
            self.datatype = 'songs'
            self.datalist = netease.dig_info(songs, 'songs')
            self.title += ' > ' + datalist[idx]['artists_name']

        # albums
        elif datatype == 'albums':
            album_id = datalist[idx]['album_id']
            songs = netease.album(album_id)
            self.datatype = 'songs'
            self.datalist = netease.dig_info(songs, 'songs')
            self.title += ' > ' + datalist[idx]['albums_name']

        # playlist
        elif datatype == 'playlists':
            playlist_id = datalist[idx]['playlist_id']
            songs = netease.playlist_detail(playlist_id)
            self.datatype = 'songs'
            self.datalist = netease.dig_info(songs, 'songs')
            self.title += ' > ' + datalist[idx]['playlists_name']

    def choice_channel(self, idx):
        # ranking list
        netease = self.netease
        if idx == 0:
            songs = netease.top_songlist()
            self.datalist = netease.dig_info(songs, 'songs')
            self.title += ' > Ranking List'
            self.datatype = 'songs'

        # artist
        elif idx == 1:
            artists = netease.top_artists()
            self.datalist = netease.dig_info(artists, 'artists')
            self.title += ' > artists'
            self.datatype = 'artists'

        # new albums
        elif idx == 2:
            albums = netease.new_albums()
            self.datalist = netease.dig_info(albums, 'albums')
            self.title += ' > New Albums'
            self.datatype = 'albums'

        # playlists
        elif idx == 3:
            playlists = netease.top_playlists()
            self.datalist = netease.dig_info(playlists, 'playlists')
            self.title += ' > Playlists'
            self.datatype = 'playlists'            

        # my
        elif idx == 4:
            # unlog
            if self.userid is None:
                # use local account
                if self.account:
                    user_info = netease.login(self.account[0], self.account[1])
                    
                # no local account
                if self.account == {} or user_info['code'] != 200:
                    data = self.ui.build_login()
                    # cancel sign in
                    if data == -1:
                        return
                    user_info = data[0]
                    self.account = data[1]

                self.username = user_info['profile']['nickname']
                self.userid = user_info['account']['id']
            # load account lists
            myplaylist = netease.user_playlist( self.userid )
            self.datalist = netease.dig_info(myplaylist, 'playlists')
            self.datatype = 'playlists'
            self.title += ' > ' + self.username + ' list'

        # DJ
        elif idx == 5:
            self.datatype = 'djchannels'
            self.title += ' > DJ'
            self.datalist = netease.djchannels()

        # discs
        elif idx == 6:
            self.datatype = 'songs'
            self.title += ' > Discs'
            self.datalist = self.djstack

        # collection
        elif idx == 7:
            self.datatype = 'songs'
            self.title += ' > Collections'
            self.datalist = self.collection

        # Search
        elif idx == 8:
            self.search()

        # help
        elif idx == 9:
            self.datatype = 'help'
            self.title += ' > Help'
            self.datalist = shortcut

        self.offset = 0
        self.index = 0 

    def search(self):
        ui = self.ui
        x = ui.build_search_menu()
        # if do search, push current info into stack
        if x in range(ord('1'), ord('5')):
            self.stack.append( [self.datatype, self.title, self.datalist, self.offset, self.index ])
            self.index = 0
            self.offset = 0

        if x == ord('1'):
            self.datatype = 'songs'
            self.datalist = ui.build_search('songs')
            self.title = 'Songs'

        elif x == ord('2'):
            self.datatype = 'artists'
            self.datalist = ui.build_search('artists')
            self.title = 'Artists'

        elif x == ord('3'):
            self.datatype = 'albums'
            self.datalist = ui.build_search('albums')
            self.title = 'Albums'

        elif x == ord('4'):
            self.datatype = 'playlists'
            self.datalist = ui.build_search('playlists')
            self.title = 'Top Lists'

