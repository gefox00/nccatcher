import PySimpleGUI as Pg

layout = [[Pg.Text('')],
          [Pg.Text('名称'), Pg.Input(), Pg.Text('装備箇所'), Pg.Input(), Pg.Text('タイミング'), Pg.Input(),
           Pg.Text(''), Pg.Input()]]

window = Pg.Window(title='', layout=layout)

end_flag = True

while end_flag:
    event, values = window.read()

    match event:
        case "":
            pass
        case Pg.WIN_CLOSED:
            end_flag = False
        case _:
            end_flag = False
