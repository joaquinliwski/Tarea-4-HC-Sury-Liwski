"""
CSV/raster generator with statistics
Name : model3
Group : 
With QGIS : 32208
"""
#########################################################################################
#########################################################################################
# SETUP PREAMBLE FOR RUNNING STANDALONE SCRIPTS.
# NOT NECESSARY IF YOU ARE RUNNING THIS INSIDE THE QGIS GUI.
#
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
import processing
#########################################################################################

mainpath = "/Users/camilasury/Desktop/Herramientas computacionales/Python & QGIS/Input"
outpath = "/Users/camilasury/Desktop/Herramientas computacionales/Python & QGIS/Output"

admin = "{}/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp".format(mainpath)
#class definition
class Model3(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Drop_fields_3', 'drop_fields_3', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_3', 'fixgeo_3', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Landq', 'landq', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Pop1800', 'pop1800', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Pop1900', 'pop1900', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Pop2000', 'pop2000', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(7, model_feedback)
        results = {}
        outputs = {}
        
        ##################################################################
        # Fix geometries from shapefile
        ##################################################################
        fixgeo_dict = {
            'INPUT': admin,
            'OUTPUT': parameters['Fixgeo_3']
        }
        outputs['FixGeometries'] = processing.run('native:fixgeometries', fixgeo_dict , context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_3'] = outputs['FixGeometries']['OUTPUT']
        return results
    
        ##################################################################
        # Drop field(s)
        ##################################################################
        dropf_dict = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','TLC','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','MAPCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','POP_YEAR','GDP_MD','GDP_YEAR','ECONOMY','INCOME_GRP','FIPS_10','ISO_A2','ISO_A2_EH','ISO_A3_EH','ISO_N3','ISO_N3_EH','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_ISO','ADM0_DIFF','ADM0_TLC','ADM0_A3_US','ADM0_A3_FR','ADM0_A3_RU','ADM0_A3_ES','ADM0_A3_CN','ADM0_A3_TW','ADM0_A3_IN','ADM0_A3_NP','ADM0_A3_PK','ADM0_A3_DE','ADM0_A3_GB','ADM0_A3_BR','ADM0_A3_IL','ADM0_A3_PS','ADM0_A3_SA','ADM0_A3_EG','ADM0_A3_MA','ADM0_A3_PT','ADM0_A3_AR','ADM0_A3_JP','ADM0_A3_KO','ADM0_A3_VN','ADM0_A3_TR','ADM0_A3_ID','ADM0_A3_PL','ADM0_A3_GR','ADM0_A3_IT','ADM0_A3_NL','ADM0_A3_SE','ADM0_A3_BD','ADM0_A3_UA','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','LABEL_X','LABEL_Y','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FA','NAME_FR','NAME_EL','NAME_HE','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_UK','NAME_UR','NAME_VI','NAME_ZH','NAME_ZHT','FCLASS_ISO','TLC_DIFF','FCLASS_TLC','FCLASS_US','FCLASS_FR','FCLASS_RU','FCLASS_ES','FCLASS_CN','FCLASS_TW','FCLASS_IN','FCLASS_NP','FCLASS_PK','FCLASS_DE','FCLASS_GB','FCLASS_BR','FCLASS_IL','FCLASS_PS','FCLASS_SA','FCLASS_EG','FCLASS_MA','FCLASS_PT','FCLASS_AR','FCLASS_JP','FCLASS_KO','FCLASS_VN','FCLASS_TR','FCLASS_ID','FCLASS_PL','FCLASS_GR','FCLASS_IT','FCLASS_NL','FCLASS_SE','FCLASS_BD','FCLASS_UA'],
            'INPUT': outputs['FixGeometries']['OUTPUT'],
            'OUTPUT': parameters['Drop_fields_3']
        }
        outputs['DropFields'] = processing.run('native:deletecolumn', dropf_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Drop_fields_3'] = outputs['DropFields']['OUTPUT']
        
        ##################################################################
        # Zonal statistics Landq
        ##################################################################
        zonalsats1_dict= {
            'COLUMN_PREFIX': '_',
            'INPUT': 'outputs['DropFields']['OUTPUT']',
            'INPUT_RASTER': 'landquality_5b32bbbd_2181_4afc_bdeb_50443f09b1e2',
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Media
            'OUTPUT': parameters['Landq']
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatisticsfb', zonalsats1_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Landq'] = outputs['ZonalStatistics']['OUTPUT']
    
        ##################################################################
        # Zonal statistics Pop1800
        ##################################################################
        zonalstats2_dict = {
            'COLUMN_PREFIX': 'pop1800',
            'INPUT': outputs['ZonalStatistics']['OUTPUT'],
            'INPUT_RASTER': 'popd_1800AD_1e9d99da_c7b4_4557_b31b_ed22669a5bcf',
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Media
            'OUTPUT': parameters['Pop1800']
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatisticsfb', zonalstats2_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Pop1800'] = outputs['ZonalStatistics']['OUTPUT']
        
        ##################################################################
        # Zonal statistics Pop1900
        ##################################################################
        zonalstats3_dict = {
            'COLUMN_PREFIX': 'pop1900',
            'INPUT': 'outputs['ZonalStatistics']['OUTPUT'],
            'INPUT_RASTER': 'popd_1900AD_84dc9588_658f_4614_b603_abf941e71fb9',
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Media
            'OUTPUT': parameters['Pop1900']
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Pop1900'] = outputs['ZonalStatistics']['OUTPUT']

        ##################################################################
        # Zonal statistics
        ##################################################################
        zonalstats4_dict = {
            'COLUMN_PREFIX': 'pop2000',
            'INPUT': outputs['ZonalStatistics']['OUTPUT'],
            'INPUT_RASTER': 'popd_2000AD_79abad50_949e_4b1a_89f2_3828258fd12d',
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Media
            'OUTPUT': parameters['Pop2000']
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatisticsfb', zonalstats4_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Pop2000'] = outputs['ZonalStatistics']['OUTPUT']
       
 
        ##################################################################
        # Save vector features to file
        ##################################################################
        savef_dict = {
            'DATASOURCE_OPTIONS': '',
            'INPUT': outputs['ZonalStatistics']['OUTPUT'],
            'LAYER_NAME': '',
            'LAYER_OPTIONS': '',
            'OUTPUT': outpath + "/raster_stats.csv",
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SaveVectorFeaturesToFile'] = processing.run('native:savefeatures', savef_dict, context=context, feedback=feedback, is_child_algorithm=True)


    def name(self):
        return 'model3'

    def displayName(self):
        return 'model3'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model3()
print('DONE!')
