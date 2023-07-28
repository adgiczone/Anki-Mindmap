from aqt import mw
from anki.hooks import addHook

import os
import shutil
from .Template import EDITOR, FRONT, BACK, CSS

MODEL_NAME = "Anki_Mindmap"
FIELD_NAME = ["Mindmap", "Notes"]


def setup_editor(editor):
    """ This function runs when the user opens the editor, creates the markdown preview area """
    if editor.note.model()["name"] == MODEL_NAME:
        editor.web.eval(EDITOR)

addHook("loadNote", setup_editor)


def create_update_template():
    """
    Runs when the user opens Anki, creates the two card types and also handles updating
    the card types CSS and HTML if the addon has a pending update
    """
    model = mw.col.models.byName(MODEL_NAME)
    if not model:
        create_template()
    update_template()


def create_template():
    m = mw.col.models
    model = m.new(MODEL_NAME)

    for name in FIELD_NAME:
        m.addField(model, m.newField(name))

    template = m.newTemplate(MODEL_NAME)

    template["qfmt"] = FRONT
    template["afmt"] = BACK
    model["css"] = CSS

    m.addTemplate(model, template)
    m.add(model)
    m.save(model)


def update_template():
    model = mw.col.models.byName(MODEL_NAME)
    model["tmpls"][0]["qfmt"] = FRONT
    model["tmpls"][0]["afmt"] = BACK
    model["css"] = CSS

    mw.col.models.save(model)

    addonFolder = os.path.join(os.path.dirname(os.path.realpath(__file__)))
    assetsFolder = os.path.join(addonFolder, "assets")
    mediaFolder = mw.col.media.dir()
    for assetName in os.listdir(assetsFolder):
        assetFullPath = os.path.join(assetsFolder, assetName)
        if not os.path.exists(os.path.join(mediaFolder, assetName)):
            mw.col.media.add_file(assetFullPath)


addHook("profileLoaded", create_update_template)
