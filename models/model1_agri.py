"""
Agricultural Suitability
Model exported as python.
Name : model1
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
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsCoordinateReferenceSystem
import processing
#########################################################################################
# paths to inputs and outputs
mainpath = "/Users/camilasury/Desktop/Herramientas computacionales/Python & QGIS/Input"
outpath = "/Users/camilasury/Desktop/Herramientas computacionales/Python & QGIS/Output"
suit = "/Users/camilasury/Desktop/Herramientas computacionales/Python & QGIS/Input/SUIT/suit/hdr.adf"
adm2 = "gadm41_USA_shp/gadm41_USA_2.shp"

#define class
class Model1(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterDestination('Agrisuit', 'agrisuit', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Counties', 'counties', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Zonal', 'Zonal', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(4, model_feedback)
        results = {}
        outputs = {}
        ##################################################################
        # Warp (reproject) the raster
        ##################################################################
        reproj_dict = {
            'DATA_TYPE': 0,  # Use Input Layer Data Type
            'EXTRA': '',
            'INPUT': suit,
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'RESAMPLING': 0,  # Nearest Neighbour
            'SOURCE_CRS': None,
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:4326'),
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': parameters['Agrisuit']
        }
        outputs['WarpReproject'] = processing.run('gdal:warpreproject', reproj_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Agrisuit'] = outputs['WarpReproject']['OUTPUT']

        ##################################################################
        # Drop field(s)
        ##################################################################
        dropf_dict = {
            'COLUMN': ['GID_0','NAME_0','GID_1','GID_2','HASC_2','CC_2','TYPE_2','NL_NAME 2','VARNAME_2','NL_NAME_1','NL_NAME_2',' ENGTYPE_2\n'],
            'INPUT': mainpath + adm2,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DropFields'] = processing.run('native:deletecolumn', dropf_dict, context=context, feedback=feedback, is_child_algorithm=True)

  
        ##################################################################
        # Add autoincremental field
        ##################################################################
        addautoinc_dict = {
            'FIELD_NAME': 'cid',
            'GROUP_FIELDS': [''],
            'INPUT': outputs['DropFields']['OUTPUT'],
            'MODULUS': 0,
            'SORT_ASCENDING': True,
            'SORT_EXPRESSION': '',
            'SORT_NULLS_FIRST': False,
            'START': 1,
            'OUTPUT': parameters['Counties']
        }
        outputs['AddAutoincrementalField'] = processing.run('native:addautoincrementalfield', addautoinc_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Counties'] = outputs['AddAutoincrementalField']['OUTPUT']
        return results
    
        ##################################################################
        # Zonal statistics calculation
        ##################################################################
        zonalstats_dict = {
            'COLUMN_PREFIX': '_',
            'INPUT': outputs['AddAutoincrementalField']['OUTPUT'],
            'INPUT_RASTER': 'OUTPUT_b005dbd3_72d7_4d6d_a897_ced797253c26',
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Mean
            'OUTPUT': parameters['Zonal']
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatisticsfb', zonalstats_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Zonal'] = outputs['ZonalStatistics']['OUTPUT']


    def name(self):
        return 'model1'

    def displayName(self):
        return 'model1'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model1()
    
print('DONE!')
