<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <%block name="header">
      % if not title is UNDEFINED:
        <title>${title} - MoOGLi</title>
      % else:
        <title>MoOGLi</title>
      % endif
      <link rel="apple-touch-icon" sizes="180x180" href="${request.static_url('caerp:static/favicons/apple-touch-icon.png')}">
      <link rel="icon" type="image/png" sizes="32x32" href="${request.static_url('caerp:static/favicons/favicon-32x32.png')}">
      <link rel="icon" type="image/png" sizes="16x16" href="${request.static_url('caerp:static/favicons/favicon-16x16.png')}">
      <link rel="manifest" href="${request.static_url('caerp:static/favicons/site.webmanifest')}">
      <link rel="mask-icon" href="${request.static_url('caerp:static/favicons/safari-pinned-tab.svg')}" color="#000000">
      <link rel="shortcut icon" href="${request.static_url('caerp:static/favicons/favicon.ico')}">
      <meta name="msapplication-TileColor" content="#2b5797">
      <meta name="msapplication-config" content="${request.static_url('caerp:static/favicons/browserconfig.xml')}">
      <meta name="theme-color" content="#ffffff">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <meta name="robots" content="noindex">
    </%block>
    <%block name="headjs" />
    <%block name="css" />
  </head>
  <body class="caerp theme_manage_people ${request.matched_route.name if request.matched_route else 'default'}-view preload
  % if request.is_popup:
    caerp_popup
  % endif
  ">
  % if not request.is_popup:
  <div id="vue-notification-header_message-app" class='notification'></div>
  % endif

    % if not request.is_popup:
    <div class="access_tools" role="navigation" aria-label="page" tabindex="-1" accesskey="I">
	  <a href="#target_content"><span>Aller au contenu</span> <em>C</em></a>
	  <a href="#target_menu"><span>Aller au menu</span> <em>M</em></a>
	  <a href="#company-select-menu"><span>Aller au sélecteur d’enseigne</span> <em>E</em></a>
	  <a href="javascript:void(0);" onclick="toggleOpen('user_menu_wrapper',document.getElementById('user_menu_display_btn'));this.blur();"><span>Déplier/Replier le menu utilisateur</span> <em>U</em></a>
	  <a class="no_tablet" href="javascript:void(0);" onclick="resize('menu',document.getElementById('menu_size_btn'));this.blur();"><span><span class="menu_maxi">Re</span><span class="menu_mini">Dé</span>plier la barre latérale</span> <em>F</em></a>
	  <a class="no_desktop" href="#sidebar_display_btn"><span>Replier/Déplier la barre latérale</span> <em>S</em></a>
	  <a href="javascript:void(0);"><span>Replier/Déplier la recherche</span> <em>R</em></a>
	  <a href="javascript:void(0);" onclick="this.blur();"><span>Ce bloc de raccourcis</span> <em>I</em></a>
	</div>
    % endif
    <div class="base_layout layout flex screen">

      % if not request.is_popup:
        <div id="caerp_base_menu" class="base_menu flex">
          <ul class="menu_tools">
            <li class="menu_show">
              <button id="sidebar_display_btn" onclick="toggleOpen('caerp_base_menu');" title="Afficher le menu" aria-label="Afficher le menu" class="icon" accesskey="S">
                <svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#bars"></use></svg>
              </button>
            </li>
            <li class="menu_hide">
              <button onclick="toggleOpen('caerp_base_menu');" title="Masquer le menu" aria-label="Masquer le menu" class="icon" accesskey="S">
                <svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#times"></use></svg>
              </button>
            </li>
            <li class="menu_size">
              <button id="menu_size_btn" onclick="resize('menu', this);" title="Réduire le menu" aria-label="Réduire le menu" class="icon" accesskey="F">
                <svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#chevron-left"></use></svg>
              </button>
            </li>
          </ul>
          % if request.matched_route:
              ${request.layout_manager.render_panel('menu')}
              ${request.layout_manager.render_panel('submenu')}
          % endif
          <footer id='page-footer-block'>
            <strong>${request.config.get('cae_business_name', ' ')}</strong>
            <br /><br />
            <img width="94" height="26" alt="Logo de MoOGLi" title="MoOGLi" src="${request.static_url('caerp:static/img/logo.png')}">
            <br />Version ${layout.caerp_version}
            <br />
            <%block name='footer' />
          </footer>
        </div>
      % endif

      <div class="base_content layout flex">

        <header class="main_header" role="banner">
          <div class="header_content layout flex">
            <div>
              <%block name="headtitle">
                % if title is not UNDEFINED and title is not None:
                    <h1>
                      ${title}
                      % if title_detail is not UNDEFINED and title_detail is not None:
                        <small> ${title_detail}</small>
                      % endif
                    </h1>
                % endif
              </%block>
            </div>
            </div>
        </header>

        <div class="main_area">
          <main id="target_content" role="main" tabindex="-1" accesskey="C">
            <div class="main_content">

              % if not request.is_popup:

                <div id="popupmessage"></div>
                <%block name="actionmenu">
                  <div class='main_toolbar nav_tools'><!--
                    % if not request.actionmenu.void():
                      -->${request.actionmenu.render(request)|n}<!--
                    % endif
                    -->${request.layout_manager.render_panel('navigation')}<!--
                  --></div>
                  <div class='main_toolbar'><!--
                    --><%block name='actionmenucontent' /><!--
                  --></div>
                </%block>

              % endif

                <%block name='afteractionmenu' />

                <%block name='pop_message'>
                  % for message in request.session.pop_flash(queue=""):
                    % if message is not None:
                      <div class='row hidden-print'>
                        <div class="alert alert-success">
                          <button class="icon only unstyled close" title="Masquer ce message" aria-label="Masquer ce message" data-dismiss="alert" type="button">
                            <svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#times"></use></svg>
                          </button>
                          <span class="icon"><svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#success"></use></svg></span>
                          ${api.clean_html(message)|n}
                        </div>
                      </div>
                    % endif
                  % endfor
                  % for message in request.session.pop_flash(queue="error"):
                    % if message is not None:
                      <div class='row hidden-print'>
                        <div class="alert alert-danger">
                          <button class="icon only unstyled close" title="Masquer ce message" aria-label="Masquer ce message" data-dismiss="alert" type="button">
                            <svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#times"></use></svg>
                          </button>
                          <span class="icon"><svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#danger"></use></svg></span>
                          ${api.clean_html(message)|n}
                        </div>
                      </div>
                    % endif
                  % endfor
                </%block>

              <%block name='beforecontent' />

              <%block name='content' />

              % if request.popups is not UNDEFINED:
                % for name, popup in request.popups.items():
                  <section id="${name}" style="display:none;" class="hidden-print caerp-utils-popup-widget modal_view" data-title="${popup.title}">
                    <div role="dialog" id="popup" aria-modal="true" aria-labelledby="popup_title">
                      <div class="modal_layout">
                        <header>
                          <button class="icon only unstyled close" title="Fermer cette fenêtre" aria-label="Fermer cette fenêtre" onclick="toggleModal('${name}'); return false;">
                            <svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#times"></use></svg>
                          </button>
                          <h2 id="popup_title">${popup.title}</h2>
                        </header>
                        <div class="modal_content_layout">
                          ${popup.html|n}
                        </div>
                      </div>
                    </div>
                  </section>
                % endfor
              % endif

            </div>
          </main>
        </div>

      </div>

      <div id='loading-box' class='loading_box' style='display:none'>
        <svg><use href="${request.static_url('caerp:static/icons/endi.svg')}#circle-notch"></use></svg>
      </div>

      <div id='login_form'></div>

    </div>
  % if not request.is_popup:
  <div id="vue-notification-message-app" class='notifications_list' aria-live="polite" role="alert"></div>
  <div id="vue-notification-alert-app"></div>
  % endif

    <script type='text/javascript'>
      var CAERP_STATIC_ICON_URL = "${request.static_url('caerp:static/icons/endi.svg')}";
      % if getattr(layout, "js_app_options", None):
      var AppOption = AppOption || {};
        % for option, value in layout.js_app_options.items():
          ${api.write_js_app_option(option, value)}
        % endfor
      % endif
      <%block name='footerjs' />
    </script>

  </body>
</html>
