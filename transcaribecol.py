import os
# ==============================================================================
# SISTEMA DE NÓMINA - TRANSCARIBECOL S.C.A.
# Programa: Técnico en Programación de Software (SENA - Riwi)
# Actividad 3.4: Liquidación de Nómina Automatizada
# ==============================================================================


# ------------------------------------------------------------------------------
# 1. CONSTANTES Y CONFIGURACIÓN DEL SISTEMA
# ------------------------------------------------------------------------------

# Tarifas por hora 
VALOR_HORA_ADMINISTRATIVO = 20000       # $20.000 por hora
VALOR_HORA_EXTRA_ADMIN = 25000          # $25.000 por hora extra
VALOR_HORA_OPERATIVO = 40000            # $40.000 por hora

# Porcentajes legales para Administrativos
PORCENTAJE_SALUD_ADMIN = 0.04           # 4%
PORCENTAJE_PENSION_ADMIN = 0.04         # 4%
PORCENTAJE_ARL_RIESGO_I = 0.00522       # 0.522% (Riesgo Nivel I)

# Porcentajes legales para Operativos (Prestación de Servicios)
PORCENTAJE_IBC_OPERATIVO = 0.40         # IBC = 40% del salario bruto
PORCENTAJE_SALUD_OPERATIVO = 0.125      # 12.5%
PORCENTAJE_PENSION_OPERATIVO = 0.160    # 16.0%

# Cargos operativos predefinidos por la empresa
CARGOS_OPERATIVOS = {
    "1": {
        "cargo": "Conductor",
        "horas": 160,
        "porcentaje_arl": 0.01044,
        "texto_arl": "ARL(1,044%)"
    },
    "2": {
        "cargo": "Oficios Generales",
        "horas": 100,
        "porcentaje_arl": 0.00522,
        "texto_arl": "ARL(0,522%)"
    },
    "3": {
        "cargo": "Vigilancia",
        "horas": 336,
        "porcentaje_arl": 0.04350,
        "texto_arl": "ARL(4,350%)"
    }
}

# Nombre del archivo plano TXT solicitado en la guía
NOMBRE_ARCHIVO_TXT = "nomina_transcaribecol.txt"

# Estructura de datos en memoria
lista_empleados = []


# ------------------------------------------------------------------------------
# 2. FUNCIONES DE VALIDACIÓN DE ENTRADA
# ------------------------------------------------------------------------------

def pedir_texto(mensaje):
    """Pide un texto y verifica que no quede vacío."""
    while True:
        valor = input(mensaje).strip()
        if valor != "":
            return valor
        print("El campo no puede estar vacío. Intente de nuevo.")


def pedir_entero_positivo(mensaje):
    """Pide un número entero >= 0. Evita caídas del programa si se ingresan letras."""
    while True:
        entrada = input(mensaje).strip()
        try:
            numero = int(entrada)
            if numero >= 0:
                return numero
            else:
                print("Debe ingresar un valor mayor o igual a 0.")
        except ValueError:
            print("Entrada inválida. Debe escribir un número entero (ejemplo: 40).")


# ------------------------------------------------------------------------------
# 3. REGISTRO Y CÁLCULOS DE EMPLEADOS
# ------------------------------------------------------------------------------

