from app.models.usuarioModelo import RolUsuario, Usuario


def obtenerTokenUsuario(clienteTest, sesionDbTest, email="usuario@ejemplo.com"):
    """Helper para registrar y loguear un usuario común (USER)."""
    clienteTest.post(
        "/api/v1/auth/registro",
        json={
            "nombre": "Usuario",
            "apellido": "Prueba",
            "email": email,
            "password": "UserPassword123!"
        }
    )
    res = clienteTest.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "UserPassword123!"}
    )
    return res.json()["tokenAcceso"]


def obtenerTokenOperador(clienteTest, sesionDbTest, email="tecnico@ejemplo.com"):
    """Helper para registrar y elevar un usuario a rol OPERATOR."""
    clienteTest.post(
        "/api/v1/auth/registro",
        json={
            "nombre": "Tecnico",
            "apellido": "Soporte",
            "email": email,
            "password": "TecnicoPassword123!"
        }
    )
    usr = sesionDbTest.query(Usuario).filter(Usuario.email == email).first()
    usr.rol = RolUsuario.OPERATOR
    sesionDbTest.commit()

    res = clienteTest.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "TecnicoPassword123!"}
    )
    return res.json()["tokenAcceso"]


def crearCategoriaYArticuloBase(clienteTest, sesionDbTest):
    """Helper para preparar categoría y artículo en la BD de pruebas."""
    token_op = obtenerTokenOperador(clienteTest, sesionDbTest)
    headers = {"Authorization": f"Bearer {token_op}"}

    # Crear Categoría
    cat_res = clienteTest.post(
        "/api/v1/categorias",
        headers=headers,
        json={"nombre": "Conectividad VPN", "descripcion": "Problemas de red remota"}
    ).json()
    cat_id = cat_res["id"]

    # Crear Artículo de Conocimiento
    art_res = clienteTest.post(
        "/api/v1/articulos",
        headers=headers,
        json={
            "titulo": "Solución a caídas de VPN FortiClient",
            "contenidoTecnico": "Reiniciar servicio FortiShield",
            "etiquetas": "vpn, forticlient, desconexion, red",
            "categoriaId": cat_id
        }
    ).json()
    art_id = art_res["id"]

    return cat_id, art_id, token_op


def testCrearReclamoYCalcularCoincidencia(clienteTest, sesionDbTest):
    """
    Verifica que un usuario común cree un reclamo y el backend calcule el % de coincidencia automática.
    """
    cat_id, _, _ = crearCategoriaYArticuloBase(clienteTest, sesionDbTest)
    token_user = obtenerTokenUsuario(clienteTest, sesionDbTest, email="juan@ejemplo.com")
    headers = {"Authorization": f"Bearer {token_user}"}

    payload = {
        "titulo": "Desconexión constante en VPN FortiClient",
        "descripcion": "Tengo problemas de red al conectarme desde mi casa por VPN.",
        "prioridad": "HIGH",
        "categoriaId": cat_id
    }

    res = clienteTest.post("/api/v1/reclamos", headers=headers, json=payload)
    assert res.status_code == 201
    datos = res.json()
    assert datos["titulo"] == "Desconexión constante en VPN FortiClient"
    assert datos["estado"] == "PENDING"
    assert datos["prioridad"] == "HIGH"
    assert datos["porcentajeCoincidenciaAuto"] is not None
    assert datos["porcentajeCoincidenciaAuto"] > 0


def testFiltroSeguridadReclamosPorUsuario(clienteTest, sesionDbTest):
    """
    Verifica que un usuario final (USER) solo pueda ver sus propios reclamos,
    mientras que un operador puede listar todos.
    """
    cat_id, _, token_op = crearCategoriaYArticuloBase(clienteTest, sesionDbTest)

    # User 1 crea ticket
    token_u1 = obtenerTokenUsuario(clienteTest, sesionDbTest, email="u1@ejemplo.com")
    clienteTest.post(
        "/api/v1/reclamos",
        headers={"Authorization": f"Bearer {token_u1}"},
        json={"titulo": "Ticket User 1", "descripcion": "Detalle 1", "categoriaId": cat_id}
    )

    # User 2 crea ticket
    token_u2 = obtenerTokenUsuario(clienteTest, sesionDbTest, email="u2@ejemplo.com")
    clienteTest.post(
        "/api/v1/reclamos",
        headers={"Authorization": f"Bearer {token_u2}"},
        json={"titulo": "Ticket User 2", "descripcion": "Detalle 2", "categoriaId": cat_id}
    )

    # User 1 lista -> debe ver solo 1 ticket
    res_u1 = clienteTest.get("/api/v1/reclamos", headers={"Authorization": f"Bearer {token_u1}"})
    assert res_u1.status_code == 200
    assert len(res_u1.json()) == 1
    assert res_u1.json()[0]["titulo"] == "Ticket User 1"

    # Operador lista -> debe ver ambos (2 tickets)
    res_op = clienteTest.get("/api/v1/reclamos", headers={"Authorization": f"Bearer {token_op}"})
    assert res_op.status_code == 200
    assert len(res_op.json()) == 2


