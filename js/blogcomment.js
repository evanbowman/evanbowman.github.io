
load_comments = null;


(function () {
    var issues = "https://github.com/evanbowman/evanbowman.github.io/issues/";
    var api_url = "https://api.github.com/repos/evanbowman/evanbowman.github.io/issues/";

    load_comments = function(title, receiver) {
        var xml_http = new XMLHttpRequest();

        xml_http.onreadystatechange = function() {
            if (xml_http.readyState == XMLHttpRequest.DONE) {
                if (xml_http.status == 200) {
                    results = JSON.parse(xml_http.responseText);
                    receiver(results);
                }
                else if (xml_http.status == 400) {
                    alert('There was an error 400');
                }
                else {
                    alert('something else other than 200 was returned');
                }
            }
        };
        xml_http.open("GET", api_url + title + "/comments", true);
        xml_http.send();
    };

    window.onload = function() {
        var comments = document.getElementsByClassName("load-comments");
        for (var i = 0; i < comments.length; ++i) {
            (function (comment_box) {
                load_comments(comment_box.id, function(results) {
                    var comments = comment_box.parentElement.children[1];
                    if (results.length == 1) {
                        comment_box.innerHTML = "1 comment";
                    } else {
                        comment_box.innerHTML = results.length + " comments";
                    }
                    var row = null;
                    for (var i = 0; i < results.length; ++i) {
                        row = document.createElement("DIV");
                        row.classList.add("comment_box");
                        var head = document.createElement("DIV");
                        head.innerHTML =
                            results[i]["user"]["login"] + " posted at " +
                            new Date(results[i]["created_at"]).toUTCString();
                        head.classList.add("comment_head");
                        var body = document.createElement("DIV");
                        body.innerHTML = results[i]["body"];
                        body.classList.add("comment_body");
                        row.appendChild(head);
                        row.appendChild(body);
                        comments.appendChild(row);
                    }
                    var a = document.createElement("A");
                    a.href = issues + comment_box.id;
                    a.innerHTML = "post a comment via github";
                    comments.appendChild(a);
                    comment_box.onclick = function() {
                        if (comments.style.display == "block") {
                            comments.style.display = "none";
                        } else {
                            comments.style.display = "block";
                        }
                    };
                });
            })(comments[i]);
        }
    };
})();
