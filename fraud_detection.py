# Henry Ginder
# CSE 160
# HW 6

import csv
import matplotlib.pyplot as plt
import random


def extract_election_vote_counts(filename, column_names):
    """Read file, then use the DictReader function from csv to iterate through.
    Convert to string to make cleaning the data easier. Get rid of unnessesary
    commas. Finally, return the list of numbers (as ints).

    Arguments:
        filename: a string representing the file's current directory
        column_names: a list of strings who represent the colunms we care about
    """

    with open(filename) as csv_file:
        jj = []
        pp = csv.DictReader(csv_file)
        for row in pp:
            for i in column_names:
                j = str(row[i])
                k = j.replace(',', '')
                if k == '':
                    continue
                else:
                    jj.append(int(k))
    return(jj)


def ones_and_tens_digit_histogram(numbers):
    """Given a list of intergers, compute the frequencies of all 10 intergers
    of the last two digits (the ones and tens places).

    Arguments:
        numbers: a list of ints
    """

    lst = []
    d = {}
    total = 0

    for i in numbers:
        j = i % 100
        lst.append(j)

    for i in lst:
        total += 2
        s = i % 10
        if s not in d:
            d[s] = 1
        else:
            d[s] += 1
        r = i // 10
        if r not in d:
            d[r] = 1
        else:
            d[r] += 1
    for i in range(10):
        if i not in d:
            d[i] = 0

    return[d[0]/total, d[1]/total, d[2]/total, d[3]/total, d[4]/total,
           d[5]/total, d[6]/total, d[7]/total, d[8]/total, d[9]/total]


def plot_random(numbers):
    """Given a list of intergers, make a new list of random intergers that is
    the same length as the input list.

    Arguments:
        numbers = list of ints
    """

    freqs = []

    for i in range(len(numbers)):
        freq = ones_and_tens_digit_histogram(numbers[i])
        freqs.append(freq)

    plt.clf()
    ideal = [.1, .1, .1, .1, .1, .1, .1, .1, .1, .1]
    plt.plot(ideal, label='ideal')

    for f in freqs:
        index = freqs.index(f)
        plt.plot(f, label='random {}'.format(index))
        plt.xlabel('Frequency')
        plt.ylabel('Digit')
        plt.title('Distribution of last two digits random dataset')
    plt.legend()
    # plt.show()
    plt.savefig('random-digits.png')


def plot_iranian_least_digits_histogram(histogram):
    """Plots graph of histogram, showing frequencies over all 10 digits.
    Plots ideal frequency line at 0.1. Saves a png image the to
    current directory.

    Arguments:
        freq = list of floats
    """

    plt.clf()
    ideal = [.1, .1, .1, .1, .1, .1, .1, .1, .1, .1]
    plt.plot(ideal, label='ideal')
    plt.plot(histogram, label='Iran')
    plt.xlabel('Frequency')
    plt.ylabel('Digit')
    plt.title('Distribution of last two digits in Iranian dataset')
    plt.legend()
    plt.savefig('iran-digits.png')
    # plt.show()


def plot_distribution_by_sample_size():
    """Creates five list of random numbers from 1 to 99 inclusive
    whose lengths are predetermined to be 10, 50, 100, 1000, 10000.
    Calls the plot_random function to plot the results.
    """

    length = [10, 50, 100, 1000, 10000]
    rr = []

    for i in length:
        r = []
        for j in range(i):
            z = random.randint(0, 99)
            r.append(z)
        rr.append(r)
    plot_random(rr)


def randoms_specific(length):
    """Create a list of random numbers from 1 to 99 inclusive, whose
    length is determined by input.

    Arguments:
        length = int
    """

    rs = []

    for i in range(length):
        z = random.randint(0, 99)
        rs.append(z)
    return rs


