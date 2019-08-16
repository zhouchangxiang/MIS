(function(view){
    "use strict";
    var document = view.document
    var $ = function(id) {
		return document.getElementById(id);
	}
    var session = view.sessionStorage
    var html = $("html")
    var html_options_form = $("html-options")
    var html_filename = $("html-filename")
    var get_blob = function() {
		return view.Blob;
	}
    var guess_title = function(doc) {
		var h = "h6 h5 h4 h3 h2 h1".split(" "),
			i = h.length,
			headers,
			header_text
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
    var doc_impl = document.implementation
    var create_html_doc = function(html) {
		var dt = doc_impl.createDocumentType('html', "", ""),
			doc = doc_impl.createDocument("http://www.w3.org/1999/xhtml","html", dt),
			doc_el = doc.documentElement,
			head = doc_el.appendChild(doc.createElement("head")),
			charset_meta = head.appendChild(doc.createElement("meta")),
			title = head.appendChild(doc.createElement("title")),
			body = doc_el.appendChild(doc.createElement("body")),
			i = 0,
			len = html.childNodes.length
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
    html_options_form.addEventListener("submit",function(event){
        var BB = get_blob()
        var xml_serializer = new XMLSerializer()
        var doc = create_html_doc(html)
        var blob = new BB([xml_serializer.serializeToString(doc)], {type: "application/xhtml+xml;charset=" + document.characterSet})
        if(html_filename.value != ""){
            saveAs(blob, html_filename.value + ".html");
        }
    })
}(self))