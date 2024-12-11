## Business PPayment deadline représenté comme item d'une timeline
## 
<li> 
    <blockquote class="${status_css}">
        <span class="icon status ${status_css}" role="presentation">
            ${api.icon(icon)}
        </span>
        <div>
            <h5>${title}</h5>
            <div class='layout flex'>
                <p>
                    ${date_string | n} :                
                    ${api.format_amount(task.ttc, precision=5) | n}&nbsp;€&nbsp;TTC
                    (${api.format_amount(task.ht, precision=5) | n}&nbsp;€&nbsp;HT)
                    <br />
                    ${description}
                </p>
                <div class="btn-container">
                % for link in main_links:
                    ${request.layout_manager.render_panel(link.panel_name, context=link)}
                % endfor
                </div>
            </div>
        </div>
    </blockquote>
</li>