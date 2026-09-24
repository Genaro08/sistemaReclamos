from datetime import datetime, timedelta, timezone
from typing import Any, Optional
import bcrypt
import jwt
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
    Crea un token JWT de acceso firmado conteniendo los datos del payload especificados.
    """
    copiaPayload = datosPayload.copy()
    if deltaExpiracion:
        expiracion = datetime.now(timezone.utc) + deltaExpiracion
    else:
        expiracion = datetime.now(timezone.utc) + timedelta(minutes=configuracion.minutosExpiracionToken)

    copiaPayload.update({"exp": expiracion, "type": "access"})

    tokenFirmado = jwt.encode(
        copiaPayload,
        configuracion.secretKey,
        algorithm=configuracion.algoritmo
    )
    return tokenFirmado


def crearRefreshToken(sub: str | int) -> str:
    """Crea un Refresh Token JWT de larga duración."""
    expiracion = datetime.now(timezone.utc) + timedelta(days=configuracion.refreshTokenExpireDays)
    payload = {
        "sub": str(sub),
        "type": "refresh",
        "exp": expiracion
    }
    return jwt.encode(payload, configuracion.secretKey, algorithm=configuracion.algoritmo)


def crearTokenRecuperacion(email: str) -> str:
    """Crea un token JWT temporal para recuperación de contraseña."""
    expiracion = datetime.now(timezone.utc) + timedelta(hours=configuracion.emailResetTokenExpireHours)
    payload = {
        "sub": email,
        "type": "reset",
        "exp": expiracion
    }
    return jwt.encode(payload, configuracion.secretKey, algorithm=configuracion.algoritmo)


def verificarTokenRecuperacion(token: str) -> str | None:
    """
    Decodifica y valida un token de recuperación.
    Devuelve el email si es válido o None si expiró/es inválido.
    """
    try:
        payload = jwt.decode(token, configuracion.secretKey, algorithms=[configuracion.algoritmo])
        if payload.get("type") != "reset":
            return None
        return payload.get("sub")
    except jwt.PyJWTError:
        return None


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
