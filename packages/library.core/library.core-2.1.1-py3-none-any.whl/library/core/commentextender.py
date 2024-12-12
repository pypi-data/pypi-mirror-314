from AccessControl import ClassSecurityInfo
from library.core.interfaces import ILibraryCoreLayer
from persistent import Persistent
from plone.app.discussion.browser.comments import CommentForm
from plone.app.discussion.comment import Comment
from plone.app.standardtiles import PloneMessageFactory as _
from plone.namedfile.field import NamedBlobImage
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.z3cform.fieldsets import extensible
from Products.CMFCore.permissions import View
from z3c.form.field import Fields
from zope.annotation import factory
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface

from zope.annotation.interfaces import IAnnotations



class ICommentExtenderFields(Interface):
    """Marker interface for comments.
    """

    picture = NamedBlobImage(
        title=_("Picture"),
        description=_("Picture to illustrate your comment"),
        required=False,
    )


# Persistent class that implements the ICommentExtenderFields interface
@adapter(Comment)
@implementer(ICommentExtenderFields, IImageScaleTraversable)
class CommentExtenderFields(Persistent):
    """" """
    # security = ClassSecurityInfo()
    # security.declareProtected(View, 'picture')

    def __init__(self, context):
        self.context = context  # Initialise le champ picture
        self.picture = context.picture

    def set_picture(self, value):
        self.picture = value

    def get_picture(self):
        import pdb;pdb.set_trace()
        return self.picture


#    def __init__(self, context):
#        self.context = context
#        import pdb;pdb.set_trace()
#        annotations = IAnnotations(self.context)
#        # Utilisation des annotations pour stocker l'image
#        self._picture_key = 'library.core.commentextender.picture'

#    @property
#    def picture(self):
#        annotations = IAnnotations(self.context)
#        return annotations.get(self._picture_key, None)

#    @picture.setter
#    def picture(self, value):
#        annotations = IAnnotations(self.context)
#        annotations[self._picture_key] = value



# CommentExtenderFields factory
CommentExtenderFactory = factory(CommentExtenderFields)


# context, request, form
@adapter(Interface, ILibraryCoreLayer, CommentForm)
class CommentExtender(extensible.FormExtender):

    fields = Fields(ICommentExtenderFields)

    def __init__(self, context, request, form):
        self.context = context
        self.request = request
        self.form = form

    def update(self):
        # Add the fields defined in ICommentExtenderFields to the form.
        self.add(ICommentExtenderFields, prefix="")
        # Move the picture field to the top of the comment form.
        self.move('picture', before='text', prefix="")
        #


@adapter(Comment, IImageScaleTraversable)
@implementer(IImageScaleTraversable)
def comment_image_scale_traversable(obj):
    import pdb;pdb.set_trace()
    # Cela permet de récupérer l'image pour l'URL @@images/comment_picture
    return obj