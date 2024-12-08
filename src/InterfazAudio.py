#!/usr/bin/env python3

# Reconocimiento de voz
import sounddevice
import speech_recognition as sr
from enum import Enum

from set_goal import send_goal

class InterfazAudio:
    class Acciones(Enum):
        BAÑO = "baño"
        CLASE = "clase"
        LAB_ROBOTICA = "robótica"
        LAB_AUTOMATICA = "automática"
        LAB_ELECTRONICA = "electrónica"

    __PALABRA_CLAVE = "llévame"


    def __init__(self,cliente, device_index=0):
        self.__microphone: sr.Microphone = sr.Microphone(device_index=device_index)
        self.__recognizer: sr.Recognizer = sr.Recognizer()
        self.client = cliente

    def escuchar(self, segundos_de_espera=3) -> str:
        with self.__microphone as source:
            print("Escuchando...")
            audio = self.__recognizer.listen(source, segundos_de_espera, 3)
            print("Procesando...")
            text_result: str = self.__recognizer.recognize_google(audio, language='es-ES')
            print(f"Texto escuchado: {text_result}")
        return text_result

    def escucharAccion(self, segundos_de_espera=3) -> Acciones:
        texto: str = self.escuchar(segundos_de_espera=segundos_de_espera)
        accion: InterfazAudio.Acciones = self.__procesar_texto(texto.split())
        return accion

    def __procesar_texto(self, texto) -> Acciones:
        ir: bool = False
        accion: Optional[InterfazAudio.Acciones] = None
        for palabra in texto:
            if palabra == self.__PALABRA_CLAVE and ir==False:
                ir = True
            elif palabra == InterfazAudio.Acciones.BAÑO.value and ir==True:
                accion = InterfazAudio.Acciones.BAÑO
                x = -11.48
                y = 7.4
            elif palabra == InterfazAudio.Acciones.CLASE.value and ir==True:
                accion = InterfazAudio.Acciones.CLASE
                x = -8.40
                y = -13.5
            elif palabra == InterfazAudio.Acciones.LAB_ROBOTICA.value and ir==True:
                accion = InterfazAudio.Acciones.LAB_ROBOTICA
                x = 2.31
                y = -5.42
            elif palabra == InterfazAudio.Acciones.LAB_AUTOMATICA.value and ir==True:
                accion = InterfazAudio.Acciones.LAB_AUTOMATICA
                # Coords. NO implementadas en mapa
            elif palabra == InterfazAudio.Acciones.LAB_ELECTRONICA.value and ir==True:
                accion = InterfazAudio.Acciones.LAB_ELECTRONICA
                x = 4.51
                y = -0.58
        
        if accion:
            print(f"Te llevo a {accion.value}")
            send_goal(self.client, x,y,1)
            return accion
        else:
            print("No se han detectado acciones")
            return None
'''
# Consulta si continuar o detener el funcionamiento
def continuar():
    respuesta = input('Continuar ? (s/n): ')
    if respuesta.lower() == 's':
        return True
    else:
        return False'''

