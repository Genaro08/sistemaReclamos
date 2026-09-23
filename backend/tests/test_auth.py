def testRegistrarUsuarioExitoso(clienteTest):
    """
    Prueba que el registro de un nuevo usuario funcione correctamente.
    """
    payload = {
        "nombre": "Genaro",
        "apellido": "García",
        "email": "genaro@ejemplo.com",
        "password": "PasswordSegura123!"
    }
    respuesta = clienteTest.post("/api/v1/auth/registro", json=payload)
    
    assert respuesta.status_code == 201
    datos = respuesta.json()
    assert datos["nombre"] == "Genaro"
    assert datos["apellido"] == "García"
    assert datos["email"] == "genaro@ejemplo.com"
    assert datos["rol"] == "USER"
    assert "passwordHash" not in datos


def testRegistrarEmailDuplicadoError(clienteTest):
    """
    Prueba que no se permita registrar dos usuarios con el mismo email.
    """
    payload = {
        "nombre": "Genaro",
        "apellido": "García",
        "email": "duplicado@ejemplo.com",
        "password": "PasswordSegura123!"
    }
    clienteTest.post("/api/v1/auth/registro", json=payload)
    
    # Segundo intento con el mismo email
    respuestaSegunda = clienteTest.post("/api/v1/auth/registro", json=payload)
    assert respuestaSegunda.status_code == 400
    datosError = respuestaSegunda.json()
    assert datosError["exito"] is False
    assert "correo electrónico" in datosError["error"]


def testLoginYObtenerPerfilMe(clienteTest):
    """
    Prueba el flujo completo: Registro -> Login -> Obtener Perfil con Token JWT.
    """
    # 1. Registrar
    payloadRegistro = {
        "nombre": "Usuario",
        "apellido": "Test",
        "email": "test@ejemplo.com",
        "password": "MiPasswordSuperSegura"
    }
    clienteTest.post("/api/v1/auth/registro", json=payloadRegistro)

    # 2. Login
    payloadLogin = {
        "email": "test@ejemplo.com",
        "password": "MiPasswordSuperSegura"
    }
    respuestaLogin = clienteTest.post("/api/v1/auth/login", json=payloadLogin)
    assert respuestaLogin.status_code == 200
    datosLogin = respuestaLogin.json()
    assert "tokenAcceso" in datosLogin
    token = datosLogin["tokenAcceso"]

    # 3. Consultar /me enviando el token Bearer
    encabezados = {"Authorization": f"Bearer {token}"}
    respuestaMe = clienteTest.get("/api/v1/auth/me", headers=encabezados)
    assert respuestaMe.status_code == 200
    datosMe = respuestaMe.json()
    assert datosMe["email"] == "test@ejemplo.com"
    assert datosMe["nombre"] == "Usuario"
    assert datosMe["apellido"] == "Test"
