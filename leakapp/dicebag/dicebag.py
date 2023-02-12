#!/usr/bin/env python3

import random


class DiceBag:
    """The virtual dicebag.  Pull out a set of dice."""
    def __init__(self, dice_req: str=None) -> None:

        # The default dice is a d20 w/o a modifier.
        if dice_req is None:
            self.dice = "d20"
            self.num_rolls = 1
            self.num_sides = 20
            self.modifier = 0

        # Store the dice roll, number of sides, and modifier from the supplied string.
        else:
            self.dice = dice_req
            self.num_rolls, self.num_sides, self.modifier = self._parse_request(dice_req)

        # 
        self.rolled = False
        self.rolls = {}

        # 
        self.total = 0
        self.advantage = 0
        self.disadvantage = 0

    def __str__(self):

        # Print basic info about selected dice.
        msg  = f"Selected Dice:"
        msg += f"  Dice: {self.dice}\n"
        msg += f"  Modifier: {self.modifier}\n"
        msg += f"  Rolled:  {self.rolled}\n"
        
        # 
        if self.rolled:
            msg += f"Rolls:\n"
            for roll, result in self.rolls.items():
                msg += f"  Roll #{roll}: {result}\n"

        # 
            msg = f"Total: {self.total}"
            
        # 
        return msg

    # 
    allowed_dice = [
        "1",
        "2",
        "4",
        "6",
        "8",
        "10",
        "12",
        "20",
        "100"
    ]

    class RollRequestParseError(Exception):
        def __init__(self, roll_request: str) -> None:
            message = "\n"
            message += "Failed to process this roll request:\n"
            message += f"    {roll_request}"
            super().__init__(message)

    class InvalidRollNumber(Exception):
        def __init__(self, num_rolls) -> None:
            message = "\n"
            message += "The total number of rolls must be a numeric value:\n"
            message += f"    {num_rolls}"
            super().__init__(message)

    class InvalidDieRequest(Exception):
        def __init__(self, requested_die) -> None:
            message = "\n"
            message += "This die is not supported:\n"
            message += f"    {requested_die}"
            super().__init__(message)

    class InvalidModifier(Exception):
        def __init__(self, modifier) -> None:
            message = "\n"
            message += "The modifier must be a numeric value:\n"
            message += f"    {modifier}"
            super().__init__(message)

    @classmethod
    def _parse_request(cls, roll_request: str):

        # Split the request at the d.  If the length of the request_list isn't 2, the request can't be parsed.
        request_d_split = roll_request.split("d")
        if len(request_d_split) != 2:
            raise cls.RollRequestParseError(roll_request)

        # The first number is the number of rolls.  If the number is omited, we can assume it's 1.
        num_rolls = request_d_split[0]
        if num_rolls == '':
            num_rolls = 1

        # Check if there's a + or a - in the request, indicating a modifier to the roll.
        modifier = 0
        request_pos_split = request_d_split[1].split("+")
        request_neg_split = request_d_split[1].split("-")

        # The number of sides will be either last or directly before the modifier.
        num_sides = request_d_split[1]
        if len(request_pos_split) == 2:
            num_sides = request_pos_split[0]
            modifier = request_pos_split[1]
        elif len(request_neg_split) == 2:
            num_sides= request_neg_split[0]
            modifier = f"-{request_neg_split[1]}"

        # Make sure the roll is allowed.
        if num_sides not in cls.allowed_dice:
            raise cls.InvalidDieRequest(num_sides)

        # Since we need to do actual maths with these, convert these to integers.
        num_sides = int(num_sides)

        try:
            num_rolls = int(num_rolls)
        except ValueError:
            raise cls.InvalidRollNumber(num_rolls)

        try:
            modifier = int(modifier)
        except ValueError:
            raise cls.InvalidModifier(modifier)

        # Return the number of rolls, number of sides, and the modifier.
        return num_rolls, num_sides, modifier

    @classmethod
    def roll_the_dice_old(cls, roll_request: str):

        # TODO: Once the rework is done, make this a proper class method that returns a rolled d20 by default.
        # Otherwise, roll the requested dice.

        # Parse the request.
        num_rolls, num_sides, modifier = cls._parse_request(roll_request)

        # Roll the requested number of the specified dice.
        total = 0
        rolls = {}
        for roll_num in range(1, num_rolls+1):
            roll = random.randrange(1, num_sides)
            total += roll
            rolls[roll_num] = roll

        # Add the modifier (this can be negative).
        total += modifier

        return total, rolls

    @classmethod
    def roll_the_dice(cls, roll_request: str):
        dice = cls(roll_request)
        dice.roll()
        return dice


    def roll(self):

        # Roll the selected dice.
        for roll_num in range(1, self.num_rolls+1):
            roll = random.randrange(1, self.num_sides+1)
            self.total += roll
            self.rolls[roll_num] = roll

        # Add the modifier (this can be negative).
        self.total += self.modifier

        # If rolling a d20, check for advantage/disadvantage.
        if self.num_sides == 20:
            self.advantage = self._find_advantage()
            self.disadvantage = self._find_disadvantage()

        # The dice has been rolled.
        self.rolled = True

    def _find_advantage(self):

        # Loop through the rolls, storing the highest roll.
        highest = 0
        for roll in self.rolls.values():
            if roll > highest:
                highest =  roll

        # Return the highest value.
        return highest

    def _find_disadvantage(self):

        # Loop through the rolls, storing the lowest roll.
        lowest = 0
        for roll in self.rolls.values():
            if roll < lowest:
                lowest = roll

        # Return the lowest value.
        return lowest

