import os

from dotenv import load_dotenv

from services.manual_medical_service import (
    ManualMedicalService,
)


load_dotenv()


def get_medical_ai_service():

    provider = os.getenv(
        "AI_PROVIDER",
        "manual",
    ).lower()

    if provider == "manual":

        analysis_path = os.getenv(
            "MANUAL_ANALYSIS_PATH",
            "data/manual_monograph_analysis.json",
        )

        return ManualMedicalService(
            analysis_path
        )

    raise ValueError(
        f"Provider não suportado: {provider}"
    )