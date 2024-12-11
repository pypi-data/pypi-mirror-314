<%inherit file="/layouts/default.mako" />
<%block name='afteractionmenu'>

% if info_message != UNDEFINED:
<div>
	<div class="alert alert-success">
		<span class="icon"><svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#success"></use></svg></span> 
		${info_message|n}
	</div>
</div>
% endif
% if warn_message != UNDEFINED:
<div>
	<div class="alert alert-warning">
		<span class="icon"><svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#danger"></use></svg></span> 
		${warn_message|n}
	</div>
</div>
% endif
% if help_message != UNDEFINED:
<div>
	<div class='alert alert-info'>
	<span class="icon"><svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#info-circle"></use></svg></span> 
	${help_message|n}
	</div>
</div>
% endif
${request.layout_manager.render_panel('admin_index_nav', context=navigation)}
<%block name='afteradminmenu'>
</%block>
</%block>
