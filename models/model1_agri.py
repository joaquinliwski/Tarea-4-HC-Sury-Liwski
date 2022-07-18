"""
Model exported as python.
Name : model1
Group : 
With QGIS : 32208
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Model1(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Zonal', 'Zonal', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': '_',
            'INPUT': 'Incremented_b0012913_9fb5_4aef_970b_37b9b1367c23',
            'INPUT_RASTER': 'OUTPUT_b005dbd3_72d7_4d6d_a897_ced797253c26',
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Mean
            'OUTPUT': parameters['Zonal']
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Zonal'] = outputs['ZonalStatistics']['OUTPUT']
        return results

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
