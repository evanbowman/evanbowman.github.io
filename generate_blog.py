import os
import htmlmin

#
# This script assembles the posts in the posts/ directory into a series of blog
# pages.
#


posts_dir = "posts/"
post_separator = '<div><u class="load-comments" id="%s"></u><div class="comments"></div></div><div class="separator"></div>'


def file_contents(fname):
    with open(fname) as f:
        return f.read();


def load_template():
    header = htmlmin.minify(file_contents("blog-page-template-header.html"))
    footer = htmlmin.minify(file_contents("blog-page-template-footer.html"))
    return header, footer


def load_post_file_names():
    for root, dirs, files in os.walk(posts_dir):
        # note: ignore my emacs temporary files
        return [f for f in files if not '~' in f]


header, footer = load_template()


posts = load_post_file_names()


blog_page = 0


posts_per_page = 6


while posts:
    out = "" + header
    for post in posts[-1 * posts_per_page:]:
        ident = post.split(".")[0]
        content = file_contents(posts_dir + post)
        separator = post_separator % ident
        result = htmlmin.minify(content) + separator
        out += result
        # Write each post to a unique file, so that people can share links to
        # the specific post.
        with open("post_%s.html" % ident, "w") as post_file:
            post_file.write(htmlmin.minify(header + result + footer))
        posts.pop()

    if blog_page != 0:
        out += '<a href="blog_page_%s.html">older posts</a>' % (blog_page - 1)

    out += footer

    with open("blog_page_%s.html" % blog_page, "w") as out_file:
        out_file.write(htmlmin.minify(out))

    blog_page += 1


os.system("mv blog_page_%s.html index.html" % (blog_page - 1))
