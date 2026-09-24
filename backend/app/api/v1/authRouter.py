from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.dependencias import obtenerUsuarioActual
from app.db.sesion import obtenerSesionDb
from app.models.usuario import Usuario
from app.schemas.usuarioSchema import (
    LoginEsquema,
    RefreshTokenEsquema,
    RestablecerPasswordEsquema,
    SolicitudRecuperacionPassword,
    TokenRespuesta,
    UsuarioCrear,
    UsuarioRespuesta,
)
from app.services.authService import AuthService

authRouter = APIRouter(prefix="/auth", tags=["Autenticación"])


@authRouter.post(
    "/registro",
    response_model=UsuarioRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo usuario"
)
def registrarUsuario(
    datos: UsuarioCrear,
    sesionDb: Session = Depends(obtenerSesionDb)
):
    """
    Permite el registro de nuevos usuarios en el sistema.
    Por defecto, los usuarios se crean con rol USER.
    """
    servicioAuth = AuthService(sesionDb)
    return servicioAuth.registrarUsuario(datos)


@authRouter.post(
    "/login",
    response_model=TokenRespuesta,
    status_code=status.HTTP_200_OK,
    summary="Iniciar sesión y recibir Tokens JWT (Access & Refresh)"
)
def iniciarSesion(
    datos: LoginEsquema,
    sesionDb: Session = Depends(obtenerSesionDb)
):
    """
    Autentica al usuario mediante email y contraseña.
    Retorna un par de tokens (Access & Refresh) firmados si las credenciales son válidas.
    """
    servicioAuth = AuthService(sesionDb)
    return servicioAuth.autenticarUsuario(datos)


@authRouter.post(
    "/refresh",
    response_model=TokenRespuesta,
    status_code=status.HTTP_200_OK,
    summary="Renovar el Token de Acceso JWT enviando un Refresh Token válido"
)
def refrescarToken(
    datos: RefreshTokenEsquema,
    sesionDb: Session = Depends(obtenerSesionDb)
):
    servicioAuth = AuthService(sesionDb)
    return servicioAuth.refrescarAccessToken(datos.refreshToken)


@authRouter.post(
    "/recuperar-password",
    status_code=status.HTTP_200_OK,
    summary="Solicitar enlace de recuperación de contraseña por email"
)
def solicitarRecuperacion(
    datos: SolicitudRecuperacionPassword,
    sesionDb: Session = Depends(obtenerSesionDb)
):
    servicioAuth = AuthService(sesionDb)
    servicioAuth.solicitarRecuperacionPassword(datos.email)
    return {
        "mensaje": "Si el correo electrónico está registrado, recibirás un mensaje con las instrucciones para restablecer tu contraseña."
    }


@authRouter.post(
    "/restablecer-password",
    status_code=status.HTTP_200_OK,
    summary="Restablecer la contraseña con un token de recuperación válido"
)
def restablecerPassword(
    datos: RestablecerPasswordEsquema,
    sesionDb: Session = Depends(obtenerSesionDb)
):
    servicioAuth = AuthService(sesionDb)
    servicioAuth.restablecerPassword(datos.token, datos.nuevaPassword)
    return {
        "mensaje": "La contraseña ha sido actualizada exitosamente."
    }


@authRouter.get(
    "/me",
    response_model=UsuarioRespuesta,
    status_code=status.HTTP_200_OK,
    summary="Obtener perfil del usuario autenticado"
)
def obtenerPerfilActual(
    usuarioActual: Usuario = Depends(obtenerUsuarioActual)
):
    """
    Retorna la información del usuario correspondiente al token JWT provisto.
    """
    return UsuarioRespuesta.model_validate(usuarioActual)
