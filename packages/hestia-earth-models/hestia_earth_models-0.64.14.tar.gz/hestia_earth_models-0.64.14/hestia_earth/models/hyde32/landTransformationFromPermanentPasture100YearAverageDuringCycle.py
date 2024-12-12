from hestia_earth.schema import SiteSiteType

from .utils import run_land_transformation

REQUIREMENTS = {
    "ImpactAssessment": {
        "or": {
            "country": {"@type": "Term", "termType": "region"},
            "site": {
                "@type": "Site",
                "region": {"@type": "Term", "termType": "region"}
            }
        },
        "endDate": "",
        "product": {"@type": "Term"},
        "cycle": {
            "@type": "Cycle",
            "or": [
                {
                    "@doc": "if the [cycle.functionalUnit](https://hestia.earth/schema/Cycle#functionalUnit) = 1 ha, additional properties are required",  # noqa: E501
                    "cycleDuration": "",
                    "products": [{
                        "@type": "Product",
                        "primary": "True",
                        "value": "> 0",
                        "economicValueShare": "> 0"
                    }],
                    "practices": [{"@type": "Practice", "value": "", "term.@id": "longFallowRatio"}]
                },
                {
                    "@doc": "for plantations, additional properties are required",
                    "practices": [
                        {"@type": "Practice", "value": "", "term.@id": "nurseryDensity"},
                        {"@type": "Practice", "value": "", "term.@id": "nurseryDuration"},
                        {"@type": "Practice", "value": "", "term.@id": "plantationProductiveLifespan"},
                        {"@type": "Practice", "value": "", "term.@id": "plantationDensity"},
                        {"@type": "Practice", "value": "", "term.@id": "plantationLifespan"},
                        {"@type": "Practice", "value": "", "term.@id": "rotationDuration"}
                    ]
                }
            ]
        }
    }
}
LOOKUPS = {
    "@doc": "One of (depending on `site.siteType`)",
    "region-cropland-landTransformation100years": "`permanent pasture`",
    "region-forest-landTransformation100years": "`permanent pasture`",
    "region-other_natural_vegetation-landTransformation100years": "`permanent pasture`"
}
RETURNS = {
    "Indicator": [{
        "value": "",
        "landCover": ""
    }]
}
TERM_ID = 'landTransformationFromPermanentPasture100YearAverageDuringCycle'


def run(impact_assessment: dict):
    return run_land_transformation(impact_assessment, TERM_ID, SiteSiteType.PERMANENT_PASTURE, 100)
