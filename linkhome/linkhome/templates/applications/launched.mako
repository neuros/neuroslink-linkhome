<%page args="application" /> 
<%inherit file="/applications/base.mako" />

<%def name="head_tags()">
<title>LinkHome - Application: ${application.AppName} Launched</title>
</%def>

<p>The following application has been launched ${application.AppName}:</p>
<code><pre>${application.Comment}</pre></code>
