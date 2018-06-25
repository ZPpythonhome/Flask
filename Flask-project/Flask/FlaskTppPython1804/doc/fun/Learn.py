import random
from time import sleep, time


def total_time(fun):

    def f(*args, **kwargs):
        before_time = time()
        fun(*args, **kwargs)
        after_time = time()
        print(after_time-before_time)
    return f


def sum():
    sleep(1)
    print(1 + 1)
    print("加法好难啊，听说1+1=3")


@total_time
def sub(a, b, c=10):
    sleep(2)
    print("减法好复杂，减不明白", str(a - b -c))


def control(salt):
    def can_play(fun):

        def f(*args, **kwargs):

            if random.randrange(100 * salt) > 90:
                fun(*args, **kwargs)
            else:
                print("作业没写完，回去写作业，写完睡觉")
        return f
    return can_play


@control(10)
def play_game():

    sleep(1)

    print("玩游戏了，好开心啊")


if __name__ == '__main__':
    # before_time = time()
    # sum()
    # after_time = time()
    # total_time = after_time - before_time
    #
    # print(total_time)

    # sub(5, 2, c=5)
    play_game()
