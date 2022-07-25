"""
Languages SHP 
Model exported as python.
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
from qgis.core import QgsProcessingParameterFeatureSink
import processing
#########################################################################################
#########################################################################################

# paths to inputs and outputs
mainpath = "/Users/camilasury/Desktop/Herramientas computacionales/Python & QGIS/Input"
outpath = "/Users/camilasury/Desktop/Herramientas computacionales/Python & QGIS/Output"

langa = mainpath + "/langa/langa.shp"

#model class definition
class Model1(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Autoinc_id', 'autoinc_id', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Wldsout', 'wldsout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Length', 'length', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Field_calc', 'field_calc', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Output_menor_a_11', 'OUTPUT_menor_a_11', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fix_geo', 'fix_geo', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(6, model_feedback)
        results = {}
        outputs = {}
        
        ##################################################################
        # Fix geometries
        ##################################################################
        fixgeo_dict = {
            'INPUT': langa,
            'OUTPUT': parameters['Fix_geo']
        }
        outputs['FixGeometries'] = processing.run('native:fixgeometries', fixgeo_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fix_geo'] = outputs['FixGeometries']['OUTPUT']
        
        ##################################################################
        # Add autoincremental field Id per country
        ##################################################################
        add_autoinc_dict = {
            'FIELD_NAME': 'GID',
            'GROUP_FIELDS': [''],
            'INPUT': outputs['FixGeometries']['OUTPUT'],
            'MODULUS': 0,
            'SORT_ASCENDING': True,
            'SORT_EXPRESSION': '',
            'SORT_NULLS_FIRST': False,
            'START': 1,
            'OUTPUT': parameters['Autoinc_id']
        }
        outputs['AddAutoincrementalField'] = processing.run('native:addautoincrementalfield', add_autoinc_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Autoinc_id'] = outputs['AddAutoincrementalField']['OUTPUT']
        return results
        
        ##################################################################
        # Field calculator, length ofcharacters
        ##################################################################
        fieldcalc2_dict = {
            'FIELD_LENGTH': 2,
            'FIELD_NAME': 'length',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': 'length(NAME_PROP)',
            'INPUT': outputs['AddAutoincrementalField']['OUTPUT'],
            'OUTPUT': parameters['Length']
        }
        outputs['FieldCalculator'] = processing.run('native:fieldcalculator', fieldcalc2_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Length'] = outputs['FieldCalculator']['OUTPUT']
        
        ##################################################################
        # Feature filter, less than 11 characters
        ##################################################################
        featurefilter_dict = {
            'INPUT':  outputs['FieldCalculator']['OUTPUT'],
            'OUTPUT_menor_a_11': parameters['Output_menor_a_11']
        }
        outputs['FeatureFilter'] = processing.run('native:filter', featurefilter_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Output_menor_a_11'] = outputs['FeatureFilter']['OUTPUT_menor_a_11']

        ##################################################################
        # Field calculator clone, create NAME_PROP if less than 11 characters
        ##################################################################
        fieldcalc1_dict = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'lnm',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # String
            'FORMULA': '"NAME_PROP"',
            'INPUT': outputs['FeatureFilter']['OUTPUT_menor_a_11'],
            'OUTPUT': parameters['Field_calc']
        }
        outputs['FieldCalculatorClone'] = processing.run('native:fieldcalculator', fieldcalc1_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Field_calc'] = outputs['FieldCalculatorClone']['OUTPUT']
      
        ##################################################################
        # Drop field(s)
        ##################################################################
        dropf_dict = {
            'COLUMN': ['ID_ISO_A3','ID_ISO_A2','ID_FIPS','NAM_LABEL','NAME_PROP','NAME2','NAM_ANSI','CNT','C1','POP','LMP_POP1','G','LMP_CLASS','FAMILYPROP','FAMILY','langpc_km2','length'],
            'INPUT': outputs['FieldCalculatorClone']['OUTPUT'],
            'OUTPUT': parameters['Wldsout']
        }
        outputs['DropFields'] = processing.run('native:deletecolumn', dropf_dict, context=context, feedback=feedback, is_child_algorithm=True)
        results['Wldsout'] = outputs['DropFields']['OUTPUT']


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
