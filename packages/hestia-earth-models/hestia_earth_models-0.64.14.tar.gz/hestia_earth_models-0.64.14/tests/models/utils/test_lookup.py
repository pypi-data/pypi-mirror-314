from hestia_earth.models.utils.lookup import is_siteType_allowed


def test_is_siteType_allowed():
    term = {'@id': 'pastureGrass', 'termType': 'landUseManagement'}
    site = {'@type': 'Site', 'siteType': 'cropland'}
    assert not is_siteType_allowed(site, term)

    cycle = {'otherSites': [{'@type': 'Site', 'siteType': 'permanent pasture'}]}
    assert is_siteType_allowed(cycle, term) is True
