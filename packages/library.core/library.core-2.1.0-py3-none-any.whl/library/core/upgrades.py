from plone import api


def geolocation_behavior(context):
    context.runAllImportStepsFromProfile("profile-collective.faceted.map:default")
    context.runImportStepFromProfile("profile-library.core:default", "typeinfo")

def add_comment_picture_index(context):
    catalog = api.portal.get_tool("portal_catalog")    
    # Vérifie si l'index 'comment_picture' existe déjà
    if 'comment_picture' in catalog.indexes():
        return
    catalog.addIndex('comment_picture', 'FieldIndex')
    catalog.reindexIndex('comment_picture', context.REQUEST)