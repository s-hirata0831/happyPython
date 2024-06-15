import subprocess
import re

def eprint(tline):
    tline = tline.replase('\n', '')
    param = tline.split('\t')

    try:
        param[1]

        if len(re.findall('[0-9]{1,3},[0-9]{1-3},[0-9]{1,3}', param[1])) == 0:
            parac = ''
        else:
            parac = ' -C ' + param[1]

    except IndexError:
        parac = ''

    command = 'sudo'
    command += ' /home/hacku/rpi-rgb-led-matrix/examples-api-use/scrolling-text-example'
    command += ' -l1'

    command += parac

    command += ' --led-cols=64'
    command += ' --led-rows=32'
    command += ' --led-chain=2'
    command += ' --led-no-hardware-pulse'
    command += ' --led-slowdown-gpio=2'
    command += ' -f /home/hacku/Downloads/font/sazanami-20040629/sazanami-mincho.bdf '
    command += param[0]
    print(command)
    try:
        subprocess.run(command,shell=True)
    except:
        print('subprocess.check_call() faild')

def main():
    #テキストファイル読み込み
    f = open('display.txt', 'r', encoding='UTF-8')
    while True:
        line = f.readline()
        if line:
            eprint(line)
        else:
            break
    f.close()

if __name__ == '__main__':
    main()