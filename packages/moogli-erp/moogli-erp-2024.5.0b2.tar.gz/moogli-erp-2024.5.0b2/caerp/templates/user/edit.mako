<%inherit file="${context['main_template'].uri}" />
<%block name="mainblock">
${request.layout_manager.render_panel('help_message_panel', parent_tmpl_dict=context.kwargs)}
<div class="col-md-12">
    ${form|n}
</div>
</%block>
