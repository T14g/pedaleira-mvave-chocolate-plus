import mido
import subprocess
import time
from datetime import datetime
import ctypes

# Códigos virtuais das teclas multimídia
VK_MEDIA_NEXT_TRACK = 0xB0
VK_MEDIA_PREV_TRACK = 0xB1
VK_MEDIA_PLAY_PAUSE = 0xB3

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002


def press_key(vk_code):
    """Simula pressionar e soltar uma tecla multimídia."""
    ctypes.windll.user32.keybd_event(vk_code, 0, KEYEVENTF_EXTENDEDKEY, 0)
    ctypes.windll.user32.keybd_event(vk_code, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0)


def play_pause():
    """Play/Pause"""
    press_key(VK_MEDIA_PLAY_PAUSE)


def next_track():
    """Próxima música"""
    press_key(VK_MEDIA_NEXT_TRACK)


def previous_track():
    """Música anterior"""
    press_key(VK_MEDIA_PREV_TRACK)

input_name = "loopMIDI Port 1 1"

# Lista portas disponíveis
print("Portas MIDI disponíveis:")
ports = mido.get_input_names()
for name in ports:
    print("  ", name)

if input_name not in ports:
    print(f"❌ Porta '{input_name}' não encontrada. Confere o loopMIDI e o nome exato.")
else:
    print(f"✅ Conectado na porta: {input_name}")
    print("🎵 Aguardando comandos MIDI... (Ctrl+C para sair)\n")

    last_trigger_time = 0.0
    debounce_seconds = 0.2  # evita spam

    try:
        with mido.open_input(input_name) as inport:
            for msg in inport:
                print(msg)

                if msg.type == 'program_change' and getattr(msg, 'channel', None) == 0 and getattr(msg, 'program', None) == 1:
                    now = time.time()
                    if now - last_trigger_time >= debounce_seconds:
                        print("✅ Program Change 1 detectado! Enviando 'P' via PowerShell...")
                        powershell_cmd = (
                            'powershell -NoProfile -Command '
                            '"Add-Type -AssemblyName System.Windows.Forms; '
                            '[System.Windows.Forms.SendKeys]::SendWait(\\"P\\")"'
                        )
                        try:
                            subprocess.call(powershell_cmd, shell=True)
                        except Exception as e:
                            print("Erro ao chamar PowerShell SendKeys:", e)
                        last_trigger_time = now
                    else:
                        print("Ignorado por debounce (muito próximo do último).")
                elif msg.type == 'program_change' and getattr(msg, 'channel', None) == 0 and getattr(msg, 'program', None) == 0:
                    now = time.time()
                    if now - last_trigger_time >= debounce_seconds:
                        print("✅ Botão detectado! Enviando 'space' via PowerShell...")
                        # comando PowerShell que usa .NET SendKeys
                        powershell_cmd = (
                            'powershell -NoProfile -Command '
                            '"Add-Type -AssemblyName System.Windows.Forms; '
                            '[System.Windows.Forms.SendKeys]::SendWait(\\" \\")"'
                        )
                        try:
                            # subprocess.call aguarda terminar; use Popen se quiser não bloquear
                            subprocess.call(powershell_cmd, shell=True)
                        except Exception as e:
                            print("Erro ao chamar PowerShell SendKeys:", e)
                        last_trigger_time = now
                elif msg.type == 'program_change' and getattr(msg, 'channel', None) == 0 and getattr(msg, 'program', None) == 4:
                    now = time.time()
                    if now - last_trigger_time >= debounce_seconds:
                        play_pause()
                        last_trigger_time = now
                elif msg.type == 'program_change' and getattr(msg, 'channel', None) == 0 and getattr(msg, 'program', None) == 5:
                    now = time.time()
                    if now - last_trigger_time >= debounce_seconds:
                        previous_track()
                        last_trigger_time = now

                elif msg.type == 'program_change' and getattr(msg, 'channel', None) == 0 and getattr(msg, 'program', None) == 6:
                    now = time.time()
                    if now - last_trigger_time >= debounce_seconds:
                        next_track()
                        last_trigger_time = now
                    
                    else:
                        print("Ignorado por debounce (muito próximo do último).")
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário. Saindo.")
    except Exception as e:
        print("Erro ao abrir porta MIDI ou processar mensagens:", e)
