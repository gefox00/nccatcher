class nsc:
    row_template = {'name': '',
                    'word': '',
                    'pattern': {'eye': '', 'brown': '', 'mouth': ''},
                    'effect': '',
                    'effect_time': '',
                    'voice': '',
                    'layer': ''
                    }
    def __init__(self, stand):
        self.stand_pic = stand
        pass

    def set_command_voice(self, rows: {}):
        chara "2,chara/[スラッグ]目普通口いぎぎ眉怒り.png,rc,10,100,255"
        chara "0,face/[スラッグ]目普通口いぎぎ眉怒り.png,10,100"
        dwave 0, "06/nodata.wav"
        [スラッグ]「私の姉妹に手を出させないよ」 \
        chara "2,chara/[スラッグ]目普通口いぎぎ眉怒り.png,rc,10,100,190"


        set_pre_stand = f'chara "{layer},chara/{stand_pic},{pos},{effect},{ef_time},255"'
        set_face = f'chara 0 "{face_pic},{effect},{ef_time}"'
        set_voice = f'dwave 0,"{voice}"'
        set_word = f'[{name}]{word}'
        set_after_stand =  f'chara "{layer},chara/{stand_pic},{pos},{effect},{ef_time},100"'
        pass