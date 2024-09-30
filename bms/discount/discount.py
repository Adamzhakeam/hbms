# import unittest
# from db import calculateDiscount
# def setTieredDiscount(discountDetails: dict) -> dict:
#         '''
#         This function applies a tiered discount based on the total sale amount.
        
#         @param discountDetails: A dictionary containing:
#             - 'totalAmount': The total sale amount.
#             - 'tiers': A list of tuples, each containing (min_amount, discount_rate)
#         '''
#         total_amount = discountDetails['totalAmount']
#         tiers = discountDetails['tiers']
        
#         # Initialize variables to track applicable discount
#         applicable_discount = 0
#         highest_discount_rate = None
#         closest_discount_rate = None
#         smallest_difference = float('inf')

#         for min_amount, discount_rate in tiers:
#             # Convert discount rate to float for calculation
#             discount_value = calculateDiscount({'discountRate': discount_rate})['discount']
            
#             if total_amount >= min_amount:
#                 # If the total amount exceeds this tier
#                 if highest_discount_rate is None or min_amount > highest_discount_rate[0]:
#                     highest_discount_rate = (min_amount, discount_rate)

#                 # Check for the closest tier
#                 difference = total_amount - min_amount
#                 if difference < smallest_difference:
#                     smallest_difference = difference
#                     closest_discount_rate = discount_rate

#         # Determine which discount to apply
#         if highest_discount_rate:
#             # Apply the highest discount if total_amount is greater than all
#             print('>>>>>>>>>>>>>>>>>>highestDiscount rate',highest_discount_rate[1])
#             applicable_discount = calculateDiscount({'discountRate': highest_discount_rate[1]})['discount'] * total_amount
#         elif closest_discount_rate:
#             # Otherwise, apply the closest discount
#             print('>>>>>>>>>>>>>>>closestAmount',closest_discount_rate)
#             applicable_discount = calculateDiscount({'discountRate': closest_discount_rate})['discount'] * total_amount

#         # Calculate the final discounted price
#         discounted_price = total_amount - applicable_discount

#         return {
#             'discountedPrice': discounted_price,
#             'applicableDiscount': applicable_discount,
#             'status': True if applicable_discount > 0 else False
#         }

#     # Example usage
# class TieredDiscountTestCase(unittest.TestCase):
#         def setUp(self):
#             self.test_cases = [
#     {
#         'totalAmount': 203,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (202, '12%'),
#             (204, '13%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 181.7,
#             'applicableDiscount': 21.3,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 50,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 50,
#             'applicableDiscount': 0,
#             'status': False
#         }
#     },
#     {
#         'totalAmount': 400,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 340,
#             'applicableDiscount': 60,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 75,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 75,
#             'applicableDiscount': 0,
#             'status': False
#         }
#     },
#     {
#         'totalAmount': 250,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 212.5,
#             'applicableDiscount': 37.5,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 150,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 135,
#             'applicableDiscount': 15,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 350,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 297.5,
#             'applicableDiscount': 52.5,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 80,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 76,
#             'applicableDiscount': 4,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 600,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 510,
#             'applicableDiscount': 90,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 30,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 30,
#             'applicableDiscount': 0,
#             'status': False
#         }
#     },
#     {
#         'totalAmount': 450,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 382.5,
#             'applicableDiscount': 67.5,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 70,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 63.5,
#             'applicableDiscount': 6.5,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 700,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 595,
#             'applicableDiscount': 105,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 40,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 38,
#             'applicableDiscount': 2,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 800,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 680,
#             'applicableDiscount': 120,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 20,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 19,
#             'applicableDiscount': 1,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 900,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 765,
#             'applicableDiscount': 135,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 10,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 9.5,
#             'applicableDiscount': 0.5,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1000,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 850,
#             'applicableDiscount': 150,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 5,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 4.75,
#             'applicableDiscount': 0.25,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1100,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 935,
#             'applicableDiscount': 165,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.95,
#             'applicableDiscount': 0.05,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1200,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1020,
#             'applicableDiscount': 180,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.1,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.095,
#             'applicableDiscount': 0.005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1300,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1095,
#             'applicableDiscount': 205,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.01,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.0095,
#             'applicableDiscount': 0.0005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1400,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1196,
#             'applicableDiscount': 204,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.001,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.00095,
#             'applicableDiscount': 0.00005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1500,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1275,
#             'applicableDiscount': 225,
#             'status': True
#         }
        
