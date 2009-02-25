<%page args="files" />
<%inherit file="/applications/base.mako" />

<%def name="head_tags()">
<title>LinkHome - Applications</title>
</%def>


% for f in files:
  <li><a href="/applications/${f.fname}">${f.AppName}</a> : ${f.Comment}<BR><BR></li>
% endfor
