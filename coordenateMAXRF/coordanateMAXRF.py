import pyautogui, subprocess, time, win32gui, win32con


#print(pyautogui.getActiveWindow())
#print(pyautogui.position())
#print(pyautogui.pixel(837, 348))
#pyautogui.moveTo(100, 200)
#sampleName=findValueBetween(caminho, "_", "_")

#print(sampleName)



def checkStarted(name):
    call = 'TASKLIST /FI "IMAGENAME eq %s.exe"' % name
    output = subprocess.check_output(call)
    return(len(output)>87)

def bWTF(hwnd):
    if hwnd:
        try:
            if(hwnd==minix):
                win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
            else:
                win32gui.ShowWindow(hwnd, win32con.SW_SHOWMAXIMIZED)
            win32gui.SetForegroundWindow(hwnd)
            win32gui.BringWindowToTop(hwnd)
            return True
        except Exception as e:
            print(f"Error bringing window to foreground: {e}")
            return False


def findValueBetween(filename, firstseparator, secondseparator):
    index1 = filename.find(firstseparator)    
    index2 = filename.find(secondseparator)
    offset=len(firstseparator)
        
    if index1 != -1 and index2 != -1:
        value = filename[index1+offset:index2]
        return(value)
    else:
        print("Separator not found in the string.")


def trvlWTAB(num):
    for i in range(num):
        pyautogui.hotkey('tab')

def trvlWshftTAB(num):
    for i in range(num):
        pyautogui.hotkey('shift', 'tab')


def tempoPorPonto(pontos):
    segundosTotal= pontos*(float(detectionTime)+monitorTime+4.5)+sideStepTime*sideSteps+climbTime*upSteps+upSteps*xHalfStepTime
    horas=int(segundosTotal/3600)
    minutos=int((segundosTotal-horas*3600)/60)
    segundos=(segundosTotal-horas*3600-minutos*60)
    return horas, minutos, segundos

teste=-1
testeMINIX=-1
testeADMCA=-1
testeREPTI=-1
monitor=-1

monitorTime=0

# -------------- CAMINHO PARA AS APLICAÇÕES --------------
pathMiniX = #["----/MiniXCtrl.exe"]     Caminho para MiniX
pathADMCA = #["----/ADMCA.exe"]         Caminho para ADMCA
pathRepetier = #["-/RepetierHost.exe"]  Caminho para Repetier

# -------------- PARAMETROS DE MOVIMENTAÇÃO MINI-X --------------
xON_XRAY=  #COORDENADA X DO PIXEL AMARELO DO BOTÃO "HV ON"
yON_XRAY=  #COORDENADA Y DO PIXEL AMARELO DO BOTÃO "HV ON"
xOFF_XRAY=xON_XRAY
yOFF_XRAY=yON_XRAY-30
xEXIT_XRAY=xON_XRAY
yEXIT_XRAY=yON_XRAY+50
xSIM_XRAY=xON_XRAY-140
ySIM_XRAY=yON_XRAY+60
xNAO_XRAY=xON_XRAY-50
yNAO_XRAY=yON_XRAY+60
xOfR_XRAY=xON_XRAY-125
yOfR_XRAY=yON_XRAY-40

# -------------- PARAMETROS DE MOVIMENTAÇÃO ADMCA ---------------
xCONNECT_ADMCA=  #COORDENADA X DO PIXEL VERDE DE CONECTADO
yCONNECTG_ADMCA=  #COORDENADA Y DO PIXEL VERDE DE CONECTADO
yCONNECTB_ADMCA=yCONNECTG_ADMCA+5
xSAVE_BLANK=410 #COORDENADA X DO PIXEL CIANO DA ABA "Save As"
ySAVE_BLANK=xSAVE_BLANK-200
xRED_STOP=  #COORDENADA X DO PIXEL VERMELHO DE PARADA
yRED_STOP=  #COORDENADA Y DO PIXEL VERMELHO DE PARADA
xGREEN_START=xRED_STOP
yGREEN_START=yRED_STOP+7
xCLEAR_READ=xRED_STOP+30
yCLEAR_READ=yGREEN_START
xCLOSE_ADMCA=xCONNECT_ADMCA+100
yCLOSE_ADMCA=yCONNECTG_ADMCA-990

