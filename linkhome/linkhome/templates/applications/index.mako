<%page args="files" /> 
<html><head><title>LinkHome - Applications</title></head><body><ul>
% for f in files:
  <li><a href="/applications/${f}">${f}</a></li>
% endfor
</ul></body></html>
