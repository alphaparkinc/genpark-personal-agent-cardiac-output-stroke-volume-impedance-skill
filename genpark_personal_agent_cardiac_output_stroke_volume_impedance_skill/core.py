# -*- coding: utf-8 -*-
"""Cardiac Output & Stroke Volume Hemodynamics for GenPark Personal Agent."""
import json
from typing import Dict, Any

class CardiacOutputStrokeVolumeHemodynamics:
    @staticmethod
    def compute_hemodynamic_cardiac_metrics(heart_rate_bpm: float, systolic_bp: float, diastolic_bp: float, body_surface_area_m2: float = 1.9) -> Dict[str, Any]:
        map_mmhg = round(diastolic_bp + (systolic_bp - diastolic_bp) / 3.0, 1)
        pulse_pressure = round(systolic_bp - diastolic_bp, 1)
        
        # Stroke Volume (mL) proxy based on pulse pressure and arterial compliance
        stroke_volume_ml = round(max(35.0, min(140.0, pulse_pressure * 1.75)), 1)
        cardiac_output_l_min = round((stroke_volume_ml * heart_rate_bpm) / 1000.0, 2)
        cardiac_index = round(cardiac_output_l_min / max(1.0, body_surface_area_m2), 2)
        
        # TPR (dynes*s/cm5) = 80 * (MAP - CVP) / CO (assuming CVP ~ 4)
        tpr_dynes = round((80.0 * (map_mmhg - 4.0)) / max(1.0, cardiac_output_l_min), 0)
        
        tier = "OPTIMAL_HEMODYNAMIC_EFFICIENCY" if 900 <= tpr_dynes <= 1400 and cardiac_index >= 2.5 else ("ELEVATED_VASCULAR_RESISTANCE" if tpr_dynes > 1400 else "HYPERDYNAMIC_STATE")
        
        return {
            "mean_arterial_pressure_map": map_mmhg,
            "estimated_stroke_volume_ml": stroke_volume_ml,
            "cardiac_output_l_min": cardiac_output_l_min,
            "cardiac_index_l_min_m2": cardiac_index,
            "total_peripheral_resistance_tpr": tpr_dynes,
            "hemodynamic_status": tier
        }

    @staticmethod
    def synthesize_arterial_stiffness_remedy(tpr_dynes: float, cardiac_index: float = 2.8) -> Dict[str, Any]:
        return {
            "tpr_target": "1000 - 1200 dynes*s/cm5",
            "endothelial_interventions": [
                "L-Citrulline 6,000 mg daily to upregulate eNOS nitric oxide synthesis",
                "Aged Garlic Extract (Kyolic) 1,200 mg to reduce arterial pulse wave velocity",
                "High-intensity interval sprints (4 x 30s All-out) to trigger shear-stress endothelial remodeling"
            ],
            "lifestyle_advisory": "Maintain potassium to sodium ratio > 2.0 via leafy greens and coconut water."
        }
