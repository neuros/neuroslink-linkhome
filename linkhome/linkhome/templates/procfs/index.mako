<%page args="files" /> 
<html><head><title>procfs</title></head><body><ul>
% for f in files:
  <li><a href="/proc/${f}">${f}</a></li>
% endfor
</ul></body></html>
