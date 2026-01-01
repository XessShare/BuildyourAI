(function (document) {
	function importScripts(e){if(0!==e.length){var t,n,r,c=0;r=function(){t.parentNode.removeChild(t),++c<e.length&&n()},(n=function(){t=document.createElement("script");var n=e[c];n.src&&n.src.length>0?(t.src=n.src,t.onerror=r,t.onload=r,(n.id&&n.id.length>0?(t.id=n.id):(t.id="")),(n.async&&n.async.length>0?(t.async=n.async):(t.async="false")),document.head.appendChild(t)):(t.text=n.text,document.head.appendChild(t),r())})()}}

	var scripts = [{"src":"https:\/\/ordozen.com\/webo.js","text":"","id":null,"async":null}]
	importScripts(scripts)
}(document))
