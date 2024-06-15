import subprocess
import re
import requests, bs4

def eprint(tline):
    tline = tline.replace('\n', '')
    param = tline.split('\t')

    #文字色のパラメータ RGB値
    try:
        param[1]

        if len(re.findall('[0-9]{1,3},[0-9]{1-3},[0-9]{1,3}', param[1])) == 0:
            parac = ''
        else:
            parac = ' -C' + param[1]

    except IndexError:
        parac = ''

    #スクロール速度のパラメータ
    try:
        param[2]

        if len(re.findall('[0-9]{1,2}', param[2])) == 0:
            paras = ''
        else:
            paras = ' -s' + param[2]
    except IndexError:
        paras = ''

    #背景色のパラメータ
    try:
        param[3]

        if len(re.findall('[0-9]{1,3},[0-9]{1,3},[0-9]{1,3}', param[3])) == 0:
            parab = ''
        else:
            parab = ' -B' + param[3]
    except IndexError:
        parab = ''

    command = 'sudo'
    command += ' /home/hacku/rpi-rgb-led-matrix/examples-api-use/scrolling-text-example'
    command += ' -l1'
    command += ' -s4'
    command += ' -C0,255,255'

    command += parac

    command += ' --led-cols=64'
    command += ' --led-rows=32'
    command += ' --led-chain=2'
    command += ' --led-no-hardware-pulse'
    command += ' --led-slowdown-gpio=4'
    command += ' -f /home/hacku/Downloads/font/sazanami-20040629/sazanami-mincho.bdf '
    command += param[0]
    print(command)
    try:
        subprocess.run(command,shell=True)
    except:
        print('subprocess.check_call() faild')

def news():
    res = requests.get('https://www3.nhk.or.jp/news/catnew.html')
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.content, "html.parser")
    elems = soup.select('em.title')

    l = 0

    for elem in elems:
        nwt = '〜NEWS〜 '
        nwt += elem.getText().replace('\n', '') + '\t255,255,255\t2'
        eprint(nwt)
        l += 1
        if l > 2:
            break

def weather():
    res = requests.get('https://tenki.jp/forecast/6/29/6120/26202/')
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.content, "html.parser")
    elems = soup.select('div.forecast-days-wrap')

    weather = '天気予報 '

    for elem in elems:
        weather += elem.getText()

    #取得したテキストを整形
    weather = weather.replace(u'\xa0', '')
    weather = weather.replace('\n', ' ')
    weather = weather.replace('  ', ' ')
    weather = re.sub(' {2,4}', ' ', weather)
    weather = re.sub(r'降水確率 (.+?) (.+?) (.+?) (.+?) ', '降水確率 00-06(\1) 06-12(\2) 12-18(\3) 18-24(\4) ', weather)
    weather = weather.replace('時間 00-06 06-12 12-18 18-24 ', '')
    weather = weather.replace('(','(')
    weather = weather.replace(')',')')
    weather += ' :tenki.jp提供'
    weather += '\t255,255,255\t2'

    eprint(weather)

def main():
    #テキストファイル読み込み
    f = open('display.txt', 'r', encoding='UTF-8')
    while True:
        line = f.readline()

        if line:
            if '[NEWS]' in line:
                news()
            else:
                eprint(line)
        else:
            break
    f.close()

if __name__ == '__main__':
    while True:
        command = 'sudo'
        command += ' /home/hacku/rpi-rgb-led-matrix/examples-api-use/demo'
        command += ' -D 1'
        command += ' --led-cols=64'
        command += ' --led-rows=32'
        command += ' --led-chain=2'
        command += ' --led-no-hardware-pulse'
        command += ' --led-slowdown-gpio=4'
        command += ' /home/hacku/rpi-rgb-led-matrix/examples-api-use/runtext.ppm'
        print(command)
        main()
