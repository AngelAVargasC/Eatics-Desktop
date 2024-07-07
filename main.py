import tkinter as tk
import sqlite3
from PIL import Image, ImageTk
from tkinter import messagebox, ttk
import customtkinter as ctk

def main():
    ventana_principal = tk.Tk()
    ventana_principal.title("Eatics Mexico")
    ventana_principal.geometry("1200x700")

    # Estilo para el Treeview
    style = ttk.Style()
    style.configure("Treeview", 
                    background="#FFFFFF", 
                    foreground="black", 
                    rowheight=25, 
                    fieldbackground="#FFFFFF")
    style.map('Treeview', 
              background=[('selected', '#FFFFFF')])

    # Para mostrar las líneas de las filas y columnas
    style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
    style.configure("Treeview.Heading", font=('Arial', 12))
    style.configure("Treeview", bordercolor="black", borderwidth=1)
    style.configure("Treeview", rowheight=25)
    style.map("Treeview", background=[("selected", "#000000")], foreground=[("selected", "white")])

    # Cargar la imagen de fondo
    ruta_imagen = "imagenes/Fondo_eatics.jpg"  # Ruta de tu imagen de fondo
    imagen_fondo = Image.open(ruta_imagen)
    imagen_fondo = imagen_fondo.resize((1920, 1080))  # Redimensionar la imagen
    foto_fondo = ImageTk.PhotoImage(imagen_fondo)

    # Crear un widget Label para el fondo de la ventana principal
    fondo_label = tk.Label(ventana_principal, image=foto_fondo)
    fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Asegurarse de que la imagen de fondo no sea recolectada por el recolector de basura
    fondo_label.image = foto_fondo

    # Inicializar las referencias a los frames y widgets específicos
    ventana_principal.frame_table = None
    ventana_principal.frame_table2 = None
    ventana_principal.treeview_pedidos = None  # Variable para guardar el Treeview
    
    frame_botones_superiores(ventana_principal)

    ventana_principal.mainloop()

def frame_botones_superiores(ventana):
    ventana.frame_botones_superiores1 = tk.Frame(ventana, background="#FFFFFF")  # Asignar a ventana.frame_botones_superiores1
    
    Button1 = tk.Button(ventana.frame_botones_superiores1, background="#FFFFFF", border=False, text="Generar Pedidos", command=lambda: mostrar_frame(ventana, "frame_table"))
    Button1.pack(side="left", padx=4)
    """""
    Button2 = tk.Button(ventana.frame_botones_superiores1, background="#FFFFFF", border=False, text="Mostrar Pedidos")
    Button2.pack(side="left", padx=4)
    """""
    Button3 = tk.Button(ventana.frame_botones_superiores1, background="#FFFFFF", border=False, text="Subir Pedidos Netsuite", command=lambda: mostrar_frame(ventana, "frame_table2"))
    Button3.pack(side="left", padx=4)

    Button4 = tk.Button(ventana.frame_botones_superiores1, background="#FFFFFF", border=False, text="Configuracion")
    Button4.pack(side="left", padx=4)

    Button5 = tk.Button(ventana.frame_botones_superiores1, background="#FFFFFF", border=False, text="Actualizar DB")
    Button5.pack(side="left", padx=4)

    Button6 = tk.Button(ventana.frame_botones_superiores1, background="#FF0000", border=False, text="X", fg="#FFFFFF", font=("Arial",12), command=lambda: borrar_widgets(ventana))
    Button6.pack(side="right", padx=10)

    ventana.frame_botones_superiores1.pack(fill="x", padx=0, pady=0)

def mostrar_frame(ventana, frame_name):
    # Función para mostrar o crear un frame según el nombre proporcionado
    if frame_name == "frame_table":
        if not ventana.frame_table:
            frame_tabla_generar_pedidos(ventana)
    elif frame_name == "frame_table2":
        if not ventana.frame_table2:
            frame_tabla_generar_pedidos2(ventana)

def mostrar_menu_contextual(event, ventana, entradas):
    # Obtener la fila seleccionada en el Treeview
    item = ventana.treeview_pedidos.identify_row(event.y)
    if item:
        # Configurar el menú contextual
        menu = tk.Menu(ventana, tearoff=0)
        menu.add_command(label="Editar registro", command=lambda: editar_registro(ventana, entradas))
        menu.add_command(label="Eliminar registro", command=lambda: eliminar_registro(ventana))
        menu.post(event.x_root, event.y_root)
        
