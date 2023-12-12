from tkinter import * # type: ignore
from time import sleep
from random import randint
from os import system
import threading

def cls():
    try:
        system('cls')
    except:
        system('clear')

def recomecar():
    global ponteiro, score, tirarUltimo, fim, altXlarSnake, posicaoPlayerXY, posicoesSnake, comecou, textoScore, textoTempo, pausado, loopTempo, resetar, textoRecord

    if not fim and not inicio and resetar:
        textoTempo = Label(janela, fg='black', bg='gray95', text=f'TIME: {0:02.0f}:{0:02.0f}:{0:02.0f}', font=('', 40))
        textoTempo.place(x=0, y=-5)
        textoScore = Label(janela, fg='DeepSkyBlue2', bg='gray95', text=f'SCORE: {0:03.0f}', font=('', 40))
        textoScore.place(x=larguraTela/2-160, y=-5)
        textoRecord = Label(janela, fg='black', bg='gray95', text=f'RECORDE: {record:03.0f}', font=('', 40))
        textoRecord.place(x=larguraTela-385, y=-5)
        fundo = Label(janela, bg=corFundo)
        fundo.place(x=0, y=50, height=alturaTela, width=larguraTela)
        try:
            txtPG.destroy()
            txtPress.destroy()
            txtCPress.destroy()
        except:
            pass
        ponteiro = [50, 0]
        tirarUltimo = True
        loopTempo = False
        resetar = False
        fim = True
        pausado = False
        score = 0
        tamanhoSnakeInicial = 3
        altXlarSnake = 48
        if comecou:
            for x in posicoesSnake: # type: ignore
                x[0].destroy()
        comecou = False
        posicoesSnake = []
        for a in range(tamanhoSnakeInicial+1, 1, -1):
            quadradoVerde = Label(janela, bg=corSnake)
            quadradoVerde.place(x=802-a*50, y=452, height=altXlarSnake, width=altXlarSnake)
            posicoesSnake.append([quadradoVerde, 802-a*50, 452])
        posicaoPlayerXY = [posicoesSnake[len(posicoesSnake)-1][1], posicoesSnake[len(posicoesSnake)-1][2]]
        criarMaca()
        janela.bind('w', lambda e: mudarPosicao([-50, 1], 'w'))      # Cima
    janela.bind('<Up>', lambda e: mudarPosicao([-50, 1], 'w'))   # Cima
    janela.bind('s', lambda e: mudarPosicao([50, 1], 's'))       # Baixo
    janela.bind('<Down>', lambda e: mudarPosicao([50, 1], 's'))  # Baixo
    janela.bind('d', lambda e: mudarPosicao([50, 0], 'd'))       # Direita
    janela.bind('<Right>', lambda e: mudarPosicao([50, 0], 'd')) # Direita
    janela.bind('a', lambda e: mudarPosicao([-50, 0], 'a'))      # Esquerda
    janela.bind('<Left>', lambda e: mudarPosicao([-50, 0], 'a')) # Esquerda

