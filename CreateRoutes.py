#created by Dr. T.M. Rengarsu under TURIS project.
#This code joins the transporttion feature classes of Sri Lanka and add spation references(Kandawala grid)

import os
import arcpy
import fnmatch

# Overwrite pre-existing files
arcpy.env.overwriteOutput = True
 
def inventory_data(workspace, datatypes):
    """
    Generates full path names under a catalog tree for all requested
    datatype(s).
 
    Parameters:
    workspace: string
        The top-level workspace that will be used.
    datatypes: string | list | tuple
        Keyword(s) representing the desired datatypes. A single
        datatype can be expressed as a string, otherwise use
        a list or tuple. See arcpy.da.Walk documentation 
        for a full list.
    """
    for path, path_names, data_names in arcpy.da.Walk(
            workspace, datatype=datatypes):
        for data_name in data_names:
            yield os.path.join(path, data_name)
 
 
for feature_class in inventory_data(r"F:\Backup\E\localgis\trunk\surveynew", "FeatureClass"):
    if fnmatch.fnmatch(feature_class, '*trans?arc'):
        print(feature_class)
#


fcList=fnmatch.filter(inventory_data(r"F:\Backup\E\localgis\trunk\surveynew", "FeatureClass"),'*trans?arc')
print(fcList)


# Set environment settings
arcpy.env.workspace = r"C:/data/turis"

# Set local variables
outLocation = "C:\\data\\turis\\tt.gdb"
emptyFC = "SL_roads"
schemaType = "NO_TEST"
fieldMappings = ""
subtype = ""
template="F:\\Backup\\E\\localgis\\trunk\\surveynew\\trans\\91\\trans\\arc"
has_m = "DISABLED"
has_z = "DISABLED"
spatial_reference="C:\\data\\extent.prj"
try:
    # Process:  Create a new empty feature class to append shapefiles into
    arcpy.CreateFeatureclass_management(outLocation, emptyFC, "POLYLINE",template,has_m,has_z,spatial_reference)

    # Process: Append the feature classes into the empty feature class
    arcpy.Append_management(fcList, outLocation + os.sep + emptyFC, schemaType, fieldMappings, subtype)

except Exception as err:
    print(err.args[0])

  
  #
expression = "roadClass(!TYPE!)" 
codeblock = """def roadClass(type):
    if type == "A1":
        return "AA001"
    elif type == "A2":
        return "A002"
    elif type == "A3":
        return "A003"
    elif type == "A4":
        return "A004"
    elif type == "A5":
        return "A005"
    elif type == "A6":
        return "A006"
    elif type == "A7":
        return "A007"
    else:
        return type"""


# Execute AddField
arcpy.AddField_management(roadsfull, "ROADT", "TEXT")
 
# Execute CalculateField 
arcpy.CalculateField_management(roadsfull, "ROADT", expression, "PYTHON", codeblock) 


rid = "ROADT" 
out_routes = "SLRoutes" 

# Execute CreateRoutes
arcpy.CreateRoutes_lr(roadsfull, rid, out_routes, "LENGTH", "#", "#",  "LOWER_LEFT")
