from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from memoria import crear_memoria, tamano_valido
from planificador import gestor_memoria_bestfit
from consola import cargar_procesos_desde_archivo
import os
import tkinter as tk
from tkinter import filedialog

console = Console()


# Tablas y presentación de datos

def tabla_memoria(memoria):
    """Crea la tabla con las particiones de memoria."""
    t = Table(title="Tabla de Particiones de Memoria", box=box.SIMPLE, header_style="bold cyan")
    t.add_column("Id", justify="center")
    t.add_column("DirInicio", justify="center")
    t.add_column("Tamaño (K)", justify="center")
    t.add_column("Proc. asignado", justify="center")
    t.add_column("Frag. interna (K)", justify="center")
    t.add_column("Disponible", justify="center")

    for p in memoria:
        disp = "[green]Sí[/]" if p["Disponible"] else "[red]No[/]"
        t.add_row(
            str(p["NroParticion"]),
            str(p["DirInicio"]),
            str(p["TamanoParticion"]),
            str(p["ProcesoAsignado"]),
            str(p["FragmentacionInterna"]),
            disp,
        )
    return t


def tabla_procesos(lista, titulo, color="white"):
    """Genera la tabla de procesos para un estado determinado."""
    t = Table(title=titulo, box=box.SIMPLE, header_style=f"bold {color}")
    t.add_column("ID", justify="center")
    t.add_column("Tamaño", justify="center")
    t.add_column("Arribo", justify="center")
    t.add_column("Irrupción", justify="center")
    t.add_column("Restante", justify="center")
    t.add_column("Estado", justify="center")

    if not lista:
        t.add_row("-", "-", "-", "-", "-", "-")
        return t

    for p in lista:
        # getattr sirve para que funcione con distintos nombres de atributos
        pid = getattr(p, "id", getattr(p, "nombre", getattr(p, "ID", "-")))
        tam = getattr(p, "tamano", getattr(p, "tamaño", getattr(p, "size", "-")))
        arr = getattr(p, "ta", getattr(p, "arribo", getattr(p, "tiempo_arribo", "-")))
        irr = getattr(p, "ti", getattr(p, "irrupcion", getattr(p, "tiempo_irrupcion", "-")))
        res = getattr(p, "tiempo_restante", getattr(p, "restante", getattr(p, "tiempoRestante", "-")))
        est = getattr(p, "estado", "-")
        t.add_row(str(pid), str(tam), str(arr), str(irr), str(res), str(est))
    return t


def mostrar_estado(clk, memoria, nuevo, listo, susp, ejec, term):
    """Muestra en pantalla el estado completo del sistema."""
    console.clear()
    console.rule(f"[bold yellow]Tiempo del sistema: {clk}[/bold yellow]")

    # Panel superior con resumen general
    proc_cpu = getattr(ejec[0], "id", getattr(ejec[0], "nombre", "(ninguno)")) if ejec else "(ninguno)"
    restante_cpu = getattr(ejec[0], "tiempo_restante", getattr(ejec[0], "restante", "-")) if ejec else "-"
    grado_multi = len(listo) + len(susp) + len(ejec)
    terminados = len(term)

    console.print(
        Panel(
            f"[bold yellow]CPU:[/] {proc_cpu}  "
            f"[bold blue]|[/]  [yellow]Restante:[/] {restante_cpu}  "
            f"[bold blue]|[/]  [cyan]Grado de multiprogramación:[/] {grado_multi}/5  "
            f"[bold blue]|[/]  [green]Terminados:[/] {terminados}",
            border_style="bright_black",
            title="[bold green]Estado general del sistema[/bold green]",
        )
    )

    # Tablas principales
    console.print(tabla_memoria(memoria))
    console.print(tabla_procesos(listo, "Listo", "bright_blue"))
    console.print(tabla_procesos(susp, "Listo/Suspendido", "magenta"))
    console.print(tabla_procesos(nuevo, "Nuevo", "cyan"))
    console.print(tabla_procesos(ejec, "Ejecución", "green"))
    console.print(tabla_procesos(term, "Terminado", "grey50"))