# -------------- PARAMETROS DE MOVIMENTAÇÃO ADMCA ---------------
xCONNECT_REPERTIER=  #COORDENADA X DO BOTÃO "Connect"
yCONNECT_REPERTIER=  #COORDENADA Y DO BOTÃO "Connect"
xMANUAL_REPERTIER=xCONNECT_REPERTIER+1248
yMANUAL_REPERTIER=yCONNECT_REPERTIER+44
xCODE_REPERTIER=xMANUAL_REPERTIER
yCODE_REPERTIER=yMANUAL_REPERTIER+77
xCLOSE_REPERTIER=xCONNECT_REPERTIER+1630
yCLOSE_REPERTIER=xCONNECT_REPERTIER-20


while teste!=1 and teste!=0:
    teste=int(input("TESTE (0/1): "))
if teste:
    print("INFORME O ESTADOS DOS SISTEMAS (0 - DESLIGADO / 1 - LIGADO):")
    while testeMINIX!=1 and testeMINIX!=0:
        testeMINIX=int(input("Mini-X (0/1): "))
    while testeADMCA!=1 and testeADMCA!=0:
        testeADMCA=int(input("ADMCA (0/1): "))
    while testeREPTI!=1 and testeREPTI!=0:
        testeREPTI=int(input("Repetier (0/1): "))
        
if checkStarted("WindowsCamera"):
    while monitor!=1 and monitor!=0:
        monitor=int(input("Camera Ligada: Monitorar (0/1)? "))
        
    if monitor==1:   
        camera=pyautogui.getWindowsWithTitle("Câmera")[0]._hWnd
        monitorTime=float(input("Tempo de Monitoramento: "))
    
print("\n\nVERIFIQUE A PRESENÇA DOS COLIMADORES!!!")
input("COLIMADORES POSICIONADOS? PRECIONE ENTER PARA CONTINUAR...\n\n")

xLength=float(input("Dimensao horizontal(mm): "))
zLength=float(input("Dimensao vertical(mm): "))
step=float(input("Passo(mm): "))
halfStep=step/2
waitTime=float(input("Tempo de Leitura(s): "))
detectionTime=waitTime
name=input("Nome da Amostra: ")

multX=1
multZ=1
mult=0


#mult=int(input("\nPassos diferentes para os eixos (0/1)? "))

if mult==1:
    multX=float(input("\nMultiplicacao de X: "))
    multZ=float(input("\nMultiplicacao de Z: "))


sideSteps=round(xLength/(step*multX))

upSteps=round(zLength/(multZ*step))

error_xMovementPerMM=14.04/14 #AJUSTE PARA ERRO DOS MOTORES DO EIXO-X

xStep=(step*error_xMovementPerMM)*multX
xHalfStep=(halfStep*error_xMovementPerMM)*multX

zStep=(step-step/100)*multZ #AJUSTE PARA ERRO DOS MOTORES DO EIXO-Z

print(f"Passo ajustado por erro dos motores: \n  -Passo horizontal: {xStep}\n  -Passo Vertical: {zStep}")



command_HalfSideStepRight = f"G1 X{xHalfStep} F150;"
command_SideStepLeft = f"G1 X-{(sideSteps-1)*xStep+xHalfStep} F150;"
command_SideStepRight = f"G1 X{xStep} F150;"
command_UpStep = f"G1 Z{zStep} F150;"
command_Wait = f"G4 P{int(waitTime*1000)};"
command_Leitura="M0 S60 Waiting permission...;"

points = (sideSteps)*(upSteps)

print(f"Numero de pontos: {points}")

waitTimeStr=str(waitTime)
waitTime=waitTimeStr.replace('.',',')
fileName=f"caminho_{name}__{xLength}mmx{zLength}mm_{step}mmStep_{waitTime}sEspera.gcode"


caminho=fileName

sideStepTime=xStep/2.5
upSteptime=zStep/2.5

climbTime=(sideSteps)*sideStepTime+1*upSteptime

xHalfStepTime=xHalfStep/2.5

print(f"Step Time: {sideStepTime}s")
print(f"Climb Time: {climbTime}s")
print(f"Detection Time: {detectionTime}s")

h, m, s = tempoPorPonto(points)

print(f"Tempo de operação (estimado): {h}h {m}min e {s}s")

segundosTotal= points*6
horas=int(segundosTotal/3600)
minutos=int((segundosTotal-horas*3600)/60)
segundos=(segundosTotal-horas*3600-minutos*60)
print(f"Tempo aproximado total (por experiência): {horas}h {minutos}min e {segundos}s")


