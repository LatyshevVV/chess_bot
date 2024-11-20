from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from stockfish import Stockfish
from datetime import datetime
import random

paramsfish = {'Write Debug Log': 'false',
                  'Contempt': 0, 'Min Split Depth': 0, 'Threads': 2,
                  'Ponder': 'true', 'Hash': 16, 'MultiPV': 1,
                  'Skill Level': 20, 'Move Overhead': 30,
                  'Minimum Thinking Time': 20, 'Slow Mover': 80,
                  'UCI_Chess960': 'false'}

stockfish = Stockfish("C:\Program Files\stockfish-10-win\Windows\stockfish_10_x64.exe",
                      depth = 15, params = paramsfish)

global ot #pixel offset
ot = 102

global dict1
dict1 = {'a':'1', 'b':'2', 'c':'3', 'd':'4',
               'e':'5', 'f':'6', 'g':'7', 'h':'8'}

global dict2
dict2 = {1:'a', 2:'b', 3:'c', 4:'d',
               5:'e', 6:'f', 7:'g', 8:'h'}
               

def make_move(st,worb):
    action = webdriver.ActionChains(driver)
    st1='0'+dict1[st[0]]+'0'+st[1]
    f.write('make_move st1= '+st1+'\n')
    elem = driver.find_element_by_class_name("square-"+st1)
    action.move_to_element(elem)
    action.click()
    if worb == 'w':
        action.move_by_offset((ord(st[2])-ord(st[0]))*ot , (int(st[1])-int(st[3]))*ot)
    else:
        action.move_by_offset((ord(st[0])-ord(st[2]))*ot , (int(st[3])-int(st[1]))*ot)
    action.click()
    action.perform()

def get_move():
    r=''
    elem = driver.find_elements_by_class_name("move-square")
    for i in range(2):
        s = elem[i].get_attribute('class')
        f.write('get_move s = '+s+'\n')
        t = s.find("-")
        s1 = s[t+1:t+3]
        s2 = s[t+3:t+5]
        n1 = int(s1)
        n2 = int(s2)
        r += dict2[n1]
        r += str(n2)

    if (stockfish.is_move_correct(r) == False):
                r = r[2]+r[3]+r[0]+r[1]

    f.write('get_move r='+r+'\n')

    return r

def WorB():
    try:
        elem = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[3]/div[1]/div[1]')
    except:
        return 'b'
    return 'w'



login = "vadokus1"
#login = "Bagokyc"
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

mode = input("Mode:\n1 - auto\n2 - manual\n")
st=''
while (st != 'y'):
    st = input("Ready to start? y/n\n")

stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
pos=[]
fl = 0
worb = WorB()
stepnum = 0
t=[]
if worb == 'b':
    f.write("\nWe play for Black!\n\n")
else:
    f.write("\nWe play for White!\n\n")


while (True):
    try:
        """
        try:
            elem = driver.find_elements_by_class_name('clock-icon')
            # (elem[0].is_displayed()) and (elem[1].is_displayed())
            print("elem[0] "+str(elem[0].is_displayed())+' ')
            print("elem[1] "+str(elem[1].is_displayed())+'\n')
        except:
            time.sleep(0.001)
        """
        stepnum += 1
        f.write('\n==Turn'+str(stepnum)+'==\n')
        #sector 1
        s_time = time.time()
        if (worb == 'b') and (fl==0):
            #elem = driver.find_element_by_class_name('clock-icon')
            elem = driver.find_element_by_class_name('clock-time-monospace')
            while (elem.is_displayed()):
                time.sleep(0.01)
            move = get_move()
            pos.append(move)
            stockfish.set_position(pos)
            f.write("his "+move+'\n')
            f.write('[')
            for st in pos:
                f.write("'"+st+"', ")
            f.write(']\n')
            fl = 1
        t.append(time.time()-s_time)

        #sector2
        s_time = time.time()
        """
        stockfish.depth = random.randint(1,12)
        td = stockfish.depth/4+random.random()
        if (stepnum > 10) and (stepnum <25):
            time.sleep(td)
        """
        move = stockfish.get_best_move()
        make_move(move,worb)
        pos.append(move)
        stockfish.set_position(pos)
        f.write("my "+move+'\ninfo = '+str(stockfish.info)+'\n')

        #time.sleep(1)
        t.append(time.time()-s_time)

        #sector3
        s_time = time.time()
        try:
            elem = driver.find_element_by_class_name('game-over-button-button')
            elem.click()
            time.sleep(random.randint(7,8))
            if mode == '1':
                raise IOError
        except NoSuchElementException:
            time.sleep(0.01)
        t.append(time.time()-s_time)
            
        
        elem = driver.find_element_by_class_name('clock-icon')
        while (elem.is_displayed()):
            time.sleep(0.01)

        #sector 4
        s_time = time.time()
        move = get_move()
        pos.append(move)
        stockfish.set_position(pos)
        f.write("his "+move+'\n')
        t.append(time.time()-s_time)

        f.write('[')
        for st in pos:
            f.write("'"+st+"', ")
        f.write(']\n')

        #time.sleep(1)

        #sector5
        s_time = time.time()
        try:
            elem = driver.find_element_by_class_name('game-over-button-button')
            elem.click()
            time.sleep(8)
            if mode == '1':
                raise IOError
        except NoSuchElementException:
            time.sleep(0.01)
        t.append(time.time()-s_time)
    except IOError:
        fl = 0
        worb = WorB()
        stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        pos=[]
        f.write('\nNew game '+str(datetime.now())+'\n\n\n')
        continue
    except:
        f.write('Time :\n')
        f.write('\nQuit\n')
        for i in range(5):
            t[i] = t[i]/stepnum
            f.write('sector'+str(i+1)+' = '+str(t[i])+'\n')
        f.close()
        f = open('log.txt', 'a')
        st = input("Ready?\ny-continue\ns-new game\nq-quit\no-otl\n")
        if (st == 'y'):
            continue
        elif(st == 'q'):
            driver.quit()
            break
        elif(st == 's'):
            fl = 0
            worb = WorB()
            stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
            pos=[]
            f.write('\nNew game\n\n\n')
            continue
        elif(st == 'o'):
            break
