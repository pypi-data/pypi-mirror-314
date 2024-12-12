<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link rel="shortcut icon" href="${request.static_url('caerp:static/favicons/favicon.ico')}" type="image/x-icon" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" comment="">
    <meta name="KEYWORDS" CONTENT="">
    <meta NAME="ROBOTS" CONTENT="INDEX,FOLLOW,ALL">
  </head>
  <body>
      <div class="jumbotron">
          <h1>
            ${title}
        </h1>
        <p>
            % if not detail is UNDEFINED:
                ${detail}
            % endif
            <a href="/">Revenir à la page d'accueil</a>
        </p>
    </div>
  </body>
</html>