def registrar_administrativo():
    """
    Registra un empleado Administrativo y realiza sus cálculos según la guía:
    - Salario Bruto = Horas * 20.000
    - Horas Extras = Extras * 25.000
    - Base = Salario Bruto + Horas Extras
    - Salud (4%), Pensión (4%), ARL (0.522%)
    - Total a pagar = Base - (Salud + Pensión + ARL)
    """
    print("\n" + "=" * 65)
    print("           REGISTRO DE EMPLEADO ADMINISTRATIVO")
    print("=" * 65)

    nombre = pedir_texto("Ingrese el nombre completo: ")
    cargo = pedir_texto("Ingrese el cargo administrativo: ")
    ht = pedir_entero_positivo("Ingrese las Horas Trabajadas en el mes: ")
    he = pedir_entero_positivo("Ingrese las Horas Extras trabajadas: ")

    # Cálculos
    salario_bruto = ht * VALOR_HORA_ADMINISTRATIVO
    tphe = he * VALOR_HORA_EXTRA_ADMIN
    base_cotizacion = salario_bruto + tphe

    salud = round(base_cotizacion * PORCENTAJE_SALUD_ADMIN)
    pension = round(base_cotizacion * PORCENTAJE_PENSION_ADMIN)
    arl = round(base_cotizacion * PORCENTAJE_ARL_RIESGO_I)

    # En el volante de la guía original, el renglón "Total Descuentos" suma Salud + Pensión ($104.000),
    # pero el "Total a pagar" descuenta también la ARL ($1.189.214).
    total_descuentos_mostrado = salud + pension
    total_pagar = base_cotizacion - (salud + pension + arl)

    registro = {
        "nombre": nombre,
        "tipo": "ADMINISTRATIVO",
        "cargo": cargo,
        "ht": ht,
        "salario": salario_bruto,
        "he": he,
        "tphe": tphe,
        "salud": salud,
        "pension": pension,
        "arl": arl,
        "total_descuentos": total_descuentos_mostrado,
        "total_pagar": total_pagar
    }

    lista_empleados.append(registro)
    print("\n ¡Empleado administrativo registrado con éxito!")
    imprimir_volante(registro)


def registrar_operativo():
    """
    Registra un empleado Operativo (Prestación de Servicios):
    - Horas predeterminadas según el cargo (160, 100 o 336).
    - Tarifa: $40.000 por hora. Sin horas extras.
    - IBC = 40% del Salario Bruto.
    - Salud (12.5%), Pensión (16%), ARL (según nivel de riesgo I, II o IV).
    - Total a pagar = Salario Bruto - Deducciones.
    """
    print("\n" + "=" * 65)
    print("    REGISTRO DE EMPLEADO OPERATIVO (PRESTACIÓN DE SERVICIOS)")
    print("=" * 65)

    nombre = pedir_texto("Ingrese el nombre completo del contratista: ")

    print("\nSeleccione el cargo:")
    print("  1. Conductor         (160 horas | ARL Riesgo II: 1.044%)")
    print("  2. Oficios Generales (100 horas | ARL Riesgo I: 0.522%)")
    print("  3. Vigilancia        (336 horas | ARL Riesgo IV: 4.350%)")

    while True:
        opcion = input("Seleccione una opción (1, 2 o 3): ").strip()
        if opcion in CARGOS_OPERATIVOS:
            datos_cargo = CARGOS_OPERATIVOS[opcion]
            break
        print("Opción inválida. Digite 1, 2 o 3.")

    cargo = datos_cargo["cargo"]
    ht = datos_cargo["horas"]
    porcentaje_arl = datos_cargo["porcentaje_arl"]
    texto_arl = datos_cargo["texto_arl"]

    # Para operativos no aplican horas extras
    he = 0
    tphe = 0

    # Cálculos
    salario_bruto = ht * VALOR_HORA_OPERATIVO
    ibc = salario_bruto * PORCENTAJE_IBC_OPERATIVO

    salud = round(ibc * PORCENTAJE_SALUD_OPERATIVO)       # 12.5%
    pension = round(ibc * PORCENTAJE_PENSION_OPERATIVO)   # 16.0%
    arl = round(ibc * porcentaje_arl)                     # Según nivel de riesgo

    total_descuentos = salud + pension + arl
    total_pagar = salario_bruto - total_descuentos

    registro = {
        "nombre": nombre,
        "tipo": "OPERATIVO",
        "cargo": cargo,
        "ht": ht,
        "salario": salario_bruto,
        "he": he,
        "tphe": tphe,
        "salud": salud,
        "pension": pension,
        "arl": arl,
        "texto_arl": texto_arl,
        "total_descuentos": total_descuentos,
        "total_pagar": total_pagar
    }

    lista_empleados.append(registro)
    print("\n ¡Empleado operativo registrado con éxito!")
    imprimir_volante(registro)


