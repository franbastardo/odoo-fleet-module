# Extensión de Flota Odoo y API Node.js

El proyecto consiste en dos componentes principales: un módulo personalizado que extiende la funcionalidad de Flota en Odoo 16 y una API en Node.js para recibir datos de dicho módulo.

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

*   **Odoo Versión 16.0**
*   **Node.js** (v18.x o superior recomendada)
*   **npm** (generalmente se instala con Node.js)

---

## 1. 🚚 Módulo de Odoo: Extensión de Flota (`odoo_fleet_module_extend`)

Este módulo no reemplaza el módulo `fleet` nativo de Odoo 16, sino que lo **extiende** para añadir las funcionalidades clave requeridas en la prueba técnica.

### ✨ Características Principales

*   **Secuencia Automática:** Creación de un código único y secuencial (`VEH/00001`) para cada nuevo vehículo.
*   **Campos Obligatorios:** Sea sobreescriben campos del modulo de flota para que sean requeridos.
*   **Campos Personalizados:** Se añade un campo de imagen (`Foto del Vehículo`) y se hace obligatorio el campo `Conductor` y `Placa`.
*   **Integración con Contactos:**
    *   Un *smart button* en el formulario de contacto muestra el número de vehículos asociados.
    *   Un botón de acción en la cabecera del contacto para enviar los datos de sus vehículos a una API externa.
*   **Módulo de Logs:** Un nuevo menú dentro de la aplicación de Flota para visualizar los logs de respuesta de la API (solo lectura).
*   **Seguridad Avanzada:**
    *   Creación de grupos de seguridad personalizados ("Administrador de Flota", que hereda los grupos anteriores).
    *   El acceso a menús y la acción de envío a la API están restringidos al grupo de "Administrador de Flota".
*   **Configuración Centralizada:** La URL de la API y la API Key se gestionan desde los Parámetros del Sistema en Odoo para mayor seguridad y flexibilidad (cuenta con un valor por defecto para su uso inmediato, sin embargo se recomienda cambiarlo apenas se instale el módulo).

### ⚙️ Instalación y Configuración

Sigue estos pasos para integrar el módulo en tu instancia de Odoo.

#### Paso 1: Añadir el Módulo a tus Addons

Clona este repositorio y coloca la carpeta `odoo_fleet_module_extend` dentro de tu directorio de `addons` personalizados.

#### Paso 2: Actualizar la Configuración de Odoo

Odoo necesita saber dónde buscar tus módulos personalizados. Para ello, debes añadir la ruta a tu carpeta de addons en el archivo de configuración `odoo.conf`.

Abre tu archivo `odoo.conf` y modifica la línea `addons_path`:

```ini
; Ejemplo de cómo debería quedar la línea
addons_path = /ruta/a/addons/nativos,/ruta/a/tus/addons/personalizados
```

#### Paso 3: Reiniciar e Instalar

1.  **Reinicia el servicio de Odoo** para que reconozca la nueva configuración y el nuevo módulo.
2.  Inicia sesión en tu instancia de Odoo con una cuenta de administrador.
3.  Activa el **Modo Desarrollador** (`Ajustes` > `Activar el modo desarrollador`).
4.  Ve al menú `Apps`.
5.  Haz clic en **"Actualizar Lista de Apps"**.
6.  Busca el módulo `Extensión de Flota Personalizada` (o `odoo_fleet_module_extend`).
7.  Haz clic en el botón **Instalar**.

---

## 2. 🚀 API en Node.js: Receptor de Datos (`api-fleet`)

Este componente es una API simple construida con **Node.js, Express y TypeScript** siguiendo una arquitectura de Puertos y Adaptadores.

### ✨ Funcionalidades

*   Actúa como un endpoint `POST /api/vehicles` para recibir datos desde Odoo.
*   **Seguridad:** Valida una `x-api-key` secreta en la cabecera de la petición para asegurar que solo Odoo pueda enviarle datos.
*   **Procesamiento:**
    *   Recibe un array de vehículos en formato JSON a través de la key data del body.
    *   Imprime los datos de cada vehículo recibido en la consola para fines de depuración.
    *   Devuelve una respuesta de éxito (código 200) o error a Odoo, la cual será registrada en el módulo de logs.

### ⚙️ Instalación y Ejecución

Sigue estos pasos para poner en marcha la API en tu entorno local.

#### Paso 1: Navegar e Instalar Dependencias

```bash
# Muévete a la carpeta de la API
cd api-fleet

# Instala todas las dependencias necesarias definidas en package.json
npm install
```

#### Paso 2: Configurar las Variables de Entorno

Crea un archivo llamado `.env` en la raíz del directorio `api-fleet`. Este archivo contendrá las configuraciones locales.

Copia y pega el siguiente contenido en tu archivo `.env`:

```env
# Puerto en el que se ejecutará la API
PORT=3000

# Clave secreta para la autenticación. DEBE COINCIDIR con la configurada en Odoo.
ODOO_API_KEY=clave-secreta
```

#### Paso 3: Ejecutar la API

Puedes ejecutar la API en dos modos:

*   **Modo Desarrollo (Recomendado para pruebas):**
    ```bash
    npm run dev
    ```
    Este comando usa `nodemon` para vigilar los cambios en los archivos y reiniciar automáticamente el servidor, agilizando el desarrollo.

*   **Modo Producción:**
    ```bash
    # Primero, compila el código TypeScript a JavaScript
    npm run build

    # Luego, inicia el servidor desde los archivos compilados en la carpeta /dist
    npm start
    ```

Una vez iniciada, verás un mensaje en la consola indicando que el servidor está escuchando en `http://localhost:3000`.

---

## 🔗 Conectando Odoo con la API

Para que la comunicación funcione, asegúrate de que:

1.  La **API de Node.js esté en ejecución**.
2.  En Odoo, ve a `Ajustes > Técnico > Parámetros > Parámetros del Sistema`.
3.  Configura los siguientes parámetros:
    *   `custom_fleet.api_endpoint`: El valor debe ser `http://localhost:3000/api/vehicles`.
    *   `custom_fleet.api_key`: El valor debe ser **exactamente el mismo** que pusiste en el archivo `.env` de la API (`clave-secreta`).