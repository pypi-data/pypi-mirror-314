# -*- coding: utf-8 -*-
from datetime import datetime
from plone import api
from plone.dexterity.browser import add
from plone.dexterity.browser import edit
from Products.Five import BrowserView
from redturtle.bandi import bandiMessageFactory as _
from redturtle.bandi.interfaces import IBandoFolderDeepening
from z3c.form import field
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import Interface
from zope.schema.interfaces import IVocabularyFactory

try:
    from plone.restapi.serializer.utils import uid_to_url
    from plone.restapi.serializer.converters import json_compatible

    HAS_PLONERESTAPI = True
except ImportError:
    HAS_PLONERESTAPI = False


class AddForm(add.DefaultAddForm):
    def updateWidgets(self):
        add.DefaultAddForm.updateWidgets(self)

        for group in self.groups:
            if group.label == "Settings":
                manager = field.Fields(group.fields)
                group.fields = manager.select(
                    "IShortName.id",
                    "IAllowDiscussion.allow_discussion",
                    "IExcludeFromNavigation.exclude_from_nav",
                    "ITableOfContents.table_of_contents",
                )


class AddView(add.DefaultAddView):
    form = AddForm


class EditForm(edit.DefaultEditForm):
    def updateWidgets(self):
        edit.DefaultEditForm.updateWidgets(self)

        for group in self.groups:
            if group.label == "Settings":
                manager = field.Fields(group.fields)
                group.fields = manager.select(
                    "IShortName.id",
                    "IAllowDiscussion.allow_discussion",
                    "IExcludeFromNavigation.exclude_from_nav",
                    "ITableOfContents.table_of_contents",
                )


class EditView(edit.DefaultEditView):
    form = EditForm


class IBandoView(Interface):
    pass


