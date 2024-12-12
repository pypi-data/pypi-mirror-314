<%inherit file="${context['main_template'].uri}" />

<%block name='actionmenucontent'>
    <div id="js_actions"></div>
</%block>

<%block name='content'>
    <div id="js-main-area"></div>
</%block>

<%block name="footerjs">
AppOption = {};
% for key, url in urls.items():
AppOption["${key}"] = "${url}"
% endfor;
</%block>
