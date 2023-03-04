from django.shortcuts import render
import gantt
import datetime
import dateutil.relativedelta
import svgwrite
import sys
import logging

__LOG__ = None
mm = 3.543307
cm = 35.43307

VACATIONS = []
NOT_WORKED_DAYS = [5, 6]
FONT_ATTR = {
    'fill': 'black',
    'stroke': 'black',
    'stroke_width': 0,
    'font_family': 'Verdana',
    'font_size': 15
}


def init_log_to_sysout(level=logging.INFO):
    """
    Init global variable __LOG__ used for logging purpose

    Keyword arguments:
    level -- logging level (from logging.debug to logging.critical)
    """
    global __LOG__
    logger = logging.getLogger("Gantt")
    logger.setLevel(level)
    fh = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    __LOG__ = logging.getLogger("Gantt")
    return


if __name__ == '__main__':
    import doctest
    # non regression test
    doctest.testmod()

else:
    init_log_to_sysout(level=logging.CRITICAL)


def _font_attributes():
    """
    Return dictionnary of font attributes
    Example :
    FONT_ATTR = {
      'fill': 'black',
      'stroke': 'black',
      'stroke_width': 0,
      'font_family': 'Verdana',
    }
    """
    global FONT_ATTR
    return FONT_ATTR


def _not_worked_days():
    """
    Returns list of days off (0: Monday ... 6: Sunday)
    """
    global NOT_WORKED_DAYS
    return NOT_WORKED_DAYS


