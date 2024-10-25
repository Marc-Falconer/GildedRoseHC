# -*- coding: utf-8 -*-

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        
        def clamp_value(value, floor, ceiling):
            return max(
                min(value, ceiling),
                floor
            )
        
        """
        My plan here was to make this code more extensitable. To that end i've
        used a dictonary to collate all the rules for Gilded Rose. You'll notice
        that not all product types have all rules. This is because further down 
        I combine the default rules with the overide rules.
        
        I think by using a dictonary and defining the rules before the logic 
        is applied make this more extenistable and easier to maintain. This
        allows for future expansion with alternative rules that could be passed
        in from another module if forrequired for other companies.
        
        You'll notice i've used lambda quite a bit while setting out the rule.
        I conisdered using eval or the operator module. However, lambda has 
        better performance and I believe it's easier to read.
        """

        rules = {
            "default": {
                "sell_in_amount": lambda x: x - 1,
                # Below if `sell_in`` date is 0 or less 2 will be decrimented
                # from `quality``. Y is `sell_in`` X is prev quality.
                "quality_amount": lambda x, y: x - 2 if y <= 0 else - 1,
                # Set ceiling and floor so only values inbetween are returned.
                "quality_ceiling": 50,
                "quality_floor": 0,
            },
            "overides": {
                "aged brie": {
                    "quality_amount": lambda x, y: x + 1,
                    # Below was being used to calculate increasing decline in
                    # quality. However, this has a fault and was not giving
                    # the correct result. See Caluclation below.
                    # Now moved in 'quality_amount'.
                    "past_sell_in_mul": 1
                },
                "sulfuras": {
                    "quality_amount": lambda x, y: 80,
                    "sell_in_amount": lambda x: x,
                    "quality_ceiling": 80,
                },
                "backstage passes": {
                    "sell_in_case": [
                        {
                            "test": lambda x: x > 10,
                            "quality_amount": lambda x, y: 1
                        },
                        {
                            "test": lambda x: 5 < x <= 10,
                            "quality_amount": lambda x, y : 2
                        },
                        {
                            "test": lambda x: 0 < x <= 5,
                            "quality_amount": lambda x, y: 3
                        },
                        {
                            "test": lambda x: x <= 0,
                            "quality_amount": lambda x, y: 0
                        }
                    ]
                },
            },
            "Conjured": {
                "quality_amount": lambda x, y: x - 2
            }
        }
        
        for item in self.items:            
            # Determine what type of item it is as the required spec outlines it.
            # However, because this isn't in the data, we need to infer
            # it from the item name. We iterate over all the `overide` keys
            # in the rules dict and see if we get a substring match.
            for type_key in rules["overides"].keys():
                if type_key in item.name.lower():
                    # Combine and overwrite rules
                    item_rules = {
                        **rules["default"], **rules["overides"][type_key]
                    }
                    # TODO: with more time a check should be put in place to
                    # ensure we don't have another match
                    break
            else:
                # If there is no substring match we just use default rules.
                # eg: '+5 Dexterity Vest'
                item_rules = rules["default"]
            
            # Must set new sell in day first as other logic will depend on it.
            item.sell_in = item_rules["sell_in_amount"](item.sell_in,)
            
            # Lets check for speical case for `sell_in` like 'Backstage Passes'
            if "sell_in_case" in item_rules:
                # Loop through cases till we get a hit matching `test` criteria.
                for case in item_rules["sell_in_case"]:
                    if case["test"](item.sell_in,):
                        working_quality = case["quality_amount"]\
                            (item.quality, item.sell_in)
                            
                # TODO: if no case test is passed no quality logic is applied.
                # Maybe default logic should go here? Alert fault to dev?
            # Run logic as per `item_rules`
            else:
                working_quality = item_rules["quality_amount"]\
                    (item.quality, item.sell_in)
            
            # Small function to prevent exceeding min or max values.
            item.quality = clamp_value(
                working_quality,
                item_rules["quality_floor"],
                item_rules["quality_ceiling"]
            )
            
            # This logic was moved into the lambda
            # as it wasn't working correctly.
            # item.quality = clamp_value(
            #     working_quality * item_rules["past_sell_in_mul"] \
            #         if item.sell_in < 1 else working_quality,
            #     item_rules["quality_floor"],
            #     item_rules["quality_ceiling"]
            # )          


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
