from app.models.usuarioModelo import RolUsuario, Usuario


def obtenerTokenOperador(clienteTest, sesionDbTest):
    """Helper para registrar y elevar un usuario a rol OPERATOR en los tests."""
    clienteTest.post(
        "/api/v1/auth/registro",
        json={
            "nombre": "Tecnico",
            "apellido": "Soporte",
            "email": "tecnico@ejemplo.com",
            "password": "TecnicoPassword123!"
        }
    )
    usr = sesionDbTest.query(Usuario).filter(Usuario.email == "tecnico@ejemplo.com").first()
    usr.rol = RolUsuario.OPERATOR
    sesionDbTest.commit()

    res = clienteTest.post(
        "/api/v1/auth/login",
        json={"email": "tecnico@ejemplo.com", "password": "TecnicoPassword123!"}
    )
    return res.json()["tokenAcceso"]


def crearCategoriaPrueba(clienteTest, sesionDbTest):
    """Helper para crear una categoría base para asociar artículos."""
    token = obtenerTokenOperador(clienteTest, sesionDbTest)
    res = clienteTest.post(
        "/api/v1/categorias",
        headers={"Authorization": f"Bearer {token}"},
        json={"nombre": "Correo Electrónico", "descripcion": "Problemas de correo web y cliente de escritorio"}
    )
    return res.json()["id"], token


def testCrearArticuloComoOperadorExito(clienteTest, sesionDbTest):
    """
    Verifica que un operador técnico pueda redactar un artículo de conocimiento asociado a una categoría.
    """
    categoria_id, token_operador = crearCategoriaPrueba(clienteTest, sesionDbTest)
    headers = {"Authorization": f"Bearer {token_operador}"}

    payload = {
        "titulo": "Configuración PST Outlook",
        "resumen": "Guía paso a paso para reparar archivos PST dañados.",
        "contenidoTecnico": "<p>Paso 1: Abrir SCANPST.exe...</p>",
        "etiquetas": "outlook, pst, correo, reparar",
        "categoriaId": categoria_id
    }

    res = clienteTest.post("/api/v1/articulos", headers=headers, json=payload)
    assert res.status_code == 201
    datos = res.json()
    assert datos["titulo"] == "Configuración PST Outlook"
    assert datos["categoriaId"] == categoria_id
    assert datos["vecesUtilizado"] == 0
    assert datos["categoria"]["nombre"] == "Correo Electrónico"


def testCrearArticuloCategoriaInexistenteError(clienteTest, sesionDbTest):
    """
    Verifica que lanzar un articulo con una categoriaId inexistente devuelva 400 Bad Request.
    """
    token_operador = obtenerTokenOperador(clienteTest, sesionDbTest)
    headers = {"Authorization": f"Bearer {token_operador}"}

    payload = {
        "titulo": "Error en VPN",
        "resumen": "Fallo de conexion en FortiClient.",
        "contenidoTecnico": "Reiniciar servicio de FortiGuard",
        "etiquetas": "vpn, fortinet",
        "categoriaId": 9999
    }

    res = clienteTest.post("/api/v1/articulos", headers=headers, json=payload)
    assert res.status_code == 400
    assert "no existe o está inactiva" in res.json()["error"]


def testCrearArticuloUsuarioComunProhibido(clienteTest, sesionDbTest):
    """
    Verifica que un usuario final (USER) no tenga permisos para redactar artículos (403 Forbidden).
    """
    categoria_id, _ = crearCategoriaPrueba(clienteTest, sesionDbTest)

    # Registrar usuario comun
    clienteTest.post(
        "/api/v1/auth/registro",
        json={
            "nombre": "Pedro",
            "apellido": "Usuario",
            "email": "pedro@ejemplo.com",
            "password": "Password123!"
        }
    )
    login_res = clienteTest.post(
        "/api/v1/auth/login",
        json={"email": "pedro@ejemplo.com", "password": "Password123!"}
    )
    token_user = login_res.json()["tokenAcceso"]

    res = clienteTest.post(
        "/api/v1/articulos",
        headers={"Authorization": f"Bearer {token_user}"},
        json={
            "titulo": "Intento de Articulo",
            "contenidoTecnico": "Contenido prueba",
            "etiquetas": "test",
            "categoriaId": categoria_id
        }
    )
    assert res.status_code == 403


