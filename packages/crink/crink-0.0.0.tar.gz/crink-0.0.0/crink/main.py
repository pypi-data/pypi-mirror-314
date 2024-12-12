import argparse
import decimal
import sys

from balladeer import discover_assets
from balladeer import Compass
from balladeer import Detail
from balladeer import Drama
from balladeer import Entity
from balladeer import Fruition
from balladeer import Prologue
from balladeer import quick_start
from balladeer import Resident
from balladeer import SpeechTables
from balladeer import StoryStager

import crink


class Exploration(Resident):

    @property
    def permits(self):
        return self.exits

    @property
    def nearby(self):
        focus = self.focus
        if focus:
            spot = focus.get_state(self.world.map.spot)
        else:
            spot = self.get_state(self.world.map.spot)
        if spot is None:
            return []
        else:
            return [
                i for i in self.world.statewise[str(spot)]
                if i.types.isdisjoint({"Focus"})
            ]

    def do_travel(self, this, text, director, *args, move: "permits", **kwargs):
        """
        {move.spot.label}
        go to {move.spot.label}

        """
        try:
            exit_name = self.focus.get_state(self.world.map.spot).name
            self.focus.set_state(self.world.map.exit[exit_name])
        except (AttributeError, KeyError):
            pass
        self.focus.set_state(move.spot)
        yield


class Interaction(SpeechTables, Exploration):

    @property
    def permits(self):
        "Suspend travel during conversation."
        if self.tree:
            return []
        else:
            return self.exits

    def interlude(self, *args, **kwargs) -> Entity:
        """
        self.speech.append(
            Epilogue("<> Guidance")
        )
        """
        return super().interlude(*args, **kwargs)

    def on_proposing(self, entity: Entity, *args: tuple[Entity], **kwargs):
        for ent in args:
            ent.set_state(Fruition.elaboration)
        yield

    def on_declining(self, entity: Entity, *args: tuple[Entity], **kwargs):
        # Puzzle will be terminated
        for ent in args:
            ent.set_state(Fruition.withdrawn)
        yield

    def on_withdrawing(self, entity: Entity, *args: tuple[Entity], **kwargs):
        for ent in args:
            ent.set_state(Fruition.withdrawn)
        yield

    def on_clarifying(self, entity: Entity, *args: tuple[Entity], **kwargs):
        for ent in args:
            ent.set_state(Fruition.elaboration)
        yield

    def on_offering(self, entity: Entity, *args: tuple[Entity], **kwargs):
        for ent in args:
            ent.set_state(Fruition.discussion)
        yield

    def on_confirming(self, entity: Entity, *args: tuple[Entity], **kwargs):
        for ent in args:
            ent.set_state(Fruition.construction)
        yield

    def on_promising(self, entity: Entity, *args: tuple[Entity], **kwargs):
        for ent in args:
            ent.set_state(Fruition.construction)
        yield

    def do_talk(self, this, text, director, *args, entity: "nearby", **kwargs):
        """
        Speak to {entity.names[0]}
        Talk to {entity.names[0]}

        """
        fruition = self.get_state(Fruition)
        if set(self.names).intersection(entity.links):
            if fruition == Fruition.inception:
                self.set_state(Fruition.elaboration)
           #  elif fruition == Fruition.elaboration:
           #      self.set_state(Fruition.discussion)
           #  elif fruition == Fruition.discussion:
           #      self.set_state(Fruition.elaboration)
        yield


class Story(StoryStager):
    types = StoryStager.types + [Exploration, Interaction]


def parser():
    rv = argparse.ArgumentParser()
    rv.add_argument("--html-syntax", type=decimal.Decimal, default=5, help="Specify a version of HTML [5]")
    return rv


def main(args):
    assets = discover_assets(crink, "script")
    story = Story(assets=assets)

    quick_start("", story_builder=story, **vars(args))


def run():
    p = parser()
    args = p.parse_args()
    rv = main(args)
    sys.exit(rv)


if __name__ == "__main__":
    run()
