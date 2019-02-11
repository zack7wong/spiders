from time import sleep

from scheduler import Scheduler
from db import MysqlClient

def main():
    print('程序开始运行。。')
    s = Scheduler()
    s.run()

if __name__ == '__main__':
   main()

