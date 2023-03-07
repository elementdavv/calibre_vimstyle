#!/usr/bin/env python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai


__license__   = 'GPL v3'
__copyright__ = '2023, Element Davv <lakedai@hotmail.com>'
__docformat__ = 'restructuredtext en'

# The class that all interface action plugins must inherit from
from calibre.gui2.actions import InterfaceAction


class VimStylePlugin(InterfaceAction):

    name = _('Vim style')
    auto_repeat = True
    action_add_menu = False
    action_spec = ( _('Vim style'), None, None, None )

    def create(self, spec, attr, handler):
        a = self.create_action(spec, attr)
        self.gui.addAction(a)
        a.triggered.connect(handler)

    def genesis(self):
        spec = (_('01, next book'), None, None, _('J'))
        self.create(spec, _('vimNext'), self.browseNext)
        spec = (_('02, prev book'), None, None, _('K'))
        self.create(spec, _('vimPrevious'), self.browsePrevious)

        spec = (_('03, page down'), None, None, _('Ctrl+F'))
        self.create(spec, _('vimForward'), self.browseForward)
        spec = (_('04, page up'), None, None, _('Ctrl+B'))
        self.create(spec, _('vimBackward'), self.browseBackward)

        spec = (_('05, last book'), None, None, _('Shift+G'))
        self.create(spec, _('vimLast'), self.browseLast)
        spec = (_('06, first book'), None, None, _('G'))
        self.create(spec, _('vimFirst'), self.browseFirst)

        spec = (_('07, left column'), None, None, _('H'))
        self.create(spec, 'vimLeft', self.browseLeft)
        spec = (_('08, right column'), None, None, _('L'))
        self.create(spec, _('vimRight'), self.browseRight)

        spec = (_('09, home column'), None, None, (_('0'), _('Shift+H')))
        self.create(spec, _('vimBegin'), self.browseBegin)
        spec = (_('10, end column'), None, None, (_('$'), _('Shift+L')))
        self.create(spec, _('vimEnd'), self.browseEnd)

    def browseNext(self):
        lv = self.gui.library_view
        row = lv.currentIndex().row()
        count = lv.row_count()
        if row < count - 1:
            col = lv.currentIndex().column()
            lv.select_cell(row + 1, col)

    def browsePrevious(self):
        lv = self.gui.library_view
        row = lv.currentIndex().row()
        if row > 0:
            col = lv.currentIndex().column()
            lv.select_cell(row - 1, col)

    def browseForward(self):
        lv = self.gui.library_view
        row = lv.currentIndex().row()
        count = lv.row_count()
        if row < count - 1:
            page = lv.row_at_bottom() - lv.row_at_top()
            row += page - 1
            if row > count - 1:
                row = count - 1
            col = lv.currentIndex().column()
            lv.select_rows((row,), False)
            lv.select_cell(row, col)

    def browseBackward(self):
        lv = self.gui.library_view
        row = lv.currentIndex().row()
        if row > 0:
            page = lv.row_at_bottom() - lv.row_at_top()
            row -= page - 1
            if row < 0:
                row = 0 
            col = lv.currentIndex().column()
            lv.select_rows((row,), False)
            lv.select_cell(row, col)

    def browseFirst(self):
        lv = self.gui.library_view
        row = lv.currentIndex().row()
        if row > 0:
            col = lv.currentIndex().column()
            lv.select_cell(0, col)

    def browseLast(self):
        lv = self.gui.library_view
        row = lv.currentIndex().row()
        count = lv.row_count()
        if row < count - 1:
            col = lv.currentIndex().column()
            lv.select_cell(count - 1, col)

    def browseLeft(self):
        lv = self.gui.library_view
        h = lv.horizontalHeader()
        logical_indices = [x for x in list(range(h.count())) if not h.isSectionHidden(x)]
        pairs = [(x, h.visualIndex(x)) for x in logical_indices if h.visualIndex(x) > -1]
        pairs.sort(key=lambda x: x[1])
        visual_indices = [x[0] for x in pairs]
        left = -1
        column = lv.currentIndex().column()
        for col in visual_indices:
            if col == column:
                if left != -1:
                    row = lv.currentIndex().row()
                    lv.select_cell(row, left)
                break
            else:
                left = col

    def browseRight(self):
        lv = self.gui.library_view
        h = lv.horizontalHeader()
        logical_indices = [x for x in list(range(h.count())) if not h.isSectionHidden(x)]
        pairs = [(x, h.visualIndex(x)) for x in logical_indices if h.visualIndex(x) > -1]
        pairs.sort(key=lambda x: x[1])
        visual_indices = [x[0] for x in pairs]
        right = False
        column = lv.currentIndex().column()
        for col in visual_indices:
            if col == column:
                right = True
            else:
                if right == True:
                    row = lv.currentIndex().row()
                    lv.select_cell(row, col)
                    break

    def browseBegin(self):
        lv = self.gui.library_view
        h = lv.horizontalHeader()
        logical_indices = [x for x in list(range(h.count())) if not h.isSectionHidden(x)]
        pairs = [(x, h.visualIndex(x)) for x in logical_indices if h.visualIndex(x) > -1]
        pairs.sort(key=lambda x: x[1])
        visual_indices = [x[0] for x in pairs]
        column = lv.currentIndex().column()
        col, *_ = visual_indices
        if col != column:
            row = lv.currentIndex().row()
            lv.select_cell(row, col)

    def browseEnd(self):
        lv = self.gui.library_view
        h = lv.horizontalHeader()
        logical_indices = [x for x in list(range(h.count())) if not h.isSectionHidden(x)]
        pairs = [(x, h.visualIndex(x)) for x in logical_indices if h.visualIndex(x) > -1]
        pairs.sort(key=lambda x: x[1])
        visual_indices = [x[0] for x in pairs]
        column = lv.currentIndex().column()
        *_, col = visual_indices
        if col != column:
            row = lv.currentIndex().row()
            lv.select_cell(row, col)
