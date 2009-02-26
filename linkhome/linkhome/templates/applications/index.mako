<%page args="files" />
<%inherit file="/applications/base.mako" />

<%def name="head_tags()">
<title>LinkHome - Applications</title>
</%def>


% for f in files:
  <li><a href="/applications/${f.fname}"><img src="${f.Icon}"> ${f.AppName}</a> : ${f.Comment}<br /><br 
/></li>
% endfor
