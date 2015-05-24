import time
import re

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle as PS

#replacement for the bibcode (somehow is not clean :o)
REPLS = (';', ''), ('/', '')


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 7)
        self.drawRightString(200*mm, 20*mm,
            "Page %d of %d" % (self._pageNumber, page_count))


def clean_html(raw_html):

    to_remove = re.compile('<.*?>')
    clean_text = re.sub(to_remove, '', raw_html)

    return clean_text


def generatePDF(list_of_publication, filename, DOC_ROOT, TMP_DIR):

    pdf_name = "%s/%s.pdf" % (TMP_DIR, filename)

     # Setup the document template ...
    doc = SimpleDocTemplate(pdf_name,
                            rightMargin=1.5*cm, leftMargin=1.5*cm, topMargin=1.5*cm, bottomMargin=1.5*cm)

    # ... and initialize the content block.
    story = []

    # Add your logo to the page head.
    story.append(Image('%s/static/images/ASDC_logo.jpg' % DOC_ROOT,
                       2*cm, 1*cm))

    # Fetch the document stylesheet ...
    styles = getSampleStyleSheet()

    # style to select
    styles.fontName = 'Helvetica'

    # ... and add the justify style.
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))

    h1 = PS(fontName='Helvetica', fontSize=8, leftIndent=16, name="")

    # Add the document title to the content block.
    story.append(Spacer(0.1*cm, 1*cm))
    timeStr = '<font size=12>{time}</font>'.format(time=time.ctime())
    story.append(Paragraph('<font size=16>ASDC Publications List (%s)</font>' %timeStr, styles["Center"]))
    story.append(Spacer(0.1*cm, 1*cm))

    for i in range(0, len(list_of_publication)):
        publication = list_of_publication[i]
        text = ('{num} - <font color="#7CA6CF">{biblicode}</font>'.format(
            biblicode=reduce(lambda a, kv: a.replace(*kv), REPLS, publication['biblicode']), num=i+1))
        story.append(Paragraph(text, styles["Normal"]))
        story.append(Spacer(0.1*cm, 0.01*cm))
        text = ('<b> {title} </b>'.format(title=clean_html(publication['title'])))
        story.append(Paragraph(text, h1))
        story.append(Spacer(0.1*cm, 0.01*cm))
        text = '%s' % publication['authors']
        story.append(Paragraph(text, h1))
        story.append(Spacer(0.1*cm, 0.01*cm))
        text = ('<i>{pub_date}</i>'.format(pub_date=publication['pub_date']))
        story.append(Paragraph(text, h1))
        story.append(Spacer(0.1*cm, 0.5*cm))


    # To generate the content and write it to
    # the *.pdf file (in this case firstDoc.pdf)
    # just call the build method.
    doc.build(story, canvasmaker=NumberedCanvas)
#    doc.build(story)
