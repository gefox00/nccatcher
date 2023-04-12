from tkinter import filedialog
from tkinter import messagebox
import PySimpleGUI as sg
import pyperclip, csv, os


class mnmuch:
    dbpath = 'data.csv'
    data = []
    outdict = {}
    outrow = ''

    def __init__(self, name: str):
        try:
            with open(self.dbpath, 'r', encoding='utf8') as r:
                for i in csv.reader(r):
                    self.data.append(i)
                    self.outdict[i[0]] = f'{i[5]} {i[6]}'
                self.outrow = self.outdict[name]
        except:
            self.outrow = 'nodata'
            self.namemuch(name)

    def namemuch(self, name: str):

        for i in self.data:
            if i[0] in name:
                self.outrow = f'{i[5]} {i[6]}'


class charsheet:
    mpdat = []  # 読み込んだかけらを名前と内容に分けた配列が入る
    mntxt = []  # １行ずつ読み込んだマニューバの文字列が入る
    mndat = []  # マニューバを各項目で分割したデータ配列が入る
    pntxt = ""  # 名前が入る
    potxt = ""  # ポジションが入る
    cmtxt = ""  # メインクラスが入る
    cstxt = ""  # サブクラスが入る
    antxt = ""  # 暗示が入る
    intxt = ""  # 行動値が入る
    lptxt = ""  # 寵愛点が入る
    oltxt = ""  # 年齢が入る
    bupnt = ""  # 武装レベル
    hepnt = ""  # 変異レベル
    kapnt = ""  # 改造レベル
    memotxt = ""  # シートのメモが入る
    dxcom = ''
    pts = {}
    chptxt = ""
    fp = ""

    def __init__(self, path: str, dx: bool = False):
        with open(path, 'r', encoding='utf-8-sig') as r:
            self.fp = r.read().replace('　', ' ')
        self.mn()
        self.mp()
        self.pd()
        self.plv()
        self.memo()
        self.mns()
        if dx:
            self.dx_process()
        else:
            self.chp()

    def dx_process(self):
        self.chptxt = 'NM 未練表\n1NC 行動判定\n1NC+1 行動判定\n1NC+2 行動判定\n1NC+3 行動判定\n'
        self.chptxt += '1NC 対話・狂気判定\n1NC+1 対話・狂気判定\n1NC+2 対話・狂気判定\n1NC+3 対話・狂気判定\n'
        self.chptxt += '1NA 攻撃判定\n1NA+1 攻撃判定\n1NA+2 攻撃判定\n1NA+3 攻撃判定\n'
        for i in self.mndat:
            much = mnmuch(i[1]).outrow
            line = f'{i[0]}:{i[1]}:{i[2]}:{i[3]}:{i[4]}:{much}\n'
            self.chptxt += line

    def chp(self):
        self.chptxt = 'NM 未練表\n1NC 行動判定\n1NC+1 行動判定\n1NC+2 行動判定\n1NC+3 行動判定\n'
        self.chptxt += '1NC 対話・狂気判定\n1NC+1 対話・狂気判定\n1NC+2 対話・狂気判定\n1NC+3 対話・狂気判定\n'
        self.chptxt += '1NA 攻撃判定\n1NA+1 攻撃判定\n1NA+2 攻撃判定\n1NA+3 攻撃判定\n'
        for i in self.mntxt:
            self.chptxt += str(i) + '\n'

    def plv(self):
        for i in self.fp.splitlines()[18:]:
            if '=合計=' in i:
                pnt = i.replace('   ', ' ').split(' ')
                self.bupnt = pnt[1]
                self.hepnt = pnt[2]
                self.kapnt = pnt[3]
                break

    def mp(self):
        data = str(self.fp).replace('   ', '|').replace('  ', '|').replace('|||', '|').replace('||', '|').splitlines()
        for i in data[18:]:
            if len(i) == 0:
                break
            line = i.split('|')
            if len(line) == 1:
                self.mpdat.append([line[0], 'NO DATA'])
            else:
                self.mpdat.append(line)

    def mn(self):
        data = self.fp.splitlines()
        mnbool = False
        lines = []
        for i in data[18:]:
            if '[部位]' in i:
                mnbool = True
            if len(i) == 0:
                mnbool = False
            if mnbool and not '[部位]' in i and not i[:2] == '[]':
                lines.append(i.replace(' ', ''))
        self.mntxt = lines

    def pd(self):

        data = self.fp.splitlines()[:19]
        self.pntxt = data[1].split('：')[1]
        self.oltxt = data[4].split('：')[1]
        self.intxt = data[12].split('：')[1]
        self.potxt = data[9].split('：')[1]
        if ' / ' in data[10]:
            self.cmtxt = data[10].split('：')[1].replace(' / ', ':').split(':')[0]
            self.cstxt = data[10].split('：')[1].replace(' / ', ':').split(':')[1]

        self.antxt = data[16].split('：')[1]
        for i in self.fp.splitlines():
            if '寵愛点：' in i:
                self.lptxt = i.split('：')[1].replace('点', '')

    def memo(self):
        data = self.fp.splitlines()
        for c, i in enumerate(data):
            if 'メモ：' in i:
                memo = data[c:]
                temp = ''
                for j in memo:
                    temp += str(j + '\n')
                self.memotxt = temp

    def mns(self):
        temp = []
        dict = {'[頭]': 0, '[腕]': 0, '[胴]': 0, '[脚]': 0, '[ポジション]': 0, '[メインクラス]': 0, '[サブクラス]': 0}
        for i in self.mntxt:
            temp.append(i.replace(']', ']:').split(':'))
        self.mndat = temp
        for i in temp:
            if len(i[0]) > 0:
                dict[i[0]] += 1
        self.pts = dict

    def Clip_Out(self, rtn: bool = False):
        data = {}
        mpd = ''
        mnd = ''
        for i in self.mpdat:
            mpd += f'{i[0]}:{i[1]}\n'
        for i in self.mntxt:
            mnd += i + '\n'
        memodat = f'カルマ\nシナリオ:\n戦闘:\n\nきおくのかけら一覧\n{mpd}\nマニューバ一覧\n{mnd}\n破損パーツ一覧\n\nその他\n{self.memotxt}'
        data.setdefault('kind', 'character')
        status = [{'label': '記憶のかけら', 'max': len(self.mpdat)},
                  {'label': '頭10', 'value': self.pts['[頭]'], 'max': self.pts['[頭]']},
                  {'label': '腕 9', 'value': self.pts['[腕]'], 'max': self.pts['[腕]']},
                  {'label': '胴 8', 'value': self.pts['[胴]'], 'max': self.pts['[胴]']},
                  {'label': '脚 7', 'value': self.pts['[脚]'], 'max': self.pts['[脚]']},
                  {'label': 'PC1への未練', 'value': 3, 'max': 4},
                  {'label': 'PC2への未練', 'value': 3, 'max': 4},
                  {'label': 'PC3への未練', 'value': 3, 'max': 4},
                  {'label': 'PC4への未練', 'value': 3, 'max': 4},
                  {'label': 'たからものへの未練', 'value': 3, 'max': 4}]
        params = [{'label': self.potxt, 'value': self.potxt},
                  {'label': self.cmtxt, 'value': self.cmtxt},
                  {'label': self.cstxt, 'value': self.cstxt},
                  {'label': '武装', 'value': f'{self.bupnt}/9'},
                  {'label': '変異', 'value': f'{self.hepnt}/9'},
                  {'label': '改造', 'value': f'{self.kapnt}/9'},
                  {'label': '寵愛', 'value': self.lptxt},
                  {'label': '享年', 'value': self.oltxt}]
        data.setdefault('data', {'name': self.pntxt,
                                 'initiative': int(self.intxt),
                                 'memo': memodat,
                                 'commands': self.chptxt,
                                 'status': status,
                                 'params': params})
        pyperclip.copy(str(data).replace('\'', '"'))
        if rtn:
            return str(data).replace('\'', '"')


