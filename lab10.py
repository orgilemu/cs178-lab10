import boto3

# boto3 uses the credentials configured via `aws configure` on EC2
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Foods')

def create_foods():
    FoodName = input("Enter food's name: ")
    Category = input("Enter food's category: ")
    Calories = int(input("Enter food's calories: "))

    table.put_item(Item={
        'FoodName': FoodName,
        'Category': Category,
        'Calories': Calories})

def print_food(food):
    FoodName = food.get("FoodName", "Unknown Food")
    Category = food.get("Category", "Unknown Category")
    Calories = food.get("Calories", "Unknown Calories")

    print(f"  FoodName  : {FoodName}")
    print(f"  Category   : {Category}")
    print(f"  Calories: {Calories}")
    print()



def print_all_foods():
    """Scan the entire Foods table and print each item."""

    # scan() retrieves ALL items in the table.
    # For large tables you'd use query() instead — but for our small
    # dataset, scan() is fine.
    response = table.scan()
    items = response.get("Items", [])
    
    if not items:
        print("No foods found. Make sure your DynamoDB table has data.")
        return
    
    print(f"Found {len(items)} food(s):\n")
    for food in items:
        print_food(food)    


def update_calories():

    try:
        FoodName = input("What is the food name? ")
        Calories = int(input("What is the new calorie count? "))
        table.update_item(
            Key={"FoodName": FoodName},
            UpdateExpression="SET Calories = list_append(Calories, :c)",
            ExpressionAttributeValues={':c': [Calories]}
        )
        print("updating calories")

    except Exception as e:
        print("Error in updating food calories")



def delete_foods():
    try:
        FoodName = input("What is the food name? ")
        table.delete_item(
            Key={"FoodName": FoodName})
        print("deleted the food")         
    except Exception as e:
        print("Error in deleting food")


def query_foods():

    FoodName = input("What is the food name? ")
    response = table.get_item(Key={"FoodName": FoodName})
    food = response.get("Item")

    if food:
        calories = food.get("Calories", [])
        if calories:
            average = sum(calories)/len(calories)
            print(f"The average calories for {FoodName} is {average}")

        else:
            print("no calorie information")
    else:
        print("food not found")

def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new food")
    print("Press R: to READ all foods")
    print("Press U: to UPDATE a food (add calorie information)")
    print("Press D: to DELETE a food")
    print("Press Q: to QUERY a food's average calories")
    print("Press X: to EXIT application")
    print("----------------------------")

def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_foods()
        elif input_char.upper() == "R":
            print_all_foods()
        elif input_char.upper() == "U":
            update_calories()
        elif input_char.upper() == "D":
            delete_foods()
        elif input_char.upper() == "Q":
            query_foods()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")

main()