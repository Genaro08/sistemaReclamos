from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuracion(BaseSettings):
    """
    Configuración global de la aplicación.
    Carga automáticamente las variables de entorno desde el archivo .env
    usando Pydantic Settings.
    """
    proyectoNombre: str = Field(default="Sistema de Gestión de Reclamos", validation_alias="PROYECTO_NOMBRE")
    apiV1Str: str = Field(default="/api/v1", validation_alias="API_V1_STR")

    # Cadena de conexión relacional a PostgreSQL (Supabase o Local)
    databaseUrl: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/sistemas_reclamos",
        validation_alias="DATABASE_URL"
    )

    # Seguridad y tokens JWT
    secretKey: str = Field(default="clave_desarrollo_reclamos_jwt_secret_key_2026", validation_alias="SECRET_KEY")
    algoritmo: str = Field(default="HS256", validation_alias="ALGORITMO")
    minutosExpiracionToken: int = Field(default=30, validation_alias="MINUTOS_EXPIRACION_TOKEN")
    refreshTokenExpireDays: int = Field(default=7, validation_alias="REFRESH_TOKEN_EXPIRE_DAYS")
    emailResetTokenExpireHours: int = Field(default=24, validation_alias="EMAIL_RESET_TOKEN_EXPIRE_HOURS")

    # Email SMTP
    smtpHost: str | None = Field(default=None, validation_alias="SMTP_HOST")
    smtpPort: int = Field(default=587, validation_alias="SMTP_PORT")
    smtpUser: str | None = Field(default=None, validation_alias="SMTP_USER")
    smtpPassword: str | None = Field(default=None, validation_alias="SMTP_PASSWORD")
    emailsFromEmail: str = Field(default="noreply@reclamos.com", validation_alias="EMAILS_FROM_EMAIL")
    emailsFromName: str = Field(default="Sistema de Reclamos", validation_alias="EMAILS_FROM_NAME")
    frontendUrl: str = Field(default="http://localhost:5173", validation_alias="FRONTEND_URL")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


# Instancia única reutilizable de la configuración
configuracion = Configuracion()
