from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict
from pydantic.alias_generators import to_camel
from app.models.usuario import RolUsuario


class EsquemaBaseConfig(BaseModel):
    """
    Configuración base que convierte automáticamente atributos de Python a camelCase en el JSON.
    """
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True
    )


class UsuarioCrear(EsquemaBaseConfig):
    """
    DTO para la solicitud de registro de un nuevo usuario.
    """
    nombre: str
    apellido: str
    email: EmailStr
    password: str


class UsuarioRespuesta(EsquemaBaseConfig):
    """
    DTO para retornar el perfil público del usuario (excluye el passwordHash).
    """
    id: int
    nombre: str
    apellido: str
    email: EmailStr
    rol: RolUsuario
    activo: bool
    fechaCreacion: datetime


class LoginEsquema(EsquemaBaseConfig):
    """
    DTO para la solicitud de inicio de sesión.
    """
    email: EmailStr
    password: str


class TokenRespuesta(EsquemaBaseConfig):
    """
    DTO para retornar el token de acceso JWT al cliente tras autenticación.
    """
    tokenAcceso: str
    tipoToken: str = "bearer"
    usuario: UsuarioRespuesta
