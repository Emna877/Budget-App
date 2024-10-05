class Category:
    def __init__(self,name):
        self.name=name
        self.ledger=[]

    def __str__(self):
        total = 0
        title = self.name.center(30, '*')
        res = title + '\n'
        for entry in self.ledger:
            # Skip entries that are transfers from other categories
            if entry['description'].startswith('Transfer from'):
                continue
            descrip = entry['description'][:23]
            amount = entry['amount']
            total += amount
            formatted = f'{amount:.2f}'
            res += f'{descrip:<23}{formatted:>7}\n'
        tot = f'Total: {total:.2f}'
        res += tot
        return res

    def deposit(self,amount,description=""):
        self.ledger.append({'amount': amount, 'description': description})

    def get_balance(self):
        total_balance=sum(item['amount'] for item in self.ledger)
        return total_balance
   
    def check_funds(self,amount):
        return self.get_balance()>=amount

    def withdraw(self,amount, description=""):
        if not self.check_funds(amount):
            return False
        else:
            self.ledger.append({'amount': -amount, 'description': description})
            return True
    
    def transfer(self,amount,category):
        if not self.check_funds(amount):
            return False
        else:
            self.withdraw(amount,f'Transfer to {category.name}')
            self
            category.deposit(amount, f'Transfer from {self.name}')
            return True

food = Category('Food')
food.deposit(1000, 'deposit')
food.withdraw(10.15, 'groceries')
food.withdraw(15.89, 'restaurant and more food for dessert')
clothing = Category('Clothing')
food.transfer(50, clothing)
print(food)
print(clothing)



    


def create_spend_chart(categories):
    # Calculate total spending for each category
    total_spent = {}
    overall_total = 0
    
    for category in categories:
        total = sum(item['amount'] for item in category.ledger if item['amount'] < 0)
        total_spent[category.name] = -total
        overall_total += -total

    # Calculate percentages
    percentages = {name: (spent / overall_total) * 100 for name, spent in total_spent.items()}

    # Create chart
    chart_lines = []
    chart_lines.append("Percentage spent by category")
    
    # Generate each line of the chart
    for i in range(100, -10, -10):
        line = f'{i:>3}| '  # Label for the percentage
        for category in categories:
            percentage = percentages[category.name]
            if percentage >= i:
                line += 'o  '
            else:
                line += '   '
        chart_lines.append(line)
    
    # Add the horizontal line
    chart_lines.append('    ' + '-' * (len(categories) * 3 + 1))
    
    # Add category labels
    max_length = max(len(category.name) for category in categories)
    for i in range(max_length):
        line = '     '
        for category in categories:
            name = category.name
            line += f'{name[i] if i < len(name) else " "}  '
        chart_lines.append(line)
    
    return '\n'.join(chart_lines)

# Example Usage
food = Category('Food')
food.deposit(1000, 'deposit')
food.withdraw(10.15, 'groceries')
food.withdraw(15.89, 'restaurant and more food for dessert')

clothing = Category('Clothing')
clothing.deposit(500, 'deposit')
clothing.withdraw(25.50, 'clothing purchase')

entertainment = Category('Entertainment')
entertainment.deposit(200, 'deposit')
entertainment.withdraw(60.00, 'movie tickets')

print(create_spend_chart([food, clothing, entertainment]))