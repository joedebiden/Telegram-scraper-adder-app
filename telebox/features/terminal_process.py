import subprocess

class OpenTerminal:

    def open_terminal(self):
        """Méthode qui lance un terminal avec des instructions pour l'utilisateur."""
        try: 
            subprocess.run("start cmd", shell=True)
            print("[INFO] Terminal launched successfully.")
        except Exception as e:
            print(f"[ERROR] Failed to open terminal: {e}")

    
    
    def launch_telebox_adder(self):
            """Méthode qui lance un terminal avec des instructions pour l'utilisateur."""
            try: 
                # project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
                
                instructions =  'echo    ===== Instructions for Telebox Adder ===== &' \
                                'echo   [     1. Activate virtual environment:     ]&' \
                                'echo   [   - call .venv\\Scripts\\activate       ]&' \
                                'echo   [     2. Launch the Telebox adder:         ]&' \
                                'echo   [   - python telebox_adder_cmd.py          ]&' \
                                'echo    =========================================='
                
                command = f'start cmd /k "{instructions}"'
                subprocess.run(command, shell=True)
                
                print("[INFO] Terminal with instructions launched successfully.")
                
            except Exception as e:
                print(f"[ERROR] Failed to launch terminal: {e}")







