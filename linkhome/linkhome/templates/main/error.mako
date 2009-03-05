<%inherit file="/main/base.mako" />

<%def name="head_tags()">
<title>LinkHome - Error In Launching Application: ${error.AppName}</title>
</%def>


There was a problem launching the application: ${error.AppName}<BR>
Please be sure the application exists and is in your path.<BR><BR>
Source file: ${error.fullpath}<BR><BR>
<a href="/applications">Click Here to Go Back</a>
