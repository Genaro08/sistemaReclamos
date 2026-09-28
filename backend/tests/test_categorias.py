from app.models.usuarioModelo import RolUsuario, Usuario


def obtenerTokenAdmin(clienteTest, sesionDbTest):
    """Helper para registrar y elevar un usuario a rol ADMIN en los tests."""
    clienteTest.post(
        "/api/v1/auth/registro",
        json={
            "nombre": "Admin",
            "apellido": "Sistema",
            "email": "admin@ejemplo.com",
            "password": "AdminPassword123!"
        }
    )
    # Elevar a ADMIN en la BD de memoria RAM
    admin_usr = sesionDbTest.query(Usuario).filter(Usuario.email == "admin@ejemplo.com").first()
    admin_usr.rol = RolUsuario.ADMIN
    sesionDbTest.commit()

    res = clienteTest.post(
        "/api/v1/auth/login",
        json={"email": "admin@ejemplo.com", "password": "AdminPassword123!"}
    )
    return res.json()["tokenAcceso"]


def testCrearCategoriaComoUsuarioSinPermisosError(clienteTest):
    """
    Verifica que un usuario común (rol USER) no pueda crear categorías (403 Forbidden).
    """
    clienteTest.post(
        "/api/v1/auth/registro",
        json={
            "nombre": "Juan",
            "apellido": "Pérez",
            "email": "juan@ejemplo.com",
            "password": "Password123!"
        }
    )
    login_res = clienteTest.post(
        "/api/v1/auth/login",
        json={"email": "juan@ejemplo.com", "password": "Password123!"}
    )
    token = login_res.json()["tokenAcceso"]

    res = clienteTest.post(
        "/api/v1/categorias",
        headers={"Authorization": f"Bearer {token}"},
        json={"nombre": "Hardware", "descripcion": "Equipos físicos"}
    )
    assert res.status_code == 403


def testCrearListarYActualizarCategoriaExitoso(clienteTest, sesionDbTest):
    """
    Prueba el ciclo de vida completo de una categoría: Crear -> Listar -> Obtener -> Actualizar.
    """
    token_admin = obtenerTokenAdmin(clienteTest, sesionDbTest)
    headers = {"Authorization": f"Bearer {token_admin}"}

    # 1. Crear categoría
    crear_res = clienteTest.post(
        "/api/v1/categorias",
        headers=headers,
        json={"nombre": "Outlook", "descripcion": "Problemas de correo Outlook"}
    )
    assert crear_res.status_code == 201
    cat_data = crear_res.json()
    assert cat_data["nombre"] == "Outlook"
    assert cat_data["activa"] is True
    cat_id = cat_data["id"]

    # 2. Listar categorías
    listar_res = clienteTest.get("/api/v1/categorias")
    assert listar_res.status_code == 200
    assert len(listar_res.json()) == 1

    # 3. Obtener por ID
    obtener_res = clienteTest.get(f"/api/v1/categorias/{cat_id}")
    assert obtener_res.status_code == 200
    assert obtener_res.json()["nombre"] == "Outlook"

    # 4. Actualizar categoría
    act_res = clienteTest.put(
        f"/api/v1/categorias/{cat_id}",
        headers=headers,
        json={"nombre": "Correo Outlook", "descripcion": "Correo de escritorio y web"}
    )
    assert act_res.status_code == 200
    assert act_res.json()["nombre"] == "Correo Outlook"


def testCrearCategoriaDuplicadaError(clienteTest, sesionDbTest):
    """
    Verifica que no se permita registrar dos categorías con el mismo nombre (400 Bad Request).
    """
    token_admin = obtenerTokenAdmin(clienteTest, sesionDbTest)
    headers = {"Authorization": f"Bearer {token_admin}"}

    clienteTest.post(
        "/api/v1/categorias",
        headers=headers,
        json={"nombre": "Redes", "descripcion": "Conexiones y Wi-Fi"}
    )

    # Segundo intento con el mismo nombre
    res_segundo = clienteTest.post(
        "/api/v1/categorias",
        headers=headers,
        json={"nombre": "redes", "descripcion": "Intento duplicado"}
    )
    assert res_segundo.status_code == 400
    assert "Ya existe una categoría registrada" in res_segundo.json()["error"]
