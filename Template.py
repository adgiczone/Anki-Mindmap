EDITOR = """
        var area = document.getElementById('mindmap-area');
        if(area) area.remove();
        area = document.createElement('mindmap-area');
        area.id = 'mindmap-area';
        area.style.display = 'inline-block';
        area.style.overflowY = 'auto';
        area.style.padding = '1%';
        area.style.visibility = 'hidden';
        area.style.width = '98%';
        area.style.height = '100%';

        var fields = document.getElementById('fields');
        if (fields !== null) {
			keyupFunc = function() {
				var text = '# Field 1\\n' + fields.children[0].children[1].shadowRoot.children[2].innerHTML;
				text += "\\n# Field 2\\n" + fields.children[1].children[1].shadowRoot.children[2].innerHTML;
				render(text);
			}

			document.body.appendChild(area);
		}

        else {
			var fields = document.getElementsByClassName('fields')[0];

			keyupFunc = function() {
				var text = '# Field 1\\n' + fields.children[0].getElementsByClassName("rich-text-editable")[0].shadowRoot.children[2].innerHTML;
				text += "\\n# Field 2\\n" + fields.children[1].getElementsByClassName("rich-text-editable")[0].shadowRoot.children[2].innerHTML;
				render(text);
			}

			fields.appendChild(area);
		}

"""


FRONT = """
<div class="slide">
  <svg id="mindmapgraph"></svg>
  <div id="mindmaptext" hidden>{{Mindmap}}</div>
</div>

<script>
  var ResourceType = {
    js: 1,
    css: 2,
  };
  loadResource("_d3@6.js", "https://cdn.jsdelivr.net/npm/d3@6", ResourceType.js)
    .then(() =>
      loadResource(
        "_markmap-lib.js",
        "https://cdn.jsdelivr.net/npm/markmap-lib",
        ResourceType.js
      )
    )
    .then(() =>
      loadResource(
        "_markmap-view.js",
        "https://cdn.jsdelivr.net/npm/markmap-view",
        ResourceType.js
      )
    )
    .then(() =>
      loadResource(
        "_markmap-common.js",
        "https://cdn.jsdelivr.net/npm/markmap-view",
        ResourceType.js
      )
    )
    .then(render)
    .catch(show);

  function loadResource(path, altURL, resourceType) {
    let load = function (isLocal, resolve, reject) {
      let resource =
        resourceType === ResourceType.js
          ? document.createElement("script")
          : document.createElement("link");
      if (resourceType === ResourceType.css) {
        resource.setAttribute("rel", "stylesheet");
        resource.type = "text/css";
      }
      resource.onload = resolve;
      resource.src = isLocal ? path : altURL;
      resource.onerror = isLocal
        ? function () {
            load(false, resolve, reject);
          }
        : reject;
      document.head.appendChild(resource);
    };
    return new Promise((resolve, reject) => {
      load(true, resolve, reject);
    });
  }

  function render() {
    mindmap("mindmaptext");
    show();
  }

  function clicked(t) {
    if( t.isChanged === false) {
      t.style.background="white";
      t.isChanged = true;
    } else {
      t.style.color="black";
      t.style.background="black";
      t.isChanged = false;
    }
  }

  function show() {
    document.getElementById("mindmapgraph").style.visibility = "visible";

    document.getElementById("mindmapgraph").addEventListener('click', function(e){
      const target = e.target.closest(".hide");
      if(target){
          if (!target.hasOwnProperty("isChanged")) {
            target.isChanged = false;
          }
        clicked(target);
      }
    }, true);
  }

  function mindmap(ID) {
    if (document.getElementById("mindmapgraph").children.length === 2) {
      // Already created graph, directly return
      return;
    }
    let text = escapeHTMLChars(document.getElementById(ID).innerHTML);
    const { Markmap, loadCSS, loadJS, Transformer, deriveOptions } = window.markmap;
    var transformer = new Transformer();
    const { root, features } = transformer.transform(text);
    const { styles, scripts } = transformer.getUsedAssets(features);
    if (styles) loadCSS(styles);
    if (scripts) loadJS(scripts, { getMarkmap: () => window.markmap });

    let raw = '{"initialExpandLevel":2,"colorFreezeLevel":2}';
    let defaultOptions;
    defaultOptions = raw && JSON.parse(raw);
    Markmap.create("#mindmapgraph", deriveOptions(defaultOptions), root);
  }
  function escapeHTMLChars(str) {
    return str
      .replace(/<[\/]?pre[^>]*>/gi, "")
      .replace(/<br\s*[\/]?[^>]*>/gi, "\\n")
      .replace(/<br\s*[\/]?[^>]*>/gi, "\\n")
      .replace(/<[\/]?span[^>]*>/gi, "")
      .replace(/<ol[^>]*>/gi, "")
      .replace(/<\/ol[^>]*>/gi, "\\n")
      .replace(/<ul[^>]*>/gi, "")
      .replace(/<\/ul[^>]*>/gi, "\\n")
      .replace(/<div[^>]*>/gi, "")
      .replace(/<\/div[^>]*>/gi, "\\n")
      .replace(/<li[^>]*>/gi, "- ")
      .replace(/<\/li[^>]*>/gi, "\\n")
      .replace(/&nbsp;/gi, " ")
      .replace(/&tab;/gi, "	")
      .replace(/&gt;/gi, ">")
      .replace(/&lt;/gi, "<")
      .replace(/&amp;/gi, "&");
  }
</script>
"""


BACK = """
{{FrontSide}}
<hr />
<div id="back"><pre>{{Notes}}</pre></div>
"""


CSS = """
  @font-face {
    font-family: "Cascadia Code";
    src: url("_CascadiaCode.ttf");
  }

  .card {
    font: 20px/30px yh;
    background-color: white;
    text-align: left;
  }

  ul,
  ol {
    margin-top: 0em;
  }
  ul li {
    margin-left: -0.9em;
  }

  i {
    padding: 0 3px 0 0;
  }

  u {
    text-decoration: none;
    border-bottom: 2px solid #ec6c4f;
  }

  hr {
    height: 1px;
    width: 100%;
    display: block;
    border: 0px solid #fff;
    margin: 5px 0px 10px 0px;
    background-color: #ccc;
  }

  #mindmapgraph {
      visibility: hidden;
  }

  #mindmapgraph{
    aspect-ratio: 4 / 3;
    width: 100%;
  }

  .markmap-foreign {
    font: 16px/20px "Cascadia Code", "Consolas", Overpass, "GlowSansSC", "Helvetica Neue",
      "pingfang sc", "microsoft yahei", sans-serif;
  }

  .example {
    font-family: "Comic Sans MS", "STXinwei";
    text-align: left;
    width: 100%;
    overflow: hidden;
  }

  .comments {
    color: orange;
  }

  .block {
    display: inline-block;
    text-align: center;
    vertical-align: text-top;
  }

  .attention {
    background-color: rgb(241, 238, 213);
    margin-left: 2em;
    padding: 10px;
    border-style: dotted solid;
    border: 2px solid;
    border-color: lightgoldenrodyellow;
    border-radius: 5px;
  }

  .explain1 {
    border-left: 5px solid #E8EAED;
    padding-left: 5px;
    background-color: #FAF8F8;
	  color: grey;
		font-size: 90%;
  }

  .explain {
	  color: grey;
		font-size: 85%;
  }

  .focus {
    font-family: Comic Sans MS, Kaiti;
    text-align: center;
    width: 100%;
    font-weight: bold;
    color: red;
    overflow: hidden;
  }

  .hide {
    color: black;
    background: black;
  }
"""
