def excess_saturated_fat(saturated_fat_g, calories_per_serving):
    return (saturated_fat_g * 9 / calories_per_serving >= .1)

def excess_trans_fat(trans_fat_g, calories_per_serving):
    return (trans_fat_g * 9 / calories_per_serving >= .01) 

def excess_sugar(sugars_g, calories_per_serving):
    return (sugars_g * 4 / calories_per_serving >= .1)


def excess_sodium(calories_per_serving, sodium_mg):
    if calories_per_serving == 0:
        return (sodium_mg >= 45)
    else:
        return (sodium_mg / calories_per_serving >= 1)
    
def excess_calories(food_type, calories_per_serving, serving_size):
    if food_type == "solid":
        return (calories_per_serving / serving_size * 100 >= 275)
    elif food_type == "liquid":
        return (calories_per_serving / serving_size * 100 >= 70)
    else:
        raise ValueError("food_type must be 'solid' or 'liquid'")