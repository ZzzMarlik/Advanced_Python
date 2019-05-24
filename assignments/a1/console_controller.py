"""
ConsoleController: User interface for manually solving
Anne Hoy's problems from the console.
"""
# Copyright 2014, 2017 Dustin Wehr, Danny Heap, Bogdan Simion,
# Jacqueline Smith, Dan Zingaro
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 1, CSC148, Winter 2017.
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
from toah_model import TOAHModel, IllegalMoveError


def move(model, origin, dest):
    """ Apply move from origin to destination in model.

    May raise an IllegalMoveError.

    @param TOAHModel model:
        model to modify
    @param int origin:
        stool number (index from 0) of cheese to move
    @param int dest:
        stool number you want to move cheese to
    @rtype: None
    """
    model.move(origin, dest)


class ConsoleController:
    """ Controller for text console.
    """

    def __init__(self, number_of_cheeses, number_of_stools):
        """ Initialize a new ConsoleController self.

        @param ConsoleController self:
        @param int number_of_cheeses:
        @param int number_of_stools:
        @rtype: None
        """
        self.number_of_cheeses = number_of_cheeses
        self.number_of_stools = number_of_stools

    def play_loop(self):
        """ Play Console-based game.

        @param ConsoleController self:
        @rtype: None

        TODO:
        -Start by giving instructions about how to enter moves (which is up to
        you). Be sure to provide some way of exiting the game, and indicate
        that in the instructions.
        -Use python's built-in function input() to read a potential move from
        the user/player. You should print an error message if the input does
        not meet the specifications given in your instruction or if it denotes
        an invalid move (e.g. moving a cheese onto a smaller cheese).
        You can print error messages from this method and/or from
        ConsoleController.move; it's up to you.
        -After each valid move, use the method TOAHModel.__str__ that we've
        provided to print a representation of the current state of the game.
        """
        print("Instruction: Player enter the start stool and destination stool"
              " at every time. \n"
              "Be ware you should enter the number of stool. "
              "i.e.'1' means first stool. Player can\n"
              "quit this game by enter 'E' when a messauge pop out.\n"
              "Be careful, "
              "You can't put big cheese over smaller ones! Good luck!\n"
              "=============================================================="
              "===================\n ")
        model = TOAHModel(self.number_of_stools)
        model.fill_first_stool(self.number_of_cheeses)
        ext = ""
        print(model)
        while ext is not "E":
            try:
                origin = int(input("Please enter the origin of movement---> "))
                dest = int(input("Please enter the destination of "
                                 "movement---> "))
                model.move(origin - 1, dest - 1)
            except IllegalMoveError as e:
                print(e)
            except ValueError:
                print("Please read instruction carefully,"
                      " and enter a positive integer.")
            finally:
                print(model)
                ext = input("Type E to exit game or any other to keep playing"
                            "---> ")
        print("Game over")

if __name__ == '__main__':
    stools = 5
    cheeses = 4
    game = ConsoleController(cheeses, stools)
    game.play_loop()
    # Leave lines below as they are, so you will know what python_ta checks.
    # You will need consolecontroller_pyta.txt in the same folder.
    import python_ta
    python_ta.check_all(config="consolecontroller_pyta.txt")
