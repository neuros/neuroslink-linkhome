<%page args="filename, contents" /> 
<html><head><title>procfs: ${filename}</title></head><body>
<p>Contents of ${filename}:</p>
<code><pre>${contents | h}</pre></code>
</body></html>
