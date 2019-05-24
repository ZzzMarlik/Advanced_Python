"""
functions to run TOAH tours.
"""


# Copyright 2013, 2014, 2017 Gary Baumgartner, Danny Heap, Dustin Wehr,
# Bogdan Simion, Jacqueline Smith, Dan Zingaro
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
# Copyright 2013, 2014 Gary Baumgartner, Danny Heap, Dustin Wehr


# you may want to use time.sleep(delay_between_moves) in your
# solution for 'if __name__ == "main":'
import time
from toah_model import TOAHModel


def get_i(n):
    """Return the number that makes min_steps(n) is smallest.
    @param int n: some integer
    @rtype: int
    """
    y = {}
    for i in range(1, n):
        a = 2 * min_steps(n - i) + 2 ** i - 1
        y[a] = i
    return y[min(y)]


def min_steps(n):
    """ Return the min of steps to move n rounds cheese.

    @param int n:
    @rtype: int

    """
    if n == 1:
        return 1
    else:
        return min([2 * min_steps(n - i) + 2 ** i - 1 for i in range(1, n)])


def move_three(n, lst, model, de, animate):
    """ Move items in src to dest recursively.

    @param int n:
    @param list lst:
    @param int de:
    @param bool animate:
    @param THOAModel model:
    @rtype: None
    """
    if n > 0:
        move_three(n - 1, [lst[0], lst[2], lst[1]], model, de, animate)
        model.move(lst[0], lst[1])
        if animate:
            time.sleep(de)
            print(model)
        move_three(n - 1, [lst[2], lst[1], lst[0]], model, de, animate)


def move_four(n, lst, model, de, animate):
    """ Move items in a to d recursively.

    @param int n:
    @param list lst:
    @param int de:
    @param bool animate:
    @param THOAModel model:
    @rtype: None
    """
    if n == 1:
        model.move(lst[0], lst[3])
        if animate:
            time.sleep(de)
            print(model)
    else:
        t = get_i(n)
        move_four(n - t, [lst[0], lst[3], lst[2], lst[1]], model, de, animate)
        move_three(t, [lst[0], lst[3], lst[2]], model, de, animate)
        move_four(n - t, [lst[1], lst[0], lst[2], lst[3]], model, de, animate)


def tour_of_four_stools(model, delay_btw_moves=0.5, animate=False):
    """Move a tower of cheeses from the first stool in model to the fourth.

    @type model: TOAHModel
        TOAHModel with tower of cheese on first stool and three empty
        stools
    @type delay_btw_moves: float
        time delay between moves if console_animate is True
    @type animate: bool
        animate the tour or not
    """
    q = model.get_number_of_cheeses()
    move_four(q, [0, 1, 2, 3], model, delay_btw_moves, animate)

if __name__ == '__main__':
    num_cheeses = 10
    delay_between_moves = 0.5
    console_animate = True

    # DO NOT MODIFY THE CODE BELOW.
    four_stools = TOAHModel(4)
    four_stools.fill_first_stool(number_of_cheeses=num_cheeses)

    tour_of_four_stools(four_stools,
                        animate=console_animate,
                        delay_btw_moves=delay_between_moves)

    print(four_stools.number_of_moves())
    # Leave lines below to see what python_ta checks.
    # File tour_pyta.txt must be in same folder
    import python_ta
    python_ta.check_all(config="tour_pyta.txt")