# ------------------------------------------------------------------------------
# 4. IMPRESIÓN DEL VOLANTE DE PAGO (FORMATO EXACTO DEL EJERCICIO)
# ------------------------------------------------------------------------------

def imprimir_volante(emp):
    """
    Imprime el volante de pago en consola siguiendo la plantilla exacta
    de asteriscos solicitada en el archivo de la actividad.
    """
    print()
    print("*****************************************************************")
    print("******************* VOLANTE DE PAGO ********************")
    print("*****************************************************************")
    print(f"Nombre: {emp['nombre']}")
    print(f"Cargo: {emp['cargo']}")
    print(f"Horas Trabajadas(mes): {emp['ht']}")
    print(f"Salario Bruto: ${emp['salario']:,}")

    # Si es Administrativo, se muestran las horas extras
    if emp['tipo'] == "ADMINISTRATIVO":
        print(f"Horas Extras: {emp['he']}")
        print(f"Total pago Horas Extras: ${emp['tphe']:,}")

    print()
    print("*****************************************************************")
    print("******************* DESCUENTOS DE LEY ********************")
    print("*****************************************************************")

    if emp['tipo'] == "ADMINISTRATIVO":
        print(f"Salud(4%): ${emp['salud']}")
        print(f"Pensión(4%): ${emp['pension']}")
        print(f"ARL(0,522%): ${emp['arl']}")
    else:
        # En Operativo los porcentajes son 12.5%, 16% y su ARL respectiva
        print(f"Salud(12.5%): ${emp['salud']}")
        print(f"Pensión(16%): ${emp['pension']}")
        print(f"{emp.get('texto_arl', 'ARL')}: ${emp['arl']}")

    print(f"Total Descuentos: ${emp['total_descuentos']}")
    print()
    print(f"Total a pagar: ${emp['total_pagar']:,}")
    print()
    print("*****************************************************************")
    print("******************* FIN DEL VOLANTE DE PAGO ********************")
    print("*****************************************************************")


def mostrar_todos_los_volantes():
    """Recorre la lista de empleados y muestra en pantalla el volante de cada uno."""
    if not lista_empleados:
        print("\n No hay empleados registrados en el sistema.")
        return

    print("\n" + "=" * 65)
    print(f"        LISTADO DE VOLANTES DE PAGO ({len(lista_empleados)} REGISTROS)")
    print("=" * 65)

    for emp in lista_empleados:
        imprimir_volante(emp)


# ------------------------------------------------------------------------------
# 5. GUARDAR LA INFORMACIÓN EN MEMORIA SECUNDARIA (ARCHIVO TXT)
# ------------------------------------------------------------------------------

def guardar_en_archivo_txt():
    """
    Guarda la nómina en formato plano TXT delimitado por barras verticales (|),
    con el formato exacto requerido por la gerencia de TransCaribeCol:
    | Nombre | Tipo | Cargo | HT | Salario | HE | TPHE | Salud | Pension | ARL | Total a pagar |
    """
    if not lista_empleados:
        print("\n No hay registros para guardar. Registre empleados primero.")
        return

    # Encabezado con barras al inicio y al final
    encabezado = "| Nombre | Tipo | Cargo | HT | Salario | HE | TPHE | Salud | Pension | ARL | Total a pagar |\n"

    try:
        carpeta_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_archivo = os.path.join(carpeta_actual, NOMBRE_ARCHIVO_TXT)

        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(encabezado)

            for emp in lista_empleados:
                linea = (
                    f"| {emp['nombre']} | "
                    f"{emp['tipo']} | "
                    f"{emp['cargo']} | "
                    f"{emp['ht']} | "
                    f"{emp['salario']} | "
                    f"{emp['he']} | "
                    f"{emp['tphe']} | "
                    f"{emp['salud']} | "
                    f"{emp['pension']} | "
                    f"{emp['arl']} | "
                    f"{emp['total_pagar']} |\n"
                )
                archivo.write(linea)

        print("\n" + "=" * 65)
        print("ARCHIVO TXT GUARDADO EXITOSAMENTE")
        print("=" * 65)
        print(f"Archivo:   {NOMBRE_ARCHIVO_TXT}")
        print(f"Ubicación: {ruta_archivo}")
        print(f"Registros guardados: {len(lista_empleados)}")
        print("=" * 65)

    except Exception as error:
        print(f"\n Error al guardar el archivo: {error}")


