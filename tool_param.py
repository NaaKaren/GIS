import arcpy
import os

# Get input parameters from the user
lon = arcpy.GetParameterAsText(0)
lat = arcpy.GetParameterAsText(1)
dist = arcpy.GetParameterAsText(2)
buff_dist_m = dist + " Meters"

in_fc = arcpy.GetParameterAsText(3)
gdb = os.path.join(os.path.dirname(in_fc))
out_point_fc = gdb + "\\out_point"
out_fc = gdb + "\\out_fc"
out_buff_fc = gdb + "\\out_buff"

arcpy.env.overwriteOutput = True
#arcpy.env.workspace = gdb
#arcpy.env.scratchWorkspace = gdb

# Clear the contents of the output point feature class
with arcpy.da.UpdateCursor(out_point_fc, '*') as updateCursor:
    for row in updateCursor:
        updateCursor.deleteRow()
del updateCursor



# Create a point geometry from the lon lat
in_point = arcpy.Point(lon,lat)
utmz30n = arcpy.SpatialReference(32630)
InPointGeomWGS84 = arcpy.PointGeometry(in_point, 4326)
InPointGeomUTMZ30N = InPointGeomWGS84.projectAs(utmz30n)


# Write out the point to the out point feature class
with arcpy.da.InsertCursor(out_point_fc, ['SHAPE@']) as insertCursor:
    insertCursor.insertRow( [InPointGeomWGS84] ) 
del insertCursor


# Create a buffer polygon
arcpy.Buffer_analysis(out_point_fc, out_buff_fc, buff_dist_m, "FULL", "ROUND", "LIST", None, "PLANAR")


# Get all marriestopes within buffer
arcpy.MakeFeatureLayer_management(in_fc, 'in_lyr') 
arcpy.SelectLayerByLocation_management("in_lyr", "WITHIN", out_buff_fc, "", "NEW_SELECTION")

NumS = str(arcpy.GetCount_management("in_lyr"))

arcpy.AddMessage("Found: " + NumS)

# Write the selected features to a new featureclass (inside the scratch fgdb)
arcpy.CopyFeatures_management("in_lyr", arcpy.env.scratchGDB + "\\out_fc")
#arcpy.CopyFeatures_management("in_lyr", out_fc)


# Write out_fc to EGDB
arcpy.CopyFeatures_management(arcpy.env.scratchGDB+"\\out_fc", out_fc)
          
arcpy.AddMessage("Done processing")     

