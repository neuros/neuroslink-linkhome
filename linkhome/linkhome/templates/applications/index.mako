<%page args="files" />
<%inherit file="/applications/base.mako" />

<%def name="head_tags()">
<title>LinkHome - Applications - ${files}</title>
</%def>

% for f in files:
  <li><a href="/applications/${f}">${f}</a></li>
% endfor
