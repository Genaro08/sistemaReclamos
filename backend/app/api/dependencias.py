from typing import Callable
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.sesion import obtenerSesionDb
from app.core.seguridad import decodificarTokenAcceso
from app.core.excepciones import ExcepcionDominio
from app.models.usuario import Usuario, RolUsuario

# Esquema de autenticación Bearer Token en OpenAPI / Swagger
oauth2Scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def obtenerUsuarioActual(
    token: str = Depends(oauth2Scheme),
    sesionDb: Session = Depends(obtenerSesionDb)
) -> Usuario:
    """
    Inyector de dependencia para extraer y validar el usuario autenticado
    a partir del token JWT enviado en el encabezado Authorization.
    """
    payload = decodificarTokenAcceso(token)
    if not payload:
        raise ExcepcionDominio(
            mensaje="Token de autenticación inválido o expirado",
            codigoEstado=status.HTTP_401_UNAUTHORIZED
        )

    usuarioId = payload.get("id")
    if not usuarioId:
        raise ExcepcionDominio(
            mensaje="Payload de token inválido",
            codigoEstado=status.HTTP_401_UNAUTHORIZED
        )

    consulta = select(Usuario).where(Usuario.id == usuarioId)
    usuario = sesionDb.execute(consulta).scalar_one_or_none()

    if not usuario or not usuario.activo:
        raise ExcepcionDominio(
            mensaje="Usuario no encontrado o inactivo",
            codigoEstado=status.HTTP_401_UNAUTHORIZED
        )

    return usuario


def requerirRoles(rolesPermitidos: list[RolUsuario]) -> Callable:
    """
    Fábrica de dependencias para el Control de Acceso Basado en Roles (RBAC).
    Verifica que el usuario actual posea al menos uno de los roles autorizados.
    """
    def verificadorRol(usuarioActual: Usuario = Depends(obtenerUsuarioActual)) -> Usuario:
        if usuarioActual.rol not in rolesPermitidos:
            raise ExcepcionDominio(
                mensaje=f"Permisos insuficientes. Se requiere uno de los roles: {[r.value for r in rolesPermitidos]}",
                codigoEstado=status.HTTP_403_FORBIDDEN
            )
        return usuarioActual

    return verificadorRol