def simulacion_manual(ruta_csv):
    """Ejecuta la simulación de manera paso a paso."""
    Memoria = crear_memoria()
    NUEVO, LISTO, EJEC, SUSP, TERM = [], [], [], [], []
    GRADO_MULTIPROG = 0
    clk = 0

    cargar_procesos_desde_archivo(ruta_csv, None, NUEVO)

    if not NUEVO:
        console.print(
            f"[red bold]No se cargó ningún proceso.[/red bold] "
            f"Verificá el archivo CSV:\n[white]{ruta_csv}[/white]\n"
        )
        return

    console.print(Panel(
        f"Archivo CSV: [cyan]{ruta_csv}[/cyan]\n"
        f"Procesos iniciales: [bold]{len(NUEVO)}[/bold]\n"
        f"Modo: [yellow]manual[/yellow] (avanza con Enter)",
        border_style="bold yellow", title="Simulador (Rich UI)"
    ))
    input("\nPresione [Enter] para comenzar...")

    ejecutando = True
    while ejecutando:
        mostrar_estado(clk, Memoria, NUEVO, LISTO, SUSP, EJEC, TERM)

        # 1) Finalización del proceso en ejecución
        if EJEC and getattr(EJEC[0], "tiempo_restante", 1) == 0:
            GRADO_MULTIPROG -= 1
            p_fin = EJEC.pop(0)
            p_fin.estado = "Terminado"

            # Libera la partición correspondiente
            for part in Memoria:
                if part["NroParticion"] == getattr(p_fin, "particion_asignada", None):
                    part["Disponible"] = True
                    part["ProcesoAsignado"] = None
                    part["FragmentacionInterna"] = 0
            p_fin.particion_asignada = None
            TERM.append(p_fin)

            # Al liberar memoria, primero se intenta reactivar un suspendido
            reactivado = False
            if SUSP:
                candidato = min(SUSP, key=lambda p: getattr(p, "tiempo_restante", 9999))
                # Ya llegó antes, así que no hace falta verificar ta <= clk
                if gestor_memoria_bestfit(candidato, Memoria, LISTO):
                    SUSP.remove(candidato)
                    reactivado = True
                    # GRADO_MULTIPROG no cambia: estaba contado en SUSP y pasa a LISTO

            # Si no hay suspendidos que entren, se revisa la cola de nuevos
            if not reactivado and NUEVO:
                for p in NUEVO[:]:
                    if GRADO_MULTIPROG < 5 and getattr(p, "ta", 0) <= clk:
                        # p ya fue filtrado por tamano_valido en la admisión normal
                        if gestor_memoria_bestfit(p, Memoria, LISTO):
                            NUEVO.remove(p)
                            GRADO_MULTIPROG += 1
                            break

        # 2) Planificación SRTF (solo procesos en memoria)
        menor_restante = getattr(EJEC[0], "tiempo_restante", float("inf")) if EJEC else float("inf")
        elegido = None
        for p in LISTO:
            if getattr(p, "tiempo_restante", 9999) < menor_restante:
                elegido = p
                menor_restante = getattr(p, "tiempo_restante", 9999)

        if elegido:
            # Caso 1: hay proceso ejecutando y el elegido lo interrumpe
            if EJEC and getattr(elegido, "tiempo_restante", 9999) < getattr(EJEC[0], "tiempo_restante", 9999):
                proceso_saliente = getattr(EJEC[0], "id", getattr(EJEC[0], "nombre", "?"))
                proceso_entrante = getattr(elegido, "id", getattr(elegido, "nombre", "?"))
                console.print(
                    f"[yellow]Cambio de contexto:[/] "
                    f"el proceso [cyan]{proceso_saliente}[/cyan] es interrumpido por "
                    f"[green]{proceso_entrante}[/green] (menor tiempo restante)"
                )

                EJEC[0].estado = "Listo"
                LISTO.append(EJEC.pop(0))
                LISTO.sort(key=lambda q: getattr(q, "tiempo_restante", 9999))

                elegido.estado = "Ejecución"
                EJEC.append(elegido)
                LISTO.remove(elegido)

            # Caso 2: CPU libre
            elif not EJEC:
                elegido.estado = "Ejecución"
                EJEC.append(elegido)
                LISTO.remove(elegido)

        # 3) Avance del tiempo de CPU
        if EJEC:
            EJEC[0].tiempo_restante -= 1

        # 4) Admisión de nuevos procesos
        for p in NUEVO[:]:

            # 4.1 — Primero: verificar si el proceso puede entrar alguna vez
            if not tamano_valido(p, Memoria):
                p.estado = "Descartado"
                console.print(
                    f"[red]El proceso {p.id} se descarta: excede el tamaño de todas las particiones[/red]"
                )
                NUEVO.remove(p)
                continue

            # 4.2 — Si el tamaño es válido, sigue el flujo normal
            if GRADO_MULTIPROG < 5 and getattr(p, "ta", 0) <= clk:

                # Intentar cargarlo por Best-Fit
                if gestor_memoria_bestfit(p, Memoria, LISTO):
                    NUEVO.remove(p)
                    GRADO_MULTIPROG += 1

                else:
                    # No hay partición libre, pero sí cabe → suspendido
                    p.estado = "Listo y suspendido"
                    SUSP.append(p)
                    NUEVO.remove(p)
                    GRADO_MULTIPROG += 1

            elif GRADO_MULTIPROG >= 5:
                # No se admiten más procesos al sistema
                break

        clk += 1
        mostrar_estado(clk, Memoria, NUEVO, LISTO, SUSP, EJEC, TERM)

        # 5) Condición de fin de simulación
        if not NUEVO and not LISTO and not SUSP and not EJEC:
            ejecutando = False
            console.print("\n[bold green]Simulación finalizada[/bold green]")
            break

        input("\nPresione [Enter] para avanzar un paso...")

    # Estadísticas finales

    console.rule("[bold yellow]Estadísticas finales[/bold yellow]")
    total_tiempo = clk
    if not TERM:
        console.print("[italic]No hay procesos terminados.[/italic]")
        return

    prom_ret = prom_esp = 0
    for p in TERM:
        p.tiempo_finalizacion = total_tiempo
        p.tiempo_retorno = total_tiempo - getattr(p, "ta", 0)
        p.tiempo_espera = p.tiempo_retorno - getattr(p, "ti", 0)
        prom_ret += p.tiempo_retorno
        prom_esp += p.tiempo_espera
        console.print(
            f"[cyan]{getattr(p, 'id', getattr(p, 'nombre', '?'))}[/cyan] "
            f"→ Retorno={p.tiempo_retorno}, Espera={p.tiempo_espera}"
        )

    prom_ret /= len(TERM)
    prom_esp /= len(TERM)
    rendimiento = len(TERM) / total_tiempo if total_tiempo > 0 else 0
    console.print(
        f"\n[bold yellow]Promedio Retorno:[/] {prom_ret:.2f}  |  "
        f"[bold yellow]Promedio Espera:[/] {prom_esp:.2f}  |  "
        f"[bold yellow]Rendimiento:[/] {rendimiento:.3f} procesos/UT"
    )
    console.print("\n[bold green]Fin de la simulación manual[/bold green]\n")


# Selector de archivo CSV (interfaz)

def seleccionar_csv():
    """Abre una ventana del explorador de archivos para seleccionar el CSV."""
    root = tk.Tk()
    root.withdraw()
    ruta = filedialog.askopenfilename(
        title="Seleccionar archivo CSV de procesos",
        filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
    )
    root.destroy()
    return ruta


# Ejecución principal

if __name__ == "__main__":
    console.print("[bold cyan]Seleccione el archivo CSV desde el explorador...[/bold cyan]")
    ruta = seleccionar_csv()
    if not ruta:
        console.print("[red]No se seleccionó ningún archivo. Saliendo...[/red]")
    elif not os.path.exists(ruta):
        console.print(f"[red]El archivo no existe:[/] {ruta}")
    else:
        simulacion_manual(ruta)