def frame_tabla_generar_pedidos(ventana):
    # Crear el frame_table si no existe
    if ventana.frame_table is None:
        frame_table = tk.LabelFrame(ventana, width=1100, height=100, background="#FFFFFF", text="Generar Pedidos")
        frame_table.pack(fill="both", side="left", expand=True, padx=10, pady=10)
        ventana.frame_table = frame_table

        # Campos del formulario
        campos = [
            "ID", "Pedido Eatics", "Cantidad Real", "FECHA", "FECHA DE INICIO", 
            "Pedido", "FECHA DE FINALIZACIÓN", "Cantidad", "Grupo", 
            "CÓDIGO", "EAN", "SKU/chedraui", "$Eatics Vs Garcia", 
            "$ BH VS Eatics", "P NETO", "P BRUTO", "P NETO EMP", 
            "P BRUTO EMP", "Internal ID"
        ]

        entradas = []

        # Crear etiquetas y entradas para cada campo
        for index, campo in enumerate(campos[1:], start=1):
            label = ctk.CTkLabel(frame_table, text=campo,corner_radius=5, text_color="#000000", font=("Arial",12,"bold"))
                                                   # background="#00BAD4"
            label.grid(row=index, column=0, padx=10, pady=0, sticky="w")

            entry = ctk.CTkEntry(frame_table, height=10, fg_color="#E4F0FF")
            entry.grid(row=index, column=1, padx=10, pady=5, sticky="w")

            # Agregar la entrada a la lista de entradas
            entradas.append(entry)

        # Botón para guardar el formulario
        guardar_button = ctk.CTkButton(frame_table, text="Guardar", command=lambda: guardar_formulario(ventana, entradas))
        guardar_button.grid(row=len(campos), columnspan=3, pady=10)

        # Crear el frame para mostrar los pedidos
        frame_pedidos = tk.LabelFrame(ventana, width=500, background="#FFFFFF", text="Lista de Pedidos")
        frame_pedidos.pack(fill="both", side="left", expand=True, padx=10, pady=10)

        # Crear un frame para contener el Treeview y las barras de desplazamiento
        tree_frame = tk.Frame(frame_pedidos)
        tree_frame.pack(fill="both", expand=True)

        # Crear Treeview para mostrar los pedidos
        tree = ttk.Treeview(tree_frame, columns=campos, show="headings", style="Treeview")
        tree.pack(side="left", fill="both", expand=True)

        # Añadir barras de desplazamiento
        tree_scroll_y = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree_scroll_y.pack(side="right", fill="y")
        tree.configure(yscrollcommand=tree_scroll_y.set)

        tree_scroll_x = ttk.Scrollbar(frame_pedidos, orient="horizontal", command=tree.xview)
        tree_scroll_x.pack(side="bottom", fill="x")
        tree.configure(xscrollcommand=tree_scroll_x.set)

        # Configurar los tags
        tree.tag_configure("oddrow", background="white")
        tree.tag_configure("evenrow", background="#E4F0FF")

        # Guardar el Treeview en la variable del objeto ventana
        ventana.treeview_pedidos = tree

        # Configurar columnas del Treeview
        for campo in campos:
            tree.heading(campo, text=campo)
            tree.column(campo, width=150, anchor="center")  # Aumentar el ancho de cada columna

        # Asociar evento de clic derecho en el Treeview para mostrar menú contextual
        tree.bind("<Button-3>", lambda event: mostrar_menu_contextual(event, ventana, entradas))
        tree.bind("<Button-1>", lambda event: llenar_entries_desde_treeview(event, ventana, entradas))

        # Mostrar los pedidos en el Treeview
        mostrar_pedidos(ventana)



def mostrar_pedidos(ventana):
    # Conectar con la base de datos y obtener los pedidos
    conexion = sqlite3.connect("DB_Pedidos.db")
    cursor = conexion.cursor()

    cursor.execute('''
        SELECT id, Pedido_Eatics, Cantidad_Real, FECHA, FECHA_DE_INICIO, 
            Pedido, FECHA_DE_FINALIZACION, Cantidad, Grupo, 
            CODIGO, EAN, SKU_chedraui, Eatics_Vs_Garcia, 
            BH_VS_Eatics, P_NETO, P_BRUTO, P_NETO_EMP, 
            P_BRUTO_EMP, Internal_ID
        FROM Pedidos
        ORDER BY id DESC;
    ''')
    pedidos = cursor.fetchall()

    conexion.close()

    # Limpiar datos anteriores en el Treeview
    ventana.treeview_pedidos.delete(*ventana.treeview_pedidos.get_children())

    # Insertar datos de los pedidos en el Treeview
    for index, pedido in enumerate(pedidos):
        if index % 2 == 0:
            ventana.treeview_pedidos.insert("", "end", values=pedido, tags=("evenrow",))
        else:
            ventana.treeview_pedidos.insert("", "end", values=pedido, tags=("oddrow",))

