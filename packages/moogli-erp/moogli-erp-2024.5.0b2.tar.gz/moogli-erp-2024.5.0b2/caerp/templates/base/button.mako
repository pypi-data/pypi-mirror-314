<%doc>
    Template used to render buttons (see utils/widgets.py)
</%doc>
% if not hasattr(elem, 'permitted') or elem.permitted(request.context, request):
    <a title='${elem.title}' href="${elem.url(request)}"
        %if elem.onclick():
            onclick="${elem.onclick()}"
        %endif
        % if hasattr(elem, "css") and elem.css:
            class="${elem.css}"
        % endif
        % if hasattr(elem, 'title'):
            title="${elem.title}"
        % endif
        >
        %if elem.icon:
            <svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#${elem.icon}"></use></svg>
        % endif
        ${elem.label}
    </a>
% endif
