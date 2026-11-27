import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, date
import calendar
import hashlib
import os
import shutil
import subprocess
import sys

import mysql.connector

from tkinter import messagebox

# Marina Itzel Juárez Nava: actualización de conexión MySQL y persistencia de accesos compartidos.
def conectar():

    try:

        conexion = mysql.connector.connect(

            host=os.environ.get("MYSQL_HOST", "localhost"),

            user=os.environ.get("MYSQL_USER", "root"),

            password=os.environ.get("MYSQL_PASSWORD", ""),

            database=os.environ.get("MYSQL_DATABASE", "sistema_alerta_temprana"),
            connection_timeout=8

        )

        return conexion

    except mysql.connector.Error as error:

        messagebox.showerror(

            "Error de conexión",

            f"No se pudo conectar a MySQL:\n{error}"

        )

        return None
    # Valentina Gutiérrez Romero: Diseño y elaboración del script SQL para la estructura de la base de datos.                      
''' DROP DATABASE IF EXISTS sistema_alerta_temprana;
CREATE DATABASE sistema_alerta_temprana
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE sistema_alerta_temprana;

CREATE TABLE grupos (
    id_grupo INT AUTO_INCREMENT PRIMARY KEY,
    grado VARCHAR(20) NOT NULL,
    grupo VARCHAR(10) NOT NULL,
    turno VARCHAR(20) NOT NULL,
    ciclo_escolar VARCHAR(20) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE alumnos (
    id_alumno INT AUTO_INCREMENT PRIMARY KEY,
    matricula VARCHAR(30) UNIQUE NOT NULL,
    nombre_completo VARCHAR(150) NOT NULL,
    id_grupo INT NOT NULL,
    tutor_nombre VARCHAR(150),
    tutor_telefono VARCHAR(20),
    FOREIGN KEY (id_grupo) REFERENCES grupos(id_grupo)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE asistencia (
    id_asistencia INT AUTO_INCREMENT PRIMARY KEY,
    id_alumno INT NOT NULL,
    fecha DATE NOT NULL,
    estado ENUM('Presente', 'Falta', 'Retardo', 'Justificado') NOT NULL,
    observaciones TEXT,
    FOREIGN KEY (id_alumno) REFERENCES alumnos(id_alumno)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE justificantes (
    id_justificante INT AUTO_INCREMENT PRIMARY KEY,
    id_alumno INT NOT NULL,
    fecha_emision DATE NOT NULL,
    fecha_falta DATE NOT NULL,
    motivo TEXT NOT NULL,
    documento_respaldo VARCHAR(255),
    estado ENUM('Pendiente', 'Aprobado', 'Rechazado') DEFAULT 'Aprobado',
    FOREIGN KEY (id_alumno) REFERENCES alumnos(id_alumno)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE reportes_conducta (
    id_reporte INT AUTO_INCREMENT PRIMARY KEY,
    id_alumno INT NOT NULL,
    docente_reporta VARCHAR(150) NOT NULL,
    fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    tipo_incidencia ENUM('Leve', 'Grave', 'Muy Grave') NOT NULL,
    descripcion TEXT NOT NULL,
    estado_alerta ENUM('pendiente', 'vista') DEFAULT 'pendiente',
    FOREIGN KEY (id_alumno) REFERENCES alumnos(id_alumno)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE eventos_escolares (
    id_evento INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    descripcion TEXT,
    fecha_inicio DATETIME NOT NULL,
    fecha_fin DATETIME,
    lugar VARCHAR(100),
    dirigido_a ENUM('Todos', 'Docentes', 'Alumnos', 'Padres') DEFAULT 'Todos'
) ENGINE=InnoDB;

CREATE TABLE carta_compromiso (
    id_carta INT AUTO_INCREMENT PRIMARY KEY,
    id_alumno INT NOT NULL,
    fecha_firma DATE NOT NULL,
    motivo_acuerdo TEXT NOT NULL,
    acuerdos_establecidos TEXT NOT NULL,
    firmado_tutor TINYINT(1) DEFAULT 0,
    estado ENUM('Vigente', 'Cumplida', 'Incumplida') DEFAULT 'Vigente',
    FOREIGN KEY (id_alumno) REFERENCES alumnos(id_alumno)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE seguimiento (
    id_seguimiento INT AUTO_INCREMENT PRIMARY KEY,
    id_alumno INT NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    responsable VARCHAR(100) NOT NULL,
    acciones_realizadas TEXT NOT NULL,
    acuerdos_proximos TEXT,
    estatus_caso ENUM('En proceso', 'Canalizado', 'Cerrado') DEFAULT 'En proceso',
    FOREIGN KEY (id_alumno) REFERENCES alumnos(id_alumno)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;'''

modo_actual = "oscuro"
# Valentina Gutiérrez Romero: Diseño de la paleta de colores para las interfaces y los modos claro y oscuro.
FONDO = "#081426"
AZUL = "#102B50"
AZUL_CLARO = "#173B68"
CIAN = "#32C5F4"
BLANCO = "#FFFFFF"
GRIS = "#8A9BB2"
CAMPO = "#F0F4F9"
TEXTO = "#152B46"
VERDE = "#19B887"
ROJO = "#D9485F"
AMARILLO = "#B7791F"

TEMAS = {
    "oscuro": {
        "fondo": "#081426",
        "encabezado": "#102B50",
        "azul_claro": "#10233D",
        "tarjeta": "#10233D",
        "texto": "#FFFFFF",
        "secundario": "#8A9BB2",
        "campo": "#172C46",
        "texto_campo": "#FFFFFF",
        "borde": "#29425F",
        "separador": "#081426",
        "sombra": "#050D18",
        "acento": "#32C5F4",
        "acento_hover": "#168ED0",
        "verde": "#19B887",
        "rojo": "#FF7185",
        "amarillo": "#F6C76B",
        "boton_texto": "#081426",
        "boton_secundario": "#10233D",
        "boton_secundario_texto": "#32C5F4",
        "pie": "#081426",
        "reloj": "#32C5F4",
        "icono": "#32C5F4",
        "error": "#FF7185",
        "aviso": "#F6C76B",
        "panel": "#10233D",
        "barra": "#081426",
        "seleccion": "#173B68",
        "tabla_cabecera": "#173B68",
        "texto_barra": "#FFFFFF",
        "secundario_barra": "#B9CBE2",
        "seleccion_barra": "#203D60",
        "hover_barra": "#173B68"
    },
    "claro": {
        "fondo": "#F1F5F9",
        "encabezado": "#FFFFFF",
        "azul_claro": "#E2EAF4",
        "tarjeta": "#FFFFFF",
        "texto": "#172033",
        "secundario": "#526176",
        "campo": "#FFFFFF",
        "texto_campo": "#172033",
        "borde": "#CBD5E1",
        "separador": "#D7E0EA",
        "sombra": "#CBD5E1",
        "acento": "#0756A8",
        "acento_hover": "#064580",
        "verde": "#087F5B",
        "rojo": "#B4233D",
        "amarillo": "#805900",
        "boton_texto": "#FFFFFF",
        "boton_secundario": "#FFFFFF",
        "boton_secundario_texto": "#0756A8",
        "pie": "#F1F5F9",
        "reloj": "#0756A8",
        "icono": "#0756A8",
        "error": "#B4233D",
        "aviso": "#805900",
        "panel": "#FFFFFF",
        "barra": "#081426",
        "seleccion": "#CFE4FF",
        "tabla_cabecera": "#DCE7F3",
        "texto_barra": "#FFFFFF",
        "secundario_barra": "#B9CBE2",
        "seleccion_barra": "#203D60",
        "hover_barra": "#173B68"
    }
}

def C(clave):
    return TEMAS[modo_actual][clave]

ventana = tk.Tk()
raiz_principal = ventana
ventana.title("Sistema de Alerta Temprana Para Situaciones de riesgo | Escuela Primaria Nezahualcóyotl")
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()
ancho = int(ancho_pantalla * 1.00)
alto = int(alto_pantalla * 1.00)
ventana.geometry(f"{ancho}x{alto}+0+0")
ventana.update_idletasks()
ventana.minsize(320, 450)


                                             
GRUPO_DOCENTE = "4° A"
GRUPO_SESION = GRUPO_DOCENTE
USUARIO_SESION = ""
CONTRASENAS_GRUPOS = {f"{n}° A": f"grupo{n}" for n in range(1, 7)}
CALENDARIO_PDF = ""
ALUMNOS_COMPARTIDOS = []
REGISTROS_ASISTENCIA = []
ALERTAS_SEGUIMIENTO = []
ARCHIVOS_JUSTIFICANTES = []
GRUPOS_ESCOLARES = {f"{n}° A": [] for n in range(1, 7)}
UMBRAL_ALERTA = 3

GRADOS_DB = {1: "Primero", 2: "Segundo", 3: "Tercero", 4: "Cuarto", 5: "Quinto", 6: "Sexto"}
GRADOS_UI = {v: f"{k}° A" for k, v in GRADOS_DB.items()}

def hash_clave(clave):
    return hashlib.sha256(clave.encode("utf-8")).hexdigest()

def ejecutar_consulta(sql, parametros=(), obtener=False, commit=True):
    conexion = conectar()
    if conexion is None:
        return None if obtener else False
    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(sql, parametros)
        resultado = cursor.fetchall() if obtener else True
        if commit:
            conexion.commit()
        return resultado
    except mysql.connector.Error as error:
        conexion.rollback()
        messagebox.showerror("Error de base de datos", str(error))
        return None if obtener else False
    finally:
        if cursor:
            cursor.close()
        conexion.close()