def mean_squared_error(numbers1, numbers2):
    """For two lists of the same length, determined the mean squared error.

    Arguments:
        numbers1 = list of floats
        numbers2 = list of floats
    """

    mse = 0
    n = len(numbers1)

    for i in range(len(numbers1)):
        error = numbers1[i] - numbers2[i]
        sq_er = error ** 2
        mse += sq_er / n
    return mse


def calculate_mse_with_uniform(histogram):
    """Given a list of freqeuncies for all 10 digits, call the
    mean_squared_error function on the input list and an ideal list of 10
    0.1 floats.

    Arguments:
        histogram = list of floats
    """

    ideal = [.1, .1, .1, .1, .1, .1, .1, .1, .1, .1]

    mse = mean_squared_error(histogram, ideal)
    return mse


def compare_iranian_mse_to_samples(iranian_mse, number_of_iranian_samples):
    """Builds 10000 groups of random numbers whose lengths are determined
    by input length by calling randoms_specific. Calls ones_and_tens_histogram
    and calculate_mse_with_uniform to get a list of mean squared errors(mses).
    Runs through the mses and checks how many of the 10000 groups are over or
    under the input mse. Calculates p-value to test our null hypothesis
    based on our over/ under data sample.

    Arguments:
        iran_mse = float
        number_of_iranian_samples = int
    """
    mses = []
    for i in range(10000):
        rs = randoms_specific(number_of_iranian_samples)
        r_freq = ones_and_tens_digit_histogram(rs)
        random_mse = calculate_mse_with_uniform(r_freq)
        mses.append(random_mse)

    over = 0
    under = 0
    for i in mses:
        if i < iranian_mse:
            under += 1
        else:
            over += 1

    p_val = 1 - (under / len(mses))

    printing(iranian_mse, over, under, p_val)


def compare_us_mse_to_samples(us_mse, number_of_us_samples):
    """Calls extract_election_vote_counts, ones_and_tens_histogram, and
    calculate_mse_with_uniform for our 2008 US election results. Then calls
    compare_iranian_mse_to_samples to check our null hypothesis for the data.
    """

    compare_iranian_mse_to_samples(us_mse, number_of_us_samples)


def printing(mse, over, under, p_val):
    """Prints desired outputs, given all the relevant statistics.

    Arguments:
        mse = float
        over = int
        under = int
        p_val = float
    """

    us = '2008 United States Election'
    iran = '2009 Iranian Election'

    if p_val > 0.1:
        print('')
        print('{} MSE: {}'.format(us, mse))
        print('Quantity of MSEs larger than or equal to the '
              '{}:{}'.format(us, over))
        print('Quantity of MSEs smaller than the {}: {}'.format(us, under))
        print('{} null hypothesis rejection '
              'level p: {}'.format(us, p_val))

    else:
        print('{} MSE: {}'.format(iran, mse))
        print('Quantity of MSEs larger than or equal to the '
              '{}: {}'.format(iran, over))
        print('Quantity of MSEs smaller than the {}: {}'.format(iran, under))
        print('{} null hypothesis rejection '
              'level p: {}'.format(iran, p_val))


def main():

    filename = 'election-iran-2009.csv'
    filename2 = 'election-us-2008.csv'
    cols = ["Ahmadinejad", "Rezai", "Karrubi", "Mousavi"]
    us_cols = ["Obama", "McCain", "Nader", "Barr", "Baldwin", "McKinney"]

    extract = extract_election_vote_counts((filename), cols)
    freq = ones_and_tens_digit_histogram(extract)
    plot_iranian_least_digits_histogram(freq)
    plot_distribution_by_sample_size()
    mse = calculate_mse_with_uniform(freq)
    compare_iranian_mse_to_samples(mse, len(extract))

    us_extract = extract_election_vote_counts(filename2, us_cols)
    us_freq = ones_and_tens_digit_histogram(us_extract)
    us_mse = calculate_mse_with_uniform(us_freq)
    compare_us_mse_to_samples(us_mse, len(us_extract))


if __name__ == "__main__":
    main()
