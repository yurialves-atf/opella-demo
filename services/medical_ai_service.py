from abc import ABC, abstractmethod

from models.analysis import MonographAnalysis


class MedicalAIService(ABC):

    @abstractmethod
    def analyze_monograph(
        self,
        pdf_bytes: bytes,
        filename: str,
    ) -> MonographAnalysis:
        pass