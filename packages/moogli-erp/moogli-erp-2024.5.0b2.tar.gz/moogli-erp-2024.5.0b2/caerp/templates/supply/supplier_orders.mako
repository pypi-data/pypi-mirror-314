<%inherit file="${context['main_template'].uri}" />
<%namespace file="/base/utils.mako" import="dropdown_item"/>
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%namespace file="/base/searchformlayout.mako" import="searchform"/>

<%block name='actionmenucontent'>
    % if api.has_permission('context.add_supplier_order') and not is_admin_view:
        <div class='layout flex main_actions'>
            <a class='btn btn-primary'
               href="${request.route_path('/companies/{id}/supplier_orders', _query=dict(action='new'),  id=request.context.id)}"
            >
                <svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#plus"></use></svg>Ajouter une commande<span class="no_mobile">&nbsp;fournisseur</span>
            </a>
        </div>

    % endif
</%block>
<%block name='content'>

    ${searchform()}
    <% is_search_filter_active = '__formid__' in request.GET %>
    <div>
        <div>
            ${records.item_count} Résultat(s)
        </div>
        <div class='table_container'>
            ${request.layout_manager.render_panel('supplier_order_list', records, is_admin_view=is_admin_view, stream_actions=stream_actions)}
            ${pager(records)}
        </div>
    </div>
</%block>
<%block name='footerjs'>
    $(function(){
    $('input[name=search]').focus();
    });
</%block>
