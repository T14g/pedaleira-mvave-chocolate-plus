import mido
import subprocess
import time
from datetime import datetime

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
                    else:
                        print("Ignorado por debounce (muito próximo do último).")
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário. Saindo.")
    except Exception as e:
        print("Erro ao abrir porta MIDI ou processar mensagens:", e)
