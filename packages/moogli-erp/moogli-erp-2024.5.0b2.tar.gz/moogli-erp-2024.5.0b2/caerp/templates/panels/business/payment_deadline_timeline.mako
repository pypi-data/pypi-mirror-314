   <div class="content_vertical_padding">
        <h3>Facturation</h3>
        % if len(request.context.estimations) > 0:
        <p>
            <em>Reste à facturer : ${api.format_amount(to_invoice, precision=5) | n}&nbsp;€ HT</em>
        </p>
        % endif 
        <div class="timeline">
            <ul>
                % for item in items:
                    ${request.layout_manager.render_panel(
                        "timeline_item", 
                        context=item, 
                        business=request.context
                    )}                    
                % endfor
            </ul>
        </div>
    </div>