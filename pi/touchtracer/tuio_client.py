from oscpy.client import OSCClient
import pyautogui

osc = OSCClient('127.0.0.1', 3334)
while (True):
    (m1,m2)=pyautogui.position()
    s=pyautogui.size()
    m1=m1/s[0]
    m2=m2/s[1]
    osc.send_message(b'/tuio/2Dcur',(b'alive',100))
    osc.send_message(b'/tuio/2Dcur',(b'set',100,m1,m2))