class CustomProject(gantt.Project):

    dias_nombre_completo = {
        'monday': 'Lunes',
        'tuesday': 'Martes',
        'wednesday': 'Miércoles',
        'thursday': 'Jueves',
        'friday': 'Viernes',
        'saturday': 'Sábado',
        'sunday': 'Domingo',
    }

    dias_nombre_mnemonico = {
        'm': 'L',
        't': 'M',
        'w': 'X',
        't': 'J',
        'f': 'V',
        's': 'S',
        's': 'D',
    }

    mes_nombre_completo = {
        'january': 'Enero',
        'february': 'Febrero',
        'march': 'Marzo',
        'april': 'Abril',
        'may': 'Mayo',
        'june': 'Junio',
        'july': 'Julio',
        'august': 'Agosto',
        'september': 'Septiembre',
        'october': 'Octubre',
        'november': 'Noviembre',
        'december': 'Diciembre',
    }

    def traducir_dia_nombre(self, text):
        return self.dias_nombre_completo[text.lower()]

    def traducir_dia_mnemonico(self, text):
        return self.dias_nombre_mnemonico[text.lower()]

    def traducir_mes_nombre(self, text):
        return self.mes_nombre_completo[text.lower()]

    def check_conflicts_between_task_and_resources_vacations(self):
        """
        Displays a warning for each conflict between milestones and vacation of
        resources affected to the milestone

        And returns a dictionnary for resource vacation conflicts
        """
        return []

    def svg(self, prev_y=0, start=None, end=None, color=None, level=0, scale='d', title_align_on_left=False, offset=0):
        if start is None:
            start = self.start_date()
        if end is None:
            end = self.end_date()
        if color is None or self.color is not None:
            color = self.color

        cy = prev_y + 1*(self.name != "")

        prj = svgwrite.container.Group()

        for t in self.tasks:
            trepr, theight = t.svg(cy, start=start, end=end, color=color, level=level+1,
                                   scale=scale, title_align_on_left=title_align_on_left, offset=offset)
            if trepr is not None:
                prj.add(trepr)
                cy += theight

        fprj = svgwrite.container.Group()
        prj_bar = False
        if self.name != "":
            if ((self.start_date() >= start and self.end_date() <= end)
                    or ((self.end_date() >= start and self.start_date() <= end))) or level == 1:
                fprj.add(svgwrite.text.Text('{0}'.format(self.name), insert=((6*level+3+offset)*mm, ((prev_y)*10+7)*mm), fill=_font_attributes()[
                         'fill'], stroke=_font_attributes()['stroke'], stroke_width=_font_attributes()['stroke_width'], font_family=_font_attributes()['font_family'], font_size=15+3))

                fprj.add(svgwrite.shapes.Rect(
                    insert=((6*level+0.8+offset)*mm, (prev_y+0.5)*cm),
                    size=(0.2*cm, ((cy-prev_y-1)+0.4)*cm),
                    fill='green',
                    stroke='lightgray',
                    stroke_width=0,
                    opacity=0.5
                ))
                prj_bar = True
            else:
                cy -= 1

        if (cy - prev_y) == 0 or ((cy - prev_y) == 1 and prj_bar):
            return (None, 0)

        fprj.add(prj)

        return (fprj, cy-prev_y)

    def _svg_calendar(self, maxx, maxy, start_date, today=None, scale='d', offset=0):
        dwg = svgwrite.container.Group()

        cal = {0: 'Mo', 1: 'Tu', 2: 'We', 3: 'Th', 4: 'Fr', 5: 'Sa', 6: 'Su'}

        maxx += 1

        vlines = dwg.add(svgwrite.container.Group(
            id='vlines', stroke='lightgray'))
        for x in range(maxx):
            vlines.add(svgwrite.shapes.Line(
                start=((x+offset/10)*cm, 2*cm), end=((x+offset/10)*cm, (maxy+2)*cm)))
            if scale == 'd':
                jour = start_date + datetime.timedelta(days=x)
            elif scale == 'w':
                jour = start_date + \
                    dateutil.relativedelta.relativedelta(weeks=+x)
            elif scale == 'm':
                jour = start_date + \
                    dateutil.relativedelta.relativedelta(months=+x)
            elif scale == 'q':
                # how many quarter do we need to draw ?
                __LOG__.critical(
                    'DRAW_WITH_QUATERLY_SCALE not implemented yet')
                sys.exit(1)

            if not today is None and today == jour:
                vlines.add(svgwrite.shapes.Rect(
                    insert=((x+0.4+offset)*cm, 2*cm),
                    size=(0.2*cm, (maxy)*cm),
                    fill='#76e9ff',
                    stroke='lightgray',
                    stroke_width=0,
                    opacity=0.8
                ))

            if scale == 'd':
                # draw vacations
                if (start_date + datetime.timedelta(days=x)).weekday() in _not_worked_days() or (start_date + datetime.timedelta(days=x)) in VACATIONS:
                    vlines.add(svgwrite.shapes.Rect(
                        insert=((x+offset/10)*cm, 2*cm),
                        size=(1*cm, maxy*cm),
                        fill='#3D3D3D',
                        stroke='#626262',
                        stroke_width=1,
                        opacity=0.7,
                    ))

                # Current day
                vlines.add(
                    svgwrite.text.Text(
                        '{1} {0:02}'.format(
                            jour.day,
                            self.traducir_dia_mnemonico(cal[jour.weekday()][0])
                        ),
                        insert=((x*10+1+offset)*mm, 19*mm),
                        fill='black', stroke='black', stroke_width=0,
                        font_family=_font_attributes(
                        )['font_family'], font_size=15-3
                    )
                )
                # Year
                if jour.day == 1 and jour.month == 1:
                    vlines.add(svgwrite.text.Text('{0}'.format(jour.year),
                                                  insert=(
                                                      (x*10+1+offset)*mm, 5*mm),
                                                  fill='#400000', stroke='#400000', stroke_width=0,
                                                  font_family=_font_attributes(
                    )['font_family'], font_size=15+5,
                        font_weight="bold"))
                # Month name
                if jour.day == 1:
                    vlines.add(svgwrite.text.Text('{0}'.format(self.traducir_mes_nombre(jour.strftime("%B"))),
                                                  insert=(
                                                      (x*10+1+offset)*mm, 10*mm),
                                                  fill='#EB6923', stroke='#EB6923', stroke_width=0,
                                                  font_family=_font_attributes(
                    )['font_family'], font_size=15+3,
                        font_weight="bold"))
                # Week number
                if jour.weekday() == 0:
                    vlines.add(svgwrite.text.Text('{0:02}'.format(jour.isocalendar()[1]),
                                                  insert=(
                                                      (x*10+1+offset)*mm, 15*mm),
                                                  fill='black', stroke='black', stroke_width=0,
                                                  font_family=_font_attributes()[
                        'font_family'],
                        font_size=15+1,
                        font_weight="bold"))

            elif scale == 'w':
                # Year
                if jour.isocalendar()[1] == 1 and jour.month == 1:
                    vlines.add(svgwrite.text.Text('{0}'.format(jour.year),
                                                  insert=(
                                                      (x*10+1+offset)*mm, 5*mm),
                                                  fill='#400000', stroke='#400000', stroke_width=0,
                                                  font_family=_font_attributes()['font_family'], font_size=15+5, font_weight="bold"))
                # Month name
                if jour.day <= 7:
                    vlines.add(svgwrite.text.Text('{0}'.format(self.traducir_mes_nombre(jour.strftime("%B"))),
                                                  insert=(
                                                      (x*10+1+offset)*mm, 10*mm),
                                                  fill='#EB6923', stroke='#EB6923', stroke_width=0,
                                                  font_family=_font_attributes()['font_family'], font_size=15+3, font_weight="bold"))
                vlines.add(svgwrite.text.Text('{0:02}'.format(jour.isocalendar()[1]),
                                              insert=(
                                                  (x*10+1+offset)*mm, 15*mm),
                                              fill='black', stroke='black', stroke_width=0,
                                              font_family=_font_attributes()['font_family'], font_size=15+1, font_weight="bold"))

            elif scale == 'm':
                # Month number
                vlines.add(svgwrite.text.Text('{0}'.format(jour.strftime("%m")),
                                              insert=(
                                                  (x*10+1+offset)*mm, 19*mm),
                                              fill='black', stroke='black', stroke_width=0,
                                              font_family=_font_attributes()['font_family'], font_size=15-3))
                # Year
                if jour.month == 1:
                    vlines.add(svgwrite.text.Text('{0}'.format(jour.year),
                                                  insert=(
                                                      (x*10+1+offset)*mm, 5*mm),
                                                  fill='#400000', stroke='#400000', stroke_width=0,
                                                  font_family=_font_attributes()['font_family'], font_size=15+5, font_weight="bold"))

            elif scale == 'q':
                # how many quarter do we need to draw ?
                __LOG__.critical(
                    'DRAW_WITH_QUATERLY_SCALE not implemented yet')
                sys.exit(1)

        vlines.add(svgwrite.shapes.Line(start=((maxx+offset/10)*cm,
                   2*cm), end=((maxx+offset/10)*cm, (maxy+2)*cm)))

        hlines = dwg.add(svgwrite.container.Group(
            id='hlines', stroke='lightgray'))

        dwg.add(svgwrite.shapes.Line(start=((0+offset/10)*cm, (2)*cm),
                end=((maxx+offset/10)*cm, (2)*cm), stroke='black'))
        dwg.add(svgwrite.shapes.Line(start=((0+offset/10)*cm, (maxy+2)*cm),
                end=((maxx+offset/10)*cm, (maxy+2)*cm), stroke='black'))

        for y in range(2, maxy+3):
            hlines.add(svgwrite.shapes.Line(
                start=((0+offset/10)*cm, y*cm), end=((maxx+offset/10)*cm, y*cm)))

        return dwg
