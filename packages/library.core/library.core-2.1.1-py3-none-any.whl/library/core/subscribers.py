from zope.component import adapter
from zope.lifecycleevent.interfaces import IObjectModifiedEvent, IObjectAddedEvent
# from plone.app.discussion.comment import Comment
from library.core.commentextender import CommentExtenderFields
from Products.CMFCore.utils import getToolByName


@adapter(CommentExtenderFields, IObjectModifiedEvent)
@adapter(CommentExtenderFields, IObjectAddedEvent)
def reindex_comment_picture(comment, event):
    print("subscriber")
    import pdb; pdb.set_trace()
    catalog = getToolByName(comment, 'portal_catalog')
    # Force la réindexation du champ 'comment_picture' pour le commentaire
    catalog.reindexObject(comment, idxs=['comment_picture'])