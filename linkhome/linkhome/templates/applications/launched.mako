<%page args="application" /> 
<%inherit file="/applications/base.mako" />

<%def name="head_tags()">
<title>LinkHome - Application: ${application.AppName} Launched</title>
</%def>

<p><a id="back_button" href="/applications">Back</a></p>

<li>The following application has been launched: <b> ${application.AppName}</b></li>
<code><pre>${application.Comment}</pre></code>
<li><a href="/applications"> Go Back to Applications Menu </a></li>
