<%inherit file="${context['main_template'].uri}" />

<%block name="content">
<div class="alert alert-info">
    <p>
        <small>
            Légende&nbsp;:
            <strong><span class="icon tag neutral" title="Financé par Nom">
                <svg><use href="../static/icons/endi.svg#euro-sign"></use></svg>
                <span class="screen-reader-text">Financé par</span> Nom
            </span></strong>
            Nom du ou des financeurs de l’évolution ou de la correction.
        </small>
    </p>
</div>
% for version in release_notes:
    <%
    if version['is_last_version']:
        visibility = ""
        expanded = "true"
        tooltip = "Masquer cette version"
    else:
        visibility = "hidden"
        expanded = "false"
        tooltip = "Afficher cette version"
    %>
    <div class="version collapsible">
        <div class="separate_block">
            <h2 class="title collapse_title">
                <a href="javascript:void(0);" onclick="toggleCollapse( this );" aria-expanded="${expanded}" title="${tooltip}" aria-label="${tooltip}">
                    ${api.icon("chevron-down", "arrow")}
                    Version ${version["version"]} <small>${version["date"]}</small>
                </a>
            </h2>
            <div class="collapse_content" ${visibility}>
                <div class="content">
                % for notes in (version["enhancements"], version["bugfixs"]):
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
                                        <span class="icon">${api.icon("link")}</span>
                                        <a class="note_link" href="${note['link']['url']}" target="_blank">${note["link"]['title']}</a>
                                    % endif
                                </li>
                            % endfor
                            </ul>
                    % endif
                % endfor
                </div>
            </div>
        </div><!-- div.separate_block -->
    </div>
% endfor
</%block>
