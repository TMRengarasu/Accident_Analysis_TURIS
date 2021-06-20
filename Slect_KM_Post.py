# Collect KM post lcation into one file
#Import Modules
import arcpy
from arcpy import env
import os


env.overwriteOutput =True


# define a finction to create a list of point features in several coverages inside a folder
def fcs_in_workspace(workspace):
    pointFcList=[]
    arcpy.env.workspace = workspace
    print env.workspace
    for folder in arcpy.ListWorkspaces():
        file= os.path.join(folder,"places\point")
        pointFcList.append(os.path.join(folder,"places\point"))          
    return pointFcList

# folder Location
folderLocation="F:\\Backup\\E\\localgis\\trunk\\surveynew\\Luse_Trans"


# Check the functions
fclist = fcs_in_workspace(folderLocation)
print fclist


field_name ="GFCODE"
state_value="KLMPP"


out_feature_class="F:\\Backup\\E\\localgis\\trunk\\points\\kmpoint\\km_temp.shp"

Final_out_feature_class="F:\\Backup\\E\\localgis\\trunk\\points\\kmpoint\\kmpoint_all.shp"




# main work done here
for fc in fcs_in_workspace(folderLocation):
    where_clause ="""{0} = '{1}'""".format(arcpy.AddFieldDelimiters(fc, field_name),state_value)
    arcpy.analysis.Select(fc, out_feature_class, where_clause)
    arcpy.Append_management(out_feature_class, Final_out_feature_class)
    print fc

