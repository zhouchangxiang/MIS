(function(view) {
"use strict";
var
	  document = view.document
	, $ = function(id) {
		return document.getElementById(id);
	}
	, session = view.sessionStorage
	, get_blob = function() {
		return view.Blob;
	}

	, canvas = $("canvas")
	, canvas_options_form = $("canvas-options")
	, canvas_filename = $("canvas-filename")
	, canvas_clear_button = $("canvas-clear")

	, text = $("text")
	, text_options_form = $("text-options")
	, text_filename = $("text-filename")

	, html = $("html")
	, html_options_form = $("html-options")
	, html_filename = $("html-filename")

	// Title guesser and document creator available at https://gist.github.com/1059648
	, guess_title = function(doc) {
		var
			  h = "h6 h5 h4 h3 h2 h1".split(" ")
			, i = h.length
			, headers
			, header_text
		;
		while (i--) {
			headers = doc.getElementsByTagName(h[i]);
			for (var j = 0, len = headers.length; j < len; j++) {
				header_text = headers[j].textContent.trim();
				if (header_text) {
					return header_text;
				}
			}
		}
	}
	, doc_impl = document.implementation
	, create_html_doc = function(html) {
		var
			  dt = doc_impl.createDocumentType('html', null, null)
			, doc = doc_impl.createDocument("http://www.w3.org/1999/xhtml", "html", dt)
			, doc_el = doc.documentElement
			, head = doc_el.appendChild(doc.createElement("head"))
			, charset_meta = head.appendChild(doc.createElement("meta"))
			, title = head.appendChild(doc.createElement("title"))
			, body = doc_el.appendChild(doc.createElement("body"))
			, i = 0
			, len = html.childNodes.length
		;
		charset_meta.setAttribute("charset", html.ownerDocument.characterSet);
		for (; i < len; i++) {
			body.appendChild(doc.importNode(html.childNodes.item(i), true));
		}
		var title_text = guess_title(doc);
		if (title_text) {
			title.appendChild(doc.createTextNode(title_text));
		}
		return doc;
	}
;
if (session.html) {
	html.innerHTML = session.html;
} if (session.html_filename) {
	html_filename.value = session.html_filename;
}
html_options_form.addEventListener("submit", function(event) {
	event.preventDefault();
	var
		  BB = get_blob()
		, xml_serializer = new XMLSerializer()
		, doc = create_html_doc(html)
	;
	saveAs(
		  new BB(
			  [xml_serializer.serializeToString(doc)]
			, {type: "application/xhtml+xml;charset=" + document.characterSet}
		)
		, (html_filename.value || html_filename.placeholder) + ".html"
	);
}, false);

view.addEventListener("unload", function() {
	session.x_points = JSON.stringify(x_points);
	session.y_points = JSON.stringify(y_points);
	session.drag_points = JSON.stringify(drag_points);
	session.canvas_filename = canvas_filename.value;

	session.text = text.value;
	session.text_filename = text_filename.value;

	session.html = html.innerHTML;
	session.html_filename = html_filename.value;
}, false);
}(self));
