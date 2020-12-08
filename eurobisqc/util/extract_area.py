import xmltodict
from eurobisqc.util import misc

def find_area(xml_input):

    """ This may be not generic enough, must verify within the eml.xml specs
        if the geographical area is always in the same element structure then it should work
        :returns list of x bondaries, y bondaries [(east,west), (north,south)]
        :returns None if area not present or not found where expected
    """

    dict_input = xmltodict.parse(xml_input)
    north = south = east = west = 0

    geo_area_dict = None
    if 'coverage' in dict_input['eml:eml']['dataset']:
        if 'geographicCoverage' in dict_input['eml:eml']['dataset']['coverage']:
            if 'boundingCoordinates' in dict_input['eml:eml']['dataset']['coverage']['geographicCoverage']:
                geo_area_dict = dict_input['eml:eml']['dataset']['coverage']['geographicCoverage']['boundingCoordinates']

    # Is it well formed
    valid = True
    if geo_area_dict is not None:
        if misc.is_number(geo_area_dict['westBoundingCoordinate']):
            west = float(geo_area_dict['westBoundingCoordinate'])
        else:
            valid = False

        if valid and misc.is_number(geo_area_dict['eastBoundingCoordinate']):
            east = float(geo_area_dict['eastBoundingCoordinate'])
        else:
            valid = False

        if valid and misc.is_number(geo_area_dict['northBoundingCoordinate']):
            north = float(geo_area_dict['northBoundingCoordinate'])
        else:
            valid = False

        if valid and misc.is_number(geo_area_dict['southBoundingCoordinate']):
            south = float(geo_area_dict['southBoundingCoordinate'])
        else:
            valid = False

        if valid :
            return [(east,west), (north,south)]
        else:
            return None



