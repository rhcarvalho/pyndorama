# -*- coding: utf-8 -*-
import unittest
from aventura import *

####################################################################
# This is for creating a new test adventure!
##class UsefulData(object):
##    worlds = [["LABASE", "You are and intern at the Laboratory"
##                         " of Automated Systems Engineering"]]
##    places = [["Table", "A flat table."],
##              ["Glass Wall", "A wall made of glass."]]
##            "User Story Cards", "A bunch of user story cards"
##            ("pen", "a colorful pen")
####################################################################

class TestCreateThings(unittest.TestCase):
    def testCreateWorld(self):
        world = World("name", "desc")
        self.assertEqual(world.name, "name")
        self.assertEqual(world.description, "desc")

    def testCreatePlace(self):
        place = Place("name", "desc")
        self.assertEqual(place.name, "name")
        self.assertEqual(place.description, "desc")

    def testCreateObject(self):
        object = Object("name", "desc")
        self.assertEqual(object.name, "name")
        self.assertEqual(object.description, "desc")

    def testCreateVerb(self):
        verb = Verb("name", "desc")
        self.assertEqual(verb.name, "name")
        self.assertEqual(verb.description, "desc")

    def testCreateVerbWithoutDesc(self):
        verb = Verb("name")
        self.assertEqual(verb.name, "name")

    def testCreateAction(self):
        action = Action("type")
        self.assertEqual(action.name, "type")

    def testCreateActionWithReturnText(self):
        action = Action("type", "return text")
        self.assertEqual(action.name, "type")
        self.assertEqual(action.description, "return text")


class TestCreateThingsWithContents(unittest.TestCase):
    def testCreateWorldWithContents(self):
        place = Place("name", "desc")
        world = World("name", "desc", [place])
        self.assertEqual(world.contents, [place])

    def testCreatePlaceWithContents(self):
        object = Object("name", "desc")
        place = Place("name", "desc", [object])
        self.assertEqual(place.contents, [object])

    def testCreateObjectWithContents(self):
        verb = Verb("name", "desc")
        object = Object("name", "desc", [verb])
        self.assertEqual(object.contents, [verb])

    def testCreateVerbWithContents(self):
        action = Action("type", "return text")
        verb = Verb("name", "desc", [action])
        self.assertEqual(verb.contents, [action])

    def testCreateVerbWithoutDescWithContents(self):
        action = Action("type", "return text")
        verb = Verb("name", contents=[action])
        self.assertEqual(verb.contents, [action])


class TestAddThings(unittest.TestCase):
    def testAddPlaceToWorld(self):
        world = World("name", "desc")
        place = Place("name", "desc")
        place.additself(world)
        self.assertEqual(world.contents, [place])

    def testAddObjectToPlace(self):
        place = Place("name", "desc")
        object = Object("name", "desc")
        object.additself(place)
        self.assertEqual(place.contents, [object])

    def testAddVerbToObject(self):
        object = Object("name", "desc")
        verb = Verb("name", "desc")
        verb.additself(object)
        self.assertEqual(object.contents, [verb])

    def testAddActionToVerb(self):
        verb = Verb("name", "desc")
        action = Action("type", "return text")
        action.additself(verb)
        self.assertEqual(verb.contents, [action])


class TestRemoveThings(unittest.TestCase):
    def testRemovePlaceFromWorld(self):
        place = Place("name", "desc")
        world = World("name", "desc", [place])
        place.removeitself(world)
        self.assertEqual(world.contents, [])

    def testRemoveObjectFromPlace(self):
        object = Object("name", "desc")
        place = Place("name", "desc", [object])
        object.removeitself(place)
        self.assertEqual(place.contents, [])

    def testRemoveVerbFromObject(self):
        verb = Verb("name", "desc")
        object = Object("name", "desc", [verb])
        verb.removeitself(object)
        self.assertEqual(object.contents, [])

    def testRemoveActionFromVerb(self):
        action = Action("type", "return text")
        verb = Verb("name", "desc", [action])
        action.removeitself(verb)
        self.assertEqual(verb.contents, [])


if __name__ == '__main__':
    unittest.main()