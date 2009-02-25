<%page args="filename, contents" /> 
<html><head><title>Application: ${filename} Launched</title></head><body>
<p>This Application has been launched ${filename}:</p>
<code><pre>${contents | h}</pre></code>
</body></html>
