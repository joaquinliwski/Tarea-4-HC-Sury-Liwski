"""
Countries area
Model exported as python.
Name : model4c
Group : 
With QGIS : 32208
"""
#########################################################################################
################################################################################
# SETUP PREAMBLE FOR RUNNING STANDALONE SCRIPTS.
# NOT NECESSARY IF YOU ARE RUNNING THIS INSIDE THE QGIS GUI.
print('setting up')
import sys
import os
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsCoordinateReferenceSystem
import processing

# set paths to inputs and outputs
print ('setting paths')
mainpath = "/Users/camilasury/Desktop/Herramientas computacionales/Python & QGIS/Input"
output = "/Users/camilasury/Desktop/Herramientas computacionales/Python & QGIS/Output"
admin = "/Users/camilasury/Desktop/Herramientas computacionales/Python & QGIS/Input/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp"
areas_out = "/Users/camilasury/Desktop/Herramientas computacionales/Python & QGIS/Output/country_areas.csv"

#class definition
class Model4c(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Countries_drop_fields', 'countries_drop_fields', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Areas_out', 'areas_out', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Countries_fixgeo', 'countries_fixgeo', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Countries_reprojected', 'countries_reprojected', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(5, model_feedback)
        results = {}
        outputs = {}
     
##################################################################
# Drop field(s)
##################################################################
print('dropping unnecessary fields')
        dropf_dict = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','TLC','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','MAPCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','POP_YEAR','GDP_MD','GDP_YEAR','ECONOMY','INCOME_GRP','FIPS_10','ISO_A2','ISO_A2_EH','ISO_A3_EH','ISO_N3','ISO_N3_EH','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_ISO','ADM0_DIFF','ADM0_TLC','ADM0_A3_US','ADM0_A3_FR','ADM0_A3_RU','ADM0_A3_ES','ADM0_A3_CN','ADM0_A3_TW','ADM0_A3_IN','ADM0_A3_NP','ADM0_A3_PK','ADM0_A3_DE','ADM0_A3_GB','ADM0_A3_BR','ADM0_A3_IL','ADM0_A3_PS','ADM0_A3_SA','ADM0_A3_EG','ADM0_A3_MA','ADM0_A3_PT','ADM0_A3_AR','ADM0_A3_JP','ADM0_A3_KO','ADM0_A3_VN','ADM0_A3_TR','ADM0_A3_ID','ADM0_A3_PL','ADM0_A3_GR','ADM0_A3_IT','ADM0_A3_NL','ADM0_A3_SE','ADM0_A3_BD','ADM0_A3_UA','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','LABEL_X','LABEL_Y','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FA','NAME_FR','NAME_EL','NAME_HE','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_UK','NAME_UR','NAME_VI','NAME_ZH','NAME_ZHT','FCLASS_ISO','TLC_DIFF','FCLASS_TLC','FCLASS_US','FCLASS_FR','FCLASS_RU','FCLASS_ES','FCLASS_CN','FCLASS_TW','FCLASS_IN','FCLASS_NP','FCLASS_PK','FCLASS_DE','FCLASS_GB','FCLASS_BR','FCLASS_IL','FCLASS_PS','FCLASS_SA','FCLASS_EG','FCLASS_MA','FCLASS_PT','FCLASS_AR','FCLASS_JP','FCLASS_KO','FCLASS_VN','FCLASS_TR','FCLASS_ID','FCLASS_PL','FCLASS_GR','FCLASS_IT','FCLASS_NL','FCLASS_SE','FCLASS_BD','FCLASS_UA','ADMIN_2','ISO_A3_2\n'],
            'INPUT': admin,
            'OUTPUT': parameters['Countries_drop_fields']
        }
        outputs['DropFields'] = processing.run('native:deletecolumn', dropf_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Countries_drop_fields'] = outputs['DropFields']['OUTPUT']
##################################################################
# Reproject layer
##################################################################
print('projecting to world cylindical equal area')
        reproj_dict = {
            'INPUT': outputs['DropFields']['OUTPUT'],
            'OPERATION': '',
            'TARGET_CRS': QgsCoordinateReferenceSystem('ESRI:54034'),
            'OUTPUT': parameters['Countries_reprojected']
        }
        outputs['ReprojectLayer'] = processing.run('native:reprojectlayer', reproj_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Countries_reprojected'] = outputs['ReprojectLayer']['OUTPUT']

##################################################################
# Fix geometries
##################################################################
print('fixing geometries')
        fixgeo_dict = {
            'INPUT': outputs['ReprojectLayer']['OUTPUT'],
            'OUTPUT': parameters['Countries_fixgeo']
        }
        outputs['FixGeometries'] = processing.run('native:fixgeometries', fixgeo_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Countries_fixgeo'] = outputs['FixGeometries']['OUTPUT']

##################################################################
# Field calculator
##################################################################
print('calculating country areas')
        fieldcalc_dict = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'km2area',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': 'area($geometry)/1000000',
            'INPUT': outputs['FixGeometries']['OUTPUT'],
            'OUTPUT': parameters['Areas_out']
        }
        outputs['FieldCalculator'] = processing.run('native:fieldcalculator', fieldcalc_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Areas_out'] = outputs['FieldCalculator']['OUTPUT']

##################################################################
#Save vector file to 
##################################################################
print('saving output to csv')
        savef_dict = {
            'DATASOURCE_OPTIONS': '',
            'INPUT': outputs['FieldCalculator']['OUTPUT'],
            'LAYER_NAME': '',
            'LAYER_OPTIONS': '',
            'OUTPUT': '/Users/camilasury/Desktop/Herramientas computacionales/Python & QGIS/Output/areas.csv',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SaveVectorFeaturesToFile'] = processing.run('native:savefeatures', savef_dict, context=context, feedback=feedback, is_child_algorithm=True)
        return results

 print ('DONE!')
