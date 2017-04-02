# Name: Jack Palmstrom
# Username: jnpalmstrom
# Date: 3/28/2017

# Imports
import random

# Array of 100 values randomly selected from the range [1, 1000].
# This will be the array that is sorted.
comparison = 0
array_of_values = random.sample(xrange(1, 1001), 100)


# Function to calculate the median value of any 3 Ints
def median(x, y, z):

    if (x - y) * (z - x) >= 0:
        return x

    elif (y - x) * (z - y) >= 0:
        return y

    else:
        return z


# Function for the partition based off the median
def partition(array, left_ele, right_ele):

    left_index = array[left_ele]
    right_index = array[right_ele - 1]
    length = right_ele - left_ele

    if length % 2 == 0:
        middle_index = array[left_ele + length/2 - 1]

    else:
        middle_index = array[left_ele + length/2]

    pivot = median(left_index, right_index, middle_index)

    pivot_index = array.index(pivot)

    array[pivot_index] = array[left_ele]
    array[left_ele] = pivot

    j = left_ele + 1
    for element in range(left_ele + 1, right_ele):
        if array[element] < pivot:
            temp_ele = array[element]
            array[element] = array[j]
            array[j] = temp_ele
            j += 1

            # Writes the array to an output file for every iteration
            f = open('quicksort.txt', 'a')
            f.writelines(["%s, " % item for item in array])
            f.write("\n")
            f.close()

    left_end = array[left_ele]
    array[left_ele] = array[j - 1]
    array[j - 1] = left_end
    return j - 1


# Main quick_sort function
def quick_sort(array, left, right):
    global comparison

    # Makes sure left minus right never produces a negative number
    if left < right:
        new_pivot_index = partition(array, left, right)

        comparison += (right - left - 1)
        quick_sort(array, left, new_pivot_index)
        quick_sort(array, new_pivot_index + 1, right)

# Calls the array of 100 random integers between (1, 1000)
quick_sort(array_of_values, 0, len(array_of_values))

