<%page args="error" />
<%inherit file="/applications/base.mako" />

<%def name="head_tags()">
<title>LinkHome - Error In Launching Application: ${error.AppName}</title>
</%def>
<p><a id="back_button" href="/applications">Back</a></p>

There was a problem launching the application: ${error.AppName}<BR>
Please be sure the application exists and is in your path.<BR><BR>
Source file: ${error.fullpath}<BR><BR>
