<%page args="files" />
<%inherit file="/applications/base.mako" />

<%def name="head_tags()">
<title>LinkHome - Applications</title>
</%def>

<p><a id="back_button" href="/">Back</a></p>

<div id="menu_area">
% for f in files:
<a id="menu_item" href="/applications/${f.name}" title="${f.Comment}"><img alt="${f.AppName} Icon" src="/applications/${f.name}/icon"><br>${f.AppName}</br></a>
% endfor
</div>