if not checkStarted('MiniXCtrl'):
    b=subprocess.Popen(pathMiniX)
    time.sleep(10)
minix=pyautogui.getWindowsWithTitle("Amptek Mini-X Controller")[0]._hWnd
print(minix)
bWTF(minix)
while ((teste==0 or testeMINIX==1) and pyautogui.pixel(xON_XRAY, yON_XRAY)!=(255,255,0) and (pyautogui.pixel(xOFF_XRAY, yOFF_XRAY)!=(255,0,0))):
    print("Conecte-se a fonte para continuar")

    time.sleep(10)
print("\nConectado a fonte\n")
    
if not checkStarted('ADMCA'):
    b=subprocess.Popen(pathADMCA)
    time.sleep(10)
admca=pyautogui.getWindowsWithTitle("Amptek ADMCA     live_data.mca     ")[0]._hWnd
print(admca)
bWTF(admca)
while ((teste==0 or testeADMCA==1) and pyautogui.pixel(xCONNECT_ADMCA, yCONNECTG_ADMCA)!=(0,255,0) and (pyautogui.pixel(xCONNECT_ADMCA, yCONNECTB_ADMCA)!=(0,0,255))):
    print("!MAXIMISE A JANELA DO ADMCA!\nConecte-se ao detector para continuar")
    
    time.sleep(10)

pyautogui.click(x=411, y=210)    
pyautogui.hotkey('ctrl', 's')
time.sleep(2)
while ((teste==0 or testeADMCA==1) and pyautogui.pixel(xSAVE_BLANK, ySAVE_BLANK)==(0,255,255)):
    print("SALVE UM ESPECTRO QUALQUER NA PASTA A SEREM SALVOS OS OUTROS antes de continuar")
    
    time.sleep(10)

    
print("\nConectado ao detector\n")

if not checkStarted('RepetierHost'):
    a=subprocess.Popen(pathRepetier)
    time.sleep(10)
repetier=pyautogui.getWindowsWithTitle("Repetier-Host V2.3.2")[0]._hWnd
print(repetier)
bWTF(repetier)
while ((teste==0 or testeREPTI==1) and pyautogui.pixel(xCONNECT_REPERTIER, yCONNECT_REPERTIER)!=(0, 163, 206)):
    print("!MAXIMISE A JANELA DO REPETIER HOST!\nConecte-se à estrutura para continuar")
    
    time.sleep(10)
print("\nConectado à estrutura\n")