def jogo():
    global score, tirarUltimo, textoScore, fim, horas, minutos, segundos, loopTempo, thread3, resetar, record

    def pausar():
        global pausado

        if comecou:
            pausado = False if pausado == True else True

    def mostrarPG(pg):
        global txtPG

        if pg == 'g':
            txtPG = Label(janela, text='VOCÊ GANHOU!', bg=corFundo, fg='green3', font=('Impact', 50))
        else:
            txtPG = Label(janela, text='VOCÊ PERDEU!', bg=corFundo, fg='red', font=('Impact', 50))
        txtPG.place(x=larguraTela/2-183, y=alturaTela/2-25)
        txtPress = Label(janela, text='PRESS      TO RESTART', bg=corFundo, fg='white', font=('Impact', 30))
        txtRPress = Label(janela, text='R', bg=corFundo, fg='brown4', font=('Impact', 30))
        if resetar == True:
            txtPress.place(x=larguraTela/2-164, y=(alturaTela/2)+(alturaTela/2)/2)
            txtRPress.place(x=larguraTela/2-54, y=(alturaTela/2)+(alturaTela/2)/2)
            while True:
                sleep(0.5)
                if not fim:
                    txtPress['fg'] = 'white' if txtPress['fg'] == corFundo else corFundo
                    txtRPress['fg'] = 'brown4' if txtRPress['fg'] == corFundo else corFundo
                else:
                    break

    def tempo():
        global horas, minutos, segundos, thread3

        while True:
            sleep(1)
            if not fim:
                break
            elif pausado:
                continue
            segundos += 1
            if segundos == 60:
                segundos = 0
                minutos += 1
            if minutos == 60:
                minutos = 0
                horas += 1
            textoTempo['text'] = f'TIME: {horas:02.0f}:{minutos:02.0f}:{segundos:02.0f}'


    janela.bind('p', lambda e: pausar())
    while fim:
        if not loopTempo:
            horas = 0
            minutos = 0
            segundos = 0
            loopTempo = True
            thread3 = threading.Thread(target=tempo)
            thread3.daemon = True
            thread3.start()
        sleep(velocidade)
        if score+3 == (int((larguraTela-50)/50)*(int((alturaTela-50)/50))):
            fim = False
            janela.bind('r', lambda e: recomecar()) # Recomecar
            mostrarPG('g')
            sleep(1.1)
            resetar = True
            mostrarPG('g')
            continue
        if pausado:
            continue
        posicoesSnake[-1][0]['image'] = ''
        posicoesSnake[-1][0]['bg'] = corSnake
        quadradoVerde = Label(janela, bg=corSnake)
        quadradoVerde.place(x=posicaoPlayerXY[0], y=posicaoPlayerXY[1], height=48, width=48)
        posicaoPlayerXY[ponteiro[1]] += ponteiro[0]
        if verificarPerda():
            fim = False
            janela.bind('r', lambda e: recomecar()) # Recomecar
            mostrarPG('p')
            sleep(1.1)
            resetar = True
            mostrarPG('p')
            break
        elif tirarUltimo:
            posicoesSnake[0][0].destroy()
            del posicoesSnake[0]
        tirarUltimo = True
        if posicaoPlayerXY == [xMaca, yMaca]:
            maca.destroy()
            score += 1
            tirarUltimo = False
            criarMaca()
            record = score if score > record else record
            textoScore['text'] = f'SCORE: {score:03.0f}'
            textoRecord['text'] = f'RECORDE: {record:03.0f}'

        quadradoVerde.place(x=posicaoPlayerXY[0], y=posicaoPlayerXY[1], height=48, width=48)
        posicoesSnake.append([quadradoVerde, posicaoPlayerXY[0], posicaoPlayerXY[1]])
        try:
            for x in posicoesSnake[:-2]:
                if posicaoPlayerXY == [x[1], x[2]]:
                    posicoesSnake[-1][0]['bg'] = corSnake
                    break
            else:
                posicoesSnake[-1][0]['bg'] = corFundo
        except:
            pass
        posicoesSnake[-1][0]['image'] = direcaoImg

def criarMaca():
    global xMaca, yMaca, maca

    maca = Label(janela, image=imgMaca, bg=corFundo)
    while True:
        if score == 0:
            xMaca = 902
            yMaca = 452
            break
        xMaca = randint(0, int((larguraTela-50)/50)) * 50 + 2
        yMaca = randint(1, int((alturaTela-50)/50)) * 50 + 2
        for i in posicoesSnake:
            if [i[1], i[2]] == [xMaca, yMaca]:
                break
        else:
            break
    maca.place(x=xMaca, y=yMaca, height=altXlarSnake, width=altXlarSnake)

def verificarPerda():
    global direcaoImg

    if posicaoPlayerXY[0] > larguraTela-48 or posicaoPlayerXY[0] < 2:
        if modoJogo != 'atravessar' and modoJogo != 'livre':
            return True
        posicaoPlayerXY[0] = larguraTela-48 if posicaoPlayerXY[0] < 2 else 2
    elif posicaoPlayerXY[1] > alturaTela-48 or posicaoPlayerXY[1] < 52:
        if modoJogo != 'atravessar' and modoJogo != 'livre':
            return True
        posicaoPlayerXY[1] = alturaTela-48 if posicaoPlayerXY[1] < 52 else 52
    for i in posicoesSnake:
        if [i[1], i[2]] == posicaoPlayerXY:
            if posicoesSnake[-2][1:] == posicaoPlayerXY and ponteiro[1] == 0:
                direcaoImg = PhotoImage(file='snakeDireita.png') if ponteiro[0] == -50 else PhotoImage(file='snakeEsquerda.png')
                ponteiro[0] *= -1
                posicaoPlayerXY[0] += ponteiro[0]
                break
            elif posicoesSnake[-2][1:] == posicaoPlayerXY and ponteiro[1] == 1:
                direcaoImg = PhotoImage(file='snakeBaixo.png') if ponteiro[0] == -50 else PhotoImage(file='snakeCima.png')
                ponteiro[0] *= -1
                posicaoPlayerXY[1] += ponteiro[0]
                break
            if modoJogo != 'livre':
                i[0]['bg'] = 'orange'
                return True
    else:
        return False

