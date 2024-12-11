import pygame
import sys
import tkinter as tk
from tkinter import simpledialog

# Initialiser Pygame
pygame.init()

# Définir les dimensions de la fenêtre
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Moteur Graphique avec Blocs Scratch-like")

# Couleurs
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Classe Sprite de base
class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.velocity = [0, 0]
        self.scripts = []

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        # Exécuter les scripts
        for condition, action in self.scripts:
            if condition():
                action()

    def set_velocity(self, x, y):
        self.velocity = [x, y]

    def add_script(self, condition, action):
        self.scripts.append((condition, action))

# Créer un groupe de sprites
all_sprites = pygame.sprite.Group()

# Créer des sprites de test
sprite1 = Sprite(BLUE, 50, 50)
sprite1.rect.x = 100
sprite1.rect.y = 100
all_sprites.add(sprite1)

sprite2 = Sprite(RED, 50, 50)
sprite2.rect.x = 300
sprite2.rect.y = 300
all_sprites.add(sprite2)

# Interface Tkinter
root = tk.Tk()
root.title("Programmation par Blocs")
root.geometry("800x600")

# Classe pour les blocs
class Block(tk.Label):
    def __init__(self, master, text, command):
        super().__init__(master, text=text, bg="lightgrey", bd=1, relief="solid", width=20, height=2)
        self.command = command
        self.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        self.command()

# Zone de dessin pour les blocs
canvas = tk.Canvas(root, width=400, height=600, bg="white")
canvas.pack(side=tk.LEFT)

# Zone de script pour afficher les scripts assemblés
scripts_frame = tk.Frame(root, bg="lightgrey", width=400, height=600)
scripts_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Ajouter des blocs de commandes
blocks_frame = tk.Frame(root)
blocks_frame.pack(side=tk.LEFT, fill=tk.Y)

def create_block(name, command):
    block = Block(blocks_frame, text=name, command=command)
    block.pack(pady=5)

# Définir les fonctions de commande pour les blocs
def set_velocity():
    x = simpledialog.askinteger("Input", "Entrez la vitesse X:", minvalue=-10, maxvalue=10)
    y = simpledialog.askinteger("Input", "Entrez la vitesse Y:", minvalue=-10, maxvalue=10)
    sprite1.set_velocity(x, y)

def stop_sprite():
    sprite1.set_velocity(0, 0)

def move_up():
    sprite1.set_velocity(0, -5)

def move_down():
    sprite1.set_velocity(0, 5)

def move_left():
    sprite1.set_velocity(-5, 0)

def move_right():
    sprite1.set_velocity(5, 0)

def add_script():
    def condition_always_true():
        return True

    sprite1.add_script(condition_always_true, stop_sprite)

def on_key_press(key):
    def condition():
        return pygame.key.get_pressed()[key]
    return condition

def add_key_script():
    key = simpledialog.askstring("Input", "Entrez la touche (ex: 'K_UP'):")
    key_constant = getattr(pygame, key, None)
    if key_constant:
        sprite1.add_script(on_key_press(key_constant), stop_sprite)

def update_scripts_display():
    for widget in scripts_frame.winfo_children():
        widget.destroy()

    for condition, action in sprite1.scripts:
        condition_text = condition.__name__
        action_text = action.__name__
        script_text = f"Si {condition_text}, alors {action_text}"
        script_label = tk.Label(scripts_frame, text=script_text, bg="lightgrey")
        script_label.pack(pady=2)

# Créer les blocs de commandes
create_block("Définir la Vitesse", set_velocity)
create_block("Arrêter le Sprite", stop_sprite)
create_block("Déplacer en Haut", move_up)
create_block("Déplacer en Bas", move_down)
create_block("Déplacer à Gauche", move_left)
create_block("Déplacer à Droite", move_right)
create_block("Ajouter Script (Toujours)", add_script)
create_block("Ajouter Script (Touche)", add_key_script)

# Bouton pour afficher le rendu
def show_render():
    render_window = tk.Toplevel(root)
    render_window.title("Rendu Pygame")
    render_window.geometry("800x600")

    embed_frame = tk.Frame(render_window, width=800, height=600)
    embed_frame.pack()

    os.environ['SDL_WINDOWID'] = str(embed_frame.winfo_id())
    os.environ['SDL_VIDEODRIVER'] = 'windib'

    screen = pygame.display.set_mode((width, height))

    def render_loop():
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Mettre à jour les sprites
            all_sprites.update()

            # Remplir l'écran de blanc
            screen.fill(WHITE)

            # Dessiner tous les sprites
            all_sprites.draw(screen)

            # Rafraîchir l'écran
            pygame.display.flip()

            # Limiter la vitesse de la boucle
            pygame.time.Clock().tick(60)

        pygame.quit()
        sys.exit()

    render_loop()

render_button = tk.Button(root, text="Afficher le Rendu", command=show_render, width=20, height=2)
render_button.pack(pady=10)

update_button = tk.Button(root, text="Mettre à Jour les Scripts", command=update_scripts_display, width=20, height=2)
update_button.pack(pady=10)

# Lancer la boucle principale Tkinter
root.mainloop()
