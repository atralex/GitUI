import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import subprocess


def select_folder():
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(tk.END, folder_path)


def initialize_git():
    folder_path = folder_entry.get()
    if folder_path:
        subprocess.run(["git", "init"], cwd=folder_path)
        output_text.insert(tk.END, "Repositorio Git inicializado en {}\n".format(folder_path))
    else:
        output_text.insert(tk.END, "Por favor, seleccione una carpeta antes de inicializar Git.\n")


def add_files():
    folder_path = folder_entry.get()
    if folder_path:
        subprocess.run(["git", "add", "."], cwd=folder_path)
        output_text.insert(tk.END, "Elementos agregados al commit.\n")
    else:
        output_text.insert(tk.END, "Por favor, seleccione una carpeta antes de agregar los elementos al commit.\n")


def commit_files():
    folder_path = folder_entry.get()
    if folder_path:
        commit_message = tk.simpledialog.askstring("Commit", "Ingrese el mensaje del commit:")
        if commit_message:
            subprocess.run(["git", "commit", "-m", commit_message], cwd=folder_path)
            output_text.insert(tk.END, "Commit realizado correctamente.\n")
        else:
            output_text.insert(tk.END, "Por favor, ingrese un mensaje para el commit.\n")

        try:
            subprocess.run(["git", "push", "origin", "main"], cwd=folder_path)
            output_text.insert(tk.END, "Push realizado correctamente.\n")
        except:
            output_text.insert(tk.END, "No se pudo realizar el push.\n")
    else:
        output_text.insert(tk.END, "Por favor, seleccione una carpeta antes de realizar el commit.\n")


def enter_github_username():
    username = simpledialog.askstring('GitHub Username', 'Enter your GitHub username:')
    if username:
        result = subprocess.run(['git', 'config', 'user.name', username], capture_output=True, text=True)
        if result.returncode == 0:
            messagebox.showinfo('Success', f'GitHub username set to: {username}')
        else:
            messagebox.showerror('Error', 'Failed to set GitHub username.')
    else:
        messagebox.showwarning('Warning', 'GitHub username cannot be empty.')


def enter_email():
    email = simpledialog.askstring('Email', 'Enter your email:')
    if email:
        result = subprocess.run(['git', 'config', 'user.email', email], capture_output=True, text=True)
        if result.returncode == 0:
            messagebox.showinfo('Success', f'Email set to: {email}')
        else:
            messagebox.showerror('Error', 'Failed to set email.')
    else:
        messagebox.showwarning('Warning', 'Email cannot be empty.')


def initialize_github_repository():
    # Obtener el nombre del repositorio de GitHub desde el cuadro de texto
    repo_url = repo_entry.get()
    folder_path = folder_entry.get()
    print(repo_url)
    print(folder_path)
    with open(folder_path+'/README.md', 'w') as f:
        f.write("# README")

    # Inicializar el repositorio local
    result_init = subprocess.run(['git', 'init'], cwd=folder_path, capture_output=True, text=True)
    if result_init.returncode == 0:
        messagebox.showinfo('Success', 'Local repository initialized successfully.')
        # Ejecutar los comandos git para agregar el repositorio remoto y hacer el push
        git_init = subprocess.run(['git', 'init'], cwd=folder_path, capture_output=True, text=True)
        git_add_readme = subprocess.run(['git', 'add', 'README.md'], cwd=folder_path, capture_output=True, text=True)
        git_first_commit = subprocess.run(['git', 'commit', '-m', '"First commit"'], cwd=folder_path, capture_output=True, text=True)
        git_branch = subprocess.run(['git', 'branch', '-M', 'main'], cwd=folder_path, capture_output=True, text=True)
        git_add_remote = subprocess.run(['git', 'remote', 'add', 'origin', repo_url], cwd=folder_path, capture_output=True, text=True)
        git_push = subprocess.run(['git', 'push', '-u', 'origin', 'main'], cwd=folder_path, capture_output=True, text=True)
        if git_init.returncode == 0 and git_add_readme.returncode == 0 and git_first_commit.returncode == 0 and git_branch.returncode == 0 and git_add_remote.returncode == 0 and git_push.returncode == 0:
            messagebox.showinfo('Success', 'Repository initialized on GitHub successfully.')
        else:
            messagebox.showerror('Error', 'Failed to initialize repository on GitHub.')
            print('Error', git_init.stderr, git_add_readme.stderr, git_first_commit.stderr, git_branch.stderr, git_add_remote.stderr, git_push.stderr)
    else:
        messagebox.showerror('Error', 'Failed to initialize local repository.')


root = tk.Tk()
root.title("Git GUI")

folder_label = tk.Label(root, text="Carpeta:")
folder_label.pack(padx=5, pady=5)

folder_entry = tk.Entry(root, width=50)
folder_entry.pack(padx=5, pady=5)

select_button = tk.Button(root, text="Examinar", command=select_folder)
select_button.pack(padx=5, pady=5)

repo_label = tk.Label(root, text="URL del Repositorio:")
repo_label.pack(padx=5, pady=5)

repo_entry = tk.Entry(root)
repo_entry.pack(padx=5, pady=5)

init_button = tk.Button(root, text='Inicializar Git Local y GitHub', command=initialize_github_repository)
init_button.pack(padx=5, pady=5)

add_button = tk.Button(root, text="Agregar al Commit", command=add_files)
add_button.pack(padx=5, pady=5)

commit_button = tk.Button(root, text="Realizar Commit", command=commit_files)
commit_button.pack(padx=5, pady=5)

github_user_button = tk.Button(root, text='Enter GitHub Username', command=enter_github_username)
github_user_button.pack(padx=5, pady=5)

email_button = tk.Button(root, text='Enter GitHub Email', command=enter_email)
email_button.pack(padx=5, pady=5)

graph_button = tk.Button(root, text="Cerrar", command=root.destroy)
graph_button.pack(padx=5, pady=5)

output_text = tk.Text(root, height=10)

root.mainloop()