fle = ''
sg.theme('Default1')
##################################################
# ウィンドウに配置するコンポーネント設定
##################################################
layout = [
    [sg.Text('キャラシのテキストファイルまたはキャラシのURLを指定してください')],
    [sg.Input(size=(80, 1), key='tb_open'), sg.Button('参照', key='btn_openpath')],
    [sg.Button('変換開始', key='bt_start')]
    , [sg.Output(size=(83, 20), key='log')]
]
window = sg.Window('キャラシコンバーター', layout)
while True:
    event, values = window.read()
    loaddata = {}
    ##################################################
    # ×ボタンクリック時の動作
    ##################################################
    if event == sg.WIN_CLOSED or event == 'キャンセル':
        break
    elif event == 'btn_openpath':
        typ = [('テキストファイル', '*.txt')]
        dir = os.getcwd()
        fle = filedialog.askopenfilename(filetypes=typ, initialdir=dir)
        if len(fle) > 0:
            with open(fle, 'r', encoding='utf8') as r:
                chdat = r.read()
                if not 'タイトル：' in chdat:
                    messagebox.showinfo('処理できません', f'非対応ファイルです')
                else:
                    window['tb_open'].update(fle)
    elif event == 'btn_savepath':
        typ = [('テキストファイル', '*.txt')]
        text = filedialog.asksaveasfile(filetypes=typ)
        text.write('ss')
    elif event == 'bt_start':
        if len(fle) > 0:
            target = window['tb_open'].get()
            if not target[-4:] == '.txt':
                target += '.txt'
            d = charsheet(target, dx=True)
            window['log'].update(d.Clip_Out(rtn=True))
            messagebox.showinfo('変換完了',
                                f'{d.pntxt}のココフォリア用駒データをクリップボードに書き込みました\nココフォリアの盤面を右クリックして貼り付けを選択してください')
