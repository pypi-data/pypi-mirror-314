<div class="alert alert-info">
    <p>
        Vous accédez pour la première fois à la nouvelle version d’enDI, voici la liste des nouveautés.
    </p>
    <p>
        Vous pouvez à tout moment retrouver ces informations dans le menu <strong>Aide</strong> &gt; <strong>Notes de version</strong>.
    </p>
    <p>
        <small>
            <br>Légende&nbsp;:
            <strong><span class="icon tag neutral" title="Financé par Nom">
                <svg><use href="../static/icons/endi.svg#euro-sign"></use></svg>
                <span class="screen-reader-text">Financé par </span>Nom
            </span></strong>
            Nom du ou des financeurs de l’évolution ou de la correction.
        </small>
    </p>
</div>

% for notes in (enhancements, bugfixs):
    % if len(notes) > 0:
        % if notes[0]["category"] == "enhancement":
            <h3>
                <span class="icon">${api.icon("star")}</span>
                Évolutions
            </h3>
        % else:
            <h3>
                <span class="icon">${api.icon("wrench")}</span>
                Corrections
            </h3>
        % endif
            <ul class="version_notes">
            % for note in notes:
                <li>
                    <h4>
                        ${note["title"]}
                        % for sponsor in note["sponsors"]:
                            <span class="icon tag neutral" title="Financé par ${sponsor}">${api.icon("euro-sign")}<span class="screen-reader-text">Financé par</span> ${sponsor}</span>
                        % endfor
                    </h4>
                    % for description in note["description"]:
                        % if len(note["description"]) > 1:
                            <p class="note_description">&bull; ${description}</p>
                        % else:
                            <p class="note_description">${description}</p>
                        % endif
                    % endfor
                    % if "link" in note:
                        <a class="note_link" href="${note['link']['url']}" target="_blank">${note["link"]['title']}</a>
                    % endif
                </li>
            % endfor
            </ul>
    % endif
% endfor
