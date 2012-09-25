from collective.plonetruegallery.utils import createSettingsFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from collective.plonetruegallery.browser.views.display import BaseDisplayType
from collective.plonetruegallery.interfaces import IBaseSettings
from zope import schema
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('collective.ptg.easyslider')

class IEasysliderDisplaySettings(IBaseSettings):
    easyslider_imagewidth = schema.Int(
        title=_(u"label_easyslider_imagewidth",
            default=u"Width of (each) image (when mouse hovers)"),
        default=400,
        min=50)
    easyslider_imageheight = schema.Int(
        title=_(u"label_easyslider_imageheight",
            default=u"Height of (each) image"),
        default=260,
        min=50)
    easyslider_use_icons = schema.Bool(
        title=_(u"label_easyslider_use_icons",
            default=u"Use Thumbnail size instead of Size"),
        default=False)
    easyslider_overlay_opacity = schema.Choice(
        title=_(u"label_easyslider_overlay_opacity",
                default=u"Opacity on mouse over"),
        default=0.3,
        vocabulary=SimpleVocabulary([
            SimpleTerm(0, 0,
                _(u"label_easyslider_overlay_opacity0",
                    default=u"0 Off")),
            SimpleTerm(0.1, 0.1,
                _(u"label_easyslider_overlay_opacity1",
                    default=u"0.1 Light")),
            SimpleTerm(0.2, 0.2,
                _(u"label_easyslider_overlay_opacity2", default=u"0.2")),
            SimpleTerm(0.3, 0.3,
                _(u"label_easyslider_overlay_opacity3", default=u"0.3")),
            SimpleTerm(0.4, 0.4,
                _(u"label_easyslider_overlay_opacity4",
                    default=u"0.4 Medium")),
            SimpleTerm(0.5, 0.5,
                _(u"label_easyslider_overlay_opacity5", default=u"0.5")),
            SimpleTerm(0.6, 0.6,
                _(u"label_easyslider_overlay_opacity6",
                    default=u"0.6")),
            SimpleTerm(0.7, 0.7,
                _(u"label_easyslider_overlay_opacity7",
                    default=u"0.7 Dark")),
            SimpleTerm(0.8, 0.8,
                _(u"label_easyslider_overlay_opacity8",
                    default=u"0.8 Very Dark")),
            SimpleTerm(0.9, 0.9,
                _(u"label_easyslider_overlay_opacity9",
                    default=u"0.9 Almost Black")),
            SimpleTerm(1, 1,
                _(u"label_easyslider_overlay_opacity10",
                    default=u"1 Pitch Dark")
            )
        ]))

    easyslider_style = schema.Choice(
        title=_(u"label_easyslider_style",
                default=u"What stylesheet (css file) to use"),
        default="style.css",
        vocabulary=SimpleVocabulary([
            SimpleTerm("style.css", "style.css",
                _(u"label_easyslider_style_default",
                    default=u"Default")),
            SimpleTerm("no_style.css", "no_style.css",
                _(u"label_easyslider_style_no",
                    default=u"No style / css file")),
            SimpleTerm("custom_style", "custom_style",
                _(u"label_easyslider_style_custom",
                    default=u"Custom css file")
            )
        ]))

    easyslider_custom_style = schema.TextLine(
        title=_(u"label_custom_style",
            default=u"Name of Custom css file if you chose that above"),
        default=u"mycustomstyle.css")


class EasysliderDisplayType(BaseDisplayType):
    name = u"easyslider"
    schema = IEasysliderDisplaySettings
    description = _(u"label_easyslider_display_type",
        default=u"Easyslider")

    def javascript(self):
        return u"""
<script type="text/javascript"
src="%(portal_url)s/++resource++ptg.easyslider/easySlider.js">
</script>
     <script type="text/javascript">
$(document).ready(function(){	
	$("#slider").easySlider({
		auto: true,
		continuous: true 
	});
});
</script>

""" % {
         'boxheight': self.settings.easyslider_imageheight,
         'boxwidth': self.settings.easyslider_imagewidth,
         'speed': self.settings.duration,
    }

    def css(self):
        relpath = '++resource++ptg.easyslider'
        style = '%s/%s/%s' % (self.portal_url, relpath,
            self.settings.easyslider_style)

        if self.settings.easyslider_style == 'custom_style':
            style = '%s/%s' % (self.portal_url,
                self.settings.easyslider_custom_style)

        return u"""
        <style>
.easyslider {
    height: %(boxheight)ipx;
    width: %(boxwidth)ipx;
}

.easyslider a div {
    background-color: rgba(15, 15, 15, %(overlay_opacity)f);
}

</style>
<link rel="stylesheet" type="text/css" href="%(style)s"/>
""" % {
        'columns': self.settings.easyslider_columns,
        'boxheight': self.settings.easyslider_imageheight,
        'boxwidth': self.settings.easyslider_imagewidth,
        'overlay_opacity': self.settings.easyslider_overlay_opacity,
        'style': style
       }
EasysliderSettings = createSettingsFactory(EasysliderDisplayType.schema)