ini=input("Iniciar?(S/N): ")
if ini=="S":
    waittime=10
    for i in range(waittime):
        time.sleep(1)
        print(f"\r Iniciando em: {waittime-i}s", end='\r')
    time.sleep(1)
    print("\nIniciando scan")
    i=1
    
    time.sleep(5)
    bWTF(minix)
    if pyautogui.pixelMatchesColor(xON_XRAY, yON_XRAY, (255,255,0)):
        pyautogui.click(x=xON_XRAY, y=yON_XRAY)
        trvlWTAB(1) if teste==1 else trvlWTAB(0)
        pyautogui.hotkey('space')
        print(f"Iniciando Raio-X - !!CUIDADO RADIAÇÃO!!")
        
        
        
    time.sleep(5)
    bWTF(repetier)
    if pyautogui.pixelMatchesColor(xCONNECT_REPERTIER, yCONNECT_REPERTIER, (0, 163, 206)):
        pyautogui.click(x=xMANUAL_REPERTIER, y=yMANUAL_REPERTIER)
        time.sleep(1)
        pyautogui.click(x=xCODE_REPERTIER, y=yCODE_REPERTIER)
        time.sleep(1)
        pyautogui.write("G21;")
        pyautogui.press('enter')
        print("G21;")
        time.sleep(0.5)
        pyautogui.write("G91;")
        pyautogui.press('enter')
        print("G91;")
        time.sleep(0.5)
        pyautogui.write("G60 S0;")
        pyautogui.press('enter')
        print("G60 S0;")
        print(f"Configurada MOVIMENTAÇÃO")
            
    
    for y in range(upSteps):
        bWTF(repetier)
        print("MOVENDO PARA O PRIMEIRO PONTO DA LINHA")
        pyautogui.click(x=xCODE_REPERTIER, y=yCODE_REPERTIER)
        pyautogui.write(command_HalfSideStepRight)
        pyautogui.press('enter')
        print(command_HalfSideStepRight)
        time.sleep(xHalfStepTime)
        
        for x in range(sideSteps):

            
            bWTF(minix)
            if pyautogui.pixelMatchesColor(xOfR_XRAY, yOfR_XRAY, (255,255,0)):
                print("\n\nOUT OF RANGE")
                pyautogui.click(x=xOFF_XRAY, y=yOFF_XRAY)
                print("Esperando 10s")
                
                time.sleep(10)
                
                pyautogui.click(x=xON_XRAY, y=yON_XRAY)
                trvlWTAB(1) if teste==1 else trvlWTAB(0)
                pyautogui.hotkey('space')
                print(f"Reiniciando Raio-X - !!CUIDADO RADIAÇÃO!!\n\n")
                time.sleep(2)

                
            
            if monitor==1:
                bWTF(camera)
                print("MONITORANDO POSIÇÃO")
                time.sleep(monitorTime)

            bWTF(admca)
            if pyautogui.pixelMatchesColor(xRED_STOP, yRED_STOP, (255, 0, 0)):
                pyautogui.click(x=xRED_STOP, y=yRED_STOP) #Stop detection
                print("PARANDO DETECCAO")
                
            if pyautogui.pixelMatchesColor(xGREEN_START, yGREEN_START, (0, 255, 0)):
                print(f"Iniciando DETECCAO - ponto: {y},{x}")
                if teste!=1 or testeADMCA==1:
                    pyautogui.click(x=xCLEAR_READ, y=yCLEAR_READ) #Clear detector
                    time.sleep(1)
                    pyautogui.click(x=xGREEN_START, y=yGREEN_START) #Begin detection
                    
                    time.sleep(detectionTime)
            
                    pyautogui.click(x=xRED_STOP, y=yRED_STOP) #Stop detection
                print("PARANDO DETECCAO")
                print(f"Espectro Obtido - ponto:  Row {y}, Column {x}")
                if teste!=1 or testeADMCA==1:
                    time.sleep(1)
                    pyautogui.hotkey('ctrl', 's')
                    time.sleep(1)
                    pyautogui.write(f"{name}__row{y}_column{x}") #nomeando arquivo
                    pyautogui.hotkey('enter')
                print(f"Salvo - ponto: {i}")
                hP, mP, sP=tempoPorPonto(i)
                print(f"Tempo percorrido: {hP}h {mP}min e {sP}s")
                
                i=i+1

            bWTF(repetier)
            print("RETOMANDO MOVIMENTAÇÃO")
            if x!=sideSteps-1:
                if teste!=1 or testeREPTI==1:
                    pyautogui.click(x=xCODE_REPERTIER, y=yCODE_REPERTIER)
                    pyautogui.write(command_SideStepRight)
                    pyautogui.press('enter')
                    time.sleep(0.5)
                    time.sleep(sideStepTime)
                print(command_SideStepRight)
                
        bWTF(repetier)
        if y!=upSteps-1:
            pyautogui.click(x=xCODE_REPERTIER, y=yCODE_REPERTIER)
            pyautogui.write(command_SideStepLeft)
            pyautogui.press('enter')
            print(command_SideStepLeft)
            time.sleep(0.5)
            pyautogui.write(command_UpStep)
            pyautogui.press('enter')
            print(command_UpStep)
            time.sleep(0.5)
        
            if teste!=1 or testeREPTI==1:
                time.sleep(climbTime)
        
    bWTF(repetier)          
    pyautogui.write("G61 S0;")
    pyautogui.press('enter')
    print("G61 S0;")

    if monitor==1:
        bWTF(camera)
        time.sleep(monitorTime)
        print("MONITORANDO RETORNO")

    
 
bWTF(minix)
pyautogui.click(x=xOFF_XRAY, y=yOFF_XRAY)
time.sleep(5)
pyautogui.click(x=xEXIT_XRAY, y=yEXIT_XRAY)
print(f"DESLIGANDO Raio-X")
time.sleep(5)

time.sleep(climbTime*upSteps)
bWTF(repetier)
pyautogui.click(x=xCLOSE_REPERTIER, y=yCLOSE_REPERTIER) #FECHANDO REPETIER
print("FECHANDO REPETIER")

time.sleep(0.5)
bWTF(admca)    
pyautogui.click(x=xCLOSE_ADMCA, y=yCLOSE_ADMCA) #FECHANDO ADMCA
print("FECHANDO ADMCA")

    
input("Pressione ENTER para fechar...")

