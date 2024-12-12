"""
Release notes view
"""
import json
from caerp.utils.sys_environment import resource_filename


def release_notes(request):
    # Récupération des notes de version depuis le fichier JSON
    release_notes_filepath = resource_filename("static/release_notes.json")
    with open(release_notes_filepath) as release_notes_file:
        data = json.load(release_notes_file)
    release_notes = data["release_notes"]
    # Traitement des données pour envoi au template
    i = 1
    for version in release_notes:
        version["version_code"] = version["version"].replace(".", "")
        version["is_last_version"] = i == 1
        version_notes = version.pop("changelog")
        version["enhancements"] = [
            note for note in version_notes if note["category"] == "enhancement"
        ]
        version["bugfixs"] = [
            note for note in version_notes if note["category"] != "enhancement"
        ]
        i = i + 1
    return dict(
        title="Notes de version",
        release_notes=release_notes,
    )


def includeme(config):
    config.add_route("release_notes", "/release_notes")
    config.add_view(
        release_notes,
        route_name="release_notes",
        renderer="release_notes.mako",
    )
