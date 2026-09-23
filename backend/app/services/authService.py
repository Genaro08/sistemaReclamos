from fastapi import status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.usuario import Usuario
from app.schemas.usuarioSchema import UsuarioCrear, LoginEsquema, TokenRespuesta, UsuarioRespuesta
from app.core.seguridad import generarPasswordHash, verificarPassword, crearTokenAcceso
from app.core.excepciones import ExcepcionDominio


class AuthService:
    """
    Servicio de Lógica de Negocio para la gestión de registro, login y autenticación.
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
        Verifica el email y contraseña del usuario y genera un Token JWT.
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

        return TokenRespuesta(
            tokenAcceso=tokenAcceso,
            tipoToken="bearer",
            usuario=UsuarioRespuesta.model_validate(usuario)
        )
