class Solution:
    def maxSatisfied(self, customers: List[int], grumpy: List[int], minutes: int) -> int:

        # Only count grumpy-minute customers in the window
        customer_sum = sum(customers[i] * grumpy[i] for i in range(minutes))
        max_sum = customer_sum
        max_index = 0 

        for i in range(minutes, len(customers)): 
            # Only count grumpy-minute customers
            customer_sum += customers[i] * grumpy[i] - customers[i - minutes] * grumpy[i - minutes]

            if customer_sum > max_sum: 
                max_index = i - minutes + 1 
                max_sum = customer_sum 

        for j in range(max_index, max_index + minutes): 
            grumpy[j] = 0

        return sum(customers[k] for k in range(len(customers)) if grumpy[k] == 0 )
        