# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time
from multiprocessing import Process

import pika
import pygame

import game.control
from game import hero
from common import image_source
from common import config
from game import land
import asyncio
from bliv import sample
import threading
from game import player_commond


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def start_game():
    pygame.init()
    fps = 20
    win_size = (config.WIN_WIDTH, config.WIN_HEIGHT)
    screen = pygame.display.set_mode(win_size)
    pygame.display.set_caption("修仙投资")

    font = pygame.font.SysFont("SimHei", 20)
    samil_font = pygame.font.SysFont("SimHei", 10)

    images = image_source.GameImageSource()
    images.load()
    land.Lands, land.Land_group = land.create_lands(images, font, samil_font)
    hero.Heroes, hero.Hero_groups = hero.create_heroes(images)

    game.control.start()


def start_listen():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='127.0.0.1', port=5672))
    channel = connection.channel()
    channel.queue_declare(queue='test')
    channel.basic_consume(queue="test", on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


class myThread (threading.Thread):
    def __init__(self, threadID, name, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delay = delay
    def run(self):
        if self.threadID == 1:
            start_game()
        if self.threadID == 2:
            start_listen()
        print ("开始线程：" + self.name)
        print_time(self.name, self.delay, 5)
        print ("退出线程：" + self.name)


exitFlag = 0


def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1


def callback(ch, method, properties, body):
    '''回调函数,处理从rabbitmq中取出的消息'''
    msg = body.decode()
    print(" [x] Received %r" % msg)
    player = player_commond.player_instance
    player.exe_command(msg)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # game = Process(target=start_game)
    # game.start()
    #
    # bliv = Process(target=start_listen)
    # bliv .start()
    #
    # game.join()
    # bliv.join()

    thread1 = myThread(1, "Thread-1", 1)
    thread2 = myThread(2, "Thread-2", 2)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    while True:
        time.sleep(60 * 60 * 24)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
