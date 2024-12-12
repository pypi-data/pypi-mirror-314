from .utils import run_inputs_production

REQUIREMENTS = {
    "ImpactAssessment": {
        "product": {"@type": "Term"},
        "cycle": {
            "@type": "Cycle",
            "products": [{
                "@type": "Product",
                "primary": "True",
                "value": "> 0",
                "economicValueShare": "> 0"
            }]
        }
    }
}
RETURNS = {
    "Indicator": [{
        "value": ""
    }]
}
TERM_ID = 'landOccupationInputsProduction'


def run(impact_assessment: dict): return run_inputs_production(impact_assessment, TERM_ID)
