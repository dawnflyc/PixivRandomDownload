import random
import re
import sys
import threading
import time
from typing import Optional, Callable, Any, Iterable, Mapping

import core


class thread_find(threading.Thread):
    name = None
    number = 0
    r18 = False

    def __init__(self, name, number, r18=False) -> None:
        threading.Thread.__init__(self)
        self.name = name
        self.number = number
        self.r18 = r18

    def filter(self, ret) -> None:
        result = len(re.findall('R-18', str(ret.content))) > 0
        if not result:
            print('...')
        return result

    def run(self) -> None:
        print(self.name + '\t开始工作')
        suc = 0
        while 1:
            if suc != self.number:
                num = random.randint(0, 9999999)
                num_str = str(num)
                if core.find(num_str, 'image_r', self.filter):
                    suc += 1
                    print(self.name+'已完成'+str(suc)+'条任务')


if __name__ == '__main__':
    if len(sys.argv) > 2:
        num_1 = sys.argv[1]
        num_2 = sys.argv[2]
        num_3 = ''
        if len(sys.argv) > 3:
            num_3 = sys.argv[3]
        if num_1.isdigit() and num_2.isdigit():
            threads = list()
            n = range(int(num_2))
            for i in n:
                thread = None
                if num_3 == '18':
                    thread = thread_find('线程_' + str(i), number=int(num_1), r18=True)
                else:
                    thread = thread_find('线程_' + str(i), number=int(num_1))
                thread.start()
                threads.append(thread)

            while 1:
                if len(threads) > 0:
                    for i in range(len(threads)):
                        if not threads[i].is_alive():
                            threads.remove(threads[i])
                            break
                        time.sleep(1)

                else:
                    break
