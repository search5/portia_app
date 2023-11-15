from flask import render_template


def placeholder_img(size):
    if ('x' not in size) or (size.count('x') != 1):
        return "Bad Request", 400
    width, height = size.split("x")
    bg_fill = '#cccccc'
    txt_fill = '#9c9c9c'
    txt = size

    return (render_template('placeholder.jinja2', width=width, height=height,
                            bg_fill=bg_fill, txt_fill=txt_fill, txt=txt),
            (('Content-Type', 'image/svg+xml'),))