# ------------------------------------------------------------------------------
# 6. CARGAR DATOS DE PRUEBA OFICIALES DE LA GUÍA
# ------------------------------------------------------------------------------

def cargar_datos_prueba_guia():
    """Carga los dos ejemplos oficiales que figuran en el ejercicio original."""
    # 1. Ana María Jaimes González (Administrativo)
    ejemplo_admin = {
        "nombre": "Ana María Jaimes González",
        "tipo": "ADMINISTRATIVO",
        "cargo": "Auxiliar Administrativo",
        "ht": 40,
        "salario": 800000,
        "he": 20,
        "tphe": 500000,
        "salud": 52000,
        "pension": 52000,
        "arl": 6786,
        "total_descuentos": 104000,
        "total_pagar": 1189214
    }

    # 2. Blanca Luz Iglesias Serpa (Operativo - Oficios Generales)
    ejemplo_operativo = {
        "nombre": "Blanca Luz Iglesias Serpa",
        "tipo": "OPERATIVO",
        "cargo": "Oficios Generales",
        "ht": 100,
        "salario": 4000000,
        "he": 0,
        "tphe": 0,
        "salud": 200000,
        "pension": 256000,
        "arl": 8352,
        "texto_arl": "ARL(0,522%)",
        "total_descuentos": 464352,
        "total_pagar": 3535648
    }

    lista_empleados.append(ejemplo_admin)
    lista_empleados.append(ejemplo_operativo)

    print("\n Se han cargado los 2 registros de prueba oficiales:")
    print("   1. Ana María Jaimes González (Administrativo)")
    print("   2. Blanca Luz Iglesias Serpa (Operativo)")
    print(" Puedes ver sus volantes con la opción 3 o exportarlos al TXT con la opción 4.")


# ------------------------------------------------------------------------------
# 7. MENÚ PRINCIPAL
# ------------------------------------------------------------------------------

def menu_principal():
    """Menú interactivo con opciones numéricas."""
    while True:
        print("\n" + "=" * 60)
        print("        SISTEMA DE NÓMINA TRANSCARIBECOL S.C.A.")
        print("=" * 60)
        print(" 1. Registrar Empleado Administrativo")
        print(" 2. Registrar Empleado Operativo (Prestación de Servicios)")
        print(" 3. Mostrar todos los Volantes en Pantalla")
        print(" 4. Guardar Nómina en Archivo TXT")
        print(" 5. Salir")
        print(" 6. Cargar datos de prueba de la guía (Prueba 1 y 2)")
        print("=" * 60)

        opcion = input("Seleccione una opción (1-6): ").strip()

        if opcion == "1":
            registrar_administrativo()
        elif opcion == "2":
            registrar_operativo()
        elif opcion == "3":
            mostrar_todos_los_volantes()
        elif opcion == "4":
            guardar_en_archivo_txt()
        elif opcion == "5":
            print("\n Gracias por utilizar el sistema de nómina de TransCaribeCol S.C.A. ¡Hasta pronto!\n")
            break
        elif opcion == "6":
            cargar_datos_prueba_guia()
        else:
            print("Opción no válida. Por favor digite un número del 1 al 6.")


# ------------------------------------------------------------------------------
# INICIO DE EJECUCIÓN
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    menu_principal()