@implementer(IBandoView)
class BandoView(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.voc_tipologia = getUtility(
            IVocabularyFactory, name="redturtle.bandi.tipologia.vocabulary"
        )(self.context)

    def retrieveFolderDeepening(self):
        """Retrieves all Folder Deppening objects contained in Structured Document"""
        struct_doc = self.context
        values = []
        dfolders = struct_doc.getFolderContents(
            contentFilter={"object_provides": IBandoFolderDeepening.__identifier__}
        )
        for df in dfolders:
            if not df.exclude_from_nav:
                values.append(
                    dict(
                        title=df.Title,
                        description=df.Description,
                        url=df.getURL(),
                        path=df.getPath(),
                    )
                )
        return values

    def retrieveContentsOfFolderDeepening(self, path_dfolder):
        """Retrieves all objects contained in Folder Deppening"""

        values = []
        brains = self.context.portal_catalog(
            path={"query": path_dfolder, "depth": 1},
            sort_on="getObjPositionInParent",
        )
        siteid = api.portal.get().getId()
        for brain in brains:
            if not brain.getPath() == path_dfolder and not brain.exclude_from_nav:
                effective = brain.effective
                if effective.year() == 1969:
                    # content not yet published
                    effective = None
                dictfields = dict(
                    title=brain.Title,
                    description=brain.Description,
                    url=brain.getURL(),
                    path=brain.getPath(),
                    effective=effective,
                    modified=brain.modified,
                )
                if brain.Type == "Link":
                    dictfields["url"] = brain.getRemoteUrl
                    # resolve /resolveuid/... to url
                    # XXX: ma qui non funziona perchè il path è /Plone/resolveuid/...
                    # mentre la regex di uid_to_url si aspetta /resolveuid/... o
                    # ../resolveuid/...
                    # dictfields["url"] = uid_to_url(dictfields["url"])
                    # XXX: bug di Link ? in remoteUrl per i link interni nei brain
                    # c'è il path completo (con /Plone) invece che una url
                    # probabilmente legato al fatto che i link ora sono creati via
                    # api e non da interfaccia Plone (?)
                    if dictfields["url"].startswith(f"/{siteid}"):
                        dictfields["url"] = dictfields["url"][len(siteid) + 1 :]
                        if HAS_PLONERESTAPI:
                            dictfields["url"] = uid_to_url(dictfields["url"])
                elif brain.Type == "File":
                    obj_file = brain.getObject().file
                    if obj_file:
                        dictfields["url"] = (
                            f"{brain.getURL()}/@@download/file/{obj_file.filename}"  # noqa E501
                        )
                        obj_size = obj_file.size
                        dictfields["filesize"] = self.getSizeString(obj_size)
                # else:
                #     dictfields["url"] = brain.getURL() + "/view"
                dictfields["content-type"] = brain.mime_type
                # icon = getMultiAdapter((self.context, self.request, obj), IContentIcon)
                # dictfields['icon'] = icon.html_tag()
                dictfields["type"] = brain.Type

                if HAS_PLONERESTAPI:
                    dictfields = json_compatible(dictfields)
                values.append(dictfields)

        return values

    def getSizeString(self, size):
        const = {"kB": 1024, "MB": 1024 * 1024, "GB": 1024 * 1024 * 1024}
        order = ("GB", "MB", "kB")
        smaller = order[-1]
        if not size:
            return "0 %s" % smaller

        if size < const[smaller]:
            return "1 %s" % smaller
        for c in order:
            if int(size / const[c]) > 0:
                break
        return "%.2f %s" % (float(size / float(const[c])), c)

    def getDestinatariNames(self):
        """
        Return the values of destinatari vocabulary
        """
        dest_utility = getUtility(
            IVocabularyFactory, "redturtle.bandi.destinatari.vocabulary"
        )
        destinatari = self.context.destinatari
        if not dest_utility:
            return destinatari
        dest_values = []
        dest_vocab = dest_utility(self.context)
        for dest in destinatari:
            try:
                dest_title = dest_vocab.getTerm(dest).title
            except LookupError:
                dest_title = dest
            dest_values.append(dest_title)
        return dest_values

    def getEffectiveDate(self):
        """
        Return effectiveDate
        """
        plone = getMultiAdapter((self.context, self.request), name="plone")
        # da sistemare meglio questa parte
        # restituisce la prima data possibile quando questa non è presente
        time = self.context.effective()

        # controllo che EffectiveDate torni il valore stringa None, se cosi significa che non e stata settata la data di pubblicazione
        # se cosi allora torna None
        if self.context.EffectiveDate() == "None":
            return None
        else:
            return plone.toLocalizedTime(time)

    def getDeadLinePartecipationDate(self):
        """
        Return deadline partecipation date
        """
        date = self.context.scadenza_bando
        long_format = date.strftime("%H:%M:%S") != "00:00:00"
        return api.portal.get_localized_time(datetime=date, long_format=long_format)

    def getOpenDate(self):
        """
        Return deadline partecipation date
        """
        date = self.context.apertura_bando
        long_format = date.strftime("%H:%M:%S") != "00:00:00"
        return api.portal.get_localized_time(datetime=date, long_format=long_format)

    def getAnnouncementCloseDate(self):
        """
        Return Annoucement close date
        """
        time = self.context.chiusura_procedimento_bando
        return time.strftime("%d/%m/%Y")

    def getBandoState(self):
        """
        return right bando state
        """
        apertura_bando = getattr(self.context, "apertura_bando", None)
        scadenza_bando = getattr(self.context, "scadenza_bando", None)
        chiusura_procedimento_bando = getattr(
            self.context, "chiusura_procedimento_bando", None
        )

        if apertura_bando:
            apertura_tz = getattr(apertura_bando, "tzinfo", None)
            if apertura_bando > datetime.now(apertura_tz):
                return ("scheduled", translate(_("Scheduled"), context=self.request))
        state = ("open", translate(_("Open"), context=self.request))
        if not scadenza_bando and not chiusura_procedimento_bando:
            return state
        scadenza_tz = getattr(scadenza_bando, "tzinfo", None)
        if scadenza_bando and scadenza_bando < datetime.now(scadenza_tz):
            if chiusura_procedimento_bando and (
                chiusura_procedimento_bando < datetime.now().date()
            ):
                state = (
                    "closed",
                    translate(_("Closed"), context=self.request),
                )
            else:
                state = (
                    "inProgress",
                    translate(_("In progress"), context=self.request),
                )
        elif chiusura_procedimento_bando and (
            chiusura_procedimento_bando < datetime.now().date()
        ):
            state = ("closed", translate(_("Closed"), context=self.request))
        return state
