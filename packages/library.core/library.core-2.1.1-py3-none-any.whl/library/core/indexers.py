from plone.indexer import indexer
from plone.app.discussion.interfaces import IComment
from library.core.commentextender import ICommentExtenderFields

@indexer(IComment)
def comment_picture_indexer(obj):
    # Récupérer l'objet étendu contenant le champ picture    
    print("indexer")
    extender = ICommentExtenderFields(obj, None)
    import pdb;pdb.set_trace()
    if extender and extender.picture:        
        return extender.picture
    return None