def testAsignarTecnicoYCambiarEstado(clienteTest, sesionDbTest):
    """
    Verifica el flujo de asignación de técnico y transición de estados PENDING -> IN_PROGRESS -> RESOLVED.
    """
    cat_id, art_id, token_op = crearCategoriaYArticuloBase(clienteTest, sesionDbTest)
    headers_op = {"Authorization": f"Bearer {token_op}"}

    token_user = obtenerTokenUsuario(clienteTest, sesionDbTest, email="cliente@ejemplo.com")
    rec_res = clienteTest.post(
        "/api/v1/reclamos",
        headers={"Authorization": f"Bearer {token_user}"},
        json={"titulo": "Fallo pantalla azul", "descripcion": "BSOD al encender", "categoriaId": cat_id}
    ).json()
    rec_id = rec_res["id"]

    # Obtener ID del operador
    op_usr = sesionDbTest.query(Usuario).filter(Usuario.email == "tecnico@ejemplo.com").first()

    # 1. Asignar técnico
    asig_res = clienteTest.put(
        f"/api/v1/reclamos/{rec_id}/asignar",
        headers=headers_op,
        json={"responsableId": op_usr.id}
    )
    assert asig_res.status_code == 200
    assert asig_res.json()["responsableId"] == op_usr.id
    assert asig_res.json()["estado"] == "IN_PROGRESS"

    # 2. Cambiar estado a RESOLVED vinculando el artículo de conocimiento
    est_res = clienteTest.put(
        f"/api/v1/reclamos/{rec_id}/estado",
        headers=headers_op,
        json={
            "estado": "RESOLVED",
            "articuloAplicadoId": art_id
        }
    )
    assert est_res.status_code == 200
    assert est_res.json()["estado"] == "RESOLVED"
    assert est_res.json()["articuloAplicadoId"] == art_id
    assert est_res.json()["fechaResolucion"] is not None


def testComentariosPublicosYNotasPrivadas(clienteTest, sesionDbTest):
    """
    Verifica que las notas internas (esInternoTecnico=True) estén ocultas para los usuarios finales.
    """
    cat_id, _, token_op = crearCategoriaYArticuloBase(clienteTest, sesionDbTest)
    token_user = obtenerTokenUsuario(clienteTest, sesionDbTest, email="user_comm@ejemplo.com")

    # Crear reclamo
    rec = clienteTest.post(
        "/api/v1/reclamos",
        headers={"Authorization": f"Bearer {token_user}"},
        json={"titulo": "Consulta de Software", "descripcion": "Necesito licencia de Photoshop", "categoriaId": cat_id}
    ).json()
    rec_id = rec["id"]

    # Usuario agrega comentario público
    clienteTest.post(
        f"/api/v1/reclamos/{rec_id}/comentarios",
        headers={"Authorization": f"Bearer {token_user}"},
        json={"contenido": "¿Cuándo me entregan la licencia?", "esInternoTecnico": False}
    )

    # Operador agrega nota interna privada
    clienteTest.post(
        f"/api/v1/reclamos/{rec_id}/comentarios",
        headers={"Authorization": f"Bearer {token_op}"},
        json={"contenido": "Pendiente de aprobación de presupuesto por compras", "esInternoTecnico": True}
    )

    # Usuario lista comentarios -> solo ve 1 (el público)
    comm_u = clienteTest.get(
        f"/api/v1/reclamos/{rec_id}/comentarios",
        headers={"Authorization": f"Bearer {token_user}"}
    ).json()
    assert len(comm_u) == 1
    assert comm_u[0]["contenido"] == "¿Cuándo me entregan la licencia?"

    # Operador lista comentarios -> ve los 2 (público e interno)
    comm_op = clienteTest.get(
        f"/api/v1/reclamos/{rec_id}/comentarios",
        headers={"Authorization": f"Bearer {token_op}"}
    ).json()
    assert len(comm_op) == 2


def testConsultarHistorialAuditoria(clienteTest, sesionDbTest):
    """
    Verifica la generación del registro cronológico de auditoría (HistorialReclamo).
    """
    cat_id, _, token_op = crearCategoriaYArticuloBase(clienteTest, sesionDbTest)
    token_user = obtenerTokenUsuario(clienteTest, sesionDbTest, email="user_hist@ejemplo.com")

    rec = clienteTest.post(
        "/api/v1/reclamos",
        headers={"Authorization": f"Bearer {token_user}"},
        json={"titulo": "Impresora atascada", "descripcion": "Papel trabado en bandeja 2", "categoriaId": cat_id}
    ).json()

    hist_res = clienteTest.get(
        f"/api/v1/reclamos/{rec['id']}/historial",
        headers={"Authorization": f"Bearer {token_user}"}
    )
    assert hist_res.status_code == 200
    historial = hist_res.json()
    assert len(historial) >= 1
    assert "Creación del ticket" in historial[0]["accion"]
