# Don't change anything in this file.
from .. import models
import otree.api


class Page(otree.api.Page):
    def z_autocomplete(self):
        subsession = models.Subsession()
        group = models.Group()
        player = models.Player()


class WaitPage(otree.api.WaitPage):
    def z_autocomplete(self):
        subsession = models.Subsession()
        group = models.Group()
        player = models.Player()


class Bot(otree.api.Bot):
    def z_autocomplete(self):
        subsession = models.Subsession()
        group = models.Group()
        player = models.Player()
