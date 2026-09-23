from datetime import datetime, timedelta, timezone
from typing import Optional, Any
import jwt
import bcrypt
from app.core.configuracion import configuracion


def generarPasswordHash(passwordPlano: str) -> str:
    """
    Genera un hash seguro mediante bcrypt a partir de una contraseña en texto plano.
    """
    bytesPassword = passwordPlano.encode("utf-8")
    salt = bcrypt.gensalt()
    hashBytes = bcrypt.hashpw(bytesPassword, salt)
    return hashBytes.decode("utf-8")


def verificarPassword(passwordPlano: str, passwordHash: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con su hash almacenado en bcrypt.
    """
    bytesPassword = passwordPlano.encode("utf-8")
    bytesHash = passwordHash.encode("utf-8")
    return bcrypt.checkpw(bytesPassword, bytesHash)


def crearTokenAcceso(datosPayload: dict[str, Any], deltaExpiracion: Optional[timedelta] = None) -> str:
    """
    Crea un token JWT firmado conteniendo los datos del payload especificados.
    """
    copiaPayload = datosPayload.copy()
    
    if deltaExpiracion:
        expiracion = datetime.now(timezone.utc) + deltaExpiracion
    else:
        expiracion = datetime.now(timezone.utc) + timedelta(minutes=configuracion.minutosExpiracionToken)
        
    copiaPayload.update({"exp": expiracion})
    
    tokenFirmado = jwt.encode(
        copiaPayload,
        configuracion.secretKey,
        algorithm=configuracion.algoritmo
    )
    return tokenFirmado


def decodificarTokenAcceso(token: str) -> Optional[dict[str, Any]]:
    """
    Decodifica y valida la firma y expiración de un token JWT.
    Retorna el payload decodificado si es válido, o None en caso contrario.
    """
    try:
        payload = jwt.decode(
            token,
            configuracion.secretKey,
            algorithms=[configuracion.algoritmo]
        )
        return payload
    except jwt.PyJWTError:
        return None
