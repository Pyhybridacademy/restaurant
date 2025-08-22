from django.core.management.base import BaseCommand
from menu.models import Category, Food
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populate the database with sample menu data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample menu data...')
        
        # Create categories
        categories_data = [
            {
                'name': 'Appetizers',
                'description': 'Start your meal with our delicious appetizers'
            },
            {
                'name': 'Main Courses',
                'description': 'Hearty and satisfying main dishes'
            },
            {
                'name': 'Desserts',
                'description': 'Sweet treats to end your meal'
            },
            {
                'name': 'Beverages',
                'description': 'Refreshing drinks and beverages'
            },
            {
                'name': 'Salads',
                'description': 'Fresh and healthy salad options'
            }
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f"Created category: {category.name}")
        
        # Create food items
        foods_data = [
            # Appetizers
            {
                'name': 'Buffalo Wings',
                'category': 'Appetizers',
                'price': Decimal('12.99'),
                'description': 'Crispy chicken wings tossed in spicy buffalo sauce, served with celery and blue cheese dip'
            },
            {
                'name': 'Mozzarella Sticks',
                'category': 'Appetizers',
                'price': Decimal('8.99'),
                'description': 'Golden fried mozzarella cheese sticks served with marinara sauce'
            },
            {
                'name': 'Loaded Nachos',
                'category': 'Appetizers',
                'price': Decimal('14.99'),
                'description': 'Crispy tortilla chips topped with cheese, jalapeños, sour cream, and guacamole'
            },
            {
                'name': 'Garlic Bread',
                'category': 'Appetizers',
                'price': Decimal('6.99'),
                'description': 'Fresh baked bread with garlic butter and herbs'
            },
            
            # Main Courses
            {
                'name': 'Classic Cheeseburger',
                'category': 'Main Courses',
                'price': Decimal('16.99'),
                'description': 'Juicy beef patty with cheese, lettuce, tomato, and pickles on a brioche bun'
            },
            {
                'name': 'Grilled Chicken Breast',
                'category': 'Main Courses',
                'price': Decimal('18.99'),
                'description': 'Seasoned grilled chicken breast served with roasted vegetables and mashed potatoes'
            },
            {
                'name': 'Fish and Chips',
                'category': 'Main Courses',
                'price': Decimal('17.99'),
                'description': 'Beer-battered cod served with crispy fries and tartar sauce'
            },
            {
                'name': 'Spaghetti Carbonara',
                'category': 'Main Courses',
                'price': Decimal('15.99'),
                'description': 'Classic Italian pasta with bacon, eggs, parmesan cheese, and black pepper'
            },
            {
                'name': 'BBQ Ribs',
                'category': 'Main Courses',
                'price': Decimal('22.99'),
                'description': 'Tender pork ribs glazed with our signature BBQ sauce, served with coleslaw'
            },
            {
                'name': 'Vegetarian Pizza',
                'category': 'Main Courses',
                'price': Decimal('14.99'),
                'description': 'Wood-fired pizza with fresh vegetables, mozzarella, and basil'
            },
            
            # Salads
            {
                'name': 'Caesar Salad',
                'category': 'Salads',
                'price': Decimal('11.99'),
                'description': 'Crisp romaine lettuce with parmesan cheese, croutons, and Caesar dressing'
            },
            {
                'name': 'Greek Salad',
                'category': 'Salads',
                'price': Decimal('12.99'),
                'description': 'Mixed greens with feta cheese, olives, tomatoes, and Greek dressing'
            },
            {
                'name': 'Chicken Cobb Salad',
                'category': 'Salads',
                'price': Decimal('15.99'),
                'description': 'Grilled chicken, bacon, blue cheese, avocado, and hard-boiled egg over mixed greens'
            },
            
            # Desserts
            {
                'name': 'Chocolate Cake',
                'category': 'Desserts',
                'price': Decimal('7.99'),
                'description': 'Rich chocolate layer cake with chocolate frosting'
            },
            {
                'name': 'Cheesecake',
                'category': 'Desserts',
                'price': Decimal('6.99'),
                'description': 'Creamy New York style cheesecake with berry compote'
            },
            {
                'name': 'Ice Cream Sundae',
                'category': 'Desserts',
                'price': Decimal('5.99'),
                'description': 'Vanilla ice cream with chocolate sauce, whipped cream, and cherry'
            },
            {
                'name': 'Apple Pie',
                'category': 'Desserts',
                'price': Decimal('6.99'),
                'description': 'Homemade apple pie with cinnamon and a flaky crust, served warm'
            },
            
            # Beverages
            {
                'name': 'Coca Cola',
                'category': 'Beverages',
                'price': Decimal('2.99'),
                'description': 'Classic Coca Cola soft drink'
            },
            {
                'name': 'Fresh Orange Juice',
                'category': 'Beverages',
                'price': Decimal('4.99'),
                'description': 'Freshly squeezed orange juice'
            },
            {
                'name': 'Coffee',
                'category': 'Beverages',
                'price': Decimal('3.99'),
                'description': 'Freshly brewed coffee, regular or decaf'
            },
            {
                'name': 'Iced Tea',
                'category': 'Beverages',
                'price': Decimal('2.99'),
                'description': 'Refreshing iced tea, sweetened or unsweetened'
            },
            {
                'name': 'Milkshake',
                'category': 'Beverages',
                'price': Decimal('5.99'),
                'description': 'Thick and creamy milkshake - vanilla, chocolate, or strawberry'
            }
        ]
        
        for food_data in foods_data:
            category = categories[food_data['category']]
            food, created = Food.objects.get_or_create(
                name=food_data['name'],
                category=category,
                defaults={
                    'price': food_data['price'],
                    'description': food_data['description'],
                    'is_available': True
                }
            )
            if created:
                self.stdout.write(f"Created food item: {food.name} - ${food.price}")
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSample data creation completed!\n'
                f'Categories created: {Category.objects.count()}\n'
                f'Food items created: {Food.objects.count()}'
            )
        )
