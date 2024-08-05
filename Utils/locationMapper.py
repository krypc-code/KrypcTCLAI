# Libraries
import pymupdf
# Location Mapper Function
def get_points(Rect, page):
    return([Rect.x0,Rect.y0,Rect.x1,Rect.y1,page])

def location_mapper(result):
    doc = pymupdf.open(result['file_path'])
    # Mapping summary fields
    for item in result['summary']:
        loc = []
        for page in doc:
            if(result['summary'][item]):
                if(len(page.search_for(result['summary'][item]))>0):
                    for location in page.search_for(result['summary'][item]):
                        loc.append(get_points(location,page.number+1))
        result['summary'][item] = {'value': result['summary'][item], 'loc':loc}
    # Mapping detailed Fields
    for item in result['detailed']:
        # Mapping table line items
        if(item == 'InvoiceItemDetails'):
            for index,item in enumerate(result['detailed']['InvoiceItemDetails']):
                loc=[]
                for page in doc:
                    if(item['Description']):
                        if(len(page.search_for(item['Description']))>0):
                            for location in page.search_for(item['Description']):
                                loc.append(get_points(location,page.number+1))
                result['detailed']['InvoiceItemDetails'][index]['Description'] = {'value': result['detailed']['InvoiceItemDetails'][index]['Description'], 'loc':loc}
        else:
            # Mapping other detailed fields
            loc = []
            for page in doc:
                if(result['detailed'][item]):
                    if(len(page.search_for(result['detailed'][item]))>0):
                        for location in page.search_for(result['detailed'][item]):
                            loc.append(get_points(location,page.number+1))
            result['detailed'][item] = {'value': result['detailed'][item], 'loc':loc}
    return(result)