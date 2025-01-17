"""
Agricultural Suitability
Model exported as python.
Name : model2
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
from qgis.core import QgsCoordinateReferenceSystem
import processing
#########################################################################################
#########################################################################################

# paths to inputs and outputs
mainpath = "/Users/camilasury/Desktop/Herramientas computacionales/Python & QGIS/Input"
outpath = "/Users/camilasury/Desktop/Herramientas computacionales/Python & QGIS/Output"

suit = "{}/SUIT/suit/hdr.adf".format(mainpath)


#class definition
class Model2(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterDestination('Suitout', 'suitout', createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
        results = {}
        outputs = {}
        ##################################################################
        # Warp (reproject) suitability (hdr.adf)
        ##################################################################
        reproject_dict = {
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
            'OUTPUT': parameters['Suitout']
        }
        outputs['WarpReproject'] = processing.run('gdal:warpreproject', reproject_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Suitout'] = outputs['WarpReproject']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}
        ##################################################################
        # Extract projection
        ##################################################################        
        extract_dict = {
            'INPUT': outputs['WarpReproject']['OUTPUT'],
            'PRJ_FILE_CREATE': True
        }
        outputs['ExtractProjection'] = processing.run('gdal:extractprojection', extract_dict, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return 'model2'

    def displayName(self):
        return 'model2'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model2()
    
print('DONE!')
