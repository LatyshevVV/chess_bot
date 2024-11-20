from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from stockfish import Stockfish
from datetime import datetime

stockfish = Stockfish("C:\Program Files\stockfish-10-win\Windows\stockfish_10_x64.exe",depth = 20)

global ot #pixel offset
ot = 108

global disp
disp = 50

global dict
dict = {'a':0, 'b':ot, 'c':ot*2, 'd':ot*3,
               'e':ot*4, 'f':ot*5, 'g':ot*6, 'h':ot*7,
               '8':0, '7':ot, '6':ot*2, '5':ot*3,
               '4':ot*4, '3':ot*5, '2':ot*6, '1':ot*7}

global dict2
dict2 = {0:'a', 108:'b', 216:'c', 324:'d',
               432:'e', 540:'f', 648:'g', 756:'h'}
               

def make_move(st, start_elem):
    action = webdriver.ActionChains(driver)
    action.move_to_element(start_elem)
    #print(dict[str[0]],dict[str[1]])
    action.move_by_offset(dict[st[0]]+disp,dict[st[1]])
    action.click()
    action.move_to_element(start_elem)
    action.move_by_offset(dict[st[2]]+disp,dict[st[3]])
    action.click()
    action.perform()
    """
    if (len(st)==5):
        time.sleep(2)
        f.write('Here peshka became queen: '+st+'\n')
        action1 = webdriver.ActionChains(driver)
        action1.move_to_element(start_elem)
        f.write(str(dict[st[2]]+disp)+' '+str(dict[st[3]]))
        action1.move_by_offset(dict[st[2]]+disp,dict[st[3]])
        action1.click()
        action1.perform
    """

def get_move():
    r=''
    elem = driver.find_element_by_xpath('//*[@id="chessboard_boardarea"]/div[18]')
    #elem = driver.find_elements_by_class_name("move-square")
    s = elem.get_attribute('style')
    #print(s)
    t = s.rfind("translate")
    s = s[t+10:]
    if (s[0]=='0'):
        n2=0
    else:
        n2 = int(s[:3])
    if (len(s)>=12):
        t = s.rfind(",")
        s = s[t+2:]
        n1 = int(s[:3])
    else:
        n1 = 0
    r += dict2[n2]
    r += str(8-n1//108)

    elem = driver.find_element_by_xpath('//*[@id="chessboard_boardarea"]/div[19]')
    s = elem.get_attribute('style')
    #print(s)
    t = s.rfind("translate")
    s = s[t+10:]
    if (s[0]=='0'):
        n4=0
    else:
        n4 = int(s[:3])
    if (len(s)>=12):
        t = s.rfind(",")
        s = s[t+2:]
        n3 = int(s[:3])
    else:
        n3 = 0
    r += dict2[n4]
    r += str(8-n3//108)

    #print(r)

    return r

login = "vadokus"
password = "password"
url = "https://www.chess.com/login"

f = open('log.txt', 'a')
f.write('\n\n\n================='+str(datetime.now())+'=================\n')

driver = webdriver.Firefox()
driver.maximize_window()

driver.get(url)
f.write("Open "+url+'\n')

try:
    
    elem = driver.find_element_by_name("_username").send_keys(login)
    elem = driver.find_element_by_name("_password").send_keys(password)
    elem = driver.find_element_by_name("login").click()
except:
    f.write('Can\'t enter into site\n')
    driver.quit()
    f.close()

f.write("Log in "+url+'\n')
driver.get("https://www.chess.com/play/computer")

time.sleep(10)

stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

start_elem = driver.find_element_by_xpath("/html/body/main/div[12]/div[1]/div/div[1]/div[1]/div/div[1]/div[1]/div/div[1]")
#start_elem = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[3]/div[3]/div[1]")
pos=[]
while (True):
    try:
        move = stockfish.get_best_move()
        make_move(move,start_elem)
        pos.append(move)
        stockfish.set_position(pos)
        f.write("white "+move+'\n')
        time.sleep(5)

        move = get_move()
        if (stockfish.is_move_correct(move) == False):
            #print("tyt ",move)
            move = move[2]+move[3]+move[0]+move[1]
        pos.append(move)
        stockfish.set_position(pos)
        f.write("black "+move+'\n')
        #time.sleep(2)

        f.write('[')
        for st in pos:
            f.write("'"+st+"', ")
        f.write(']\n')
    except KeyboardInterrupt:
        st = input("Ready?\ny-continue\ns-new game\nq-quit\no-otl]n")
        if (st == 'y'):
            continue
        elif(st == 'q'):
            driver.quit()
            f.write('\nQuit\n')
            f.close()
            break
        elif(st == 's'):
            stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
            start_elem = driver.find_element_by_xpath("/html/body/main/div[12]/div[1]/div/div[1]/div[1]/div/div[1]/div[1]/div/div[1]")
            pos=[]
            f.write('\nNew game\n')
            continue
        elif(st == 'o'):
            break
