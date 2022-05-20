import imp


import re
import fitz
from pathlib import Path
from bs4 import BeautifulSoup
from zwutils.dlso import upsert_config
from zwutils.fileutils import writefile

class Pdf(object):
    def __init__(self, pth, cfg=None, **kwargs):
        cfgdef = {
            'zoom': (4.16666, 4.16666),
            'tmpdir': 'tmp',
            'debug': False,
        }
        self.cfg = upsert_config({}, cfgdef, cfg, kwargs)
        self.pth = Path(pth)
        self.tmpdir = Path(self.cfg.tmpdir)

    def pdf2txt(self, outpth=None):
        pth = self.pth
        outs = []
        with fitz.open(pth) as doc:
            for page in doc.pages():
                s = self.page2txt(page=page)
                outs.append(s)
        if outpth:
            writefile(outpth, '\n'.join(outs))
        return outs

    def page2txt(self, pno=None, page=None):
        rtn = None
        if pno is not None:
            with fitz.open(self.pth) as doc:
                page = doc[pno]
                rtn = page.getText('text')
        elif page:
            rtn = page.getText('text')
        else:
            raise Exception('Neither page num nor page object has been given!')
        return rtn

    def pdf2png(self, outdir=None, zoom=None, alpha=False):
        pth = self.pth
        outs = []
        with fitz.open(pth) as doc:
            for page in doc.pages():
                s = self.page2png(outpath=outdir/(f'{pth.stem}_{page.number}.png'), page=page, zoom=zoom, alpha=alpha)
                outs.append(s)
        return outs

    def page2png(self, pno=None, page=None, outpath=None, zoom=None, alpha=False):
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96
        cfg = self.cfg
        zoom = zoom or cfg.zoom
        rotate = int(0)
        zoom_x = zoom[0]
        zoom_y = zoom[1]
        mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
        if pno is not None:
            with fitz.open(self.pth) as doc:
                page = doc[pno]
                pix = page.getPixmap(matrix=mat, alpha=alpha)
        elif page:
            pix = page.getPixmap(matrix=mat, alpha=alpha)
        else:
            raise Exception('Neither page num nor page object has been given!')

        if outpath:
            Path(outpath).parent.mkdir(parents=True, exist_ok=True)
            pix.writeImage(outpath)
        rtn = {
            'pgnum' : page.number,
            'width' : pix.width,
            'height': pix.height,
            'image' : pix.getPNGData(),
        }
        return rtn

    def pdf2html(self, outpath=None, exclude_re=None):
        pth = self.pth
        pages = []
        htmlstr = ''
        with fitz.open(pth) as doc:
            for page in doc:
                if exclude_re:
                    m = re.search(exclude_re, page.getText())
                    if m:
                        continue
                html = self.page2html(page=page, pageid='page_%i' % len(pages))
                pages.append(html)
        htmlstr = ''.join(pages)
        if outpath:
            writefile(outpath, htmlstr)
        return htmlstr

    def page2html(self, pno=None, page=None, outpath=None, pageid=None):
        html = None
        if pno is not None:
            with fitz.open(self.pth) as doc:
                page = doc[pno]
                html = fix_html_font(page.getText('html'))
        else:
            html = fix_html_font(page.getText('html'))

        soup = BeautifulSoup(html, 'html.parser')
        ps = soup.find_all('p')
        for p in ps:
            spans = p.find_all('span')
            if len(spans)<2:
                continue
            spantxt = ''
            spancls = spans[0]['style']
            for span in spans:
                spantxt += span.text
                span.decompose()
            markup = '<span style="%s">%s</span>' % (spancls, spantxt)
            new_span = BeautifulSoup(markup, features='html.parser')
            p.append(new_span)
        if pageid:
            soup.div['id'] = pageid
        html = str(soup)
        if outpath:
            # outpath = outpath or str(self.pth.parent/self.pth.stem)
            # outpath = '%s-%i.html' % (outpath, page.number)
            writefile(outpath, html)
        return html

def fix_html_font(htmlstr):
    otext = htmlstr                               # original html text string
    pos1 = 0                                      # search start poition
    font_serif = "font-family:Times"              # enter ...
    font_sans  = "font-family:Helvetica"          # ... your choices ...
    font_mono  = "font-family:Courier"            # ... here

    while True:
        pos0 = otext.find("font-family:", pos1)   # start of a font spec
        if pos0 < 0:                              # none found - we are done
            break
        pos1 = otext.find(";", pos0)              # end of font spec
        test = otext[pos0 : pos1]                 # complete font spec string
        testn = ""                                # the new font spec string
        if test.endswith(",serif"):               # font with serifs?
            testn = font_serif                    # use Times instead
        elif test.endswith(",sans-serif"):        # sans serifs font?
            testn = font_sans                     # use Helvetica
        elif test.endswith(",monospace"):         # monospaced font?
            testn = font_mono                     # becomes Courier

        if testn != "":                           # any of the above found?
            otext = otext.replace(test, testn)    # change the source
            pos1 = 0                              # start over
    return otext