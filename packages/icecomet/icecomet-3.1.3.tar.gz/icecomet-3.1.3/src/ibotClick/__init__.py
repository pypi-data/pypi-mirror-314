from pynput import keyboard
from pynput.keyboard import Key
from pynput import mouse
from pynput.mouse import Button
from iprint import *
from time import sleep 
import pyperclip as pyper
# import cv2 as cv
k = keyboard.Controller()
m = mouse.Controller()

delay = 0.1



def copy(delay_time = delay,delay_factor = 1):

    k.press(Key.cmd)
    sleep(delay_time*delay_factor)
    k.press('k')
    sleep(delay_time*delay_factor)
    k.release(Key.cmd)
    sleep(delay_time*delay_factor)
    k.release('k')
    sleep(delay_time*delay_factor)


def click_left(position,delay_time = delay, delay_factor = 1):

    m.position = position
    sleep(delay_time*delay_factor)
    m.click(Button.left)
    sleep(delay_time*delay_factor)

def click_right(position,delay_time = delay, delay_factor = 1):

    m.position = position
    sleep(delay_time*delay_factor)
    m.click(Button.right)
    sleep(delay_time*delay_factor)

def press_left(position,delay_time = delay, delay_factor = 1):

    m.position = position
    sleep(delay_time*delay_factor)
    m.press(Button.left)
    sleep(delay_time*delay_factor)

def press_right(position,delay_time = delay, delay_factor = 1):

    m.position = position
    sleep(delay_time*delay_factor)
    m.press(Button.right)
    sleep(delay_time*delay_factor)


########################################################
########################################################
########################################################
########################################################
########################################################
########################################################
# exit()
# sleep(1)
# k.press('a')
# k.press(keyboard.Key.space)
# k.type('Hello world')


# m.position = (0,0)
# m.move(0,0)
# m.scroll(0,1)  #(เลื่อนแนวนอน,เลื่อนแนวตั้ง)
# m.click(mouse.Button.left)
# m.press(mouse.Button.left)
# m.release(mouse.Button.left)









#show Key and click programe
##############################
# import cv2 as cv
# from iprint import *
# import numpy as np



# import pyperclip
# from pynput import keyboard
# from pynput import mouse
# from threading import Thread

# def on_press(key):
#     try:
#         ij('Key : '+key.char+' press')
#     except AttributeError:
#         if key == keyboard.Key.esc:
#             exit()
#         ij(ct.yello+'Spacial : '+str(key)+' press')
        
   
# # ฟังก์ชันที่ถูกเรียกเมื่อคลิกเมาส์
# def on_click(x, y, button, pressed):
#     if pressed:
#         # print(ct.blue+f"คลิกที่ตำแหน่ง x={x}, y={y} ด้วยปุ่ม {button}")
#         print(ct.blue+f"คลิกที่ตำแหน่ง x={x:<15}, y={y:<15}")
#         x,y = int(x),int(y)
#         c = 2
#         if c==1:
#             pyperclip.copy(f'({x},{y})')
#         if c==2:
#             pyperclip.copy(f'm.position = ({x}, {y})\nm.click(mouse.Button.left)\n')
        

# # Collect events until released
# def keyboard_click():
#     with keyboard.Listener( on_press=on_press ) as listener:
#         listener.join()

# def mouse_click():
#     with mouse.Listener( on_click=on_click ) as listener:
#         listener.join()

# K = Thread(target=keyboard_click)
# M = Thread(target=mouse_click)
# M.daemon = True
# K.start()
# M.start()


##########################################################################
##########################################################################
##########################################################################
#detect key programe
# from pynput import keyboard

# pressed_keys = set()

# def on_press(key):
#     try:
#         pressed_keys.add(key.char)
#     except AttributeError:
#         pressed_keys.add(key)

#     if pressed_keys == {'a', 's'}:
#         print('asdf')

# def on_release(key):
#     try:
#         pressed_keys.remove(key.char)
#     except :
#         pressed_keys.discard(key)

# with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
#     listener.join()





