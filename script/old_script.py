import pyperclip

class charsheet:
    mpdat = []#読み込んだかけらを名前と内容に分けた配列が入る
    mntxt = []#１行ずつ読み込んだマニューバの文字列が入る
    mndat = []#マニューバを各項目で分割したデータ配列が入る
    pntxt = ""#名前が入る
    potxt = ""#ポジションが入る
    cmtxt = ""#メインクラスが入る
    cstxt = ""#サブクラスが入る
    antxt = ""#暗示が入る
    intxt = ""#行動値が入る
    lptxt = ""#寵愛点が入る
    oltxt = ""#年齢が入る
    bupnt = ""#武装レベル
    hepnt = ""#変異レベル
    kapnt = ""#改造レベル
    memotxt = ""#シートのメモが入る
    pts = {}
    chp = ""
    fp = ""
    def __init__(self,path:str):
        with open(path,'r',encoding='utf-8-sig')as r:
            self.fp = r.read().replace('　',' ')
        self.mn()
        self.mp()
        self.pd()
        self.plv()
        self.memo()
        self.mns()
        self.chp()

    def chp(self):
        self.chp = '1NC 行動判定\n1NC +1 行動判定\n1NC +2 行動判定\n1NC +3 行動判定\n'
        self.chp += '1NC 対話判定\n1NC +1 対話判定\n1NC +2 対話判定\n1NC +3 対話判定\n'
        self.chp += '1NC 狂気判定\n1NC +1 狂気判定\n1NC +2 狂気判定\n1NC +3 狂気判定\n'
        self.chp += '1NA 攻撃判定\n1NA +1 攻撃判定\n1NA +2 攻撃判定\n1NA +3 攻撃判定\n'
        for i in self.mntxt:
            self.chp += str(i) + '\n'

    def plv(self):
        for i in self.fp.splitlines()[18:]:
            if '=合計=' in i:
                pnt = i.replace('   ',' ').split(' ')
                self.bupnt = pnt[1]
                self.hepnt = pnt[2]
                self.kapnt = pnt[3]
                break

    def mp(self):
        data = str(self.fp).replace('   ','|').replace('  ','|').replace('|||','|').replace('||','|').splitlines()
        for i in data[18:]:
            if len(i)==0:
                break
            line = i.split('|')
            if len(line) == 1:
                self.mpdat.append([line[0],'NO DATA'])
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
                lines.append(i.replace(' ',''))
        self.mntxt = lines
    def pd(self):

        data = self.fp.splitlines()[:19]
        self.pntxt = data[1].split('：')[1]
        self.oltxt = data[4].split('：')[1]
        self.intxt = data[12].split('：')[1]
        self.potxt = data[9].split('：')[1]
        self.cmtxt = data[10].split('：')[1].replace(' / ',':').split(':')[0]
        self.cstxt = data[10].split('：')[1].replace(' / ', ':').split(':')[1]
        self.antxt = data[16].split('：')[1]
        for i in self.fp.splitlines():
            if '寵愛点：' in i:
                self.lptxt = i.split('：')[1].replace('点','')

    def memo(self):
        data = self.fp.splitlines()
        for c,i in enumerate(data):
            if 'メモ：' in i:
                memo = data[c:]
                temp = ''
                for j in memo:
                    temp += str(j + '\n')
                self.memotxt = temp

    def mns(self):
        temp = []
        dict = {'[頭]':0,'[腕]':0,'[胴]':0,'[脚]':0,'[ポジション]':0,'[メインクラス]':0,'[サブクラス]':0}
        for i in self.mntxt:
            temp.append(i.replace(']',']:').split(':'))
        self.mndat = temp
        for i in temp:
            if len(i[0]) > 0:
                dict[i[0]] += 1
        self.pts = dict
    def Clip_Out(self):
        data = {}
        mpd = ''
        mnd = ''
        for i in self.mpdat:
            mpd += f'{i[0]}:{i[1]}\n'
        for i in self.mntxt:
            mnd += i + '\n'
        memodat =   f'カルマ\nシナリオ:\n戦闘:\n\nきおくのかけら一覧\n{mpd}\nマニューバ一覧\n{mnd}\n破損パーツ一覧\n\nその他\n{self.memotxt}'
        data.setdefault('kind', 'character')
        status = [{'label': '記憶のかけら', 'max': len(self.mpdat)},
                  {'label': '頭D10-10', 'value': self.pts['[頭]'], 'max': self.pts['[頭]']},
                  {'label': '腕D10-09', 'value': self.pts['[腕]'], 'max': self.pts['[腕]']},
                  {'label': '胴D10-08', 'value': self.pts['[胴]'], 'max': self.pts['[胴]']},
                  {'label': '脚D10-07', 'value': self.pts['[脚]'], 'max': self.pts['[脚]']},
                  {'label': 'PC1への未練', 'value': 3, 'max': 4},
                  {'label': 'PC2への未練', 'value': 3, 'max': 4},
                  {'label': 'PC3への未練', 'value': 3, 'max': 4},
                  {'label': 'PC4への未練', 'value': 3, 'max': 4},
                  {'label': 'たからものへの未練', 'value': 3, 'max': 4}]
        params = [{'label': self.potxt, 'value': self.potxt},
                  {'label': self.cmtxt, 'value': self.cmtxt},
                  {'label': self.cstxt, 'value': self.cstxt},
                  {'label': '武装', 'value': self.bupnt},
                  {'label': '変異', 'value': self.hepnt},
                  {'label': '改造', 'value': self.kapnt},
                  {'label': '寵愛', 'value': self.lptxt}]
        data.setdefault('data', {'name': self.pntxt,
                                 'initiative': int(self.intxt),
                                 'memo': memodat,
                                 'commands':self.chp,
                                 'status': status,
                                 'params': params})
        pyperclip.copy(str(data).replace('\'', '"'))