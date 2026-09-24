from fastapi import status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.email import enviarEmailRecuperacionPassword
from app.core.excepciones import ExcepcionDominio
from app.core.seguridad import (
    crearRefreshToken,
    crearTokenAcceso,
    crearTokenRecuperacion,
    generarPasswordHash,
    verificarPassword,
    verificarTokenRecuperacion,
)
from app.models.usuario import Usuario
from app.schemas.usuarioSchema import LoginEsquema, TokenRespuesta, UsuarioCrear, UsuarioRespuesta


class AuthService:
    """
    Servicio de Lógica de Negocio para la gestión de registro, login, tokens y recuperación de contraseña.
    """
    def __init__(self, sesionDb: Session):
        self.sesionDb = sesionDb

    def registrarUsuario(self, datos: UsuarioCrear) -> UsuarioRespuesta:
        """
        Valida que el correo no esté registrado y crea un nuevo usuario con clave encriptada.
        """
        consulta = select(Usuario).where(Usuario.email == datos.email.lower().strip())
        usuarioExistente = self.sesionDb.execute(consulta).scalar_one_or_none()

        if usuarioExistente:
            raise ExcepcionDominio(
                mensaje="Ya existe un usuario registrado con este correo electrónico",
                codigoEstado=status.HTTP_400_BAD_REQUEST
            )

        passwordHash = generarPasswordHash(datos.password)
        nuevoUsuario = Usuario(
            nombre=datos.nombre.strip(),
            apellido=datos.apellido.strip(),
            email=datos.email.lower().strip(),
            passwordHash=passwordHash
        )
        self.sesionDb.add(nuevoUsuario)
        self.sesionDb.commit()
        self.sesionDb.refresh(nuevoUsuario)

        return UsuarioRespuesta.model_validate(nuevoUsuario)

    def autenticarUsuario(self, datos: LoginEsquema) -> TokenRespuesta:
        """
        Verifica el email y contraseña del usuario y genera tokens JWT (Access & Refresh).
        """
        consulta = select(Usuario).where(Usuario.email == datos.email.lower().strip())
        usuario = self.sesionDb.execute(consulta).scalar_one_or_none()

        if not usuario or not verificarPassword(datos.password, usuario.passwordHash):
            raise ExcepcionDominio(
                mensaje="Credenciales de acceso incorrectas",
                codigoEstado=status.HTTP_401_UNAUTHORIZED
            )

        if not usuario.activo:
            raise ExcepcionDominio(
                mensaje="El usuario se encuentra inactivo",
                codigoEstado=status.HTTP_403_FORBIDDEN
            )

        payload = {
            "sub": usuario.email,
            "id": usuario.id,
            "rol": usuario.rol.value
        }
        tokenAcceso = crearTokenAcceso(datosPayload=payload)
        refreshToken = crearRefreshToken(sub=usuario.id)

        usuario.refreshToken = refreshToken
        self.sesionDb.commit()

        return TokenRespuesta(
            tokenAcceso=tokenAcceso,
            refreshToken=refreshToken,
            tipoToken="bearer",
            usuario=UsuarioRespuesta.model_validate(usuario)
        )

    def refrescarAccessToken(self, refreshToken: str) -> TokenRespuesta:
        """
        Valida un Refresh Token y emite un nuevo par Access/Refresh Token.
        """
        consulta = select(Usuario).where(Usuario.refreshToken == refreshToken)
        usuario = self.sesionDb.execute(consulta).scalar_one_or_none()

        if not usuario or not usuario.activo:
            raise ExcepcionDominio(
                mensaje="Refresh Token inválido o expirado.",
                codigoEstado=status.HTTP_401_UNAUTHORIZED
            )

        payload = {
            "sub": usuario.email,
            "id": usuario.id,
            "rol": usuario.rol.value
        }
        nuevoAccessToken = crearTokenAcceso(datosPayload=payload)
        nuevoRefreshToken = crearRefreshToken(sub=usuario.id)

        usuario.refreshToken = nuevoRefreshToken
        self.sesionDb.commit()

        return TokenRespuesta(
            tokenAcceso=nuevoAccessToken,
            refreshToken=nuevoRefreshToken,
            tipoToken="bearer",
            usuario=UsuarioRespuesta.model_validate(usuario)
        )

    def solicitarRecuperacionPassword(self, email: str) -> bool:
        """Genera un token de recuperación y envía el correo electrónico."""
        consulta = select(Usuario).where(Usuario.email == email.lower().strip())
        usuario = self.sesionDb.execute(consulta).scalar_one_or_none()

        if not usuario or not usuario.activo:
            # Por seguridad no revelamos si el correo existe o no
            return True

        token = crearTokenRecuperacion(email=usuario.email)
        enviarEmailRecuperacionPassword(emailA=usuario.email, token=token)
        return True

    def restablecerPassword(self, token: str, nuevaPassword: str) -> bool:
        """Valida el token de recuperación y actualiza la contraseña del usuario."""
        email = verificarTokenRecuperacion(token)
        if not email:
            raise ExcepcionDominio(
                mensaje="El enlace de recuperación es inválido o ha expirado.",
                codigoEstado=status.HTTP_400_BAD_REQUEST
            )

        consulta = select(Usuario).where(Usuario.email == email.lower().strip())
        usuario = self.sesionDb.execute(consulta).scalar_one_or_none()

        if not usuario or not usuario.activo:
            raise ExcepcionDominio(
                mensaje="Usuario no encontrado o inactivo.",
                codigoEstado=status.HTTP_404_NOT_FOUND
            )

        usuario.passwordHash = generarPasswordHash(nuevaPassword)
        usuario.refreshToken = None  # Invalida refresh tokens existentes por seguridad
        self.sesionDb.commit()
        return True
