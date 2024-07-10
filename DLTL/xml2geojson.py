import xml.etree.ElementTree as ET
from geojson import Feature, Polygon, FeatureCollection, dump, loads
import uuid
import numpy as np
import pandas as pd
import os
from tqdm import tqdm

def xml2df(xml_ref):
    tree = ET.parse(xml_ref)
    root = tree.getroot()
    rows = []
    df_cols = ["Name", 'Class ID', "ID", 'Coord']  # classid may not be necessary
    for child in root:  # interate through the 12 classes
        class_id = child.attrib['Id']
        for Attrib in child.iter('Attribute'):
            name_str = Attrib.attrib['Name']
            # iterate each "circle"
            for region in child.iter('Region'):  # region in child
                # initialize vertex
                vertex_arr = []
                idx = region.attrib['Id']  # idx for each region in attribute
                # collect XY coordinates into numpy list
                for coord in region.iter('Vertex'):  # vertex in each region
                    xy = np.array([[float(coord.attrib['X']), float(coord.attrib['Y'])]])
                    vertex_arr.append(tuple(xy[0]))
                rows.append({"Name": name_str, 'Class ID': class_id, "ID": idx,
                             "Coord": vertex_arr})
    df = pd.DataFrame(rows, columns=df_cols)
    return df

def xml2geojson(xml_path):
    df = xml2df(xml_path)
    df['feat'] = df.apply(lambda x: Feature(geometry=Polygon([x['Coord']]),
                                            properties={"objectType": "annotation", "classification": x['Name']},
                                            id=str(uuid.uuid1())), axis=1)
    # feature_collection = FeatureCollection(df.feat.to_list())
    return df.feat.to_list()

if __name__ == "__main__":
    xml_src= r"\\10.99.68.51\Kyu\skin_aging\Hopkins_cohort\annotation\12class"
    dst = r"\\10.99.68.54\Digital pathology image lib\HubMap Skin TMC project\240418_DLTL_master\qpproj_back\annotation_v7"
    xmls = [_ for _ in os.listdir(xml_src) if _.endswith('xml')]
    for xml_name in tqdm(xmls):
        geojson = xml2geojson(os.path.join(xml_src,xml_name))
        with open(os.path.join(dst,xml_name.replace('.xml','.geojson')), 'w') as f:
            dump(geojson, f)
        f.close()
