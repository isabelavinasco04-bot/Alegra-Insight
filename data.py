# ==========================================
# DATOS DEL RETO ALEGRA
# ==========================================

REVIEWS = [
    {
        "id": 1,
        "tipo": "Reseña",
        "pais": "México",
        "calificacion": 2,
        "comentario": "No me deja emitir la factura, dice error de RFC del receptor pero el RFC está bien. Perdí un cliente hoy.",
        "estado": "Sin analizar",
        "urgencia": "Alta"
    },
    {
        "id": 2,
        "tipo": "Reseña",
        "pais": "Colombia",
        "calificacion": 1,
        "comentario": "Desde la última actualización la app se cierra sola cuando abro Reportes.",
        "estado": "Sin analizar",
        "urgencia": "Alta"
    },
    {
        "id": 3,
        "tipo": "Reseña",
        "pais": "México",
        "calificacion": 3,
        "comentario": "Necesito subir mi e.firma desde el celular. Ahorita solo puedo desde la computadora.",
        "estado": "Sin analizar",
        "urgencia": "Media"
    },
    {
        "id": 4,
        "tipo": "Reseña",
        "pais": "Rep. Dominicana",
        "calificacion": 1,
        "comentario": "Tardé 10 minutos en cargar el reporte de ventas y no sabía si seguía cargando o se trabó.",
        "estado": "Sin analizar",
        "urgencia": "Media"
    },
    {
        "id": 5,
        "tipo": "Reseña",
        "pais": "España",
        "calificacion": 2,
        "comentario": "No encuentro cómo agregar un descuento por línea en la factura. En la web sí se puede.",
        "estado": "Sin analizar",
        "urgencia": "Media"
    },
    {
        "id": 6,
        "tipo": "Reseña",
        "pais": "México",
        "calificacion": 1,
        "comentario": "No puedo mandar la factura por WhatsApp, solo por correo, y mis clientes no leen el correo.",
        "estado": "Sin analizar",
        "urgencia": "Alta"
    },
    {
        "id": 7,
        "tipo": "Reseña",
        "pais": "Colombia",
        "calificacion": 2,
        "comentario": "Al tomar foto de un recibo de compra pide permisos y luego se queda la pantalla en blanco.",
        "estado": "Sin analizar",
        "urgencia": "Media"
    },
    {
        "id": 8,
        "tipo": "Reseña",
        "pais": "México",
        "calificacion": 4,
        "comentario": "Está buena, pero me gustaría ver en qué va mi reporte sin quedarme esperando en la pantalla.",
        "estado": "Sin analizar",
        "urgencia": "Baja"
    },
    {
        "id": 9,
        "tipo": "Reseña",
        "pais": "Colombia",
        "calificacion": 1,
        "comentario": "Actualicé y ya no me abre. Pantalla blanca.",
        "estado": "Sin analizar",
        "urgencia": "Alta"
    },
    {
        "id": 10,
        "tipo": "Reseña",
        "pais": "Rep. Dominicana",
        "calificacion": 2,
        "comentario": "No puedo imprimir la factura desde el celular en mi impresora térmica.",
        "estado": "Sin analizar",
        "urgencia": "Media"
    },
    {
        "id": 11,
        "tipo": "Reseña",
        "pais": "México",
        "calificacion": 2,
        "comentario": "Los botones son muy chiquitos, me equivoco al seleccionar el cliente.",
        "estado": "Sin analizar",
        "urgencia": "Baja"
    },
    {
        "id": 12,
        "tipo": "Reseña",
        "pais": "México",
        "calificacion": 1,
        "comentario": "Emití una factura y no sé si ya llegó al SAT, no me dice nada. Prefiero volver a la web.",
        "estado": "Sin analizar",
        "urgencia": "Alta"
    },
    {
        "id": 13,
        "tipo": "Reseña",
        "pais": "Colombia",
        "calificacion": 3,
        "comentario": "Muy lenta la lista de clientes cuando tengo más de 500.",
        "estado": "Sin analizar",
        "urgencia": "Media"
    },
    {
        "id": 14,
        "tipo": "Reseña",
        "pais": "España",
        "calificacion": 2,
        "comentario": "Mi contador no puede entrar a mi cuenta desde la app. ¿Cómo le doy acceso?",
        "estado": "Sin analizar",
        "urgencia": "Media"
    },
    {
        "id": 15,
        "tipo": "Reseña",
        "pais": "Rep. Dominicana",
        "calificacion": 1,
        "comentario": "Se cierra al guardar una cotización con más de 10 ítems.",
        "estado": "Sin analizar",
        "urgencia": "Alta"
    },
    {
        "id": 16,
        "tipo": "Reseña",
        "pais": "Colombia",
        "calificacion": 5,
        "comentario": "Excelente para cobrar en la calle. Ojalá agreguen registrar pagos recibidos.",
        "estado": "Sin analizar",
        "urgencia": "Baja"
    }
]


TICKETS = [
    {
        "id": 17,
        "tipo": "Ticket",
        "pais": "México",
        "comentario": "Cliente de México dice que no le deja emitir facturas desde el celular, le sale un error. Ya le pasó 3 veces. Es urgente porque tiene que facturar hoy. Android creo. Le dije que reinstalara y sigue igual.",
        "estado": "Sin analizar",
        "urgencia": "Alta"
    }
]


# Todos los elementos del buzón
ALL_FEEDBACK = REVIEWS + TICKETS


# ==========================================
# MIEMBROS DEL EQUIPO
# ==========================================

TEAM_MEMBERS = [
    {
        "id": 1,
        "nombre": "Juan",
        "rol": "Desarrollador",
        "estado": "Disponible"
    },
    {
        "id": 2,
        "nombre": "Carlos",
        "rol": "Desarrollador",
        "estado": "Ocupado"
    },
    {
        "id": 3,
        "nombre": "Sara",
        "rol": "Diseñadora",
        "estado": "Disponible"
    }
]
