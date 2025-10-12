
<h1 align="center"><b> Hotel Vista Dorada </b><img src="https://i.pinimg.com/originals/e2/ec/5e/e2ec5eca179a3b2e88918e3374465ea5.gif" width="75"></h1>
<!--  -->
<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Time+New+Roman&color=cyan&size=25&center=true&vCenter=true&width=600&height=100&lines=Facultad+de+Ingeniería...&hearts;++;TF:+Fundamentos+de+Programación+II;Presentado+por:+Begonia-Vela,;Alexis-Nolberto,;Ronaldo-Beltrán,;Luis-Uribe,;Ánimos+para+el+siguiente+ciclo...<3">
	<img width="13%" align="right" alt="Github" src="https://upload.wikimedia.org/wikipedia/commons/f/fc/UPC_logo_transparente.png" />
	
</p>


<br>

	
## **🏨 Sistema de Gestión Hotelera**

<br>

El Hotel Vista Dorada implementó un programa que le permita **gestionar sus habitaciones, reservas y consumos durante la estadía de los huéspedes**.



## 🏠 Descripción general del sistema

El sistema administra **45 habitaciones**, clasificadas en tres categorías, cada una con su respectivo precio base:

| Categoría     | Precio por noche |
|----------------|------------------|
| Estándar       | S/ 80            |
| Matrimonial    | S/ 100           |
| Suite          | S/ 120           |

Durante la estancia, los huéspedes pueden registrar **consumos adicionales** asociados a su habitación, los cuales se consolidan al momento del **check-out**.  
Existen **dos tipos de consumos adicionales**:

- **Room Service:** consumo fijo de S/ 50.  
- **Minibar:** consumo variable según producto seleccionado.  

| Producto | Precio |
|-----------|--------|
| Agua      | S/ 4   |
| Gaseosa   | S/ 6   |
| Vino      | S/ 30  |
| Cifrut    | S/ 3   |

El sistema permite calcular el **monto total a pagar** por habitación, sumando el costo del alojamiento y los consumos adicionales registrados durante la estadía.



## ⚙️ Flujo de procesos

### 1. Reserva
El huésped puede realizar su reserva mediante llamada, WhatsApp, correo electrónico o presencialmente.  
El recepcionista o cajero valida la disponibilidad en tiempo real. Si hay habitaciones libres, se genera la reserva, se procesa el cobro inicial y se envía la confirmación al correo electrónico del cliente.  
En caso de no haber disponibilidad, el sistema propone automáticamente **fechas y habitaciones alternativas**, garantizando la integridad de datos y evitando sobreventa.

### 2. Check-in
Al llegar al hotel, el recepcionista consulta la reserva mediante DNI o código de confirmación.  
Con un clic, el sistema registra el check-in, marca la habitación como **ocupada** y notifica al área de housekeeping.

### 3. Durante la estadía
Los consumos de minibar y room service son registrados por el personal correspondiente, quedando automáticamente **asociados al huésped y a su habitación**.  
Esto evita errores manuales o pérdidas de información.

### 4. Check-out
El sistema envía una alerta 20 minutos antes de la hora oficial de salida.  
Si el huésped cumple con el horario, se genera la **precuenta consolidada** (hospedaje + consumos).  
Si se retrasa, el sistema aplica automáticamente un **cargo fijo equivalente a 4 horas adicionales**.  
Tras la verificación de housekeeping, se emite la **factura electrónica** y la habitación se marca como **disponible**.

### 5. Reportería administrativa
El sistema permite a la recepción generar **reportes diarios** de ocupación e ingresos en segundos, reemplazando conciliaciones manuales y reduciendo tiempos de gestión.



## ⚖️ Reglas y exclusiones del sistema

- No puede existir un **consumo** que no esté asociado a una **habitación específica**.  
- Una **habitación** puede existir sin consumos registrados, pero no sin **categoría asignada**.  
- Una **reserva** solo puede crearse si existe disponibilidad real de la habitación.  
- Una **habitación** debe eliminarse solo si el hotel (administrador del sistema) también es eliminado.  
- Si el usuario ingresa una opción inexistente en los menús del sistema (p. ej. menú de recepción, caja o reportes), se debe lanzar una **excepción personalizada** con el mensaje:
    
  ```python
  "Opción inválida. Por favor seleccione una opción del menú."

<br>

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"><br><br>

## <img src="https://media2.giphy.com/media/QssGEmpkyEOhBCb7e1/giphy.gif?cid=ecf05e47a0n3gi1bfqntqmob8g9aid1oyj2wr3ds3mg700bl&rid=giphy.gif" width ="25"><b> Skills</b>
<br>

<p align="center">

- **Languages**:
    
    ![Python](https://img.shields.io/badge/Python%20-%2314354C.svg?style=for-the-badge&logo=python&logoColor=white)

<br>   
    
- **Softwares and Tools**:

    ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
    ![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)

<br>

- **Extras**:

    ![Bizagi](https://img.shields.io/badge/Bizagi-%23FFA500?style=for-the-badge&logo=gnu-bash&logoColor=white)
    ![Markdown](https://img.shields.io/badge/markdown-%23000000.svg?style=for-the-badge&logo=markdown&logoColor=white)   


</p>

<br>
<br>
