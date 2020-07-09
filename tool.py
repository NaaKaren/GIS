import arcpy  

# Get input parameters from the user
lon = -0.840776
lat = 9.403333
buff_dist_m = str(100) + " Meters"

in_fc = r"C:\KarenProject\Karen.gdb\in_mariestopes"
out_point_fc = r"C:\KarenProject\Karen.gdb\out_point"
out_fc = r"C:\KarenProject\Karen.gdb\out_selected"
out_buff_fc = r"C:\KarenProject\Karen.gdb\out_buff"

arcpy.env.overwriteOutput = True

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

# Write the selected features to a new featureclass
arcpy.CopyFeatures_management("in_lyr", out_fc)       
            

print("done")
        

