<%page args="files" />
<%inherit file="/applications/base.mako" />

<%def name="head_tags()">
<title>LinkHome - Applications</title>
</%def>

<p><a id="back_button" href="/">Back</a></p>

<div id="menu_area">
	<dl>
		% for f in files:
		<dd>
			<a id="menu_item" href="/applications/${f.name}/launch" title="${f.Comment}">
			<img alt="${f.AppName} Icon" src="/applications/${f.name}/icon" height="128" width="128">
			<p>${f.AppName}</p>
			</a>
		</dd>
		% endfor
</dl>
</div>

