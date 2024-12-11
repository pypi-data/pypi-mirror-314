<%doc>
    Administration des rôles de l'application
</%doc>
<%inherit file="${context['main_template'].uri}" />
<%block name='actionmenucontent'>
    <div class='layout flex main_actions'>
        % if addurl is not UNDEFINED and addurl is not None:
        <a class='btn btn-primary' href="${addurl}" title="Ajouter un nouveau rôle dans l'application">
            ${api.icon('plus')} Ajouter un rôle
        </a>
        % endif
        % if actions is not UNDEFINED:
        <div role="group">
            % for link in actions:
            ${request.layout_manager.render_panel(link.panel_name, context=link)}
            % endfor
        </div>
        % endif
    </div>
</%block>

<%block name='content'>
    % for group in items:
    <% data=stream_columns(group) %>
        % if loop.first:
        <% className='collapsible' %>
            % else:
            <% className='collapsible separate_top' %>
                % endif
                <div class='${className}'>
                    <h4 class="collapse_title">
                        <a href="javascript:void(0);" onclick="toggleCollapse( this );" aria-expanded="false"
                            accesskey="R" title="Masquer les champs de recherche"
                            aria-label="Afficher le détail des droits de ce rôle">
                            ${group.label}
                            ${api.icon('chevron-down')}
                        </a>
                        % for account_type in data["account_types"]:
                        <span class='icon tag neutral'
                            title="Ce compte est proposé à la création d'un compte : ${account_type}"><small>${account_type}</small></span>
                        % endfor
                        <small>(${data['user_count']} utilisateur(s) disposent de ce rôle)</small>
                        % if not group.editable:
                        <span class='icon tag neutral' title="Ce rôle n'est pas modifiable">${api.icon('lock')}</span>
                        % endif
                    </h4>
                    <div class="collapse_content" hidden="">
                        <div class="content_vertical_padding capabilities">
                            % if group.name =='admin':
                            <div class="alert alert-warning">
                                Seul un membre du groupe admin peut créer des comptes de ce groupe
                            </div>
                            % endif
                            <div class="layout flex two_cols content_vertical_padding">
                                <h3 class="vertical_align_center">Droits de ce rôle&nbsp;:</h3>
                                <div class="align_right vertical_align_center">
                                    ${request.layout_manager.render_panel("action_buttons", stream_actions(group))}
                                </div>
                            </div>

                            % for category in categories.values():
                            % if category in data['rights']:
                            <% rights=data['rights'][category] %>
                                <div>
                                    <h4>
                                        ${api.icon('cog')}
                                        ${category}
                                    </h4>
                                    <ul>
                                        % for right in rights:
                                        <li>
                                            <strong>
                                                ${right['label']}
                                                % if right.get('rgpd'):
                                                <span class="icon tag caution"
                                                    title="Ce droit donne accès à des données personnelles sensibles">RGPD
                                                    <span class="screen-reader-text">Ce droit donne accès à des données
                                                        personnelles sensibles</span>
                                                </span>
                                                % endif
                                            </strong>
                                            <small>${right['description']}</small>
                                        </li>
                                        % endfor
                                    </ul>
                                </div>
                                % endif
                                % endfor
                        </div>
                    </div>
                </div>
                % endfor
</%block>
