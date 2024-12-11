<%doc>
 Task list panel template
</%doc>
<%namespace file="/base/utils.mako" import="format_text" />
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/utils.mako" import="format_customer" />
<%namespace file="/base/utils.mako" import="format_project" />
<%namespace file="/base/utils.mako" import="table_btn"/>
<%def name='timeslot_row(event)'>
    <% workshop = event.workshop %>
    <% url = request.route_path('workshop', id=workshop.id) %>
    <% onclick = "document.location='{url}'".format(url=url) %>
        <td class="col_icon" onclick="${onclick}">
			<span class="icon">${api.icon('chalkboard-teacher')}</span><br>
			Atelier
        </td>
        <td class="col_date" onclick="${onclick}">
            ${api.format_datetime(event.start_time)}
        </td>
        <td class="col_text" onclick="${onclick}">
            ${', '.join(i.label for i in workshop.trainers)}
        </td>
        <td class="col_text">
            <a href="${url}">${workshop.name} (${event.name})</a>
        </td>
</%def>
<%def name='activity_row(event)'>
    <% url = request.route_path('activity', id=event.id) %>
    <% onclick = "document.location='{url}'".format(url=url) %>
        <td class="col_icon" onclick="${onclick}">
			<span class="icon">${api.icon('calendar-alt')}</span><br>
            Rendez-vous
        </td>
        <td class="col_date" onclick="${onclick}">
            ${api.format_datetime(event.datetime)}
        </td>
        <td class="col_text" onclick="${onclick}">
            ${', '.join([api.format_account(conseiller) for conseiller in event.conseillers])}
        </td>
        <td class="col_text">
        	<a href="${url}">
            % if event.type_object is not None:
            	${event.type_object.label}
            % endif
             (${event.mode})
            </a>
        </td>
</%def>
<div class='dash_elem'>
    <h2>
		<span class='icon'>${api.icon('calendar-alt')}</span>
		<span>${title}</span>
    </h2>
    <div class='panel-body'>
     	<p style="display: none;">
			Afficher <select id='number_of_events'>
			  % for i in (5, 10, 15, 50):
			  <option value='${i}'
			  % if events.items_per_page == i:
				selected=true
			  % endif
			  >
			  ${i}
			  </option>
			  % endfor
			</select>
			éléments à la fois
		</p>
        <table class='hover_table'>
            <thead>
                <th scope="col">
                    Type
                </th>
                <th scope="col" class="col_date" title="Date de début">
                    Date<span class="screen-reader-text"> de début</span>
                </th>
                <th scope="col" class="col_text">
                    Accompagnateur ou Animateur
                </th>
                <th scope="col" class="col_text">
                    Intitulé
                </th>
            </thead>
            <tbody>
                % for event in events:
                    % if event.type_ == 'activity':
                    <tr title="Cliquer pour voir le détail du rendez-vous">
                        ${activity_row(event)}
                    % elif event.type_ == 'timeslot':
                    <tr title="Cliquer pour voir le détail de l’atelier">
                        ${timeslot_row(event)}
                    % else:
                    <tr title="Cliquer pour voir le détail">
                        ${event.type_}
                    % endif
                    </tr>
                % endfor
            </tbody>
        </table>
    </div>
</div>
