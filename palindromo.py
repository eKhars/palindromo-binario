import tkinter as tk
from tkinter import messagebox, ttk
import re

class TuringMachine:
    def __init__(self):
        self.tape = []
        self.head_pos = 0
        self.state = 'q0'
        
    def write_tape(self, input_str):
        self.tape = list(input_str)
        self.head_pos = 0
        self.state = 'q0'
    
    def move_head(self, direction):
        if direction == 'R':
            self.head_pos += 1
            if self.head_pos >= len(self.tape):
                self.tape.append('')
        elif direction == 'L':
            self.head_pos -= 1
            if self.head_pos < 0:
                self.tape.insert(0, '')
                self.head_pos = 0
    
    def run(self):
        while True:
            current_symbol = self.tape[self.head_pos] if self.head_pos < len(self.tape) else ''
            
            if self.state == 'q0':
                if current_symbol == '0':
                    self.tape[self.head_pos] = ''
                    self.move_head('R')
                    self.state = 'q1'
                elif current_symbol == '1':
                    self.tape[self.head_pos] = ''
                    self.move_head('R')
                    self.state = 'q4'
                elif current_symbol == '':
                    self.state = 'q6'
                    return True
            
            elif self.state == 'q1':
                if current_symbol in ['0', '1']:
                    self.move_head('R')
                elif current_symbol == '':
                    self.state = 'q2'
                    self.move_head('L')
            
            elif self.state == 'q2':
                if current_symbol == '0':
                    self.tape[self.head_pos] = ''
                    self.move_head('L')
                    self.state = 'q3'
                elif current_symbol == '':
                    self.state = 'q6'
                    return True
                else:
                    return False
            
            elif self.state == 'q3':
                if current_symbol in ['0', '1']:
                    self.move_head('L')
                elif current_symbol == '':
                    self.state = 'q0'
                    self.move_head('R')
            
            elif self.state == 'q4':
                if current_symbol in ['0', '1']:
                    self.move_head('R')
                elif current_symbol == '':
                    self.state = 'q5'
                    self.move_head('L')
            
            elif self.state == 'q5':
                if current_symbol == '1':
                    self.tape[self.head_pos] = ''
                    self.move_head('L')
                    self.state = 'q3'
                elif current_symbol == '':
                    self.state = 'q6'
                    return True
                else:
                    return False
            
            elif self.state == 'q6':
                return True
            
        return False

class ModernTuringGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Validador de Palíndromos Binarios")
        self.root.geometry("600x500")
        self.root.configure(bg='#1a1a1a')  # Fondo oscuro
        
        # Configurar estilos
        self.configure_styles()
        
        # Contenedor principal
        self.main_container = ttk.Frame(root, style='Dark.TFrame')
        self.main_container.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Inicializar máquina de Turing
        self.turing = TuringMachine()
        
        # Crear widgets
        self.create_widgets()
        
    def configure_styles(self):
        # Configurar estilos personalizados
        self.style = ttk.Style()
        
        # Colores
        self.style.configure('Dark.TFrame', background='#1a1a1a')
        self.style.configure('Card.TFrame', background='#2d2d2d')
        
        # Etiquetas
        self.style.configure('Title.TLabel',
                           font=('Helvetica', 24, 'bold'),
                           foreground='#ffffff',
                           background='#1a1a1a')
        
        self.style.configure('Subtitle.TLabel',
                           font=('Helvetica', 12),
                           foreground='#b3b3b3',
                           background='#1a1a1a')
        
        self.style.configure('Result.TLabel',
                           font=('Helvetica', 14, 'bold'),
                           background='#2d2d2d',
                           foreground='#ffffff')
        
        # Botón personalizado
        self.style.configure('Modern.TButton',
                           font=('Helvetica', 12),
                           padding=10)
        
    def create_widgets(self):
        # Título
        title_frame = ttk.Frame(self.main_container, style='Dark.TFrame')
        title_frame.pack(fill='x', pady=(0, 30))
        
        title = ttk.Label(title_frame,
                         text="Validador de Palíndromos Binarios",
                         style='Title.TLabel')
        title.pack()
        
        subtitle = ttk.Label(title_frame,
                           text="Ingrese una secuencia de 0s y 1s para verificar si es un palíndromo",
                           style='Subtitle.TLabel')
        subtitle.pack(pady=(5, 0))
        
        # Tarjeta principal
        self.card = ttk.Frame(self.main_container, style='Card.TFrame')
        self.card.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Campo de entrada
        input_frame = ttk.Frame(self.card, style='Card.TFrame')
        input_frame.pack(pady=30, padx=30)
        
        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(
            input_frame,
            textvariable=self.input_var,
            font=('Helvetica', 18),
            width=20,
            bg='#3d3d3d',
            fg='#ffffff',
            insertbackground='#ffffff',  # Color del cursor
            relief='flat'
        )
        self.input_entry.pack(ipady=8)
        
        # Botón de verificación
        self.verify_button = ttk.Button(
            self.card,
            text="Verificar",
            style='Modern.TButton',
            command=self.verify_palindrome
        )
        self.verify_button.pack(pady=20)
        
        # Resultado
        self.result_frame = ttk.Frame(self.card, style='Card.TFrame')
        self.result_frame.pack(fill='x', pady=20)
        
        self.result_label = ttk.Label(
            self.result_frame,
            text="",
            style='Result.TLabel',
            justify='center'
        )
        self.result_label.pack(expand=True)
        
        # Ejemplos
        examples_frame = ttk.Frame(self.main_container, style='Dark.TFrame')
        examples_frame.pack(fill='x', pady=20)
        
        examples_label = ttk.Label(
            examples_frame,
            text="Ejemplos: 1001001   110011   0110   101",
            style='Subtitle.TLabel'
        )
        examples_label.pack()
        
    def verify_palindrome(self):
        input_string = self.input_var.get().strip()
        
        # Validación de entrada
        if not input_string:
            messagebox.showerror("Error", "Por favor ingrese una cadena binaria")
            return
        
        if not re.match(r'^[01]+$', input_string):
            messagebox.showerror("Error", "Por favor ingrese solo 0s y 1s")
            return
        
        # Ejecutar la máquina de Turing
        self.turing.write_tape(input_string)
        result = self.turing.run()
        
        # Mostrar resultado
        if result:
            self.result_label.config(
                text=f"'{input_string}' es un palíndromo binario",
                foreground='#00ff00'
            )
        else:
            self.result_label.config(
                text=f"'{input_string}' no es un palíndromo binario",
                foreground='#ff4444'
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernTuringGUI(root)
    root.mainloop()