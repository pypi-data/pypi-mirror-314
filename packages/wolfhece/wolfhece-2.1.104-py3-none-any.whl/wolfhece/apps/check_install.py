
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


    # Get list of all packages
    import pkg_resources
    installed_packages = pkg_resources.working_set
    packages = sorted(["%s" % (i.key) for i in installed_packages])

    #is osgeo in packages?
    if 'osgeo' in packages or 'gdal' in packages:
        ret += 'OSGeo seems installed\n\n'
    else:
        ret += 'OSGeo not installed\n Please install GDAL from https://github.com/cgohlke/geospatial-wheels/releases\n\n'

    try:
        from osgeo import ogr, gdal
        ret += 'Correct import of osgeo package - GDAL/OGR installed\n\n'
    except ImportError as e:
        ret += 'Error during osgeo import - GDAL/OGR not/bad installed\n Please (re)install GDAL (64 bits version) from https://github.com/cgohlke/geospatial-wheels/releases\n\n'
        ret += 'Error : ' + str(e) + '\n\n'

    if 'wolfgpu' in packages:
        ret += 'WolfGPU seems installed\n\n'
    else:
        ret += 'WolfGPU not installed\n Please install WolfGPU if needed\n\n'

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