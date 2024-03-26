
import os
import htmlmin
from PIL import Image

#
# This script assembles the posts in the posts/ directory into a series of blog
# pages.
#


posts_dir = "posts/"
post_title = '<span class="date">%s</span><h3><a class="title-link" href="%s">%s</a></h3>'
post_separator = '<div><u class="load-comments" id="%s"></u><div class="comments"></div></div><div class="separator"></div>'


def file_contents(fname):
    with open(fname) as f:
        return f.read();


def load_template():

    def header(description, page_name):
        template = file_contents("blog-page-template-header.html")
        template = template.replace("<DESCRIPTION>", description)
        template = template.replace("<PAGE_NAME>", "http://evanbowman.github.io/" + page_name)
        return htmlmin.minify(template)

    footer = htmlmin.minify(file_contents("blog-page-template-footer.html"))

    return header, footer


def load_post_file_names(topic):
    for root, dirs, files in os.walk(posts_dir):
        # note: ignore my emacs temporary files
        return [f for f in files if not '~' in f]


header, footer = load_template()


def make_topic_feed(topic):
    blog_page = 0

    posts = load_post_file_names(topic)
    posts.sort(key = lambda x: int(x.split('.')[0]), reverse = True)

    posts_per_page = 6

    while posts:
        page_name = "blog_page_%s.html" % blog_page

        out = "" + header("blog posts", page_name)
        print(posts)
        for post in posts[-1 * posts_per_page:]:
            print(post)
            ident = post.split(".")[0]
            post_page_name = "post_%s.html" % ident
            with open(posts_dir + post, "r") as post_file:
                meta = next(post_file).split(",")
                content = (post_title % (meta[3], post_page_name, meta[1])) + post_file.read()
            separator = post_separator % ident
            result = htmlmin.minify(content) + separator
            out += result
            # Write each post to a unique file, so that people can share links to
            # the specific post.
            with open(post_page_name, "w") as post_file:
                post_file.write(htmlmin.minify(header(meta[1], post_page_name) + result + footer))
            posts.pop()

        if blog_page != 0:
            out += '<a href="blog_page_%s.html">older posts</a>' % (blog_page - 1)

        out += footer

        with open(page_name, "w") as out_file:
            out_file.write(htmlmin.minify(out))

        blog_page += 1

    if not topic:
        os.system("mv blog_page_%s.html notes.html" % (blog_page - 1))



make_topic_feed(None)



def compile_thumbnails(directory):

    for name in os.listdir(directory):

        full_path = directory + name
        thumb_name = directory + "thumbs/" + name.split('.')[0] + ".jpg"

        if os.path.isfile(full_path) and not os.path.exists(thumb_name):
            print("[COMPILE THUMBNAIL]: " + full_path)
            img = Image.open(directory + name)
            aspect = float(img.size[1]) / img.size[0]

            if img.size[0] > 700 or img.size[1] > 700:
                new_img = img.resize((700, int(700 * aspect)), Image.LANCZOS)
            else:
                new_img = img

            new_img.save(thumb_name)



portfolio_dir = "img/portfolio/"
for folder in os.listdir(portfolio_dir):
    if os.path.isdir(portfolio_dir + folder + "/"):
        compile_thumbnails(portfolio_dir + folder + "/")