def mudarPosicao(lista, tecla):
    global ponteiro, comecou

    def verificarTecla():
        global direcaoImg

        if tecla == 'w':
            direcaoImg = PhotoImage(file='snakeCima.png')
        elif tecla == 's':
            direcaoImg = PhotoImage(file='snakeBaixo.png')
        elif tecla == 'd':
            direcaoImg = PhotoImage(file='snakeDireita.png')
        elif tecla == 'a':
            direcaoImg = PhotoImage(file='snakeEsquerda.png')

    if tecla == 'a' and not comecou:
        return
    elif not comecou and not inicio:
        verificarTecla()
        comecou = True
        thread1 = threading.Thread(target=jogo)
        thread1.daemon = True
        thread1.start()
    if not inicio:
        if ponteiro[1] == lista[1] and (ponteiro[0] == lista[0] or ponteiro[0] * -1 == lista[0]):
            return
        if not pausado:
            verificarTecla()
            ponteiro = lista

def inicial():
    global inicio, fundo, txtCPress, txtPress, loop, corSnake

    fundo = Label(janela, bg=corFundo)
    fundo.place(x=0, y=0, height=alturaTela, width=larguraTela)

    listaV = []
    lV = ['c', 'v', 'm']
    def stopLoop(i, v):
        global loop, corSnake, velocidade, modoJogo

        if loop and v not in listaV:
            if v == 'c':
                corSnake = infoR[i][1]
                infoR[i][0].place(x=larguraTela/2-55, y=alturaTela/2-250)
            elif v == 'v':
                velocidade = infoR[i][1]
                infoR[i][0].place(x=larguraTela/2-130, y=alturaTela/2-70)
            else:
                modoJogo = infoR[i][1]
                infoR[i][0].place(x=larguraTela/2-130, y=alturaTela/2+135)
            del infoR[i]
            for x in infoR:
                x[0].destroy()
            loop = False
        listaV.append(v)
        for h in lV:
            for y in range(listaV.count(h)-1):
                del listaV[listaV.index(h)]

    loop = True
    while True:
        # Cor
        txtCor = Label(janela, text='QUAL COR DA SNAKE QUER?', bg=corFundo, fg='white', font=('Impact', 30))
        txtCor.place(x=larguraTela/2-235, y=alturaTela/2-350)
        txtG = Label(janela, text='G', bg=corFundo, fg='green2', font=('Impact', 30))
        txtG.place(x=larguraTela/2-255, y=alturaTela/2-250)
        txtR = Label(janela, text='R', bg=corFundo, fg='red', font=('Impact', 30))
        txtR.place(x=larguraTela/2-155, y=alturaTela/2-250)
        txtY = Label(janela, text='Y', bg=corFundo, fg='yellow', font=('Impact', 30))
        txtY.place(x=larguraTela/2-55, y=alturaTela/2-250)
        txtB = Label(janela, text='B', bg=corFundo, fg='blue', font=('Impact', 30))
        txtB.place(x=larguraTela/2+45, y=alturaTela/2-250)
        txtPi = Label(janela, text='P', bg=corFundo, fg='deep pink', font=('Impact', 30))
        txtPi.place(x=larguraTela/2+145, y=alturaTela/2-250)
        infoR = [[txtG, 'green2',], [txtR, 'red'], [txtY, 'yellow'], [txtB, 'blue'], [txtPi, 'deep pink']]
        while loop:
            janela.bind('g', lambda e: stopLoop(0, 'c'))
            janela.bind('r', lambda e: stopLoop(1, 'c'))
            janela.bind('y', lambda e: stopLoop(2, 'c'))
            janela.bind('b', lambda e: stopLoop(3, 'c'))
            janela.bind('p', lambda e: stopLoop(4, 'c'))
            sleep(0.09)
        loop = True
        # Velocidade
        txtVelocidade = Label(janela, text='QUAL VELOCIDADE QUER?', bg=corFundo, fg='white', font=('Impact', 30))
        txtVelocidade.place(x=larguraTela/2-225, y=alturaTela/2-170)
        txtN = Label(janela, text='N - NORMAL', bg=corFundo, fg='gold', font=('Impact', 30))
        txtN.place(x=larguraTela/2-130, y=alturaTela/2-70)
        txtM = Label(janela, text='M - MÉDIA', bg=corFundo, fg='orange', font=('Impact', 30))
        txtM.place(x=larguraTela/2-130, y=alturaTela/2-20)
        txtRr = Label(janela, text='R - RÁPIDA', bg=corFundo, fg='red3', font=('Impact', 30))
        txtRr.place(x=larguraTela/2-130, y=alturaTela/2+30)
        infoR = [[txtN, 0.09], [txtM, 0.07], [txtRr, 0.05]]
        while loop:
            janela.bind('n', lambda e: stopLoop(0, 'v'))
            janela.bind('m', lambda e: stopLoop(1, 'v'))
            janela.bind('r', lambda e: stopLoop(2, 'v'))
        # Modo
        loop = True
        txtM = Label(janela, text='QUAL MODO QUER?', bg=corFundo, fg='white', font=('Impact', 30))
        txtM.place(x=larguraTela/2-178, y=alturaTela/2+35)
        txtN = Label(janela, text='N - NORMAL', bg=corFundo, fg='lawn green', font=('Impact', 30))
        txtN.place(x=larguraTela/2-130, y=alturaTela/2+135)
        txtA = Label(janela, text='A - ATRAVESSAR PAREDES', bg=corFundo, fg='DeepSkyBlue2', font=('Impact', 30))
        txtA.place(x=larguraTela/2-130, y=alturaTela/2+185)
        txtL = Label(janela, text='L - LIVRE', bg=corFundo, fg='cyan', font=('Impact', 30))
        txtL.place(x=larguraTela/2-130, y=alturaTela/2+235)
        infoR = [[txtN, 'normal'], [txtA, 'atravessar'], [txtL, 'livre']]
        while loop:
            janela.bind('n', lambda e: stopLoop(0, 'm'))
            janela.bind('a', lambda e: stopLoop(1, 'm'))
            janela.bind('l', lambda e: stopLoop(2, 'm'))
        listD = [txtCor, txtG, txtR, txtY, txtB, txtVelocidade, txtN, txtM, txtA, txtRr, txtL, txtPi]
        break
    for x in listD:
        x.destroy()

    # press
    txtPress = Label(janela, text='PRESS      TO START', bg=corFundo, fg='white', font=('Impact', 30))
    txtCPress = Label(janela, text='C', bg=corFundo, fg='brown4', font=('Impact', 30))
    txtPress.place(x=larguraTela/2-164, y=(alturaTela/2)+(alturaTela/2)/2)
    txtCPress.place(x=larguraTela/2-54, y=(alturaTela/2)+(alturaTela/2)/2)
    # pause
    txtP = Label(janela, text='P', bg=corFundo, fg='orange', font=('Impact', 50))
    txtPause = Label(janela, text='- PAUSAR', bg=corFundo, fg='white', font=('Impact', 50))
    txtPause.place(x=larguraTela/2-162, y=alturaTela/2-150)
    txtP.place(x=larguraTela/2-200, y=alturaTela/2-150)
    # restart
    txtR = Label(janela, text='R', bg=corFundo, fg='green', font=('Impact', 50))
    txtRecomecar = Label(janela, text='- RESTART', bg=corFundo, fg='white', font=('Impact', 50))
    txtRecomecar.place(x=larguraTela/2-162, y=alturaTela/2-62)
    txtR.place(x=larguraTela/2-200, y=alturaTela/2-62)
    # sair
    txtESC = Label(janela, text='ESC', bg=corFundo, fg='red', font=('Impact', 50))
    txtSair = Label(janela, text='- SAIR', bg=corFundo, fg='white', font=('Impact', 50))
    txtSair.place(x=larguraTela/2-162, y=alturaTela/2+26)
    txtESC.place(x=larguraTela/2-265, y=alturaTela/2+26)

    def comecar():
        global inicio

        if inicio:
            inicio = False
            txtPause.destroy()
            txtRecomecar.destroy()
            txtSair.destroy()
            txtP.destroy()
            txtR.destroy()
            txtESC.destroy()
            fundo.destroy()
            recomecar()
            cls()

    janela.bind('c', lambda e: comecar())
    janela.bind('<Escape>', lambda e: janela.destroy())
    while True:
        sleep(0.5)
        if inicio:
            txtPress['fg'] = 'white' if txtPress['fg'] == corFundo else corFundo
            txtCPress['fg'] = 'brown4' if txtCPress['fg'] == corFundo else corFundo
        else:
            break


janela = Tk()
alturaTela, larguraTela = int(janela.winfo_screenheight()), int(janela.winfo_screenwidth())
janela.geometry(f'{larguraTela}x{alturaTela}+-10+-35')
janela.resizable(False, False)
fim = False
comecou = False
pausado = False
inicio = True
resetar = True
record = 0
corFundo = 'gray7'
imgMaca = PhotoImage(file='maca.png')
direcaoImg = ''
thread2 = threading.Thread(target=inicial)
thread2.daemon = True
thread2.start()


janela.mainloop()
