import tkinter as tk
import subprocess
import threading
import pkg_resources
import sys
import os
import venv

class DependencyInstaller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Установка зависимостей")
        
        # Добавляем эту строку в начало __init__
        self.venv_path = "venv"
        
        # Словарь с наборами библиотек для каждой кнопки
        self.dependency_sets = {
            'База': ['asyncio'],
            'Запись': ['pywin32', 'psutil', 'pillow'],
            'Работа': ['']
        }
        
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)
        
        self.buttons = {}
        self.create_buttons()
        
        self.console_output = tk.Text(self.root, height=10, width=50)
        self.console_output.pack(pady=10)
        
        # Начальное обновление статуса кнопок
        self.update_all_buttons_status()
        
        # Добавляем метку для статуса
        self.status_label = tk.Label(self.root, text="", fg="black")
        self.status_label.pack(pady=5)
        
        self.create_venv_if_not_exists()
        
    def create_venv_if_not_exists(self):
        if not os.path.exists(self.venv_path):
            self.console_output.insert(tk.END, "Создание виртуального окружения...\n")
            venv.create(self.venv_path, with_pip=True)
            self.console_output.insert(tk.END, "Виртуальное окружение создано.\n")
        
    def get_python_executable(self):
        if os.name == 'nt':  # Windows
            return os.path.join(self.venv_path, 'Scripts', 'python.exe')
        return os.path.join(self.venv_path, 'bin', 'python')  # Linux/Mac

    def create_buttons(self):
        for set_name, dependencies in self.dependency_sets.items():
            btn = tk.Button(
                self.frame,
                text=f"Установить набор {set_name}",
                command=lambda s=set_name: self.start_installation(s)
            )
            btn.pack(side=tk.LEFT, padx=5)
            self.buttons[set_name] = btn

    def check_installed(self, package_list):
        installed = 0
        python_executable = self.get_python_executable()
        
        for package in package_list:
            try:
                result = subprocess.run(
                    [python_executable, '-m', 'pip', 'show', package],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    installed += 1
            except Exception:
                pass
            
        return installed, len(package_list)

    def update_button_status(self, set_name):
        installed, total = self.check_installed(self.dependency_sets[set_name])
        percentage = (installed / total) * 100
        self.buttons[set_name].config(
            text=f"Набор {set_name} ({percentage:.0f}%)"
        )

    def update_all_buttons_status(self):
        for set_name in self.dependency_sets:
            self.update_button_status(set_name)

    def install_dependencies(self, set_name):
        dependencies = self.dependency_sets[set_name]
        total_deps = len(dependencies)
        installed_deps = 0
        
        try:
            python_executable = self.get_python_executable()
            
            for dep in dependencies:
                self.console_output.insert(tk.END, f"Установка {dep}...\n")
                self.console_output.see(tk.END)
                
                process = subprocess.Popen(
                    [python_executable, '-m', 'pip', 'install', dep],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                error_output = []
                while True:
                    output = process.stdout.readline()
                    if output:
                        self.console_output.insert(tk.END, output)
                        self.console_output.see(tk.END)
                        self.root.update()
                    
                    if process.poll() is not None:
                        break
                
                # Проверяем ошибки
                for line in process.stderr:
                    error_output.append(line)
                    self.console_output.insert(tk.END, line)
                    self.console_output.see(tk.END)
                
                if process.returncode != 0:
                    self.status_label.config(
                        text=f"Ошибка при установке {dep}!",
                        fg="red"
                    )
                    return
                
                installed_deps += 1
                progress = (installed_deps / total_deps) * 100
                self.buttons[set_name].config(
                    text=f"Набор {set_name} ({progress:.0f}%)"
                )
                self.root.update()
            
            self.status_label.config(
                text=f"Установка набора {set_name} успешно завершена!",
                fg="green"
            )
            
        except Exception as e:
            self.status_label.config(
                text=f"Произошла ошибка: {str(e)}",
                fg="red"
            )
        
        self.update_button_status(set_name)

    def start_installation(self, set_name):
        # Запуск установки в отдельном потоке
        thread = threading.Thread(
            target=self.install_dependencies,
            args=(set_name,),
            daemon=True
        )
        thread.start()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    installer = DependencyInstaller()
    installer.run()
