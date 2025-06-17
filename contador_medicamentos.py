import cv2
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ultralytics import YOLO
import os
from PIL import Image, ImageTk


class ContadorMedicamentos:
    def __init__(self, root):
        self.root = root
        self.total_acumulado = 0
        self.setup_ui()
        self.carregar_modelo()

    def carregar_modelo(self):
        try:
            modelo_path = os.path.join(os.path.dirname(__file__), 'train15', 'weights', 'best.pt')
            self.modelo = YOLO(modelo_path)
        except Exception as e:
            messagebox.showerror("Erro Crítico", f"Não foi possível carregar o modelo de detecção:\n{str(e)}")
            self.root.destroy()
            exit()

    def setup_ui(self):
        self.root.title("Contador de Medicamentos v2.0")
        self.root.geometry("700x600")
        self.root.minsize(600, 500)

        # Configuração de estilo
        self.style = ttk.Style()
        if 'clam' in self.style.theme_names():
            self.style.theme_use('clam')

        # Estilo dos botões
        self.style.configure('TButton', font=('Arial', 10, 'bold'), padding=6)
        self.style.configure('Primary.TButton', foreground='white', background='#3498db')
        self.style.configure('Secondary.TButton', foreground='white', background='#2ecc71')
        self.style.map('Primary.TButton', background=[('active', '#2980b9')])

        # Frame principal
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        title_label = ttk.Label(main_frame,
                                text="CONTADOR DE MEDICAMENTOS",
                                font=('Arial', 16, 'bold'),
                                foreground='#2c3e50')
        title_label.pack(pady=(0, 15))

        # Frame de pré-visualização com scrollbars
        preview_container = ttk.Frame(main_frame)
        preview_container.pack(fill=tk.BOTH, expand=True, pady=5)

        # Canvas com scrollbars
        self.canvas = tk.Canvas(preview_container, bg='white', highlightthickness=1, highlightbackground='#cccccc')
        h_scroll = ttk.Scrollbar(preview_container, orient='horizontal', command=self.canvas.xview)
        v_scroll = ttk.Scrollbar(preview_container, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame interno para a imagem
        self.preview_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.preview_frame, anchor='nw')

        self.preview_label = ttk.Label(self.preview_frame)
        self.preview_label.pack()

        # Configurar eventos de redimensionamento
        self.preview_frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.canvas.bind('<Configure>', self._on_canvas_configure)

        # Frame de resultados
        results_frame = ttk.Frame(main_frame)
        results_frame.pack(fill=tk.X, pady=10)

        ttk.Label(results_frame, text="Total na imagem atual:", font=('Arial', 11)).grid(row=0, column=0, sticky='w')
        self.current_count = ttk.Label(results_frame, text="0", font=('Arial', 11, 'bold'), foreground='#3498db')
        self.current_count.grid(row=0, column=1, sticky='e', padx=10)

        ttk.Label(results_frame, text="Total acumulado:", font=('Arial', 11)).grid(row=1, column=0, sticky='w')
        self.total_count = ttk.Label(results_frame, text="0", font=('Arial', 11, 'bold'), foreground='#2ecc71')
        self.total_count.grid(row=1, column=1, sticky='e', padx=10)

        # Barra de progresso
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.pack(fill=tk.X, pady=10)

        # Frame de status
        status_frame = ttk.Frame(main_frame, relief='solid', borderwidth=1, padding=5)
        status_frame.pack(fill=tk.X, pady=10)

        self.status_label = ttk.Label(status_frame, text="Pronto para processar imagens", foreground='#27ae60')
        self.status_label.pack()

        # Frame de botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)

        # Botão Selecionar Imagem
        self.select_button = ttk.Button(button_frame,
                                        text="SELECIONAR IMAGEM",
                                        command=self.selecionar_imagem,
                                        style='Primary.TButton')
        self.select_button.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        # Botão para visualização em tela cheia
        self.fullscreen_button = ttk.Button(button_frame,
                                            text="VISUALIZAR EM TELA CHEIA",
                                            command=self.mostrar_tela_cheia,
                                            style='Secondary.TButton')
        self.fullscreen_button.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        # Botões auxiliares
        self.reset_button = ttk.Button(button_frame,
                                       text="ZERAR CONTAGEM",
                                       command=self.zerar_contagem)
        self.reset_button.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        self.help_button = ttk.Button(button_frame,
                                      text="AJUDA",
                                      command=self.mostrar_ajuda)
        self.help_button.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        # Configurar pesos das colunas
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

    def _on_canvas_configure(self, event):
        """Ajusta o frame interno quando o canvas é redimensionado"""
        self.canvas.itemconfig('all', width=event.width)

    def mostrar_ajuda(self):
        help_text = """INSTRUÇÕES:

1. Clique em 'SELECIONAR IMAGEM' para escolher uma foto
2. O sistema irá contar automaticamente os medicamentos
3. Use 'VISUALIZAR EM TELA CHEIA' para ver a imagem ampliada
4. Use 'ZERAR CONTAGEM' para reiniciar o contador

Formatos suportados: JPG, PNG, BMP"""
        messagebox.showinfo("Ajuda", help_text)

    def selecionar_imagem(self):
        caminho = filedialog.askopenfilename(
            title="Selecionar Imagem",
            filetypes=[("Imagens", "*.jpg *.jpeg *.png *.bmp"), ("Todos os arquivos", "*.*")]
        )
        if caminho:
            self.processar_imagem(caminho)

    def zerar_contagem(self):
        self.total_acumulado = 0
        self.current_count.config(text="0")
        self.total_count.config(text="0")
        self.status_label.config(text="Contagem zerada", foreground='#27ae60')
        self.atualizar_preview(None)

    def atualizar_preview(self, imagem_cv):
        if imagem_cv is None:
            self.preview_label.config(image='')
            self.preview_label.image = None
            return

        # Converter imagem para formato adequado
        imagem_rgb = cv2.cvtColor(imagem_cv, cv2.COLOR_BGR2RGB)
        h, w = imagem_rgb.shape[:2]

        # Redimensionar para a pré-visualização (tamanho máximo de 400x400)
        ratio = min(400 / w, 400 / h)
        new_w, new_h = int(w * ratio), int(h * ratio)
        resized = cv2.resize(imagem_rgb, (new_w, new_h))

        # Converter para formato Tkinter
        img_pil = Image.fromarray(resized)
        self.preview_img = ImageTk.PhotoImage(img_pil)

        self.preview_label.config(image=self.preview_img)
        self.preview_label.image = self.preview_img

        # Salvar a imagem original para visualização em tela cheia
        self.imagem_original = imagem_cv

    def mostrar_tela_cheia(self):
        if hasattr(self, 'imagem_original'):
            # Redimensionar para a tela (mantendo aspect ratio)
            screen_width = self.root.winfo_screenwidth() * 0.8
            screen_height = self.root.winfo_screenheight() * 0.8
            h, w = self.imagem_original.shape[:2]
            ratio = min(screen_width / w, screen_height / h)
            new_w, new_h = int(w * ratio), int(h * ratio)
            redimensionada = cv2.resize(self.imagem_original, (new_w, new_h))

            cv2.imshow("Visualização em Tela Cheia", redimensionada)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada para visualização")

    def processar_imagem(self, caminho_imagem):
        try:
            self.progress['value'] = 20
            self.root.update()

            # Verificar arquivo
            if not os.path.exists(caminho_imagem):
                raise FileNotFoundError("Arquivo não encontrado")

            if not caminho_imagem.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                raise ValueError("Tipo de arquivo não suportado")

            # Carregar imagem
            imagem = cv2.imread(caminho_imagem)
            if imagem is None:
                raise ValueError("Não foi possível ler a imagem")

            self.atualizar_preview(imagem)
            self.progress['value'] = 40
            self.status_label.config(text="Processando imagem...", foreground='#f39c12')
            self.root.update()

            # Executar detecção
            resultados = self.modelo(caminho_imagem, conf=0.1, imgsz=1024)[0]
            total_atual = len(resultados.boxes)
            self.total_acumulado += total_atual

            # Atualizar interface
            self.current_count.config(text=str(total_atual))
            self.total_count.config(text=str(self.total_acumulado))
            self.status_label.config(text="Imagem processada com sucesso ✔", foreground='#27ae60')
            self.progress['value'] = 80
            self.root.update()

            # Desenhar caixas de detecção
            for box in resultados.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(imagem, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Atualizar preview com as detecções
            self.atualizar_preview(imagem)
            self.progress['value'] = 100

        except FileNotFoundError as e:
            self.mostrar_erro(f"Erro: {str(e)}")
        except ValueError as e:
            self.mostrar_erro(f"Erro: {str(e)}")
        except Exception as e:
            self.mostrar_erro(f"Erro no processamento: {str(e)}")
        finally:
            self.progress['value'] = 0
            self.root.update()

    def mostrar_erro(self, mensagem):
        self.status_label.config(text=mensagem, foreground='#e74c3c')
        self.current_count.config(text="0")
        self.atualizar_preview(None)
        self.root.bell()  # Som de alerta


if __name__ == "__main__":
    root = tk.Tk()
    app = ContadorMedicamentos(root)
    root.mainloop()