from pathlib import Path

from models.analysis import MonographAnalysis
from services.medical_ai_service import MedicalAIService


class ManualMedicalService(MedicalAIService):

    def __init__(self, analysis_path: str):
        self.analysis_path = Path(analysis_path)

    def analyze_monograph(
        self,
        pdf_bytes: bytes,
        filename: str,
    ) -> MonographAnalysis:

        if not self.analysis_path.exists():
            raise FileNotFoundError(
                f"Análise manual não encontrada: "
                f"{self.analysis_path}"
            )

        json_content = self.analysis_path.read_text(
            encoding="utf-8"
        )

        analysis = MonographAnalysis.model_validate_json(
            json_content
        )

        return analysis