
"""
Author: HECE - University of Liege, Pierre Archambeau
Date: 2024

Copyright (c) 2024 University of Liege. All rights reserved.

This script and its content are protected by copyright law. Unauthorized
copying or distribution of this file, via any medium, is strictly prohibited.
"""

def main():
    # Check if installation is complete
    ret = 'Checking installation\n---------------------\n\n'
    try:
        from osgeo import ogr, gdal
        ret += 'GDAL/OGR installed\n\n'
    except ImportError as e:
        ret += 'GDAL/OGR not installed\n Please install GDAL from https://github.com/cgohlke/geospatial-wheels/releases\n\n'
        ret += 'Error : ' + str(e) + '\n\n'

    try:
        from ..libs import wolfpy
        ret += 'Wolfpy accessible\n\n'
    except ImportError as e:
        ret += 'Wolfpy not accessible\n\n'
        ret += 'Error : ' + str(e) + '\n\n'
    
    try:
        from ..PyGui import MapManager
        ret += 'Wolfhece installed\n\n'
    except ImportError as e:
        ret += 'Wolfhece not installed properly\n Retry installation : pip install wolfhece or pip install wolfhece --upgrade\n\n'
        ret += 'Error : ' + str(e) + '\n\n'

    try:
        from ..lazviewer.processing.estimate_normals.estimate_normals import estimate_normals
    except ImportError as e:
        ret += 'Could not import estimate_normals\n\n'
        ret += 'Wolfhece not installed properly\n Please install the VC++ redistributable\n from https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads\n\n'
        ret += 'Error : ' + str(e) + '\n\n'

    print(ret)

if __name__=='__main__':
    main()