def frame_tabla_generar_pedidos2(ventana):
    # Crear el frame_table2 si no existe
    if ventana.frame_table2 is None:
        frame_table2 = tk.LabelFrame(ventana, width=600, background="#FFFFFF", text="Subir Pedidos Netsuite")
        frame_table2.pack(fill="y", side="right", expand=True, padx=10, pady=10)
        ventana.frame_table2 = frame_table2

def borrar_widgets(ventana):
    # Eliminar todos los widgets adicionales excepto el fondo y los botones superiores
    for widget in ventana.winfo_children():
        if widget.winfo_class() not in ["Frame", "Label"] and widget is not ventana.winfo_children()[0] and widget is not ventana.frame_botones_superiores1:
            widget.destroy()

    # Restaurar los frames si existían
    if ventana.frame_table:
        ventana.frame_table.destroy()
        ventana.frame_table = None

    if ventana.frame_table2:
        ventana.frame_table2.destroy()
        ventana.frame_table2 = None

def guardar_formulario(ventana, entradas):
    # Conectar con la base de datos
    conexion = sqlite3.connect("DB_Pedidos.db")
    cursor = conexion.cursor()

    # Insertar los valores del formulario en la tabla Pedidos
    valores = [entry.get() for entry in entradas]

    cursor.execute('''
        INSERT INTO Pedidos (
            Pedido_Eatics, Cantidad_Real, FECHA, FECHA_DE_INICIO, 
            Pedido, FECHA_DE_FINALIZACION, Cantidad, Grupo, 
            CODIGO, EAN, SKU_chedraui, Eatics_Vs_Garcia, 
            BH_VS_Eatics, P_NETO, P_BRUTO, P_NETO_EMP, 
            P_BRUTO_EMP, Internal_ID
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', valores)

    # Confirmar la transacción y cerrar la conexión
    conexion.commit()
    conexion.close()

    # Mostrar mensaje de éxito
    tk.messagebox.showinfo("Guardado", "El formulario ha sido guardado correctamente.")

    # Actualizar el Treeview
    mostrar_pedidos(ventana)

def mostrar_menu_eliminar(event, ventana):
    # Crear un menú contextual para eliminar registros
    menu = tk.Menu(ventana, tearoff=0)
    menu.add_command(label="Eliminar registro", command=lambda: eliminar_registro(ventana))
    menu.post(event.x_root, event.y_root)

def eliminar_registro(ventana):
    # Obtener los ítems seleccionados en el Treeview
    items = ventana.treeview_pedidos.selection()

    # Si no se seleccionó ningún ítem, salir de la función
    if not items:
        return

    # Confirmar con el usuario antes de eliminar los registros
    respuesta = tk.messagebox.askyesno("Confirmar eliminación", "¿Estás seguro que quieres eliminar los registros seleccionados?")

    if respuesta:
        # Conectar con la base de datos y eliminar los registros seleccionados
        conexion = sqlite3.connect("DB_Pedidos.db")
        cursor = conexion.cursor()

        for item in items:
            valores = ventana.treeview_pedidos.item(item, "values")
            if valores:
                # El id del registro está en la primera columna (valores[0])
                id_registro = valores[0]
                cursor.execute('''
                    DELETE FROM Pedidos WHERE id = ?
                ''', (id_registro,))

        conexion.commit()
        conexion.close()

        # Mostrar mensaje de éxito
        tk.messagebox.showinfo("Eliminado", "Los registros seleccionados han sido eliminados correctamente.")

        # Actualizar el Treeview
        mostrar_pedidos(ventana)

def editar_registro(ventana,entradas_editar):
    # Obtener el item seleccionado en el Treeview
    item = ventana.treeview_pedidos.focus()
    valores = ventana.treeview_pedidos.item(item, "values")

    # Si no se seleccionó ningún item, salir de la función
    if not valores:
        return

    # Crear una ventana emergente para editar los valores
    ventana_editar = tk.Toplevel(ventana)
    ventana_editar.title("Editar Registro")

    # Campos del formulario
    campos2 = [
        "ID","Pedido Eatics", "Cantidad Real", "FECHA", "FECHA DE INICIO", 
        "Pedido", "FECHA DE FINALIZACIÓN", "Cantidad", "Grupo", 
        "CÓDIGO", "EAN", "SKU/chedraui", "$Eatics Vs Garcia", 
        "$ BH VS Eatics", "P NETO", "P BRUTO", "P NETO EMP", 
        "P BRUTO EMP", "Internal ID"
    ]

    entradas_editar = []  # Lista para almacenar las entradas de edición

    # Crear etiquetas y entradas para cada campo
    for index, campo in enumerate(campos2):
        label2 = tk.Label(ventana_editar, text=campo)
        label2.grid(row=index, column=0, padx=10, pady=5, sticky="w")

        entry2 = tk.Entry(ventana_editar)
        entry2.grid(row=index, column=1, padx=10, pady=5, sticky="w")
        entry2.insert(tk.END, valores[index])  # Mostrar valor actual del registro

        # Agregar la entrada a la lista de entradas de edición
        entradas_editar.append(entry2)

    def guardar_cambios():
    # Obtener el item seleccionado en el Treeview
        item2 = ventana.treeview_pedidos.focus()
        valores2 = ventana.treeview_pedidos.item(item2, "values")
        
        # Si no se seleccionó ningún item, salir de la función
        if not valores2:
            return

        # Obtener los nuevos valores ingresados en el formulario de edición
        nuevos_valores = [entry2.get() for entry2 in entradas_editar]
        print(nuevos_valores)

        values= nuevos_valores[1:19]
        print(values)

        id= nuevos_valores[0]
        print(id)
        # Actualizar el registro en la base de datos usando el ID del registro seleccionado
        conexion = sqlite3.connect("DB_Pedidos.db")
        cursor = conexion.cursor()

        cursor.execute('''
            UPDATE Pedidos SET
            Pedido_Eatics = ?,
            Cantidad_Real = ?,
            FECHA = ?,
            FECHA_DE_INICIO = ?,
            Pedido = ?,
            FECHA_DE_FINALIZACION = ?,
            Cantidad = ?,
            Grupo = ?,
            CODIGO = ?,
            EAN = ?,
            SKU_chedraui = ?,
            Eatics_Vs_Garcia = ?,
            BH_VS_Eatics = ?,
            P_NETO = ?,
            P_BRUTO = ?,
            P_NETO_EMP = ?,
            P_BRUTO_EMP = ?,
            Internal_ID = ?
            WHERE id = ?
        ''', (*values,id))

        conexion.commit()
        conexion.close()

        # Cerrar la ventana de edición
        
        ventana_editar.destroy()
        
        # Mostrar mensaje de éxito
        tk.messagebox.showinfo("Editado", "El registro ha sido actualizado correctamente.")
        
        mostrar_pedidos(ventana)


    # Botón para guardar los cambios
    guardar_button = tk.Button(ventana_editar, text="Guardar Cambios", command=guardar_cambios)
    guardar_button.grid(row=len(campos2), columnspan=2, pady=10)







def llenar_entries_desde_treeview(event, ventana, entradas):
    # Obtener el item seleccionado en el Treeview
    item = ventana.treeview_pedidos.focus()
    valores = ventana.treeview_pedidos.item(item, "values")

    # Si no se seleccionó ningún item, salir de la función
    if not valores:
        return

    # Recorrer las entradas y llenarlas con los valores del registro seleccionado
    for index, entry in enumerate(entradas):
        entry.delete(0, tk.END)  # Limpiar el entry antes de insertar nuevos datos
        entry.insert(tk.END, valores[index + 1])  # +1 porque estamos omitiendo el ID




if __name__ == "__main__":
    # Conectar con la base de datos SQLite y crear tablas si no existen
    conexion = sqlite3.connect("DB_Pedidos.db")
    cursor = conexion.cursor()

    # Creación estática de las tablas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Pedido_Eatics TEXT,
            Cantidad_Real INTEGER,
            FECHA TEXT,
            FECHA_DE_INICIO TEXT,
            Pedido TEXT,
            FECHA_DE_FINALIZACION TEXT,
            Cantidad INTEGER,
            Grupo TEXT,
            CODIGO TEXT,
            EAN TEXT,
            SKU_chedraui TEXT,
            Eatics_Vs_Garcia REAL,
            BH_VS_Eatics REAL,
            P_NETO REAL,
            P_BRUTO REAL,
            P_NETO_EMP REAL,
            P_BRUTO_EMP REAL,
            Internal_ID INTEGER
        )
    ''')

    conexion.commit()
    conexion.close()

    main()
