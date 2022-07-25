"""
Number of languages per country 
Model exported as python.
Name : model4a
Group : 
With QGIS : 32208
"""
#########################################################################################
#########################################################################################
# SETUP PREAMBLE FOR RUNNING STANDALONE SCRIPTS.
# NOT NECESSARY IF YOU ARE RUNNING THIS INSIDE THE QGIS GUI.

print ("setting up")
import sys
import os
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing

# paths to inputs and outputs
print ("setting paths") 
mainpath = "/Users/camilasury/Desktop/Herramientas computacionales/Python & QGIS/Input"
outpath = "/Users/camilasury/Desktop/Herramientas computacionales/Python & QGIS/Output"
wlds = "/Users/camilasury/Desktop/Herramientas computacionales/Python & QGIS/Output/clean.shp"
admin = "/Users/camilasury/Desktop/Herramientas computacionales/Python & QGIS/Input/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp"
outcsv = "/Users/camilasury/Desktop/Herramientas computacionales/Python & QGIS/Output/languages_by_country.csv"

#class definition 
class Model4a(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_wlds', 'fixgeo_wlds', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_countries', 'fixgeo_countries', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Intersection', 'intersection', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(4, model_feedback)
        results = {}
        outputs = {}
#########################################################
# Fix geometries - wlds
#########################################################  
print ("fixing geometries - languages")
        fxgeol_params = {
            'INPUT': wlds,
            'OUTPUT': parameters['Fixgeo_wlds']
        }
        outputs['FixGeometriesWlds'] = processing.run('native:fixgeometries', fxgeol_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_wlds'] = outputs['FixGeometriesWlds']['OUTPUT']

#########################################################
# Fix geometries - countries
#########################################################
print ("fixing geometries - countries")
        fxgeoc_direct = {
            'INPUT': admin,
            'OUTPUT': parameters['Fixgeo_countries']
        }
        outputs['FixGeometriesCountries'] = processing.run('native:fixgeometries', fxgeoc_direct, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_countries'] = outputs['FixGeometriesCountries']['OUTPUT']

#########################################################
# Intersection
#########################################################
print ("intersecting data") 
        intersect_dic = {
            'INPUT': results['Fixgeo_wlds'],
            'INPUT_FIELDS': 'GID',
            'OVERLAY': results['Fixgeo_countries'],
            'OVERLAY_FIELDS': 'ADMIN',
            'OVERLAY_FIELDS_PREFIX': '',
            'OUTPUT': parameters['Intersection']
        }
        outputs['Intersection'] = processing.run('native:intersection', intersect_dic, context=context, feedback=feedback, is_child_algorithm=True)
        results['Intersection'] = outputs['Intersection']['OUTPUT']
        return results

#########################################################
# Statistics by categories
#########################################################
print ("statistics by categories")
        stats_dict = {
            'CATEGORIES_FIELD_NAME': 'ADMIN',
            'INPUT': results['Intersection'],
            'VALUES_FIELD_NAME': '',
            'OUTPUT': outcsv
        }
        outputs['StatisticsByCategories'] = processing.run('qgis:statisticsbycategories', stats_dict, context=context, feedback=feedback, is_child_algorithm=True)

print('DONE!')