def preparar_base_aplicacion():
    """Crea únicamente la tabla auxiliar de accesos; nunca elimina ni recrea tablas existentes."""
    conexion = conectar()
    if conexion is None:
        return False
    cursor = conexion.cursor()
    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS accesos_sistema (
            id_acceso INT AUTO_INCREMENT PRIMARY KEY,
            tipo ENUM('director','docente') NOT NULL,
            id_grupo INT NULL,
            usuario VARCHAR(100) NOT NULL,
            clave_hash CHAR(64) NOT NULL,
            clave_visible VARCHAR(255) NULL,
            UNIQUE KEY uq_acceso_grupo (tipo, id_grupo),
            UNIQUE KEY uq_acceso_usuario (usuario)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""")
        cursor.execute("SHOW COLUMNS FROM accesos_sistema LIKE 'clave_visible'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE accesos_sistema ADD COLUMN clave_visible VARCHAR(255) NULL")
        conexion.commit()
                                                                                 
        cursor.execute("SELECT COUNT(*) FROM accesos_sistema WHERE tipo='director'")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO accesos_sistema (tipo,id_grupo,usuario,clave_hash,clave_visible) VALUES ('director',NULL,'director',%s,%s)", (hash_clave("654321"), "654321"))
        cursor.execute("SELECT id_grupo, grado, grupo FROM grupos")
        filas = cursor.fetchall()
        for id_grupo, grado, letra in filas:
            numero_default = next((n for n, nombre in GRADOS_DB.items()
                                   if nombre.lower() == str(grado).lower()), None)
            if numero_default:
                clave_default = f"grupo{numero_default}"
                cursor.execute("""UPDATE accesos_sistema SET clave_visible=%s
                    WHERE tipo='docente' AND id_grupo=%s AND clave_visible IS NULL
                    AND clave_hash=%s""",
                    (clave_default, id_grupo, hash_clave(clave_default)))
            etiqueta = GRADOS_UI.get(str(grado), f"{grado}° {letra}")
            cursor.execute("SELECT COUNT(*) FROM accesos_sistema WHERE tipo='docente' AND id_grupo=%s", (id_grupo,))
            if cursor.fetchone()[0] == 0:
                numero = next((n for n, nombre in GRADOS_DB.items() if nombre.lower() == str(grado).lower()), None)
                if numero:
                    cursor.execute("INSERT INTO accesos_sistema (tipo,id_grupo,usuario,clave_hash,clave_visible) VALUES ('docente',%s,%s,%s,%s)", (id_grupo, etiqueta, hash_clave(f"grupo{numero}"), f"grupo{numero}"))
        conexion.commit()
        return True
    except mysql.connector.Error as error:
        conexion.rollback()
        messagebox.showerror("Preparación de MySQL", str(error))
        return False
    finally:
        cursor.close()
        conexion.close()

def obtener_grupos_db():
    filas = ejecutar_consulta("SELECT id_grupo, grado, grupo, turno, ciclo_escolar FROM grupos ORDER BY id_grupo", obtener=True) or []
    resultado = {}
    for fila in filas:
        grado = str(fila["grado"])
        etiqueta = GRADOS_UI.get(grado, f"{grado}° {fila['grupo']}")
        resultado[etiqueta] = fila
    return resultado

def cargar_datos():
    """Carga grupos, alumnos, asistencias y alertas exclusivamente desde MySQL."""
    global ALUMNOS_COMPARTIDOS, REGISTROS_ASISTENCIA, ALERTAS_SEGUIMIENTO, GRUPOS_ESCOLARES, CONTRASENAS_GRUPOS
    if not preparar_base_aplicacion():
        return
    grupos_db = obtener_grupos_db()
    GRUPOS_ESCOLARES = {nombre: [] for nombre in grupos_db}
    CONTRASENAS_GRUPOS = {}
    accesos = ejecutar_consulta("""SELECT a.usuario, a.clave_hash, a.id_grupo, g.grado, g.grupo
        FROM accesos_sistema a LEFT JOIN grupos g ON g.id_grupo=a.id_grupo
        WHERE a.tipo='docente'""", obtener=True) or []
    for acceso in accesos:
        grado = str(acceso["grado"] or "")
        etiqueta = GRADOS_UI.get(grado, f"{grado}° {acceso['grupo']}")
                                                                                          
        CONTRASENAS_GRUPOS[etiqueta] = acceso["clave_hash"]
    alumnos_db = ejecutar_consulta("""SELECT a.id_alumno,a.matricula,a.nombre_completo,a.id_grupo,g.grado,g.grupo
        FROM alumnos a JOIN grupos g ON g.id_grupo=a.id_grupo ORDER BY a.nombre_completo""", obtener=True) or []
    ALUMNOS_COMPARTIDOS = []
    mapa_alumnos = {}
    for fila in alumnos_db:
        etiqueta = GRADOS_UI.get(str(fila["grado"]), f"{fila['grado']}° {fila['grupo']}")
        alumno = {"id_alumno": fila["id_alumno"], "matricula": fila["matricula"], "nombre": fila["nombre_completo"], "grupo": etiqueta, "asistencias": 0, "faltas": 0, "retardos": 0}
        GRUPOS_ESCOLARES.setdefault(etiqueta, []).append(alumno["nombre"])
        mapa_alumnos[alumno["id_alumno"]] = alumno
        if etiqueta == GRUPO_DOCENTE:
            ALUMNOS_COMPARTIDOS.append(alumno)
    filas_asistencia = ejecutar_consulta("""SELECT a.id_asistencia,a.id_alumno,a.fecha,a.estado,a.observaciones
        FROM asistencia a ORDER BY a.fecha""", obtener=True) or []
    REGISTROS_ASISTENCIA = []
    for fila in filas_asistencia:
        alumno = mapa_alumnos.get(fila["id_alumno"])
        if not alumno:
            continue
        estado = "Justificada" if fila["estado"] == "Justificado" else fila["estado"]
        fecha_valor = fila["fecha"].isoformat() if hasattr(fila["fecha"], "isoformat") else str(fila["fecha"])
        REGISTROS_ASISTENCIA.append({"id_asistencia": fila["id_asistencia"], "id_alumno": fila["id_alumno"], "nombre": alumno["nombre"], "grupo": alumno["grupo"], "fecha": fecha_valor, "estado": estado, "observaciones": fila.get("observaciones") or ""})
        if estado in ("Presente", "Falta", "Retardo"):
            alumno[{"Presente":"asistencias","Falta":"faltas","Retardo":"retardos"}[estado]] += 1
    ALERTAS_SEGUIMIENTO = []
    reportes = ejecutar_consulta("""SELECT r.id_reporte,r.id_alumno,r.fecha_hora,r.tipo_incidencia,r.descripcion,r.estado_alerta
        FROM reportes_conducta r ORDER BY r.fecha_hora DESC""", obtener=True) or []
    for fila in reportes:
        alumno = mapa_alumnos.get(fila["id_alumno"])
        if alumno:
            fecha_valor = fila["fecha_hora"].strftime("%Y-%m-%d") if hasattr(fila["fecha_hora"], "strftime") else str(fila["fecha_hora"])[:10]
            ALERTAS_SEGUIMIENTO.append({"id_reporte": fila["id_reporte"], "nombre": alumno["nombre"], "grupo": alumno["grupo"], "faltas": alumno["faltas"], "estado": fila["estado_alerta"], "fecha": fecha_valor, "descripcion": fila["descripcion"]})

def guardar_datos():
    """Guarda cambios de alumnos y asistencias en MySQL; no utiliza archivos JSON."""
    grupos_db = obtener_grupos_db()
    conexion = conectar()
    if conexion is None:
        return
    cursor = conexion.cursor(dictionary=True)
    try:
                                                                                                          
        import re
        for grupo, nombres in GRUPOS_ESCOLARES.items():
            info = grupos_db.get(grupo)
            if not info:
                continue
            for nombre in nombres:
                clave = re.sub(r"[^A-Za-z0-9]", "", nombre.upper())[:12] or "ALUMNO"
                matricula = f"{info['id_grupo']:02d}-{clave}-{hashlib.sha1(nombre.encode('utf-8')).hexdigest()[:6].upper()}"
                cursor.execute("""INSERT INTO alumnos (matricula,nombre_completo,id_grupo) VALUES (%s,%s,%s)
                    ON DUPLICATE KEY UPDATE nombre_completo=VALUES(nombre_completo), id_grupo=VALUES(id_grupo)""", (matricula, nombre, info["id_grupo"]))
                                                                           
        cursor.execute("SELECT id_alumno,nombre_completo,id_grupo FROM alumnos")
        alumnos_db = cursor.fetchall()
        mapa = {(r["nombre_completo"], r["id_grupo"]): r["id_alumno"] for r in alumnos_db}
        for registro in REGISTROS_ASISTENCIA:
            info = grupos_db.get(registro.get("grupo", ""))
            if not info:
                continue
            id_alumno = registro.get("id_alumno") or mapa.get((registro.get("nombre"), info["id_grupo"]))
            if not id_alumno:
                continue
            estado = "Justificado" if registro.get("estado") == "Justificada" else registro.get("estado")
            if estado not in ("Presente", "Falta", "Retardo", "Justificado"):
                continue
            cursor.execute("SELECT id_asistencia FROM asistencia WHERE id_alumno=%s AND fecha=%s ORDER BY id_asistencia LIMIT 1", (id_alumno, registro.get("fecha")))
            existente = cursor.fetchone()
            if existente:
                cursor.execute("UPDATE asistencia SET estado=%s, observaciones=%s WHERE id_asistencia=%s", (estado, registro.get("observaciones", ""), existente["id_asistencia"]))
            else:
                cursor.execute("INSERT INTO asistencia (id_alumno,fecha,estado,observaciones) VALUES (%s,%s,%s,%s)", (id_alumno, registro.get("fecha"), estado, registro.get("observaciones", "")))
                                                                                      
        for alerta in ALERTAS_SEGUIMIENTO:
            info = grupos_db.get(alerta.get("grupo", ""))
            if not info:
                continue
            id_alumno = mapa.get((alerta.get("nombre"), info["id_grupo"]))
            if not id_alumno:
                continue
            cursor.execute("SELECT id_reporte FROM reportes_conducta WHERE id_alumno=%s AND descripcion=%s LIMIT 1", (id_alumno, "Alerta automática: acumuló tres faltas o más."))
            if not cursor.fetchone():
                cursor.execute("""INSERT INTO reportes_conducta
                    (id_alumno,docente_reporta,tipo_incidencia,descripcion,estado_alerta)
                    VALUES (%s,%s,'Grave',%s,'pendiente')""",
                    (id_alumno, USUARIO_SESION or "Sistema", "Alerta automática: acumuló tres faltas o más."))
                                                                                    
        for grupo, clave in CONTRASENAS_GRUPOS.items():
            info = grupos_db.get(grupo)
            if info and len(str(clave)) == 64 and all(c in "0123456789abcdef" for c in str(clave).lower()):
                continue
            if info:
                cursor.execute("UPDATE accesos_sistema SET clave_hash=%s WHERE tipo='docente' AND id_grupo=%s", (hash_clave(str(clave)), info["id_grupo"]))
        conexion.commit()
    except (mysql.connector.Error, ValueError) as error:
        conexion.rollback()
        messagebox.showerror("Error al guardar en MySQL", str(error))
    finally:
        cursor.close()
        conexion.close()

cargar_datos()

def seleccionar_calendario_pdf():
    global CALENDARIO_PDF
    ruta = filedialog.askopenfilename(
        title="Seleccionar calendario escolar en PDF",
        filetypes=[("Documento PDF", "*.pdf")]
    )
    if ruta:
        CALENDARIO_PDF = ruta
        guardar_datos()
        messagebox.showinfo("Calendario actualizado", "El calendario escolar en PDF quedó asignado para ambos paneles.")

def abrir_calendario_pdf():
    if not CALENDARIO_PDF or not os.path.isfile(CALENDARIO_PDF):
        messagebox.showwarning(
            "Calendario no disponible",
            "Primero selecciona el archivo PDF del calendario escolar desde el panel de dirección."
        )
        return
    try:
        if sys.platform.startswith("win"):
            os.startfile(CALENDARIO_PDF)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", CALENDARIO_PDF])
        else:
            subprocess.Popen(["xdg-open", CALENDARIO_PDF])
    except OSError as error:
        messagebox.showerror("No se pudo abrir el calendario", str(error))

def dibujar_grafica_asistencia(parent, grupo, registros, colores, alumnos=None):
    fondo = colores["tarjeta"]
    texto = colores["texto"]
    area_grafica = tk.Frame(parent, bg=fondo)
    area_grafica.pack(fill="x", padx=14, pady=(4, 12))
    canvas = tk.Canvas(area_grafica, height=245, bg=fondo, highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)
    panel_detalle = tk.Frame(area_grafica, bg=fondo, width=235,
                             highlightbackground=colores["borde"], highlightthickness=1)
    panel_detalle.pack(side="right", fill="y", padx=(10, 0))
    panel_detalle.pack_propagate(False)
    canvas.update_idletasks()
    ancho = max(canvas.winfo_width(), 560)
    canvas.configure(width=ancho)
    tk.Label(panel_detalle, text="DETALLE DE ASISTENCIA", bg=fondo, fg=texto,
             font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=10, pady=(10, 6))
    lista_detalle = tk.Listbox(panel_detalle, bg=fondo, fg=texto,
                               selectbackground="#2765A5", relief="flat",
                               highlightthickness=0, font=("Segoe UI", 9))
    lista_detalle.pack(fill="both", expand=True, padx=8, pady=(0, 8))
    lista_detalle.insert("end", "Haz clic en una barra para ver los alumnos.")
    estados = [
        ("Asistió", ("Presente", "Asistió", "Asistio"), "#19B887"),
        ("Retardo", ("Retardo",), "#F6C76B"),
        ("Falta", ("Falta", "Ausente"), "#FF7185"),
        ("Justificada", ("Justificada",), "#32C5F4")
    ]
    conteos = [sum(1 for r in registros
                   if r.get("grupo", GRUPO_DOCENTE) == grupo
                   and r.get("estado") in equivalentes)
               for _, equivalentes, _ in estados]
    if alumnos is not None and grupo == GRUPO_DOCENTE and not any(
            r.get("grupo", GRUPO_DOCENTE) == grupo for r in registros):
        conteos = [
            sum(a.get("asistencias", 0) for a in alumnos),
            sum(a.get("retardos", 0) for a in alumnos),
            sum(a.get("faltas", 0) for a in alumnos),
            0
        ]
    maximo = max(conteos + [1])
    canvas.create_text(18, 18, text=f"ASISTENCIAS DEL GRUPO {grupo}",
                       anchor="w", fill=texto, font=("Segoe UI", 11, "bold"))
    margen_izq, margen_der, y_base, alto_barra = 38, 22, 188, 125
    espacio = (ancho - margen_izq - margen_der) / 4
    for i, ((nombre, _, color), valor) in enumerate(zip(estados, conteos)):
        centro = margen_izq + espacio * i + espacio / 2
        alto = (valor / maximo) * alto_barra
        x0, x1 = centro - 28, centro + 28
        canvas.create_line(x0 - 15, y_base, x1 + 15, y_base, fill=colores["borde"])
        barra_id = canvas.create_rectangle(x0, y_base - alto, x1, y_base, fill=color, outline=color,
                                           tags=(f"barra_{i}",))
        canvas.create_text(centro, y_base - alto - 14, text=str(valor),
                           fill=texto, font=("Segoe UI", 10, "bold"))
        etiqueta_id = canvas.create_text(centro, y_base + 18, text=nombre,
                                         fill=texto, font=("Segoe UI", 9),
                                         tags=(f"barra_{i}",))
        equivalentes_estado = estados[i][1]
        def ver_detalle(event=None, equivalentes=equivalentes_estado, titulo=nombre):
            coincidencias = [r for r in registros
                if r.get("grupo", GRUPO_DOCENTE) == grupo
                and r.get("estado") in equivalentes]
            if not coincidencias and alumnos:
                claves = {"Asistió": "asistencias", "Retardo": "retardos",
                          "Falta": "faltas", "Justificada": "justificadas"}
                campo = claves.get(titulo)
                coincidencias = [{"nombre": a.get("nombre", ""), "fecha": "Acumulado"}
                    for a in alumnos if campo and a.get(campo, 0)]
            lista_detalle.delete(0, "end")
            tk.Label(panel_detalle, text=f"ALUMNOS: {titulo.upper()}",
                     bg=fondo, fg=texto, font=("Segoe UI", 9, "bold")).pack_forget()
            nombres = sorted({f"{r.get('nombre','')}  —  {r.get('fecha','')}"
                              for r in coincidencias})
            for nombre_item in nombres:
                lista_detalle.insert("end", nombre_item)
            if not nombres:
                lista_detalle.insert("end", "No hay alumnos registrados.")
        canvas.tag_bind(f"barra_{i}", "<Button-1>", ver_detalle)
        canvas.tag_bind(f"barra_{i}", "<Enter>", lambda e: canvas.configure(cursor="hand2"))
        canvas.tag_bind(f"barra_{i}", "<Leave>", lambda e: canvas.configure(cursor=""))
    return canvas

def obtener_estado_dia(nombre, grupo, fecha):
    coincidencias = [r for r in REGISTROS_ASISTENCIA
                     if r.get("nombre") == nombre and r.get("grupo", GRUPO_DOCENTE) == grupo
                     and r.get("fecha") == fecha]
    return coincidencias[-1]["estado"] if coincidencias else "Sin registro"

def actualizar_alerta_alumno(alumno, grupo=GRUPO_DOCENTE):
    faltas = alumno.get("faltas", 0)
    existente = next((a for a in ALERTAS_SEGUIMIENTO
                      if a["nombre"] == alumno["nombre"] and a["grupo"] == grupo), None)
    if faltas >= UMBRAL_ALERTA:
        if existente is None:
            ALERTAS_SEGUIMIENTO.append({
                "nombre": alumno["nombre"], "grupo": grupo,
                "faltas": faltas, "estado": "Pendiente de seguimiento",
                "fecha": date.today().isoformat()
            })
        else:
            existente["faltas"] = faltas
    elif existente is not None:
        ALERTAS_SEGUIMIENTO.remove(existente)

      
def actualizar_reloj():
    ahora = datetime.now()
    texto = ahora.strftime("%d/%m/%Y  |  %H:%M:%S")
    reloj.config(text=texto)
    ventana.after(1000, actualizar_reloj)

def alternar_contrasena():
    if entrada_contra.cget("show") == "*":
        entrada_contra.config(show="")
        boton_ver.config(text="◉")
    else:
        entrada_contra.config(show="*")
        boton_ver.config(text="◎")

def alternar_tema():
    global modo_actual
    modo_actual = "claro" if modo_actual == "oscuro" else "oscuro"
    aplicar_tema()

def limpiar_campos(event=None):
    entrada_usuario.delete(0, tk.END)
    entrada_contra.delete(0, tk.END)
    mensaje.config(text="")
    entrada_usuario.focus_set()

# Marina Itzel Juárez Nava: validación de acceso con contraseñas almacenadas y verificadas en MySQL.
def ingresar():
    usuario = entrada_usuario.get().strip()
    contrasena = entrada_contra.get()
    if not usuario or not contrasena:
        mensaje.config(text="Completa los campos para continuar.", fg=TEMAS[modo_actual]["error"])
        return
    global GRUPO_SESION, USUARIO_SESION
    conexion = conectar()
    if conexion is None:
        mensaje.config(text="No se pudo conectar con MySQL.", fg=TEMAS[modo_actual]["error"])
        return
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT usuario,clave_hash FROM accesos_sistema WHERE tipo='director' LIMIT 1")
        director = cursor.fetchone()
        if director and hash_clave(contrasena) == director["clave_hash"]:
            USUARIO_SESION = usuario or director["usuario"]
            ventana.withdraw()
            abrir_director()
            return
        cursor.execute("""SELECT g.grado,g.grupo,a.clave_hash FROM accesos_sistema a
            JOIN grupos g ON g.id_grupo=a.id_grupo WHERE a.tipo='docente'""")
        for fila in cursor.fetchall():
            if hash_clave(contrasena) == fila["clave_hash"]:
                grado = str(fila["grado"])
                GRUPO_SESION = GRADOS_UI.get(grado, f"{grado}° {fila['grupo']}")
                USUARIO_SESION = usuario
                ventana.withdraw()
                abrir_docente(GRUPO_SESION, usuario)
                return
        mensaje.config(text="Contraseña incorrecta.", fg=TEMAS[modo_actual]["error"])
    except mysql.connector.Error as error:
        messagebox.showerror("Error de acceso", str(error))
    finally:
        cursor.close()
        conexion.close()

                  
def abrir_docente(grupo_docente=None, nombre_docente="Docente"):
    grupo_docente = grupo_docente or GRUPO_SESION
    if grupo_docente == GRUPO_DOCENTE:
        alumnos = ALUMNOS_COMPARTIDOS
    else:
        alumnos = []
        for nombre in GRUPOS_ESCOLARES.get(grupo_docente, []):
            relacionados = [r for r in REGISTROS_ASISTENCIA
                            if r.get("nombre") == nombre and r.get("grupo") == grupo_docente]
            alumnos.append({
                "nombre": nombre,
                "asistencias": sum(r.get("estado") in ("Presente", "Asistió", "Asistio") for r in relacionados),
                "faltas": sum(r.get("estado") == "Falta" for r in relacionados),
                "retardos": sum(r.get("estado") == "Retardo" for r in relacionados)
            })
    registros = REGISTROS_ASISTENCIA
    for alumno_inicial in alumnos:
        actualizar_alerta_alumno(alumno_inicial, grupo_docente)
    reportes_conducta = []
    sel_nombre = None
    vista_docente_actual = "Inicio"

    ventana_docente = tk.Toplevel(raiz_principal)
    ventana_docente.title("Sistema de alerta temprana | Panel de Docente ")

    def volver_login():
        ventana_docente.destroy()
        raiz_principal.deiconify()
        limpiar_campos()

    ventana_docente.protocol("WM_DELETE_WINDOW", lambda: (ventana_docente.destroy(), raiz_principal.destroy()))
    ancho_p = ventana_docente.winfo_screenwidth()
    alto_p = ventana_docente.winfo_screenheight()
    w_doc = int(ancho_p * 0.94)
    h_doc = int(alto_p * 0.90)
    x_doc = (ancho_p - w_doc) // 2
    y_doc = (alto_p - h_doc) // 2
    # Rivas Mira Yaretzi Guadalupe: el panel docente se abre maximizado y se adapta al ancho disponible.
    ventana_docente.geometry(f"{ancho_p}x{alto_p}+0+0")
    ventana_docente.minsize(640, 480)
    try:
        ventana_docente.state("zoomed")
    except tk.TclError:
        ventana_docente.attributes("-zoomed", True)
    ventana_docente.configure(bg=C("fondo"))
    ventana_docente.bind("<Configure>", lambda e: sidebar_doc.configure(
        width=max(175, min(230, int(ventana_docente.winfo_width() * 0.19)))
    ) if e.widget is ventana_docente else None)

    estilo = ttk.Style()
    estilo.theme_use("clam")

    def configurar_estilos():
        estilo.configure("Treeview", background=C("panel"), foreground=C("texto"),
                         fieldbackground=C("panel"), rowheight=34,
                         font=("Segoe UI", 10), borderwidth=0)
        estilo.configure("Treeview.Heading", background=C("tabla_cabecera"),
                         foreground=C("texto"), font=("Segoe UI", 10, "bold"),
                         padding=9, relief="flat")
        estilo.map("Treeview",
                   background=[("selected", C("seleccion"))],
                   foreground=[("selected", C("texto"))])
        estilo.configure("TCombobox", fieldbackground=C("campo"),
                         background=C("campo"), foreground=C("texto_campo"),
                         arrowcolor=C("texto"))
        estilo.map("TCombobox",
                   fieldbackground=[("readonly", C("campo"))],
                   foreground=[("readonly", C("texto_campo"))])
        estilo.configure("TEntry", fieldbackground=C("campo"),
                         foreground=C("texto_campo"), padding=7)
        ventana_docente.option_add("*TEntry.insertBackground",
                                   "#FFFFFF" if modo_actual == "oscuro" else "#172033")
        estilo.configure("Vertical.TScrollbar", background=C("borde"),
                         troughcolor=C("fondo"), borderwidth=0, arrowsize=12)

    principal_doc = tk.Frame(ventana_docente, bg=C("fondo"))
    principal_doc.pack(fill="both", expand=True)
    sidebar_doc = tk.Frame(principal_doc, bg=C("barra"), width=230)
    sidebar_doc.pack(side="left", fill="y")
    sidebar_doc.pack_propagate(False)
    zona_derecha_doc = tk.Frame(principal_doc, bg=C("fondo"))
    zona_derecha_doc.pack(side="left", fill="both", expand=True)

    marca_doc = tk.Frame(sidebar_doc, bg=C("barra"))
    marca_doc.pack(fill="x", padx=18, pady=(22, 20))
    tk.Label(marca_doc, text="NEZAHUALCÓYOTL",
             font=("Segoe UI", 15, "bold"), bg=C("barra"),
             fg=C("acento")).pack(anchor="w")
    tk.Label(marca_doc, text="SISTEMA DE ALERTA TEMPRANA\nSITUACIONES DE RIESGO ESCOLAR",
             font=("Segoe UI", 9), bg=C("barra"),
             fg=C("secundario_barra"), justify="left").pack(anchor="w", pady=(5, 0))
    tk.Frame(sidebar_doc, bg=C("borde"), height=1).pack(fill="x", padx=16, pady=(0, 14))
    tk.Label(sidebar_doc, text="MENÚ PRINCIPAL", font=("Segoe UI", 8, "bold"),
             bg=C("barra"), fg=C("secundario_barra")).pack(anchor="w", padx=18, pady=(0, 8))
    menu_frame_doc = tk.Frame(sidebar_doc, bg=C("barra"))
    menu_frame_doc.pack(fill="x")

    tk.Button(sidebar_doc, text="↪  CERRAR SESIÓN", command=volver_login,
              font=("Segoe UI", 10, "bold"), bg=C("seleccion_barra"),
              fg=C("texto_barra"), activebackground=C("hover_barra"),
              activeforeground=C("texto_barra"), relief="flat", bd=0,
              cursor="hand2", padx=10, pady=11).pack(side="bottom", fill="x", padx=10, pady=14)

    header_doc = tk.Frame(zona_derecha_doc, bg=C("encabezado"), height=76)
    header_doc.pack(fill="x")
    header_doc.pack_propagate(False)
    titulo_header_doc = tk.Label(header_doc, text="PANEL DE DOCENTE",
                                 font=("Segoe UI", 17, "bold"),
                                 bg=C("encabezado"), fg=C("texto"))
    titulo_header_doc.pack(side="left", padx=22)

    def alternar_tema_docente():
        global modo_actual
        modo_actual = "claro" if modo_actual == "oscuro" else "oscuro"
        reconstruir_interfaz_docente()

    boton_tema_doc = tk.Button(header_doc, text="☀  Tema claro",
                               command=alternar_tema_docente,
                               font=("Segoe UI", 9, "bold"), relief="flat",
                               bd=0, cursor="hand2", padx=12, pady=8)
    boton_tema_doc.pack(side="right", padx=(5, 18), pady=16)
    usuario_doc = tk.Label(header_doc, text=f"●  {nombre_docente}",
                           font=("Segoe UI", 10, "bold"),
                           bg=C("encabezado"), fg=C("verde"))
    usuario_doc.pack(side="right", padx=8)
    tk.Frame(zona_derecha_doc, bg=C("borde"), height=1).pack(fill="x")

    contenedor_panel_doc = tk.Frame(zona_derecha_doc, bg=C("fondo"))
    contenedor_panel_doc.pack(fill="both", expand=True)
    canvas_doc = tk.Canvas(contenedor_panel_doc, bg=C("fondo"), highlightthickness=0)
    scroll_vertical_doc = ttk.Scrollbar(contenedor_panel_doc, orient="vertical",
                                        command=canvas_doc.yview,
                                        style="Vertical.TScrollbar")
    canvas_doc.configure(yscrollcommand=scroll_vertical_doc.set)
    scroll_vertical_doc.pack(side="right", fill="y")
    canvas_doc.pack(side="left", fill="both", expand=True)
    panel_doc = tk.Frame(canvas_doc, bg=C("fondo"))
    panel_id_doc = canvas_doc.create_window((0, 0), window=panel_doc, anchor="nw")
    panel_doc.bind("<Configure>", lambda e: canvas_doc.configure(scrollregion=canvas_doc.bbox("all")))
    canvas_doc.bind("<Configure>", lambda e: canvas_doc.itemconfigure(panel_id_doc, width=e.width))
   # Valentina Gutiérrez Romero: Desarrollo de la función para limpiar el contenido del panel y reiniciar su desplazamiento.
    def limpiar_panel():
        for widget in panel_doc.winfo_children():
            widget.destroy()
        canvas_doc.yview_moveto(0)

    def etiqueta(parent, texto, tam=10, negrita=False, color=None, **kwargs):
        return tk.Label(parent, text=texto,
                        font=("Segoe UI", tam, "bold" if negrita else "normal"),
                        bg=kwargs.pop("bg", C("fondo")),
                        fg=color or C("texto"), **kwargs)

    def boton_padre(parent, texto, comando, color=None, texto_color=None):
        return tk.Button(parent, text=texto, command=comando,
                         bg=color or C("acento"),
                         fg=texto_color or C("boton_texto"),
                         activebackground=C("acento_hover"),
                         activeforeground="#FFFFFF",
                         font=("Segoe UI", 10, "bold"), relief="flat",
                         bd=0, cursor="hand2", padx=13, pady=9)

    def caja_tarjeta(parent, titulo, valor, detalle, color):
        caja = tk.Frame(parent, bg=C("tarjeta"),
                        highlightbackground=C("borde"), highlightthickness=1)
        tk.Frame(caja, bg=color, height=4).pack(fill="x")
        etiqueta(caja, titulo, 10, color=C("secundario"), bg=C("tarjeta")).pack(anchor="w", padx=14, pady=(12, 2))
        etiqueta(caja, valor, 24, True, bg=C("tarjeta")).pack(anchor="w", padx=14)
        etiqueta(caja, detalle, 9, color=C("secundario"), bg=C("tarjeta")).pack(anchor="w", padx=14, pady=(2, 12))
        return caja

    entrada_nombre = None
    entrada_fecha = None
    frame_tabla_checks = None
    frame_grafica_doc = None

    def registrar_check(nombre, estado):
        try:
            fecha = date.fromisoformat(entrada_fecha.get().strip()).isoformat()
        except ValueError:
            messagebox.showerror("Fecha", "Formato AAAA-MM-DD")
            return

        al = next(a for a in alumnos if a["nombre"] == nombre)
        faltas_antes = al["faltas"]
        registro = next((r for r in registros
                         if r["nombre"] == nombre and r["fecha"] == fecha
                         and r.get("grupo", grupo_docente) == grupo_docente), None)

        if registro:
            estado_anterior = registro["estado"]
            if estado_anterior == "Presente":
                al["asistencias"] -= 1
            elif estado_anterior == "Falta":
                al["faltas"] -= 1
            elif estado_anterior == "Retardo":
                al["retardos"] -= 1
            registro["estado"] = estado
        else:
            registro = {"fecha": fecha, "nombre": nombre,
                        "grupo": grupo_docente, "estado": estado}
            registros.append(registro)

        if estado == "Presente":
            al["asistencias"] += 1
        elif estado == "Falta":
            al["faltas"] += 1
        elif estado == "Retardo":
            al["retardos"] += 1

        actualizar_alerta_alumno(al, grupo_docente)
        GRUPOS_ESCOLARES[grupo_docente] = [a["nombre"] for a in alumnos]
        guardar_datos()
        try:
            if frame_grafica_doc is not None and frame_grafica_doc.winfo_exists():
                for widget in frame_grafica_doc.winfo_children():
                    widget.destroy()
                dibujar_grafica_asistencia(frame_grafica_doc, grupo_docente, registros, {
                    "tarjeta": C("tarjeta"), "texto": C("texto"), "borde": C("borde")
                }, alumnos)
        except tk.TclError:
            pass
        if faltas_antes < UMBRAL_ALERTA <= al["faltas"]:
            messagebox.showwarning(
                "Alerta de seguimiento",
                f"{nombre} acumuló {al['faltas']} faltas. "
                "Se generó una alerta para el panel de dirección."
            )
        actualizar_tabla_checks()
# Valentina Gutiérrez Romero: Desarrollo de las funciones para agregar y eliminar alumnos del sistema.  
    def agregar_alumno():
        nombre = entrada_nombre.get().strip()
        if not nombre:
            return
        if any(a["nombre"].casefold() == nombre.casefold() for a in alumnos):
            return
        alumnos.append({"nombre": nombre, "asistencias": 0, "faltas": 0, "retardos": 0})
        GRUPOS_ESCOLARES.setdefault(grupo_docente, [])
        if nombre not in GRUPOS_ESCOLARES[grupo_docente]:
            GRUPOS_ESCOLARES[grupo_docente].append(nombre)
        guardar_datos()
        entrada_nombre.delete(0, tk.END)
        actualizar_tabla_checks()

    def eliminar_alumno():
        nonlocal sel_nombre
        if not sel_nombre:
            messagebox.showwarning("Sin selección", "Toca el nombre del alumno para seleccionarlo y luego Eliminar.")
            return
        if messagebox.askyesno("Confirmar", f"¿Eliminar a {sel_nombre}?"):
            alumnos[:] = [a for a in alumnos if a["nombre"] != sel_nombre]
            GRUPOS_ESCOLARES[grupo_docente] = [n for n in GRUPOS_ESCOLARES.get(grupo_docente, []) if n != sel_nombre]
            registros[:] = [r for r in registros if r["nombre"] != sel_nombre or r.get("grupo") != grupo_docente]
            ALERTAS_SEGUIMIENTO[:] = [a for a in ALERTAS_SEGUIMIENTO if a["nombre"] != sel_nombre]
            guardar_datos()
            sel_nombre = None
            actualizar_tabla_checks()

    def actualizar_tabla_checks():
        if not frame_tabla_checks:
            return
        for w in frame_tabla_checks.winfo_children():
            w.destroy()
        fecha_val = entrada_fecha.get().strip() if entrada_fecha else date.today().isoformat()
        for i, alumno in enumerate(alumnos):
            bg_fila = C("tarjeta") if i % 2 == 0 else C("campo")
            if sel_nombre == alumno["nombre"]:
                bg_fila = "#244D78" if modo_actual == "oscuro" else "#D7EAFE"
            fila = tk.Frame(frame_tabla_checks, bg=bg_fila, padx=8, pady=6)
            fila.pack(fill="x")
            ausente_hoy = any(r["nombre"] == alumno["nombre"] and r.get("grupo", grupo_docente) == grupo_docente
                              and r["fecha"] == fecha_val and r["estado"] == "Falta" for r in registros)
            if ausente_hoy:
                bg_fila = "#5A1F30" if modo_actual == "oscuro" else "#FCE1E5"
                fila.configure(bg=bg_fila)
            tk.Label(fila, text=f"{i+1}", bg=bg_fila, fg=C("texto"),
                     font=("Segoe UI", 10), width=4, anchor="w").pack(side="left")
            lbl = tk.Label(fila, text=alumno["nombre"], bg=bg_fila, fg=C("texto"),
                           font=("Segoe UI", 10, "bold"), width=22, anchor="w", cursor="hand2")
            lbl.pack(side="left")
            def seleccionar_nombre(event, nombre=alumno["nombre"]):
                nonlocal sel_nombre
                sel_nombre = nombre
                actualizar_tabla_checks()
            lbl.bind("<Button-1>", seleccionar_nombre)

            var_a = tk.BooleanVar(value=any(r["nombre"] == alumno["nombre"] and r["estado"] == "Presente" and r["fecha"] == fecha_val and r.get("grupo", grupo_docente) == grupo_docente for r in registros))
            var_f = tk.BooleanVar(value=any(r["nombre"] == alumno["nombre"] and r["estado"] == "Falta" and r["fecha"] == fecha_val and r.get("grupo", grupo_docente) == grupo_docente for r in registros))
            var_r = tk.BooleanVar(value=any(r["nombre"] == alumno["nombre"] and r["estado"] == "Retardo" and r["fecha"] == fecha_val and r.get("grupo", grupo_docente) == grupo_docente for r in registros))
            var_j = tk.BooleanVar(value=any(r["nombre"] == alumno["nombre"] and r["estado"] == "Justificada" and r["fecha"] == fecha_val and r.get("grupo", grupo_docente) == grupo_docente for r in registros))

            def on_check(tipo, al_nombre=alumno["nombre"], va=var_a, vf=var_f, vr=var_r, vj=var_j):
                if tipo == "Presente" and va.get():
                    vf.set(False); vr.set(False); vj.set(False)
                    registrar_check(al_nombre, "Presente")
                elif tipo == "Falta" and vf.get():
                    va.set(False); vr.set(False); vj.set(False)
                    registrar_check(al_nombre, "Falta")
                elif tipo == "Retardo" and vr.get():
                    va.set(False); vf.set(False); vj.set(False)
                    registrar_check(al_nombre, "Retardo")
                elif tipo == "Justificada" and vj.get():
                    va.set(False); vf.set(False); vr.set(False)
                    registrar_check(al_nombre, "Justificada")

            tk.Checkbutton(fila, variable=var_a, bg=bg_fila, activebackground=bg_fila,
                           command=lambda t="Presente", va=var_a, vf=var_f, vr=var_r, vj=var_j, n=alumno["nombre"]: on_check(t, n, va, vf, vr, vj)).pack(side="left", padx=15)
            tk.Checkbutton(fila, variable=var_r, bg=bg_fila, activebackground=bg_fila,
                           command=lambda t="Retardo", va=var_a, vf=var_f, vr=var_r, vj=var_j, n=alumno["nombre"]: on_check(t, n, va, vf, vr, vj)).pack(side="left", padx=15)
            tk.Checkbutton(fila, variable=var_f, bg=bg_fila, activebackground=bg_fila,
                           command=lambda t="Falta", va=var_a, vf=var_f, vr=var_r, vj=var_j, n=alumno["nombre"]: on_check(t, n, va, vf, vr, vj)).pack(side="left", padx=15)
            tk.Checkbutton(fila, variable=var_j, bg=bg_fila, activebackground=bg_fila,
                           command=lambda t="Justificada", va=var_a, vf=var_f, vr=var_r, vj=var_j, n=alumno["nombre"]: on_check(t, n, va, vf, vr, vj)).pack(side="left", padx=15)
            tk.Label(fila, text=f"({alumno['asistencias']}/{alumno['faltas']}/{alumno['retardos']})",
                     bg=bg_fila, fg=C("secundario"), font=("Segoe UI", 9)).pack(side="left", padx=10)

    # Cristóbal Granados José Francisco: controles compactos, selección de alumnos y actualización de listas.
    def mostrar_inicio():
        nonlocal entrada_nombre, entrada_fecha, frame_tabla_checks, frame_grafica_doc
        limpiar_panel()
        etiqueta(panel_doc, f"¡Bienvenido/a, {nombre_docente}!", 18, True).pack(anchor="w", padx=22, pady=(20, 8))
        fila_info = tk.Frame(panel_doc, bg=C("fondo"))
        fila_info.pack(fill="x", padx=22, pady=(0, 14))
        fila_info.columnconfigure((0, 1), weight=1, uniform="tarjetas_doc")
        caja_tarjeta(fila_info, "GRUPO ASIGNADO", grupo_docente, "Escuela Primaria Nezahualcóyotl", C("acento")).grid(row=0, column=0, sticky="nsew", padx=(0, 6), pady=4)
        caja_tarjeta(fila_info, "PROFESOR TITULAR", nombre_docente, "Docente a cargo", C("verde")).grid(row=0, column=1, sticky="nsew", padx=(6, 0), pady=4)

        ahora = datetime.now()
        marco_cal = tk.Frame(panel_doc, bg=C("tarjeta"), highlightbackground=C("borde"), highlightthickness=1)
        marco_cal.pack(fill="x", padx=22, pady=(0, 18))
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        etiqueta(marco_cal, f"CALENDARIO: {meses[ahora.month - 1].upper()} {ahora.year}", 11, True, bg=C("tarjeta")).pack(anchor="w", padx=14, pady=(12, 6))
        grid_cal = tk.Frame(marco_cal, bg=C("tarjeta"))
        grid_cal.pack(fill="x", padx=14, pady=(0, 12))
        for col, d_txt in enumerate(["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]):
            tk.Label(grid_cal, text=d_txt, bg=C("tabla_cabecera"), fg=C("texto"), font=("Segoe UI", 9, "bold"), pady=6).grid(row=0, column=col, sticky="nsew", padx=1, pady=1)
            grid_cal.columnconfigure(col, weight=1, uniform="d_grid")
        for f, semana in enumerate(calendar.monthcalendar(ahora.year, ahora.month), 1):
            for col, numero in enumerate(semana):
                fondo_dia = C("seleccion") if numero == ahora.day else C("tarjeta")
                tk.Label(grid_cal, text=str(numero) if numero else "", bg=fondo_dia, fg=C("texto"), font=("Segoe UI", 9), height=1, highlightbackground=C("borde"), highlightthickness=1).grid(row=f, column=col, sticky="nsew", padx=1, pady=1)

        marco_grafica = tk.Frame(panel_doc, bg=C("tarjeta"), highlightbackground=C("borde"), highlightthickness=1)
        marco_grafica.pack(fill="x", padx=22, pady=(0, 16))
        frame_grafica_doc = marco_grafica
        dibujar_grafica_asistencia(marco_grafica, grupo_docente, registros, {
            "tarjeta": C("tarjeta"), "texto": C("texto"), "borde": C("borde")
        }, alumnos)

        bloque_sec = tk.Frame(panel_doc, bg=C("fondo"))
        bloque_sec.pack(fill="x", padx=22, pady=(10, 8))
        etiqueta(bloque_sec, "CONTROL DE ASISTENCIAS", 20, True).pack(anchor="w")
        marco_datos = tk.Frame(panel_doc, bg=C("fondo"))
        marco_datos.pack(fill="x", padx=22, pady=5)
        tarjeta_controles = tk.Frame(panel_doc, bg=C("tarjeta"),
                                     highlightbackground=C("borde"), highlightthickness=1)
        tarjeta_controles.pack(fill="x", padx=22, pady=8)
        fila_controles = tk.Frame(tarjeta_controles, bg=C("tarjeta"))
        fila_controles.pack(fill="x", padx=12, pady=12)
        fila_controles.columnconfigure(1, weight=1)
        etiqueta(fila_controles, "Alumno:", 10, True, bg=C("tarjeta")).grid(row=0, column=0, padx=(0, 8), sticky="w")
        entrada_nombre = ttk.Combobox(fila_controles, font=("Segoe UI", 10),
                                      values=[a["nombre"] for a in alumnos], width=18)
        entrada_nombre.grid(row=0, column=1, sticky="ew", padx=(0, 8))
        boton_padre(fila_controles, "＋ Agregar alumno", agregar_alumno).grid(row=0, column=2, padx=(0, 12))
        etiqueta(fila_controles, "Fecha:", 10, True, bg=C("tarjeta")).grid(row=0, column=3, padx=(0, 8))
        entrada_fecha = ttk.Entry(fila_controles, font=("Segoe UI", 10), width=13)
        entrada_fecha.insert(0, date.today().isoformat())
        entrada_fecha.grid(row=0, column=4, padx=(0, 8))
        boton_padre(fila_controles, "Actualizar", actualizar_tabla_checks,
                    C("azul_claro"), C("boton_secundario_texto")).grid(row=0, column=5)
        header_tabla = tk.Frame(panel_doc, bg=C("tabla_cabecera"), padx=8, pady=8)
        header_tabla.pack(fill="x", padx=22, pady=(12, 0))
        for texto, ancho, padx in [("No", 4, 0), ("Nombre", 22, 0), ("Asistió", 9, 5), ("Retardo", 9, 5), ("Falta", 8, 5), ("Justificada", 11, 5)]:
            tk.Label(header_tabla, text=texto, bg=C("tabla_cabecera"), fg=C("texto"), font=("Segoe UI", 10, "bold"), width=ancho, anchor="w" if texto in ("No", "Nombre") else "center").pack(side="left", padx=padx)
        frame_tabla_checks = tk.Frame(panel_doc, bg=C("tarjeta"), highlightbackground=C("borde"), highlightthickness=1)
        frame_tabla_checks.pack(fill="both", expand=True, padx=22, pady=2)
        marco_b = tk.Frame(panel_doc, bg=C("fondo"))
        marco_b.pack(padx=22, pady=12, anchor="w")
        boton_padre(marco_b, "Eliminar alumno seleccionado", eliminar_alumno, C("rojo"), "#FFFFFF").pack(side="left")
        actualizar_tabla_checks()


# Valentina Gutiérrez Romero y Cristóbal Granados José Francisco: Desarrollo del selector horizontal de grupos y la sección de control de asistencia.    
    def mostrar_asistencia_docente():
        nonlocal grupo_docente, alumnos, sel_nombre, entrada_nombre, entrada_fecha, frame_tabla_checks
        limpiar_panel()
        encabezado_asistencia = tk.Frame(panel_doc, bg=C("fondo"))
        encabezado_asistencia.pack(fill="x", padx=22, pady=(18, 8))
        etiqueta(encabezado_asistencia, "CONTROL DE ASISTENCIA", 19, True).pack(anchor="w")
        etiqueta(encabezado_asistencia, "Selecciona el grupo y registra el estado de cada alumno.", 10,
                 color=C("secundario")).pack(anchor="w", pady=(3, 0))

        selector_grupos = tk.Frame(panel_doc, bg=C("fondo"))
        selector_grupos.pack(fill="x", padx=22, pady=(8, 14))
        grupos_disponibles = [f"{n}° A" for n in range(1, 7)]
        botones_grupo = {}

        tarjeta = tk.Frame(panel_doc, bg=C("tarjeta"),
                           highlightbackground=C("borde"), highlightthickness=1)
        tarjeta.pack(fill="x", padx=22, pady=(0, 12))
        fila_controles = tk.Frame(tarjeta, bg=C("tarjeta"))
        fila_controles.pack(fill="x", padx=12, pady=12)
        fila_controles.columnconfigure(1, weight=1)
        etiqueta(fila_controles, "Alumno:", 10, True, bg=C("tarjeta")).grid(row=0, column=0, padx=(0, 8), sticky="w")
        entrada_nombre = ttk.Combobox(fila_controles, font=("Segoe UI", 10),
                                      values=[a["nombre"] for a in alumnos], width=20)
        entrada_nombre.grid(row=0, column=1, sticky="ew", padx=(0, 8))
        boton_padre(fila_controles, "＋ Agregar alumno", agregar_alumno).grid(row=0, column=2, padx=(0, 12))
        etiqueta(fila_controles, "Fecha:", 10, True, bg=C("tarjeta")).grid(row=0, column=3, padx=(0, 8))
        entrada_fecha = ttk.Entry(fila_controles, font=("Segoe UI", 10), width=13)
        entrada_fecha.insert(0, date.today().isoformat())
        entrada_fecha.grid(row=0, column=4, padx=(0, 8))
        boton_padre(fila_controles, "Actualizar", actualizar_tabla_checks,
                    C("azul_claro"), C("boton_secundario_texto")).grid(row=0, column=5)

        header_tabla = tk.Frame(panel_doc, bg=C("tabla_cabecera"), padx=8, pady=8)
        header_tabla.pack(fill="x", padx=22, pady=(8, 0))
        for texto, ancho, padx in [("No", 4, 0), ("Nombre", 22, 0), ("Asistió", 9, 5),
                                   ("Retardo", 9, 5), ("Falta", 8, 5), ("Justificada", 11, 5)]:
            tk.Label(header_tabla, text=texto, bg=C("tabla_cabecera"), fg=C("texto"),
                     font=("Segoe UI", 10, "bold"), width=ancho,
                     anchor="w" if texto in ("No", "Nombre") else "center").pack(side="left", padx=padx)
        frame_tabla_checks = tk.Frame(panel_doc, bg=C("tarjeta"),
                                      highlightbackground=C("borde"), highlightthickness=1)
        frame_tabla_checks.pack(fill="both", expand=True, padx=22, pady=2)
        marco_acciones = tk.Frame(panel_doc, bg=C("fondo"))
        marco_acciones.pack(fill="x", padx=22, pady=12)
        boton_padre(marco_acciones, "Eliminar alumno seleccionado", eliminar_alumno,
                    C("rojo"), "#FFFFFF").pack(side="left")

        def seleccionar_grupo(grupo):
            nonlocal grupo_docente, alumnos, sel_nombre
            grupo_docente = grupo
            sel_nombre = None
            nuevos = []
            for nombre in GRUPOS_ESCOLARES.get(grupo, []):
                relacionados = [r for r in registros if r.get("nombre") == nombre and r.get("grupo") == grupo]
                nuevos.append({
                    "nombre": nombre,
                    "asistencias": sum(r.get("estado") in ("Presente", "Asistió", "Asistio") for r in relacionados),
                    "faltas": sum(r.get("estado") == "Falta" for r in relacionados),
                    "retardos": sum(r.get("estado") == "Retardo" for r in relacionados)
                })
            alumnos = nuevos
            entrada_nombre.configure(values=[a["nombre"] for a in alumnos])
            for g, boton in botones_grupo.items():
                boton.configure(bg=C("seleccion_barra") if g == grupo else C("panel"),
                                fg=C("texto") if g == grupo else C("texto"))
            actualizar_tabla_checks()

        for grupo in grupos_disponibles:
            boton = tk.Button(selector_grupos, text=grupo,
                              command=lambda g=grupo: seleccionar_grupo(g),
                              font=("Segoe UI", 9, "bold"), relief="flat", bd=0,
                              cursor="hand2", padx=14, pady=9,
                              bg=C("seleccion_barra") if grupo == grupo_docente else C("panel"),
                              fg=C("texto"))
            boton.pack(side="left", padx=(0, 7), pady=3)
            botones_grupo[grupo] = boton

        if grupo_docente not in grupos_disponibles:
            seleccionar_grupo(grupos_disponibles[0])
        else:
            for grupo, boton in botones_grupo.items():
                boton.configure(bg=C("seleccion_barra") if grupo == grupo_docente else C("panel"))
            actualizar_tabla_checks()

    def mostrar_alertas_docente():
        limpiar_panel()
        bloque = tk.Frame(panel_doc, bg=C("fondo"))
        bloque.pack(fill="x", padx=22, pady=(20, 16))
        etiqueta(bloque, "ALERTAS DE SEGUIMIENTO", 20, True).pack(anchor="w")
        etiqueta(bloque, "Se generan automáticamente al acumular tres faltas.", 10,
                 color=C("secundario")).pack(anchor="w", pady=(3, 0))
        if not ALERTAS_SEGUIMIENTO:
            etiqueta(panel_doc, "No hay alertas pendientes.", 11, color=C("verde")).pack(anchor="w", padx=22, pady=15)
        for alerta in ALERTAS_SEGUIMIENTO:
            tarjeta_alerta = tk.Frame(panel_doc, bg="#5A1F30" if modo_actual == "oscuro" else "#FCE1E5",
                                      highlightbackground=C("rojo"), highlightthickness=1)
            tarjeta_alerta.pack(fill="x", padx=22, pady=6)
            tk.Label(tarjeta_alerta,
                     text=f"⚠  {alerta['nombre']}  |  Grupo: {alerta['grupo']}\n"
                          f"{alerta['faltas']} faltas — {alerta['estado']}",
                     bg=tarjeta_alerta.cget("bg"), fg=C("rojo"),
                     font=("Segoe UI", 11, "bold"), justify="left").pack(anchor="w", padx=14, pady=12)

    def mostrar_justificantes():
        limpiar_panel()
        bloque_sec = tk.Frame(panel_doc, bg=C("fondo"))
        bloque_sec.pack(fill="x", padx=22, pady=(20, 16))
        etiqueta(bloque_sec, "CONTROL DE JUSTIFICANTES", 20, True).pack(anchor="w")
        etiqueta(bloque_sec, "Adjunta documentos o fotografías y relaciónalos con el alumno y la fecha de la falta.",
                 10, color=C("secundario")).pack(anchor="w", pady=(4, 0))

        form = tk.Frame(panel_doc, bg=C("tarjeta"), padx=18, pady=16,
                        highlightbackground=C("borde"), highlightthickness=1)
        form.pack(fill="x", padx=22)
        fila1 = tk.Frame(form, bg=C("tarjeta")); fila1.pack(fill="x", pady=5)
        etiqueta(fila1, "Alumno:", 10, True, bg=C("tarjeta")).pack(side="left")
        combo_alumno = ttk.Combobox(
            fila1, values=[a["nombre"] for a in alumnos],
            state="readonly", width=25, font=("Segoe UI", 10)
        )
        combo_alumno.pack(side="left", padx=8)
        etiqueta(fila1, "Fecha falta:", 10, True, bg=C("tarjeta")).pack(side="left", padx=(15, 5))
        entrada_fecha_j = ttk.Entry(fila1, width=15, font=("Segoe UI", 10))
        entrada_fecha_j.insert(0, date.today().isoformat())
        entrada_fecha_j.pack(side="left")

        fila2 = tk.Frame(form, bg=C("tarjeta")); fila2.pack(fill="x", pady=5)
        etiqueta(fila2, "Motivo justificante:", 10, True, bg=C("tarjeta")).pack(side="left")
        entrada_motivo = ttk.Entry(fila2, width=40, font=("Segoe UI", 10))
        entrada_motivo.pack(side="left", padx=8)

        archivo_seleccionado = {"ruta": None, "nombre": None}
        fila_archivo = tk.Frame(form, bg=C("tarjeta"))
        fila_archivo.pack(fill="x", pady=(9, 5))

        etiqueta(fila_archivo, "Documento o imagen:", 10, True,
                 bg=C("tarjeta")).pack(side="left", padx=(0, 8))
        etiqueta_archivo = etiqueta(
            fila_archivo, "Ningún archivo seleccionado",
            9, color=C("secundario"), bg=C("tarjeta")
        )
        etiqueta_archivo.pack(side="left", padx=5)

        def seleccionar_archivo():
            ruta = filedialog.askopenfilename(
                title="Seleccionar justificante",
                filetypes=[
                    ("Documentos e imágenes", "*.pdf *.png *.jpg *.jpeg *.gif *.bmp *.webp *.doc *.docx"),
                    ("PDF", "*.pdf"),
                    ("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp *.webp"),
                    ("Todos los archivos", "*.*")
                ]
            )
            if ruta:
                archivo_seleccionado["ruta"] = ruta
                archivo_seleccionado["nombre"] = os.path.basename(ruta)
                etiqueta_archivo.config(text=archivo_seleccionado["nombre"],
                                        fg=C("acento"))

        boton_padre(fila_archivo, "SUBIR ARCHIVO / IMAGEN",
                    seleccionar_archivo).pack(side="left", padx=8)

        marco_tabla = tk.LabelFrame(
            panel_doc, text=" Faltas y justificantes ",
            bg=C("fondo"), fg=C("texto"), font=("Segoe UI", 10, "bold")
        )
        marco_tabla.pack(fill="both", expand=True, padx=22, pady=10)
        tabla = ttk.Treeview(
            marco_tabla, columns=("nombre", "fecha", "estado", "archivo"),
            show="headings", height=8
        )
        for c, t, ancho in [
            ("nombre", "Alumno", 170), ("fecha", "Fecha", 110),
            ("estado", "Estado", 110), ("archivo", "Archivo adjunto", 260)
        ]:
            tabla.heading(c, text=t)
            tabla.column(c, width=ancho, anchor="w")
        tabla.pack(fill="both", expand=True, padx=5, pady=5)

        def actualizar_tabla_justificantes():
            for f in tabla.get_children():
                tabla.delete(f)
            for r in registros:
                if r["estado"] in ("Falta", "Justificada"):
                    adjunto = next((
                        a["archivo"] for a in reversed(ARCHIVOS_JUSTIFICANTES)
                        if a["nombre"] == r["nombre"] and a["fecha"] == r["fecha"]
                    ), "Sin archivo")
                    tabla.insert("", "end", values=(
                        r["nombre"], r["fecha"], r["estado"], adjunto
                    ))

        def guardar_archivo_adjunto(alumno, fecha, motivo):
            ruta = archivo_seleccionado["ruta"]
            if not ruta:
                return None
            carpeta = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "justificantes_adjuntos"
            )
            os.makedirs(carpeta, exist_ok=True)
            nombre_base = os.path.basename(ruta)
            nombre_seguro = datetime.now().strftime("%Y%m%d_%H%M%S_%f") + "_" + nombre_base
            destino = os.path.join(carpeta, nombre_seguro)
            shutil.copy2(ruta, destino)
            ARCHIVOS_JUSTIFICANTES.append({
                "nombre": alumno,
                "fecha": fecha,
                "motivo": motivo,
                "archivo": nombre_base,
                "ruta": destino,
                "fecha_subida": datetime.now().isoformat(timespec="seconds")
            })
            archivo_seleccionado["ruta"] = None
            archivo_seleccionado["nombre"] = None
            etiqueta_archivo.config(text="Ningún archivo seleccionado",
                                    fg=C("secundario"))
            return nombre_base

        def justificar():
            alumno = combo_alumno.get().strip()
            fecha_texto = entrada_fecha_j.get().strip()
            motivo = entrada_motivo.get().strip()
            if not alumno or not fecha_texto:
                messagebox.showwarning("Faltan datos", "Selecciona alumno y fecha.")
                return
            try:
                fecha = date.fromisoformat(fecha_texto).isoformat()
            except ValueError:
                messagebox.showerror("Fecha incorrecta", "Usa el formato AAAA-MM-DD.")
                return

            falta = next((
                r for r in registros
                if r["nombre"] == alumno and r["fecha"] == fecha
                and r["estado"] == "Falta"
            ), None)

            if falta:
                try:
                    nombre_archivo = guardar_archivo_adjunto(alumno, fecha, motivo)
                except (OSError, shutil.Error) as error:
                    messagebox.showerror(
                        "No se pudo adjuntar",
                        f"No fue posible copiar el archivo.\n{error}"
                    )
                    return
                falta["estado"] = "Justificada"
                guardar_datos()
                texto = "La falta quedó justificada."
                if nombre_archivo:
                    texto += f"\nArchivo adjunto: {nombre_archivo}"
                else:
                    texto += "\nNo se adjuntó ningún archivo."
                messagebox.showinfo("Justificante registrado", texto)
                actualizar_tabla_justificantes()
                return

                                                                                                
            if archivo_seleccionado["ruta"]:
                try:
                    guardar_archivo_adjunto(alumno, fecha, motivo)
                    guardar_datos()
                    actualizar_tabla_justificantes()
                    messagebox.showinfo(
                        "Archivo guardado",
                        "El archivo quedó almacenado, pero no se encontró una falta pendiente para cambiar su estado."
                    )
                    return
                except (OSError, shutil.Error) as error:
                    messagebox.showerror("No se pudo adjuntar", str(error))
                    return

            messagebox.showwarning(
                "No encontrada",
                "No hay falta registrada ese día para este alumno. Puedes adjuntar el documento y guardarlo de todos modos."
            )

        def abrir_adjunto():
            seleccion = tabla.selection()
            if not seleccion:
                messagebox.showwarning("Selecciona un registro", "Selecciona una fila para abrir su justificante.")
                return
            valores = tabla.item(seleccion[0], "values")
            alumno, fecha = valores[0], valores[1]
            adjunto = next((
                a for a in reversed(ARCHIVOS_JUSTIFICANTES)
                if a["nombre"] == alumno and a["fecha"] == fecha
            ), None)
            if not adjunto or not os.path.exists(adjunto.get("ruta", "")):
                messagebox.showwarning("Archivo no disponible", "Este registro no tiene un archivo adjunto disponible.")
                return
            try:
                if sys.platform.startswith("win"):
                    os.startfile(adjunto["ruta"])
                elif sys.platform == "darwin":
                    subprocess.Popen(["open", adjunto["ruta"]])
                else:
                    subprocess.Popen(["xdg-open", adjunto["ruta"]])
            except OSError as error:
                messagebox.showerror("No se pudo abrir", str(error))

        fila_botones = tk.Frame(form, bg=C("tarjeta"))
        fila_botones.pack(fill="x", pady=(8, 0))
        boton_padre(
            fila_botones, "REGISTRAR JUSTIFICANTE", justificar,
            C("verde"), "#FFFFFF"
        ).pack(side="left", padx=(0, 8))
        boton_padre(
            fila_botones, "ABRIR ARCHIVO SELECCIONADO", abrir_adjunto
        ).pack(side="left")

        actualizar_tabla_justificantes()

    def mostrar_etica():
        limpiar_panel()
        bloque_sec = tk.Frame(panel_doc, bg=C("fondo"))
        bloque_sec.pack(fill="x", padx=22, pady=(20, 16))
        etiqueta(bloque_sec, "REPORTE DE CONDUCTA", 20, True).pack(anchor="w")
        form = tk.Frame(panel_doc, bg=C("tarjeta"), padx=18, pady=16, highlightbackground=C("borde"), highlightthickness=1)
        form.pack(fill="x", padx=22)
        fila1 = tk.Frame(form, bg=C("tarjeta")); fila1.pack(fill="x", pady=5)
        etiqueta(fila1, "Alumno:", 10, True, bg=C("tarjeta")).pack(side="left")
        combo_alumno = ttk.Combobox(fila1, values=[a["nombre"] for a in alumnos], state="readonly", width=25, font=("Segoe UI", 10))
        combo_alumno.pack(side="left", padx=8)
        etiqueta(fila1, "Día:", 10, True, bg=C("tarjeta")).pack(side="left", padx=(15, 5))
        entrada_fecha_rep = ttk.Entry(fila1, width=15, font=("Segoe UI", 10))
        entrada_fecha_rep.insert(0, date.today().isoformat()); entrada_fecha_rep.pack(side="left")
        fila2 = tk.Frame(form, bg=C("tarjeta")); fila2.pack(fill="x", pady=5)
        etiqueta(fila2, "Conducta:", 10, True, bg=C("tarjeta")).pack(side="left")
        tipo_var = tk.StringVar(value="Conducta")
        ttk.Combobox(fila2, textvariable=tipo_var, values=["Conducta", "Falta de respeto", "No trabajó", "Celular", "Otro"], state="readonly", width=18, font=("Segoe UI", 10)).pack(side="left", padx=8)
        etiqueta(fila2, "Gravedad:", 10, True, bg=C("tarjeta")).pack(side="left", padx=(10, 5))
        gravedad_var = tk.StringVar(value="Leve")
        ttk.Combobox(fila2, textvariable=gravedad_var, values=["Leve", "Media", "Grave"], state="readonly", width=10, font=("Segoe UI", 10)).pack(side="left")
        etiqueta(form, "Describe la situación", 10, True, bg=C("tarjeta")).pack(anchor="w", pady=(10, 4))
        texto_desc = tk.Text(form, height=4, font=("Segoe UI", 10), bg=C("campo"), fg=C("texto_campo"), relief="flat", padx=8, pady=8, insertbackground=C("texto_campo"))
        texto_desc.pack(fill="x")

        marco_tabla_rep = tk.LabelFrame(panel_doc, text=" Reportes guardados ", bg=C("fondo"), fg=C("texto"), font=("Segoe UI", 10, "bold"))
        marco_tabla_rep.pack(fill="both", expand=True, padx=22, pady=10)
        tabla_rep = ttk.Treeview(marco_tabla_rep, columns=("fecha", "nombre", "tipo", "gravedad"), show="headings", height=6)
        for c, t in [("fecha", "Día"), ("nombre", "Alumno"), ("tipo", "Motivo"), ("gravedad", "Gravedad")]:
            tabla_rep.heading(c, text=t); tabla_rep.column(c, width=130, anchor="w")
        tabla_rep.pack(fill="both", expand=True, padx=5, pady=5)

        def actualizar_reportes():
            for f in tabla_rep.get_children(): tabla_rep.delete(f)
            for r in reversed(reportes_conducta):
                tabla_rep.insert("", "end", values=(r["fecha"], r["nombre"], r["tipo"], r["gravedad"]))

        def guardar_reporte():
            alumno = combo_alumno.get().strip()
            if not alumno:
                messagebox.showwarning("Falta alumno", "Selecciona un alumno."); return
            try:
                fecha = date.fromisoformat(entrada_fecha_rep.get().strip()).isoformat()
            except ValueError:
                messagebox.showerror("Fecha mal", "Usa formato AAAA-MM-DD"); return
            desc = texto_desc.get("1.0", "end").strip()
            if not desc:
                messagebox.showwarning("Falta descripción", "Escribe qué ocurrió."); return
            reportes_conducta.append({"fecha": fecha, "nombre": alumno, "tipo": tipo_var.get(), "gravedad": gravedad_var.get(), "descripcion": desc})
            actualizar_reportes()
            texto_desc.delete("1.0", "end")
            messagebox.showinfo("Guardado", "Reporte de conducta registrado exitosamente.")

        boton_padre(form, "GUARDAR REPORTE", guardar_reporte).pack(anchor="w", pady=10)
        actualizar_reportes()

    def mostrar_calendario_docente():
        limpiar_panel()
        etiqueta(panel_doc, "CALENDARIO ESCOLAR", 20, True).pack(anchor="w", padx=22, pady=(22, 8))
        etiqueta(panel_doc, "El archivo PDF seleccionado por dirección está disponible aquí.", 10,
                 color=C("secundario")).pack(anchor="w", padx=22, pady=(0, 14))
        boton_padre(panel_doc, "ABRIR CALENDARIO ESCOLAR PDF", abrir_calendario_pdf).pack(anchor="w", padx=22, pady=6)

    botones_menu_doc = []

    def cambiar_vista_docente(nombre):
        nonlocal vista_docente_actual
        vista_docente_actual = nombre
        for b in botones_menu_doc:
            clave_boton = b.cget("text").strip().split("   ")[-1]
            seleccionado = clave_boton == nombre or b.cget("text").strip() == nombre
            b.configure(bg=C("seleccion_barra") if seleccionado else C("barra"),
                         fg=C("texto_barra"),
                         activebackground=C("hover_barra"),
                         activeforeground=C("texto_barra"),
                         font=("Segoe UI", 10, "bold" if seleccionado else "normal"))
        if nombre == "Inicio":
            mostrar_inicio()
        elif nombre == "Asistencia":
            mostrar_asistencia_docente()
        elif nombre == "Justificantes":
            mostrar_justificantes()
        elif nombre == "Calendario escolar":
            mostrar_calendario_docente()
        else:
            mostrar_etica()

    def construir_menu_docente():
        botones_menu_doc.clear()
        for w in menu_frame_doc.winfo_children():
            w.destroy()
        opciones_doc = [("⌂   Inicio", "Inicio"), ("▤   Asistencia", "Asistencia"),
                        ("▤   Justificantes", "Justificantes"),
                        ("✎   Reportes", "Reportes"), ("▦   Calendario escolar", "Calendario escolar")]
        compacto = False 
        for texto, clave in opciones_doc:
            texto_boton = texto if not compacto else texto.split("   ")[-1]
            seleccionado = vista_docente_actual == clave
            btn = tk.Button(menu_frame_doc, text=texto_boton,
                            command=lambda k=clave: cambiar_vista_docente(k),
                            bg=C("seleccion_barra") if seleccionado else C("barra"),
                            fg=C("texto_barra"), activebackground=C("hover_barra"),
                            activeforeground=C("texto_barra"),
                            font=("Segoe UI", 10, "bold" if seleccionado else "normal"),
                            anchor="w" if not compacto else "center",
                            padx=16 if not compacto else 4, pady=12,
                            relief="flat", bd=0, cursor="hand2")
            btn.pack(fill="x" if not compacto else "y", expand=bool(compacto),
                     padx=7 if not compacto else 1, pady=2)
            botones_menu_doc.append(btn)

    def reconstruir_interfaz_docente():
        principal_doc.configure(bg=C("fondo"))
        sidebar_doc.configure(bg=C("barra"))
        zona_derecha_doc.configure(bg=C("fondo"))
        marca_doc.configure(bg=C("barra"))
        menu_frame_doc.configure(bg=C("barra"))
        header_doc.configure(bg=C("encabezado"))
        contenedor_panel_doc.configure(bg=C("fondo"))
        canvas_doc.configure(bg=C("fondo"))
        panel_doc.configure(bg=C("fondo"))
        titulo_header_doc.configure(bg=C("encabezado"), fg=C("texto"))
        usuario_doc.configure(bg=C("encabezado"), fg=C("verde"))
        boton_tema_doc.configure(text="☾  Tema oscuro" if modo_actual == "claro" else "☀  Tema claro",
                                 bg=C("panel"), fg=C("texto"),
                                 activebackground=C("seleccion"), activeforeground=C("texto"))
        configurar_estilos()
        construir_menu_docente()
        cambiar_vista_docente(vista_docente_actual)

    configurar_estilos()
    construir_menu_docente()
    cambiar_vista_docente("Inicio")
# Panel de direccion
     
def abrir_director():
    ventana_dir = tk.Toplevel(raiz_principal)
    ventana_dir.title("Sistema de alerta temprana | Panel de Dirección")

    def volver_login():
        ventana_dir.destroy()
        raiz_principal.deiconify()
        limpiar_campos()

    ventana_dir.protocol("WM_DELETE_WINDOW", lambda: (ventana_dir.destroy(), raiz_principal.destroy()))
    ancho_p = ventana_dir.winfo_screenwidth()
    alto_p = ventana_dir.winfo_screenheight()
    w_dir = int(ancho_p * 0.94)
    h_dir = int(alto_p * 0.90)
    x_dir = (ancho_p - w_dir) // 2
    y_dir = (alto_p - h_dir) // 2
    # Rivas Mira Yaretzi Guadalupe: el panel de Dirección se abre maximizado y conserva el área de pantalla.
    ventana_dir.geometry(f"{ancho_p}x{alto_p}+0+0")
    ventana_dir.minsize(640, 480)
    try:
        ventana_dir.state("zoomed")
    except tk.TclError:
        ventana_dir.attributes("-zoomed", True)
    ventana_dir.configure(bg="#F1F5F9")
    ventana_dir.bind("<Configure>", lambda e: sidebar.configure(
        width=max(175, min(230, int(ventana_dir.winfo_width() * 0.19)))
    ) if e.widget is ventana_dir else None)

    tema_actual = "oscuro"
    vista_actual = "inicio"
    fecha_actual = datetime.now().strftime("%d/%m/%Y")

    TEMAS_DIR = {
        "oscuro": {
            "fondo": "#081426", "panel": "#10233D", "tarjeta": "#081426",
            "encabezado": "#102B50", "barra": "#081426",
            "texto": "#FFFFFF", "secundario": "#8A9BB2",
            "borde": "#29425F", "campo": "#172C46", "texto_campo": "#FFFFFF",
            "acento": "#32C5F4", "acento_hover": "#168ED0",
            "verde": "#19B887", "rojo": "#FF7185", "amarillo": "#F6C76B",
            "boton_texto": "#081426", "seleccion": "#173B68",
            "tabla_cabecera": "#173B68", "sombra": "#050D18",
            "texto_barra": "#FFFFFF", "secundario_barra": "#B9CBE2",
            "seleccion_barra": "#203D60", "hover_barra": "#173B68","encabezado1": "#054A08"
        },
        "claro": {
            "fondo": "#FFFFFF", "panel": "#FFFFFF", "tarjeta": "#FFFFFF",
            "encabezado": "#FFFFFF", "barra": "#081426",
            "texto": "#172033", "secundario": "#526176",
            "borde": "#CBD5E1", "campo": "#FFFFFF", "texto_campo": "#172033",
            "acento": "#0756A8", "acento_hover": "#064580",
            "verde": "#087F5B", "rojo": "#B4233D", "amarillo": "#805900",
            "boton_texto": "#FFFFFF", "seleccion": "#CFE4FF",
            "tabla_cabecera": "#DCE7F3", "sombra": "#ffffff",
            "texto_barra": "#FFFFFF", "secundario_barra": "#B9CBE2",
            "seleccion_barra": "#203D60", "hover_barra": "#173B68","encabezado1": "#0B8511"
        }
    }

    COLORES_GRUPOS = {
        "1° A": {"claro": "#D9EAFE", "activo": "#8DBBEF", "texto": "#244D78"},
        "2° A": {"claro": "#DDF3E5", "activo": "#91D5AC", "texto": "#245B3B"},
        "3° A": {"claro": "#FCE5D8", "activo": "#F2B18F", "texto": "#85452A"},
        "4° A": {"claro": "#F0E3FA", "activo": "#C6A0E6", "texto": "#624080"},
        "5° A": {"claro": "#FFF1C9", "activo": "#EACB72", "texto": "#755817"},
        "6° A": {"claro": "#F9DFE8", "activo": "#E8A0B9", "texto": "#813D58"},
    }

    def colores_grupo(grupo, seleccionado=False):
        colores = COLORES_GRUPOS.get(
            grupo, {"claro": "#E2E8F0", "activo": "#94A3B8", "texto": "#334155"}
        )
        oscuro = tema_actual == "oscuro"

        if seleccionado:
            fondo = colores["activo"]
            texto = "#172033" if oscuro else colores["texto"]
        else:
            fondo = colores["claro"]
            texto = colores["texto"]

        return fondo, texto


    def C_DIR(clave):
        return TEMAS_DIR[tema_actual][clave]

    grupos = {grupo: list(nombres) for grupo, nombres in GRUPOS_ESCOLARES.items()}
    for grado in range(1, 7):
        grupos.setdefault(f"{grado}° A", [])
    grupos[GRUPO_DOCENTE] = list(dict.fromkeys(
        grupos.get(GRUPO_DOCENTE, []) + [a["nombre"] for a in ALUMNOS_COMPARTIDOS]
    ))
    alumnos = [alumno for lista in grupos.values() for alumno in lista]
    registros = {(grupo, alumno): "Sin registro" for grupo, lista in grupos.items() for alumno in lista}
    eventos = []

    estilo = ttk.Style()
    estilo.theme_use("clam")

    def configurar_estilos():
        estilo.configure("Treeview", background=C_DIR("panel"), foreground=C_DIR("texto"),
                         fieldbackground=C_DIR("panel"), rowheight=34,
                         font=("Segoe UI", 10), borderwidth=0)
        estilo.configure("Treeview.Heading", background=C_DIR("tabla_cabecera"),
                         foreground=C_DIR("texto"), font=("Segoe UI", 10, "bold"),
                         padding=9, relief="flat")
        estilo.map("Treeview", background=[("selected", C_DIR("seleccion"))],
                   foreground=[("selected", C_DIR("texto"))])
        estilo.configure("TCombobox", fieldbackground=C_DIR("campo"),
                         background=C_DIR("campo"), foreground=C_DIR("texto_campo"),
                         arrowcolor=C_DIR("texto"))
        estilo.map("TCombobox", fieldbackground=[("readonly", C_DIR("campo"))],
                   foreground=[("readonly", C_DIR("texto_campo"))])
        estilo.configure("TEntry", fieldbackground=C_DIR("campo"),
                         foreground=C_DIR("texto_campo"), padding=7)
        ventana_dir.option_add("*TEntry.insertBackground",
                               "#FFFFFF" if tema_actual == "oscuro" else "#172033")
        estilo.configure("Vertical.TScrollbar", background=C_DIR("borde"),
                         troughcolor=C_DIR("fondo"), borderwidth=0, arrowsize=12)

    principal = tk.Frame(ventana_dir, bg=C_DIR("fondo"))
    principal.pack(fill="both", expand=True)
    sidebar = tk.Frame(principal, bg=C_DIR("barra"), width=230)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)
    zona_derecha = tk.Frame(principal, bg=C_DIR("fondo"))
    zona_derecha.pack(side="left", fill="both", expand=True)
    marca = tk.Frame(sidebar, bg=C_DIR("barra"))
    marca.pack(fill="x", padx=18, pady=(22, 20))
    tk.Label(marca, text="NEZAHUALCÓYOTL", font=("Segoe UI", 15, "bold"),
             bg=C_DIR("barra"), fg=C_DIR("acento")).pack(anchor="w")
    tk.Label(marca, text="SISTEMA DE ALERTA TEMPRANA\nSITUACIONES DE RIESGO ESCOLAR",
             font=("Segoe UI", 9), bg=C_DIR("barra"),
             fg=C_DIR("secundario_barra"), justify="left", wraplength=190).pack(anchor="w", pady=(5, 0))
    tk.Frame(sidebar, bg=C_DIR("borde"), height=1).pack(fill="x", padx=16, pady=(0, 14))
    tk.Label(sidebar, text="MENÚ PRINCIPAL", font=("Segoe UI", 8, "bold"),
             bg=C_DIR("barra"), fg=C_DIR("secundario_barra")).pack(anchor="w", padx=18, pady=(0, 8))
    menu_frame = tk.Frame(sidebar, bg=C_DIR("barra"))
    menu_frame.pack(fill="x")
    tk.Button(sidebar, text="↪  CERRAR SESIÓN", command=volver_login,
              font=("Segoe UI", 10, "bold"), bg=C_DIR("seleccion_barra"),
              fg=C_DIR("texto_barra"), activebackground=C_DIR("hover_barra"),
              activeforeground=C_DIR("texto_barra"), relief="flat", bd=0,
              cursor="hand2", padx=10, pady=11).pack(side="bottom", fill="x", padx=10, pady=14)

    header = tk.Frame(zona_derecha, bg=C_DIR("encabezado"), height=76)
    header.pack(fill="x")
    header.pack_propagate(False)
    titulo_header = tk.Label(header, text="PANEL DE DIRECCIÓN", font=("Segoe UI", 17, "bold"),
                             bg=C_DIR("encabezado"), fg=C_DIR("texto"))
    titulo_header.pack(side="left", padx=22)
    boton_tema_dir = tk.Button(header, text="☀  Tema claro",
                               command=lambda: alternar_tema_dir(),
                               font=("Segoe UI", 9, "bold"), relief="flat",
                               bd=0, cursor="hand2", padx=12, pady=8)
    boton_tema_dir.pack(side="right", padx=(5, 18), pady=16)
    usuario = tk.Label(header, text="● Director ", font=("Segoe UI", 10, "bold"),
                       bg=C_DIR("encabezado"), fg=C_DIR("verde"))
    usuario.pack(side="right", padx=8)
    tk.Frame(zona_derecha, bg=C_DIR("borde"), height=1).pack(fill="x")
    contenedor_panel = tk.Frame(zona_derecha, bg=C_DIR("fondo"))
    contenedor_panel.pack(fill="both", expand=True)
    canvas = tk.Canvas(contenedor_panel, bg=C_DIR("fondo"), highlightthickness=0)
    scroll_vertical = ttk.Scrollbar(contenedor_panel, orient="vertical",
                                    command=canvas.yview, style="Vertical.TScrollbar")
    canvas.configure(yscrollcommand=scroll_vertical.set)
    scroll_vertical.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    panel = tk.Frame(canvas, bg=C_DIR("fondo"))
    panel_id = canvas.create_window((0, 0), window=panel, anchor="nw")
    panel.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>", lambda e: canvas.itemconfigure(panel_id, width=e.width))

    def limpiar_panel():
        for widget in panel.winfo_children():
            widget.destroy()
        canvas.yview_moveto(0)

    def etiqueta(parent, texto, tam=10, negrita=False, color=None, **kwargs):
        return tk.Label(parent, text=texto,
                        font=("Segoe UI", tam, "bold" if negrita else "normal"),
                        bg=kwargs.pop("bg", C_DIR("fondo")),
                        fg=color or C_DIR("texto"), **kwargs)

    def boton_padre(parent, texto, comando, color=None, texto_color=None):
        return tk.Button(parent, text=texto, command=comando,
                         bg=color or C_DIR("acento"), fg=texto_color or C_DIR("boton_texto"),
                         activebackground=C_DIR("acento_hover"), activeforeground="#FFFFFF",
                         font=("Segoe UI", 10, "bold"), relief="flat", bd=0,
                         cursor="hand2", padx=13, pady=9)

    def encabezado(titulo, descripcion):
        bloque = tk.Frame(panel, bg=C_DIR("fondo"))
        bloque.pack(fill="x", padx=22, pady=(20, 16))
        etiqueta(bloque, titulo, 21, True).pack(anchor="w")
        etiqueta(bloque, descripcion, 10, color=C_DIR("secundario"),
                 wraplength=900, justify="left").pack(anchor="w", pady=(5, 0))

    def caja_tarjeta(parent, titulo, valor, detalle, color):
        caja = tk.Frame(parent, bg=C_DIR("tarjeta"), highlightbackground=C_DIR("borde"), highlightthickness=1)
        tk.Frame(caja, bg=color, height=4).pack(fill="x")
        etiqueta(caja, titulo, 10, color=C_DIR("secundario"), wraplength=210).pack(anchor="w", padx=14, pady=(13, 4))
        etiqueta(caja, valor, 23, True).pack(anchor="w", padx=14)
        etiqueta(caja, detalle, 9, color=C_DIR("secundario"), wraplength=210).pack(anchor="w", padx=14, pady=(4, 13))
        return caja

    def crear_tabla(parent, columnas, anchos=None):
        marco = tk.Frame(parent, bg=C_DIR("tarjeta"), highlightbackground=C_DIR("borde"), highlightthickness=1)
        marco.pack(fill="both", expand=True, padx=22, pady=(0, 14))
        marco.columnconfigure(0, weight=1); marco.rowconfigure(0, weight=1)
        tabla = ttk.Treeview(marco, columns=columnas, show="headings")
        for i, col in enumerate(columnas):
            tabla.heading(col, text=col)
            tabla.column(col, width=anchos[i] if anchos else 140, minwidth=70, anchor="w", stretch=True)
        scroll_y = ttk.Scrollbar(marco, orient="vertical", command=tabla.yview)
        scroll_x = ttk.Scrollbar(marco, orient="horizontal", command=tabla.xview)
        tabla.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        tabla.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        return tabla

    def alternar_tema_dir():
        nonlocal tema_actual
        tema_actual = "claro" if tema_actual == "oscuro" else "oscuro"
        reconstruir_interfaz()

    def reconstruir_interfaz():
        principal.configure(bg=C_DIR("fondo"))
        sidebar.configure(bg=C_DIR("barra"))
        zona_derecha.configure(bg=C_DIR("fondo"))
        marca.configure(bg=C_DIR("barra"))
        menu_frame.configure(bg=C_DIR("barra"))
        header.configure(bg=C_DIR("encabezado"))
        contenedor_panel.configure(bg=C_DIR("fondo"))
        canvas.configure(bg=C_DIR("fondo"))
        panel.configure(bg=C_DIR("fondo"))
        titulo_header.configure(bg=C_DIR("encabezado"), fg=C_DIR("texto"))
        usuario.configure(bg=C_DIR("encabezado"), fg=C_DIR("verde"))
        boton_tema_dir.configure(
            text="☾  Tema oscuro" if tema_actual == "claro" else "☀  Tema claro",
            bg=C_DIR("panel"), fg=C_DIR("texto"),
            activebackground=C_DIR("seleccion"), activeforeground=C_DIR("texto"))
        configurar_estilos()
        construir_menu()
        mostrar_vista(vista_actual)

    def construir_menu():
        for w in menu_frame.winfo_children():
            w.destroy()
        opciones = [("⌂   Inicio", "inicio"), ("▤   Asistencia", "asistencia"),
                    ("▣   Registro de alumnos", "registro_masivo"),
                    ("⚠   Alertas", "alertas"), ("▦   Calendario", "calendario"),
                    ("✎   Carta compromiso", "carta"),
                     ("🔒   Contraseñas de grupo", "contrasenas")]
        compacto = ventana_dir.winfo_width() < 760
        for texto, clave in opciones:
            texto_boton = texto if not compacto else texto.split("   ")[-1]
            seleccionado = vista_actual == clave
            tk.Button(menu_frame, text=texto_boton,
    command=lambda k=clave: mostrar_vista(k),
    bg=C_DIR("seleccion_barra") if seleccionado else C_DIR("barra"),
    fg=C_DIR("texto_barra"), activebackground=C_DIR("hover_barra"),
    activeforeground=C_DIR("texto_barra"),
    font=("Segoe UI", 10, "bold" if seleccionado else "normal"),
    anchor="w",
    justify="left",
    padx=28, pady=18,
    relief="flat", bd=0, cursor="hand2").pack(
        side="top",
        fill="x",
        expand=False, padx=0, pady=4)


    def mostrar_vista(clave):
        nonlocal vista_actual
        vista_actual = clave
        construir_menu()
        {"inicio": mostrar_inicio, "asistencia": mostrar_asistencia,
         "registro_masivo": mostrar_registro_masivo,
         "alertas": mostrar_alertas, "calendario": mostrar_calendario,
         "carta": mostrar_carta, "contrasenas": mostrar_contrasenas}[clave]()

    def mostrar_inicio():
        limpiar_panel()
        encabezado("Resumen general", "Bienvenido al sistema de administración escolar.")
        fila = tk.Frame(panel, bg=C_DIR("fondo"))
        fila.pack(fill="x", padx=22, pady=(0, 18))
        fila.columnconfigure((0, 1), weight=1, uniform="tarjetas")
        datos = [("Alumnos registrados", str(len(alumnos)), "Alumnos en el sistema", C_DIR("acento")),
                 ("Alertas activas", str(len(ALERTAS_SEGUIMIENTO)), "Tres faltas o más", C_DIR("rojo"))]
        for i, (t, v, d, color) in enumerate(datos):
            caja_tarjeta(fila, t, v, d, color).grid(row=0, column=i, sticky="nsew", padx=5, pady=4)
        marco_grafica_dir = tk.Frame(panel, bg=C_DIR("tarjeta"), highlightbackground=C_DIR("borde"), highlightthickness=1)
        marco_grafica_dir.pack(fill="x", padx=22, pady=(0, 16))
        selector_grafica_var = tk.StringVar(value="1° A")
        fila_grafica = tk.Frame(marco_grafica_dir, bg=C_DIR("tarjeta"))
        fila_grafica.pack(fill="x", padx=14, pady=(10, 0))
        etiqueta(fila_grafica, "Grupo:", 10, True, bg=C_DIR("tarjeta")).pack(side="left", padx=(0, 8))
        zona_grafica = tk.Frame(marco_grafica_dir, bg=C_DIR("tarjeta"))
        zona_grafica.pack(fill="x")
    #Valentina Gutiérrez Romero - Agregué botones de grupos , sustituyendo los selectores
    

        botones_grupos = {}

        def actualizar_botones_grupos():
            for grupo, boton in botones_grupos.items():
                fondo, texto = colores_grupo(
                    grupo,
                    selector_grafica_var.get() == grupo
                )
                boton.configure(
                    bg=fondo,
                    fg=texto,
                    activebackground=fondo,
                    activeforeground=texto
                )

        def actualizar_grafica_director(grupo):
            selector_grafica_var.set(grupo)

            for widget in zona_grafica.winfo_children():
                widget.destroy()

            dibujar_grafica_asistencia(
                zona_grafica,
                grupo,
                REGISTROS_ASISTENCIA,
                {
                    "tarjeta": C_DIR("tarjeta"),
                    "texto": C_DIR("texto"),
                    "borde": C_DIR("borde")
                }
            )

            actualizar_botones_grupos()

        for n in range(1, 7):
            g = f"{n}° A"

            boton = tk.Button(
                fila_grafica,
                text=g,
                command=lambda x=g: actualizar_grafica_director(x),
                font=("Segoe UI", 10, "bold"),
                relief="flat",
                bd=0,
                padx=18,
                pady=10,
                cursor="hand2"
            )

            boton.pack(side="left", padx=4, pady=5)
            botones_grupos[g] = boton

        actualizar_grafica_director("1° A")

    def mostrar_asistencia():
        limpiar_panel()
        encabezado("Listas de asistencia", "Selecciona un grupo, elige un alumno y cambia su estado.")
        controles = tk.Frame(panel, bg=C_DIR("fondo")); controles.pack(fill="x", padx=22, pady=(0, 12))
        etiqueta(controles, "Grupo:", 10, True).pack(side="left", padx=(0, 8))
        grupo_var = tk.StringVar(value="1° A")
        botones_asistencia = {}

        def seleccionar_grupo(grupo):
            grupo_var.set(grupo)
            cargar_grupo()
            actualizar_botones_asistencia()

        def actualizar_botones_asistencia():
            for grupo, boton in botones_asistencia.items():
                fondo, texto = colores_grupo(
                    grupo, grupo_var.get() == grupo
                )
                boton.configure(
                    bg=fondo,
                    fg=texto,
                    activebackground=fondo,
                    activeforeground=texto
                )

        for n in range(1, 7):
            grupo = f"{n}° A"

            boton = tk.Button(
                controles,
                text=grupo,
                command=lambda g=grupo: seleccionar_grupo(g),
                font=("Segoe UI", 10, "bold"),
                relief="flat",
                bd=0,
                padx=14,
                pady=8,
                cursor="hand2"
            )

            boton.pack(side="left", padx=3)
            botones_asistencia[grupo] = boton
        tabla = crear_tabla(panel, ("No.", "Alumno", "Grupo", "Estado"), (55, 220, 100, 130))
        def cargar_grupo(_event=None):
            for item in tabla.get_children(): tabla.delete(item)
            grupo = grupo_var.get()
            for i, alumno in enumerate(grupos[grupo], 1):
                estado = obtener_estado_dia(alumno, grupo, date.today().isoformat())
                if estado == "Presente":
                    estado = "Asistió"
                tabla.insert("", "end", iid=str(i), values=(i, alumno, grupo, estado),
                             tags=("ausente",) if estado in ("Falta", "Ausente") else ())
            tabla.tag_configure("ausente", background="#F8C9D1", foreground="#A3122A")

        def cambiar_estado():
            seleccion = tabla.selection()
            if not seleccion:
                messagebox.showwarning("Selecciona un alumno", "Selecciona un registro de la tabla."); return
            iid = seleccion[0]
            valores = tabla.item(iid, "values")
            alumno, grupo = valores[1], valores[2]
            estados = ["Presente", "Retardo", "Falta", "Justificada"]
            estado_actual = obtener_estado_dia(alumno, grupo, date.today().isoformat())
            if estado_actual == "Ausente":
                estado_actual = "Falta"
            if estado_actual == "Asistió":
                estado_actual = "Presente"
            if estado_actual not in estados:
                nuevo_estado = "Presente"
            else:
                nuevo_estado = estados[(estados.index(estado_actual) + 1) % len(estados)]
            registros[(grupo, alumno)] = nuevo_estado
            estado_guardado = "Falta" if nuevo_estado == "Ausente" else nuevo_estado
            if grupo == GRUPO_DOCENTE:
                anterior = next((r for r in reversed(REGISTROS_ASISTENCIA)
                                 if r["nombre"] == alumno and r.get("grupo", GRUPO_DOCENTE) == grupo
                                 and r["fecha"] == date.today().isoformat()), None)
                if anterior:
                    estado_anterior = anterior["estado"]
                    anterior["estado"] = estado_guardado
                else:
                    estado_anterior = None
                    REGISTROS_ASISTENCIA.append({"fecha": date.today().isoformat(), "nombre": alumno,
                                                 "grupo": grupo, "estado": estado_guardado})
                al = next((x for x in ALUMNOS_COMPARTIDOS if x["nombre"] == alumno), None)
                if al:
                    if estado_anterior == "Falta":
                        al["faltas"] = max(0, al["faltas"] - 1)
                    elif estado_anterior == "Presente":
                        al["asistencias"] = max(0, al["asistencias"] - 1)
                    elif estado_anterior == "Retardo":
                        al["retardos"] = max(0, al["retardos"] - 1)
                    if estado_guardado == "Falta":
                        al["faltas"] += 1
                    elif estado_guardado == "Presente":
                        al["asistencias"] += 1
                    elif estado_guardado == "Retardo":
                        al["retardos"] += 1
                    actualizar_alerta_alumno(al, grupo)
            if grupo != GRUPO_DOCENTE:
                registro_global = next((r for r in reversed(REGISTROS_ASISTENCIA)
                                        if r.get("nombre") == alumno and r.get("grupo") == grupo
                                        and r.get("fecha") == date.today().isoformat()), None)
                if registro_global:
                    registro_global["estado"] = estado_guardado
                else:
                    REGISTROS_ASISTENCIA.append({"fecha": date.today().isoformat(),
                                                 "nombre": alumno, "grupo": grupo,
                                                 "estado": estado_guardado})
            guardar_datos()
            tabla.item(iid, values=(valores[0], alumno, grupo, nuevo_estado),
                       tags=("ausente",) if nuevo_estado in ("Ausente", "Falta") else ())
        cargar_grupo()
        actualizar_botones_asistencia()
        boton_padre(panel, "Cambiar estado del seleccionado", cambiar_estado).pack(anchor="e", padx=22, pady=(0, 18))

    def mostrar_registro_masivo():
        limpiar_panel()
        encabezado(
            "Registro de alumnos",
            "Registra alumnos por grado. Escribe un nombre por renglón y selecciona el grupo correspondiente."
        )

        tarjeta = tk.Frame(panel, bg=C_DIR("tarjeta"),
                           highlightbackground=C_DIR("borde"), highlightthickness=1)
        tarjeta.pack(fill="x", padx=22, pady=(0, 16))

        etiqueta(tarjeta, "DATOS DEL REGISTRO", 11, True,
                 bg=C_DIR("tarjeta")).pack(anchor="w", padx=16, pady=(14, 8))

        fila_grupo = tk.Frame(tarjeta, bg=C_DIR("tarjeta"))
        fila_grupo.pack(fill="x", padx=16, pady=(0, 10))
        etiqueta(fila_grupo, "Grado y grupo:", 10, True,
                 bg=C_DIR("tarjeta")).pack(side="left", padx=(0, 10))

        grupo_var = tk.StringVar(value="1° A")
        selector = ttk.Combobox(
            fila_grupo, textvariable=grupo_var,
            values=[f"{n}° A" for n in range(1, 7)],
            state="readonly", width=14, font=("Segoe UI", 10)
        )
        selector.pack(side="left")

        etiqueta(tarjeta, "Nombres de los alumnos (uno por línea):", 10, True,
                 bg=C_DIR("tarjeta")).pack(anchor="w", padx=16, pady=(2, 6))

        entrada_nombres = tk.Text(
            tarjeta, height=8, font=("Segoe UI", 10),
            bg=C_DIR("campo"), fg=C_DIR("texto_campo"),
            insertbackground=C_DIR("texto_campo"), relief="flat",
            wrap="word", padx=10, pady=9
        )
        entrada_nombres.pack(fill="x", padx=16, pady=(0, 10))

        etiqueta(tarjeta,
                 "Puedes pegar una lista completa. Los nombres repetidos dentro del mismo grupo no se duplicarán.",
                 9, color=C_DIR("secundario"), bg=C_DIR("tarjeta"),
                 wraplength=850, justify="left").pack(anchor="w", padx=16, pady=(0, 12))

        resumen = tk.Frame(panel, bg=C_DIR("fondo"))
        resumen.pack(fill="x", padx=22, pady=(0, 10))

        etiqueta(panel, "ALUMNOS REGISTRADOS EN EL GRUPO", 11, True).pack(
            anchor="w", padx=22, pady=(2, 8)
        )

        tabla = crear_tabla(panel, ("No.", "Nombre del alumno", "Grado y grupo"),
                            (65, 360, 150))

        def actualizar_tabla(_event=None):
            grupo = grupo_var.get()
            for item in tabla.get_children():
                tabla.delete(item)
            nombres = grupos.get(grupo, [])
            for numero, nombre in enumerate(nombres, 1):
                tabla.insert("", "end", values=(numero, nombre, grupo))
            for widget in resumen.winfo_children():
                widget.destroy()
            caja_tarjeta(
                resumen, "TOTAL DE ALUMNOS", str(len(nombres)),
                f"Registrados en {grupo}", C_DIR("acento")
            ).pack(fill="x")

        def guardar_registro_masivo():
            grupo = grupo_var.get()
            texto = entrada_nombres.get("1.0", tk.END)
            nuevos = []
            for linea in texto.splitlines():
                nombre = " ".join(linea.strip().split())
                if nombre and nombre.casefold() not in {
                    existente.casefold() for existente in grupos.get(grupo, [])
                } and nombre.casefold() not in {x.casefold() for x in nuevos}:
                    nuevos.append(nombre)

            if not nuevos:
                messagebox.showwarning(
                    "Sin nombres nuevos",
                    "Escribe al menos un nombre que todavía no esté registrado en este grupo."
                )
                return

            grupos.setdefault(grupo, [])
            grupos[grupo].extend(nuevos)
            GRUPOS_ESCOLARES[grupo] = list(grupos[grupo])
            for nombre in nuevos:
                registros[(grupo, nombre)] = "Sin registro"

            alumnos[:] = [nombre for lista in grupos.values() for nombre in lista]
            guardar_datos()
            entrada_nombres.delete("1.0", tk.END)
            actualizar_tabla()
            messagebox.showinfo(
                "Registro completado",
                f"Se registraron {len(nuevos)} alumnos en {grupo}."
            )

        selector.bind("<<ComboboxSelected>>", actualizar_tabla)
        boton_padre(tarjeta, "Guardar alumnos", guardar_registro_masivo).pack(
            anchor="e", padx=16, pady=(0, 15)
        )
        actualizar_tabla()

    def mostrar_alertas():
        limpiar_panel()
        encabezado("Alertas de seguimiento", "Alumnos que acumularon tres faltas o más.")
        resumen = tk.Frame(panel, bg=C_DIR("fondo"))
        resumen.pack(fill="x", padx=22, pady=(0, 12))
        caja_tarjeta(resumen, "ALERTAS ACTIVAS", str(len(ALERTAS_SEGUIMIENTO)),
                     "Requieren revisión de dirección", C_DIR("rojo")).pack(fill="x")
        tabla = crear_tabla(panel, ("Alumno", "Grupo", "Faltas", "Estado", "Fecha"),
                            (220, 90, 80, 210, 120))
        tabla.tag_configure("alerta", background="#F8C9D1", foreground="#A3122A")
        for alerta in ALERTAS_SEGUIMIENTO:
            tabla.insert("", "end", values=(alerta["nombre"], alerta["grupo"],
                          alerta["faltas"], alerta["estado"], alerta["fecha"]), tags=("alerta",))
        if not ALERTAS_SEGUIMIENTO:
            etiqueta(panel, "No hay alumnos con tres faltas registradas.", 11,
                     color=C_DIR("verde")).pack(anchor="w", padx=22, pady=12)

    # Romero Pérez Evelin Amairani y Marina Itzel Juárez Nava: crear, guardar y visualizar contraseñas desde Dirección.
    def mostrar_contrasenas():
        limpiar_panel()
        encabezado("Contraseñas por grupo", "Crea, modifica y consulta las claves de acceso de los docentes.")
        tarjeta_claves = tk.Frame(panel, bg=C_DIR("tarjeta"),
                                  highlightbackground=C_DIR("borde"), highlightthickness=1)
        tarjeta_claves.pack(fill="both", expand=True, padx=22, pady=(0, 18))
        etiqueta(tarjeta_claves,
                 "Las contraseñas se guardan en MySQL y se comparten entre los equipos conectados al mismo servidor.",
                 10, color=C_DIR("secundario"), bg=C_DIR("tarjeta"), wraplength=900
                 ).pack(anchor="w", padx=16, pady=(12, 10))
        try:
            grupos_db = ejecutar_consulta(
                "SELECT id_grupo, grado, grupo FROM grupos ORDER BY id_grupo", obtener=True
            ) or []
            accesos = ejecutar_consulta(
                "SELECT id_grupo, usuario, clave_visible FROM accesos_sistema WHERE tipo='docente'",
                obtener=True
            ) or []
        except Exception:
            grupos_db, accesos = [], []
        mapa = {int(d["id_grupo"]): d for d in accesos if d.get("id_grupo") is not None}

        if not grupos_db:
            etiqueta(tarjeta_claves, "No se encontraron grupos en la base de datos.", 11,
                     color=C_DIR("rojo"), bg=C_DIR("tarjeta")).pack(anchor="w", padx=16, pady=12)
            return

        for info in grupos_db:
            id_grupo = int(info["id_grupo"])
            grado = str(info["grado"])
            letra = str(info["grupo"])
            numero = next((n for n, nombre in GRADOS_DB.items()
                           if nombre.lower() == grado.lower()), None)
            etiqueta_grupo = f"{numero}° {letra}" if numero else f"{grado} {letra}"
            acceso = mapa.get(id_grupo, {})
            fila = tk.Frame(tarjeta_claves, bg=C_DIR("tarjeta"))
            fila.pack(fill="x", padx=16, pady=7)
            fila.columnconfigure(1, weight=1)
            etiqueta(fila, etiqueta_grupo, 11, True, bg=C_DIR("tarjeta"), width=12).grid(
                row=0, column=0, sticky="w", padx=(0, 8))
            entrada = ttk.Entry(fila, font=("Segoe UI", 10), show="•")
            entrada.insert(0, acceso.get("clave_visible") or "")
            entrada.grid(row=0, column=1, sticky="ew", padx=6)
            visible = {"valor": False}

            def alternar_visibilidad(e=entrada, estado=visible, b=None):
                estado["valor"] = not estado["valor"]
                e.configure(show="" if estado["valor"] else "•")
                if b is not None:
                    b.configure(text="Ocultar" if estado["valor"] else "Ver")

            boton_ver = tk.Button(fila, text="Ver", font=("Segoe UI", 9, "bold"),
                                  command=lambda e=entrada, st=visible, b=None: alternar_visibilidad(e, st, b),
                                  relief="flat", bd=0, cursor="hand2",
                                  bg=C_DIR("panel"), fg=C_DIR("texto"), padx=10, pady=7)
            boton_ver.configure(command=lambda e=entrada, st=visible, b=boton_ver: alternar_visibilidad(e, st, b))
            boton_ver.grid(row=0, column=2, padx=5)

            def guardar_clave(g=etiqueta_grupo, gid=id_grupo, e=entrada, usuario_doc=acceso.get("usuario")):
                clave = e.get().strip()
                if len(clave) < 4:
                    messagebox.showwarning("Contraseña no válida", "Usa al menos cuatro caracteres.")
                    return
                nombre_usuario = usuario_doc or g
                existente = ejecutar_consulta(
                    "SELECT id_acceso FROM accesos_sistema WHERE tipo='docente' AND id_grupo=%s",
                    (gid,), obtener=True
                ) or []
                if existente:
                    ok = ejecutar_consulta(
                        """UPDATE accesos_sistema
                           SET usuario=%s, clave_hash=%s, clave_visible=%s
                           WHERE tipo='docente' AND id_grupo=%s""",
                        (nombre_usuario, hash_clave(clave), clave, gid)
                    )
                else:
                    ok = ejecutar_consulta(
                        """INSERT INTO accesos_sistema
                           (tipo,id_grupo,usuario,clave_hash,clave_visible)
                           VALUES ('docente',%s,%s,%s,%s)""",
                        (gid, nombre_usuario, hash_clave(clave), clave)
                    )
                if ok:
                    CONTRASENAS_GRUPOS[g] = clave
                    messagebox.showinfo("Contraseña guardada",
                                        f"La contraseña de {g} se creó o actualizó correctamente en MySQL.")
            boton_guardar = tk.Button(fila, text="Guardar", command=guardar_clave,
                                      font=("Segoe UI", 9, "bold"), relief="flat", bd=0,
                                      cursor="hand2", bg=C_DIR("acento"),
                                      fg=C_DIR("boton_texto"), padx=12, pady=7)
            boton_guardar.grid(row=0, column=3, padx=(5, 0))

        etiqueta(tarjeta_claves,
                 "Puedes escribir una contraseña nueva, guardarla y usarla para iniciar sesión desde cualquier equipo conectado al servidor MySQL.",
                 9, color=C_DIR("secundario"), bg=C_DIR("tarjeta"), wraplength=900
                 ).pack(anchor="w", padx=16, pady=(12, 16))

    def mostrar_calendario():
        limpiar_panel()
        encabezado("Calendario escolar", "Consulta el mes actual y abre el calendario institucional en PDF.")
        fila_pdf = tk.Frame(panel, bg=C_DIR("fondo"))
        fila_pdf.pack(fill="x", padx=22, pady=(0, 12))
        boton_padre(fila_pdf, "SELECCIONAR CALENDARIO PDF", seleccionar_calendario_pdf).pack(side="left", padx=(0, 8))
        boton_padre(fila_pdf, "ABRIR CALENDARIO PDF", abrir_calendario_pdf, C_DIR("verde"), "#FFFFFF").pack(side="left")
        ahora = datetime.now()
        marco = tk.Frame(panel, bg=C_DIR("tarjeta"), highlightbackground=C_DIR("borde"), highlightthickness=1)
        marco.pack(fill="x", padx=22, pady=(0, 16))
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        etiqueta(marco, f"{meses[ahora.month - 1].upper()} {ahora.year}", 17, True, bg=C_DIR("tarjeta")).pack(pady=14)
        grid = tk.Frame(marco, bg=C_DIR("tarjeta")); grid.pack(fill="x", padx=10, pady=(0, 12))
        for col, dia in enumerate(["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]):
            tk.Label(grid, text=dia, bg=C_DIR("tabla_cabecera"), fg=C_DIR("texto"), font=("Segoe UI", 9, "bold"), pady=8).grid(row=0, column=col, sticky="nsew", padx=2, pady=2)
            grid.columnconfigure(col, weight=1, uniform="dias")
        for f, semana in enumerate(calendar.monthcalendar(ahora.year, ahora.month), 1):
            for col, numero in enumerate(semana):
                fondo = C_DIR("seleccion") if numero == ahora.day else C_DIR("tarjeta")
                tk.Label(grid, text=str(numero) if numero else "", bg=fondo, fg=C_DIR("texto"), font=("Segoe UI", 10), height=2, highlightbackground=C_DIR("borde"), highlightthickness=1).grid(row=f, column=col, sticky="nsew", padx=2, pady=2)
        form = tk.Frame(panel, bg=C_DIR("tarjeta"), highlightbackground=C_DIR("borde"), highlightthickness=1)
        form.pack(fill="x", padx=22, pady=(0, 18))
        etiqueta(form, "Agregar evento", 12, True, bg=C_DIR("tarjeta")).pack(anchor="w", padx=14, pady=(12, 6))
        fila = tk.Frame(form, bg=C_DIR("tarjeta")); fila.pack(fill="x", padx=14, pady=(0, 12))
        fila.columnconfigure(0, weight=1)
        ent_evento = ttk.Entry(fila, font=("Segoe UI", 10)); ent_evento.pack(side="left", fill="x", expand=True, padx=(0, 8))
        zona_eventos = tk.Frame(panel, bg=C_DIR("fondo")); zona_eventos.pack(fill="x", padx=22, pady=(0, 18))
        def lista_eventos():
            for w in zona_eventos.winfo_children(): w.destroy()
            etiqueta(zona_eventos, "Eventos registrados", 11, True).pack(anchor="w", pady=(0, 7))
            if not eventos:
                etiqueta(zona_eventos, "Todavía no hay eventos.", 10, color=C_DIR("secundario")).pack(anchor="w")
            for nombre, fecha in eventos:
                etiqueta(zona_eventos, f"• {fecha} — {nombre}", 10).pack(anchor="w", pady=2)
        def agregar_evento():
            texto_evento = ent_evento.get().strip()
            if not texto_evento:
                messagebox.showwarning("Falta el evento", "Escribe el nombre del evento."); return
            eventos.append((texto_evento, datetime.now().strftime("%d/%m/%Y")))
            ent_evento.delete(0, tk.END)
            messagebox.showinfo("Evento agregado", "El evento quedó registrado en la sesión.")
            lista_eventos()
        boton_padre(fila, "Agregar", agregar_evento).pack(side="right")
        lista_eventos()

    def mostrar_carta():
        limpiar_panel()
        encabezado("Carta compromiso", "Genera y guarda una carta para el alumno y su tutor.")
        form = tk.Frame(panel, bg=C_DIR("tarjeta"), highlightbackground=C_DIR("borde"), highlightthickness=1)
        form.pack(fill="x", padx=22, pady=(0, 18))
        etiqueta(form, "Datos de la carta", 12, True, bg=C_DIR("tarjeta")).pack(anchor="w", padx=16, pady=(14, 8))
        campos = tk.Frame(form, bg=C_DIR("tarjeta")); campos.pack(fill="x", padx=16)
        campos.columnconfigure((0, 1), weight=1, uniform="carta")
        etiqueta(campos, "Nombre del alumno", 10, bg=C_DIR("tarjeta")).grid(row=0, column=0, sticky="w", pady=4)
        ent_alumno = ttk.Entry(campos, font=("Segoe UI", 10)); ent_alumno.grid(row=1, column=0, sticky="ew", padx=(0, 8), pady=(0, 10))
        etiqueta(campos, "Motivo o compromiso", 10, bg=C_DIR("tarjeta")).grid(row=0, column=1, sticky="w", pady=4)
        ent_motivo = ttk.Entry(campos, font=("Segoe UI", 10)); ent_motivo.grid(row=1, column=1, sticky="ew", pady=(0, 10))
        etiqueta(form, "Vista previa", 10, True, color=C_DIR("secundario"), bg=C_DIR("tarjeta")).pack(anchor="w", padx=16)
        vista = tk.Text(form, height=9, font=("Segoe UI", 10), bg=C_DIR("campo"), fg=C_DIR("texto_campo"), insertbackground=C_DIR("texto_campo"), relief="flat", wrap="word", padx=12, pady=10)
        vista.pack(fill="both", expand=True, padx=16, pady=9)
        def generar():
            alumno, motivo = ent_alumno.get().strip(), ent_motivo.get().strip()
            if not alumno or not motivo:
                messagebox.showwarning("Datos incompletos", "Completa el nombre y el motivo."); return
            carta = ("CARTA COMPROMISO ESCOLAR\n"
                     "ESCUELA PRIMARIA NEZAHUALCÓYOTL\n"
                     "====================================\n\n"
                     f"Fecha: {datetime.now().strftime('%d/%m/%Y')}\n\n"
                     f"Yo, {alumno}, me comprometo a mejorar en el siguiente aspecto: {motivo}.\n\n"
                     "Me comprometo a respetar el reglamento escolar y cumplir con mis responsabilidades.\n\n"
                     "Firma del alumno: ______________________\n\n"
                     "Firma del tutor: ________________________\n\n"
                     "Firma de dirección: _____________________")
            vista.delete("1.0", tk.END); vista.insert("1.0", carta)
        def guardar_pdf():
            texto_carta = vista.get("1.0", "end-1c").strip()
            if not texto_carta:
                messagebox.showwarning("Sin contenido", "Primero genera la carta.")
                return
            ruta = filedialog.asksaveasfilename(
                title="Guardar carta compromiso en PDF",
                defaultextension=".pdf",
                filetypes=[("Documento PDF", "*.pdf")]
            )
            if not ruta:
                return
            try:
                from reportlab.lib.pagesizes import letter
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.lib.enums import TA_CENTER
                from reportlab.lib import colors
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
                from reportlab.lib.units import inch
                doc = SimpleDocTemplate(ruta, pagesize=letter,
                    rightMargin=0.8*inch, leftMargin=0.8*inch,
                    topMargin=0.75*inch, bottomMargin=0.75*inch)
                estilos = getSampleStyleSheet()
                titulo_pdf = ParagraphStyle("TituloCarta", parent=estilos["Title"],
                    textColor=colors.HexColor("#102B50"), alignment=TA_CENTER,
                    fontName="Helvetica-Bold", fontSize=16, leading=21, spaceAfter=8)
                normal_pdf = ParagraphStyle("TextoCarta", parent=estilos["BodyText"],
                    fontName="Helvetica", fontSize=11, leading=18, spaceAfter=10)
                historia = []
                for indice, linea in enumerate(texto_carta.splitlines()):
                    seguro = (linea.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
                    if indice == 0:
                        historia.append(Paragraph(seguro, titulo_pdf))
                    elif not seguro.strip():
                        historia.append(Spacer(1, 10))
                    else:
                        historia.append(Paragraph(seguro, normal_pdf))
                doc.build(historia)
                messagebox.showinfo("PDF guardado", "La carta compromiso se guardó correctamente como PDF.")
            except ImportError:
                messagebox.showerror("Falta una dependencia",
                    "Para generar PDF instala ReportLab con: pip install reportlab")
            except Exception as error:
                messagebox.showerror("Error al guardar", str(error))
        acciones = tk.Frame(form, bg=C_DIR("tarjeta")); acciones.pack(fill="x", padx=16, pady=(0, 14))
        boton_padre(acciones, "Generar carta", generar).pack(side="left", padx=(0, 8))
        boton_padre(acciones, "Guardar como PDF", guardar_pdf, C_DIR("verde"), "#FFFFFF").pack(side="left")

    configurar_estilos()
    construir_menu()
    mostrar_vista("inicio")
    boton_tema_dir.configure(text="☀  Tema claro", bg=C_DIR("panel"), fg=C_DIR("texto"))

fondo_superior = tk.Frame(ventana, bg=AZUL)
fondo_superior.place(relx=0, rely=0, relwidth=1, relheight=0.48)
franja_superior = tk.Frame(ventana, bg=CIAN, height=4)
franja_superior.place(relx=0, rely=0, relwidth=1)
encabezado = tk.Frame(ventana, bg=AZUL)
encabezado.pack(fill="x", pady=(22, 0))
tk.Label(encabezado, text="NEZAHUALCÓYOTL", font=("Segoe UI", 20, "bold"), bg=AZUL, fg=BLANCO).pack(pady=(7, 2))
tk.Label(encabezado, text="Sistema de Alerta Temprana para Situaciones de Riesgo", font=("Segoe UI", 10), bg=AZUL, fg="#B9CBE2").pack()
tk.Label(encabezado, text="ESCUELA PRIMARIA NEZAHUALCÓYOTL", font=("Segoe UI", 8, "bold"), bg=AZUL, fg=CIAN).pack(pady=(3, 0))

boton_tema = tk.Button(ventana, text="☀  Modo claro", font=("Segoe UI", 9, "bold"),
                       bg=AZUL_CLARO, fg=BLANCO, activebackground=CIAN,
                       activeforeground=FONDO, relief="flat", bd=0, cursor="hand2",
                       command=alternar_tema, padx=12, pady=7)
boton_tema.place(relx=0.975, rely=0.035, anchor="ne")
sombra = tk.Frame(ventana, bg="#06101E")
sombra.place(relx=0.5, rely=0.565, anchor="center", width=426, height=450)
tarjeta = tk.Frame(ventana, bg=BLANCO)
tarjeta.place(relx=0.5, rely=0.565, anchor="center", width=420, height=450)
tarjeta.pack_propagate(False)
franja_tarjeta = tk.Frame(tarjeta, bg=CIAN, height=5); franja_tarjeta.pack(fill="x")
cabecera = tk.Frame(tarjeta, bg=BLANCO); cabecera.pack(fill="x", padx=32, pady=(17, 10))
emblema = tk.Canvas(cabecera, width=54, height=54, highlightthickness=0); emblema.pack(side="left", padx=(0, 13))
emblema.create_polygon(8, 20, 27, 8, 46, 20, fill=CIAN, outline=CIAN)
emblema.create_rectangle(12, 21, 42, 45, fill=BLANCO, outline=BLANCO)
emblema.create_rectangle(23, 33, 31, 45, fill=CIAN, outline=CIAN)
for px in (16, 34):
    emblema.create_rectangle(px, 25, px + 5, 30, fill=CIAN, outline=CIAN)
datos_escuela = tk.Frame(cabecera, bg=BLANCO); datos_escuela.pack(side="left", fill="x", expand=True)
etiqueta_primaria = tk.Label(datos_escuela, text="PRIMARIA", font=("Segoe UI", 9, "bold"), bg=BLANCO, fg=GRIS, anchor="w"); etiqueta_primaria.pack(fill="x")
etiqueta_escuela = tk.Label(datos_escuela, text="NEZAHUALCÓYOTL", font=("Segoe UI", 12, "bold"), bg=BLANCO, fg=AZUL, anchor="w"); etiqueta_escuela.pack(fill="x", pady=(1, 0))
separador = tk.Frame(tarjeta, bg="#E5EBF2", height=1); separador.pack(fill="x", padx=32, pady=(0, 14))
cuerpo = tk.Frame(tarjeta, bg=BLANCO); cuerpo.pack(fill="both", expand=True, padx=32)
titulo_bienvenida = tk.Label(cuerpo, text="Bienvenido al sistema", font=("Segoe UI", 17, "bold"), bg=BLANCO, fg=TEXTO); titulo_bienvenida.pack(anchor="w")
etiqueta_usuario = tk.Label(cuerpo, text="INGRESA TU USUARIO", font=("Segoe UI", 9, "bold"), bg=BLANCO, fg=AZUL); etiqueta_usuario.pack(anchor="w", pady=(12, 5))
frame_user = tk.Frame(cuerpo, bg=CAMPO, highlightthickness=1, highlightbackground="#DCE5F0"); frame_user.pack(fill="x", ipady=2)
icono_usuario = tk.Label(frame_user, text="♟", font=("Segoe UI", 16), bg=CAMPO, fg=AZUL_CLARO); icono_usuario.pack(side="left", padx=(12, 8))
entrada_usuario = tk.Entry(frame_user, font=("Segoe UI", 11), bg=CAMPO, fg=TEXTO, insertbackground=AZUL, relief="flat", bd=0); entrada_usuario.pack(side="left", fill="x", expand=True, padx=(0, 12), pady=11)
etiqueta_contrasena = tk.Label(cuerpo, text="INGRESA TU CONTRASEÑA", font=("Segoe UI", 9, "bold"), bg=BLANCO, fg=AZUL); etiqueta_contrasena.pack(anchor="w", pady=(13, 5))
frame_pass = tk.Frame(cuerpo, bg=CAMPO, highlightthickness=1, highlightbackground="#DCE5F0"); frame_pass.pack(fill="x", ipady=2)
icono_contrasena = tk.Label(frame_pass, text="●", font=("Segoe UI", 12), bg=CAMPO, fg=AZUL_CLARO); icono_contrasena.pack(side="left", padx=(14, 10))
entrada_contra = tk.Entry(frame_pass, font=("Segoe UI", 11), bg=CAMPO, fg=TEXTO, insertbackground=AZUL, relief="flat", bd=0, show="*"); entrada_contra.pack(side="left", fill="x", expand=True, padx=(0, 5), pady=11)
boton_ver = tk.Button(frame_pass, text="◎", font=("Segoe UI", 12), bg=CAMPO, fg=AZUL_CLARO, activebackground=CAMPO, activeforeground=AZUL, relief="flat", bd=0, cursor="hand2", command=alternar_contrasena); boton_ver.pack(side="right", padx=(0, 9))
opciones = tk.Frame(cuerpo, bg=BLANCO); opciones.pack(fill="x", pady=(10, 0))
indicador = tk.Label(opciones, text="●", font=("Arial", 10), bg=BLANCO, fg=VERDE); indicador.pack(side="left")
etiqueta_autorizacion = tk.Label(opciones, text=" Acceso solo para personal autorizado", font=("Segoe UI", 8), bg=BLANCO, fg=GRIS); etiqueta_autorizacion.pack(side="left")
boton_limpiar = tk.Button(opciones, text="LIMPIAR", font=("Segoe UI", 8, "bold"), bg=BLANCO, fg=AZUL_CLARO, activebackground=BLANCO, relief="flat", cursor="hand2", command=limpiar_campos); boton_limpiar.pack(side="right")
mensaje = tk.Label(cuerpo, text="", font=("Segoe UI", 8), bg=BLANCO, fg=ROJO, anchor="w"); mensaje.pack(fill="x", pady=(7, 0))
boton_ingresar = tk.Button(cuerpo, text="INGRESAR  →", font=("Segoe UI", 11, "bold"), bg=CIAN, fg=FONDO, activebackground="#168ED0", activeforeground=BLANCO, relief="flat", bd=0, cursor="hand2", command=ingresar, pady=10); boton_ingresar.pack(fill="x", pady=(8, 8))

def efecto_boton_entrada(event):
    boton_ingresar.config(bg=TEMAS[modo_actual]["acento_hover"])

def efecto_boton_salida(event):
    boton_ingresar.config(bg=TEMAS[modo_actual]["acento"])

boton_ingresar.bind("<Enter>", efecto_boton_entrada)
boton_ingresar.bind("<Leave>", efecto_boton_salida)
pie = tk.Frame(ventana, bg=FONDO); pie.pack(side="bottom", fill="x", pady=(0, 13))
etiqueta_sistema = tk.Label(pie, text="SISTEMA INSTITUCIONAL", font=("Segoe UI", 8, "bold"), bg=FONDO, fg=GRIS); etiqueta_sistema.pack()
reloj = tk.Label(pie, text="", font=("Segoe UI", 8), bg=FONDO, fg=CIAN); reloj.pack(pady=(5, 0))

def ajustar_diseno(event=None):
    ancho = ventana.winfo_width()
    alto = ventana.winfo_height()
    ancho_tarjeta = min(420, max(280, ancho - 24))
    alto_tarjeta = min(450, max(390, alto - 190))
    centro_y = min(0.57, max(0.53, (alto - 35) / (2 * alto)))
    sombra.place(relx=0.5, rely=centro_y, anchor="center", width=ancho_tarjeta + 6, height=alto_tarjeta + 6)
    tarjeta.place(relx=0.5, rely=centro_y, anchor="center", width=ancho_tarjeta, height=alto_tarjeta)
    compacto = ancho < 520
    margen = 18 if compacto else 32
    cabecera.pack_configure(padx=margen, pady=(14, 8))
    separador.pack_configure(padx=margen, pady=(0, 10))
    cuerpo.pack_configure(padx=margen)
    titulo_bienvenida.configure(font=("Segoe UI", 14 if compacto else 17, "bold"))
    etiqueta_escuela.configure(font=("Segoe UI", 10 if compacto else 12, "bold"))
    encabezado.winfo_children()[0].configure(font=("Segoe UI", 15 if ancho < 520 else 20, "bold"))
    encabezado.winfo_children()[1].configure(font=("Segoe UI", 8 if ancho < 520 else 10))
    boton_tema.configure(font=("Segoe UI", 8 if compacto else 9, "bold"), padx=7 if compacto else 12, pady=5 if compacto else 7)
    boton_tema.place(relx=0.98, rely=0.02, anchor="ne")

def aplicar_tema():
    colores = TEMAS[modo_actual]
    ventana.configure(bg=colores["fondo"])
    fondo_superior.configure(bg=colores["encabezado"])
    encabezado.configure(bg=colores["encabezado"])
    pie.configure(bg=colores["pie"])
    franja_superior.configure(bg=colores["acento"])
    for widget in encabezado.winfo_children():
        if isinstance(widget, tk.Label):
            texto = widget.cget("text")
            widget.configure(
                bg=colores["encabezado"],
                fg=(colores["acento"] if texto.startswith("ESCUELA PRIMARIA")
                    else ("#B9CBE2" if modo_actual == "oscuro" else colores["secundario"])
                    if texto.startswith("Sistema de Alerta") else colores["texto"])
            )
    sombra.configure(bg=colores["sombra"])
    tarjeta.configure(bg=colores["tarjeta"])
    franja_tarjeta.configure(bg=colores["acento"])
    cabecera.configure(bg=colores["tarjeta"])
    datos_escuela.configure(bg=colores["tarjeta"])
    cuerpo.configure(bg=colores["tarjeta"])
    opciones.configure(bg=colores["tarjeta"])
    separador.configure(bg=colores["separador"])
    emblema.configure(bg=colores["tarjeta"])
    emblema.itemconfigure(2, fill=colores["texto"], outline=colores["texto"])
    emblema.itemconfigure(4, fill=colores["azul_claro"], outline=colores["azul_claro"])
    etiquetas = [
        (etiqueta_primaria, colores["secundario"]),
        (etiqueta_escuela, colores["texto"]),
        (titulo_bienvenida, colores["texto"]),
        (etiqueta_usuario, colores["acento"]),
        (etiqueta_contrasena, colores["acento"]),
        (etiqueta_autorizacion, colores["secundario"]),
    ]
    for widget, color_texto in etiquetas:
        widget.configure(bg=colores["tarjeta"], fg=color_texto)
    for frame in (frame_user, frame_pass):
        frame.configure(bg=colores["campo"], highlightbackground=colores["borde"], highlightcolor=colores["acento"])
    for widget in (entrada_usuario, entrada_contra):
        widget.configure(bg=colores["campo"], fg=colores["texto_campo"], insertbackground=colores["acento"])
    icono_usuario.configure(bg=colores["campo"], fg=colores["icono"])
    icono_contrasena.configure(bg=colores["campo"], fg=colores["icono"])
    boton_ver.configure(bg=colores["campo"], fg=colores["icono"], activebackground=colores["campo"], activeforeground=colores["acento"])
    indicador.configure(bg=colores["tarjeta"], fg=colores["verde"])
    boton_limpiar.configure(bg=colores["tarjeta"], fg=colores["boton_secundario_texto"], activebackground=colores["tarjeta"], activeforeground=colores["acento"])
    mensaje.configure(bg=colores["tarjeta"])
    if mensaje.cget("text"):
        mensaje.configure(fg=colores["error"] if "Completa" in mensaje.cget("text") or "incorrecta" in mensaje.cget("text") else colores["aviso"])
    boton_ingresar.configure(bg=colores["acento"], fg=colores["boton_texto"], activebackground=colores["acento_hover"], activeforeground=BLANCO)
    if modo_actual == "oscuro":
        boton_tema.configure(text="☀  Modo claro", bg=colores["azul_claro"], fg=BLANCO, activebackground=colores["acento"], activeforeground=FONDO)
    else:
        boton_tema.configure(text="☾  Modo oscuro", bg=colores["encabezado"], fg=colores["texto"], activebackground=colores["campo"], activeforeground=colores["acento"])
    etiqueta_sistema.configure(bg=colores["pie"], fg=colores["secundario"])
    reloj.configure(bg=colores["pie"], fg=colores["reloj"])

entrada_usuario.bind("<Return>", lambda event: entrada_contra.focus_set())
entrada_contra.bind("<Return>", lambda event: ingresar())
ventana.bind("<Control-l>", limpiar_campos)
ventana.bind("<Control-t>", lambda event: alternar_tema())
ventana.bind("<Configure>", ajustar_diseno)
aplicar_tema()
ventana.after(100, ajustar_diseno)
actualizar_reloj()
entrada_usuario.focus_set()
ventana.mainloop()