#     },
#     {
#         'totalAmount': 1500,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1275,
#             'applicableDiscount': 225,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.01,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.0095,
#             'applicableDiscount': 0.0005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1400,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1196,
#             'applicableDiscount': 204,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.001,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.00095,
#             'applicableDiscount': 0.00005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1500,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1275,
#             'applicableDiscount': 225,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.01,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.0095,
#             'applicableDiscount': 0.0005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1400,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1196,
#             'applicableDiscount': 204,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.001,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.00095,
#             'applicableDiscount': 0.00005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1500,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1275,
#             'applicableDiscount': 225,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.01,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.0095,
#             'applicableDiscount': 0.0005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1400,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1196,
#             'applicableDiscount': 204,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.001,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.00095,
#             'applicableDiscount': 0.00005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1500,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1275,
#             'applicableDiscount': 225,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.01,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.0095,
#             'applicableDiscount': 0.0005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1400,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1196,
#             'applicableDiscount': 204,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.001,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.00095,
#             'applicableDiscount': 0.00005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1500,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1275,
#             'applicableDiscount': 225,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.01,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.0095,
#             'applicableDiscount': 0.0005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1400,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1196,
#             'applicableDiscount': 204,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.001,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.00095,
#             'applicableDiscount': 0.00005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1500,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1275,
#             'applicableDiscount': 225,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.01,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.0095,
#             'applicableDiscount': 0.0005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1400,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1196,
#             'applicableDiscount': 204,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.001,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.00095,
#             'applicableDiscount': 0.00005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1500,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1275,
#             'applicableDiscount': 225,
#             'status': True
#         }
#     },{
#         'totalAmount': 1500,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1275,
#             'applicableDiscount': 225,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.01,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.0095,
#             'applicableDiscount': 0.0005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1400,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1196,
#             'applicableDiscount': 204,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.001,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.00095,
#             'applicableDiscount': 0.00005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1500,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1275,
#             'applicableDiscount': 225,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.01,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.0095,
#             'applicableDiscount': 0.0005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1400,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1196,
#             'applicableDiscount': 204,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.001,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.00095,
#             'applicableDiscount': 0.00005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1500,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1275,
#             'applicableDiscount': 225,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.01,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.0095,
#             'applicableDiscount': 0.0005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1400,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1196,
#             'applicableDiscount': 204,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.001,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.00095,
#             'applicableDiscount': 0.00005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1500,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1275,
#             'applicableDiscount': 225,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.01,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.0095,
#             'applicableDiscount': 0.0005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1400,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1196,
#             'applicableDiscount': 204,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.001,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.00095,
#             'applicableDiscount': 0.00005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1500,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1275,
#             'applicableDiscount': 225,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.01,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.0095,
#             'applicableDiscount': 0.0005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1400,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1196,
#             'applicableDiscount': 204,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.001,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.00095,
#             'applicableDiscount': 0.00005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1500,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1275,
#             'applicableDiscount': 225,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.01,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.0095,
#             'applicableDiscount': 0.0005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1400,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1196,
#             'applicableDiscount': 204,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.001,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.00095,
#             'applicableDiscount': 0.00005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1500,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1275,
#             'applicableDiscount': 225,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.01,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.0095,
#             'applicableDiscount': 0.0005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1400,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1196,
#             'applicableDiscount': 204,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.001,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.00095,
#             'applicableDiscount': 0.00005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1500,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1275,
#             'applicableDiscount': 225,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.01,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.0095,
#             'applicableDiscount': 0.0005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 1400,
#         'tiers': [
#             (100, '5%'),
#             (200, '10%'),
#             (300, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 1196,
#             'applicableDiscount': 204,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 2500,
#         'tiers': [
#             (500, '10%'),
#             (1000, '20%'),
#             (1500, '30%')
#         ],
#         'expected': {
#             'discountedPrice': 1750,
#             'applicableDiscount': 750,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.05,
#         'tiers': [
#             (0.01, '5%'),
#             (0.02, '10%'),
#             (0.03, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.045,
#             'applicableDiscount': 0.005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 3500,
#         'tiers': [
#             (1000, '10%'),
#             (2000, '20%'),
#             (3000, '30%')
#         ],
#         'expected': {
#             'discountedPrice': 2450,
#             'applicableDiscount': 1050,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.0001,
#         'tiers': [
#             (0.00001, '5%'),
#             (0.00002, '10%'),
#             (0.00003, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.00009005,
#             'applicableDiscount': 0.00000005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 4500,
#         'tiers': [
#             (1500, '10%'),
#             (2500, '20%'),
#             (3500, '30%')
#         ],
#         'expected': {
#             'discountedPrice': 3150,
#             'applicableDiscount': 1350,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.001,
#         'tiers': [
#             (0.0001, '5%'),
#             (0.0002, '10%'),
#             (0.0003, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.00085,
#             'applicableDiscount': 0.00000015,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 5500,
#         'tiers': [
#             (2000, '10%'),
#             (3000, '20%'),
#             (4000, '30%')
#         ],
#         'expected': {
#             'discountedPrice': 3850,
#             'applicableDiscount': 1650,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.00001,
#         'tiers': [
#             (0.000001, '5%'),
#             (0.000002, '10%'),
#             (0.000003, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.00000875,
#             'applicableDiscount': 0.00000000025,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 6500,
#         'tiers': [
#             (2500, '10%'),
#             (3500, '20%'),
#             (4500, '30%')
#         ],
#         'expected': {
#             'discountedPrice': 4550,
#             'applicableDiscount': 1950,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.000001,
#         'tiers': [
#             (0.0000001, '5%'),
#             (0.0000002, '10%'),
#             (0.0000003, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.00000085,
#             'applicableDiscount': 0.00000000000005,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 7500,
#         'tiers': [
#             (3000, '10%'),
#             (4000, '20%'),
#             (5000, '30%')
#         ],
#         'expected': {
#             'discountedPrice': 5250,
#             'applicableDiscount': 2250,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.00001,
#         'tiers': [
#             (0.000001, '5%'),
#             (0.000002, '10%'),
#             (0.000003, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.00000875,
#             'applicableDiscount': 0.00000000025,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 8500,
#         'tiers': [
#             (3500, '10%'),
#             (4500, '20%'),
#             (5500, '30%')
#         ],
#         'expected': {
#             'discountedPrice': 5950,
#             'applicableDiscount': 2550,
#             'status': True
#         }
#     },
#     {
#         'totalAmount': 0.000001,
#         'tiers': [
#             (0.0000001, '5%'),
#             (0.0000002, '10%'),
#             (0.0000003, '15%')
#         ],
#         'expected': {
#             'discountedPrice': 0.00000085,
#             'applicableDiscount': 0.00000000000005,
#             'status': True
#         }
#     }, {
#                 'totalAmount': 1500,
#                 'tiers': [
#                     (100, '5%'),
#                     (200, '10%'),
#                     (300, '15%')
#                 ],
#                 'expected': {
#                     'discountedPrice': 1275,
#                     'applicableDiscount': 225,
#                     'status': True
#                 }
#             }

# ]
#     # print(len(test_cases))
#     # import unittest
# # from your_module import setTieredDiscount  # Replace 'your_module' with the actual module name



# def test_setTieredDiscount(self):
#         for case in self.test_cases:
#             print('>>>>>>>',case)
#             result = setTieredDiscount(case['totalAmount'], case['tiers'])
#             self.assertEqual(result['discountedPrice'], case['expected']['discountedPrice'],
#                              f"Expected discounted price {case['expected']['discountedPrice']}, got {result['discountedPrice']}")
#             self.assertEqual(result['applicableDiscount'], case['expected']['applicableDiscount'],
#                              f"Expected applicable discount {case['expected']['applicableDiscount']}, got {result['applicableDiscount']}")
#             self.assertEqual(result['status'], case['expected']['status'],
#                              f"Expected status {case['expected']['status']}, got {result['status']}")

# if __name__ == '__main__':  
#     unittest.main()