def testBuscarArticulosPorCoincidencia(clienteTest, sesionDbTest):
    """
    Verifica que el motor de búsqueda compare las palabras ingresadas contra el título/etiquetas
    y calcule el porcentaje de coincidencia correctamente.
    """
    categoria_id, token_operador = crearCategoriaPrueba(clienteTest, sesionDbTest)
    headers = {"Authorization": f"Bearer {token_operador}"}

    # Crear articulo 1
    clienteTest.post(
        "/api/v1/articulos",
        headers=headers,
        json={
            "titulo": "Problemas de envio de correo en Outlook escritorio",
            "resumen": "Resolucion de errores SMTP al enviar mails.",
            "contenidoTecnico": "Verificar puerto 587 y TLS...",
            "etiquetas": "outlook, correo, smtp, envio",
            "categoriaId": categoria_id
        }
    )

    # Crear articulo 2
    clienteTest.post(
        "/api/v1/articulos",
        headers=headers,
        json={
            "titulo": "Impresora desconectada en red local",
            "resumen": "Reiniciar spooler de impresion.",
            "contenidoTecnico": "net stop spooler...",
            "etiquetas": "impresora, red, spooler",
            "categoriaId": categoria_id
        }
    )

    # Buscar "correo outlook envio"
    res_busqueda = clienteTest.get("/api/v1/articulos/buscar?q=correo+outlook+envio")
    assert res_busqueda.status_code == 200
    resultados = res_busqueda.json()

    assert len(resultados) == 1
    assert resultados[0]["titulo"] == "Problemas de envio de correo en Outlook escritorio"
    assert resultados[0]["porcentajeCoincidencia"] == 100.0


def testCrearYListarPlantillasRespuesta(clienteTest, sesionDbTest):
    """
    Verifica la vinculación y consulta de plantillas de respuesta pública para los usuarios finales.
    """
    categoria_id, token_operador = crearCategoriaPrueba(clienteTest, sesionDbTest)
    headers = {"Authorization": f"Bearer {token_operador}"}

    # Crear articulo
    art_res = clienteTest.post(
        "/api/v1/articulos",
        headers=headers,
        json={
            "titulo": "Reset de Contraseña de Dominio",
            "contenidoTecnico": "Ejecutar comando net user en AD",
            "etiquetas": "password, reset, active directory",
            "categoriaId": categoria_id
        }
    )
    art_id = art_res.json()["id"]

    # Agregar plantilla al articulo
    plantilla_res = clienteTest.post(
        f"/api/v1/articulos/{art_id}/plantillas",
        headers=headers,
        json={
            "titulo": "Respuesta Estándar Reset OK",
            "contenidoUsuario": "Estimado usuario, su contraseña ha sido blanqueada a 'Temporal123'."
        }
    )
    assert plantilla_res.status_code == 201
    assert plantilla_res.json()["articuloId"] == art_id

    # Listar plantillas del articulo
    listar_res = clienteTest.get(f"/api/v1/articulos/{art_id}/plantillas")
    assert listar_res.status_code == 200
    assert len(listar_res.json()) == 1
    assert listar_res.json()[0]["titulo"] == "Respuesta Estándar Reset OK"


def testVincularArticulosRelacionados(clienteTest, sesionDbTest):
    """
    Verifica que un artículo pueda estar vinculado con otros artículos de conocimiento (M:N).
    """
    categoria_id, token_operador = crearCategoriaPrueba(clienteTest, sesionDbTest)
    headers = {"Authorization": f"Bearer {token_operador}"}

    # Articulo 1
    art1 = clienteTest.post(
        "/api/v1/articulos",
        headers=headers,
        json={
            "titulo": "Fallo en Fibra Óptica",
            "contenidoTecnico": "Comprobar luz en ONT",
            "etiquetas": "fibra, ont, red",
            "categoriaId": categoria_id
        }
    ).json()

    # Articulo 2 vinculando el Articulo 1
    art2 = clienteTest.post(
        "/api/v1/articulos",
        headers=headers,
        json={
            "titulo": "Sin acceso a Internet en la oficina",
            "contenidoTecnico": "Revisar Router Principal y ONT",
            "etiquetas": "internet, wifi, ont",
            "categoriaId": categoria_id,
            "articulosRelacionadosIds": [art1["id"]]
        }
    ).json()

    assert len(art2["articulosRelacionados"]) == 1
    assert art2["articulosRelacionados"][0]["id"] == art1["id"]
    assert art2["articulosRelacionados"][0]["titulo"] == "Fallo en Fibra Óptica"
