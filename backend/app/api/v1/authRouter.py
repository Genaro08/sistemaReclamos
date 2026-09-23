from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.sesion import obtenerSesionDb
from app.services.authService import AuthService
from app.schemas.usuarioSchema import UsuarioCrear, UsuarioRespuesta, LoginEsquema, TokenRespuesta
from app.api.dependencias import obtenerUsuarioActual
from app.models.usuario import Usuario

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
    summary="Iniciar sesión y recibir Token JWT"
)
def iniciarSesion(
    datos: LoginEsquema,
    sesionDb: Session = Depends(obtenerSesionDb)
):
    """
    Autentica al usuario mediante email y contraseña.
    Retorna un token de acceso JWT firmado si las credenciales son válidas.
    """
    servicioAuth = AuthService(sesionDb)
    return servicioAuth.autenticarUsuario(datos)


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
