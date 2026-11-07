from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Any

class InmuebleInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    Compacidad_Relativa: float = Field(
        ..., ge=0.50, le=1.00,
        description="Índice de compacidad relativa del inmueble [0.50 a 1.00]"
    )
    Area_Superficie: float = Field(
        ..., gt=300.0, le=1200.0,
        description="Área de superficie envolvente total en m2 (300 a 1200]"
    )
    Area_Pared: float = Field(
        ..., gt=150.0, le=600.0,
        description="Área de muros exteriores en m2 (150 a 600]"
    )
    Area_Techo: float = Field(
        ..., gt=80.0, le=400.0,
        description="Área de techo en m2 (80 a 400]"
    )
    Altura_Total: float = Field(
        ..., gt=2.5, le=15.0,
        description="Altura total del inmueble en metros (2.5 a 15.0]"
    )
    Orientacion: int = Field(
        ..., ge=2, le=5,
        description="Orientación cardinal codificada: 2=Norte, 3=Este, 4=Sur, 5=Oeste"
    )
    Area_Acristalamiento: float = Field(
        ..., ge=0.0, le=1.0,
        description="Proporción de área acristalada respecto al piso [0.0 a 1.0]"
    )
    Distribucion_Acristalamiento: int = Field(
        ..., ge=0, le=5,
        description="Esquema de distribución de ventanas [0=Sin ventanas a 5=Oeste]"
    )

class PrediccionOutput(BaseModel):
    prediccion_clase: int
    etiqueta_operativa: str
    probabilidad_critico: float
    umbral_aplicado: float
    version_modelo: str
    evaluacion_opex: Dict[str, Any]
    latencia_ms: float
