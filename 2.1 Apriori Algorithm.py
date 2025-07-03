import pandas as pd
from itertools import combinations

def categories_to_list(wd: str) -> list:
    """Import all categories of POIs from csv to a list
    
        Args:
            wd: Working directory that contain the 'dataset' folder. All datasets are in stored in the 'dataset' folder.
        Returns:
            category_list: List of categories.

    """
    category_format = '/dataset/POI_datacategories.csv'
    category_list = pd.read_csv(f'{wd}{category_format}', header=None).squeeze().tolist()

    return category_list

def data_preparation(file_path: str, head: int = 0) -> tuple:
    """Convert each grid into a basket of POIs.
        
        Args:
            file_path: File path to each city's dataset.
            head: Only for function 'for_checking()'. To refer to [head] number of rows in the dataset.
            
        Returns:
            ls: A nested list, where each element is a basket of POIs for a grid.
            distinct_category: All distinct categories in city.
    """
    
    # Convert each column into a list
    df = pd.read_csv(file_path)
    df = df.drop(columns='POI_count')

    if head == 0:
        x = df.x.tolist()
        y = df.y.tolist()
        category = df.category.tolist()
    else:
        x = df.x.head(head).tolist()
        y = df.y.head(head).tolist()
        category = df.category.head(head).tolist()
    distinct_category = list(map(lambda x: (x,), list(set(category))))

    # Convert each grid into a basket
    ls = []
    prev_x = 0
    prev_y = 0
    for xx, yy, poi in zip(x, y, category):        
        if xx != prev_x or yy != prev_y:
            if prev_x != 0: ls.append(tuple(basket))
            basket = []

        basket.append(poi)
        prev_x = xx
        prev_y = yy
    ls.append(tuple(basket))

    return ls, distinct_category

def name_format(wd: str, city: str) -> str:
    """Formats the file path based on the given city.

        Args:
            wd: Working directory that contain the 'dataset' folder. All datasets are in stored in the 'dataset' folder.
            city: City name.
        Returns:
            File path for the dataset of a given city.
    """
    city_format = '/dataset/POIdata_city'

    return f'{wd}{city_format}{city}.csv'

def candidate_generation(f_k: list, k: int) -> list:
    """Generate C_{k+1} from F_k, using the F_{k-1} x F_{k-1} method.

        Args:
            f_k: A list containing the frequent k-itemsets, where each itemset have k POIs.
            k: Current k value.
        
        Returns:
            c_kp1: Candidate itemsets for C_{k+1}.
    """
    # print('\tcandidate generation...')

    c_kp1 = [] # C_{k+1}
    length_f_k = len(f_k)
    f_k_copy = f_k.copy()

    if k == 1:
        for i in range(length_f_k):
            for j in range(i, length_f_k):
                if f_k_copy[i] != f_k_copy[j]:
                    itemset = (int(str(f_k_copy[i])[1:-2]), int(str(f_k_copy[j])[1:-2]))
                    c_kp1.append(itemset)
    else:
        # Merge two itemset in F_k if the first k-1 items are identical.
        # Append the merged itemset into C_{k+1}
        for i in range(length_f_k):
            p = f_k_copy[i]
            for j in range(i, length_f_k):
                q = f_k_copy[j]
                if p[:-1] == q[:-1]:
                    itemset = list(p).copy()
                    itemset.append(q[-1])
                    c_kp1.append(tuple(itemset))
    
    # print(f'\t\t{len(c_kp1)} candidates generated.')
    return c_kp1

def generate_subset(itemset: list, n: int) -> list:
    """Generate subsets of length n from a list.

        Args:
            ls: List to generate subset from.
            n: To generate subsets on length n.

        Returns:
            A list of all generated subsets.
    """
    return list(combinations(itemset, n))

def candidate_pruning(c_kp1: list, f_k: list, k: int) -> None:
    """Prune candidate itemsets in C_{k+1} if any of its subset of
    length k is not in F_k.

        Args:
            c_kp1: Candidate itemsets for C_{k+1}.
            f_k: A list containing the frequent k-itemsets, where each itemset have k POIs.
            k: Current k value.

    """
    # print('\tcandidate pruning...')

    i = 0
    count = 0
    while i < len(c_kp1):
        itemset = c_kp1[i]
        subsets = generate_subset(itemset, k)
        for subset in subsets:
            for index, frequent_item in enumerate(f_k):
                if subset == frequent_item:
                    index -= 1
                    break
            if index == len(f_k) - 1:
                c_kp1.remove(itemset)
                i -= 1
                count += 1
                break
        i += 1
    
    # print(f'\t\t{count} candidates pruned.')

def support_counting(c_kp1: list, ls: list) -> list:
    """Count the support of each candidate itemset.

        Args:
            c_kp1: Candidate itemsets for C_{k+1}.
            ls: A nested list, where each element is a basket of POIs for a grid.
        Returns:
            sup_count: List of support count of each candidate in C_{k+1}.
    """
    sup_count = []
    for itemset in c_kp1:
        count = 0
        for basket in ls:
            if set(itemset).intersection(set(basket)) == set(itemset):
                count += 1
        sup_count.append(count)

    return sup_count

def candidate_elimination(c_kp1: list, ls: list, minsup: int) -> None:
    """Count the support of each candidate itemset and eliminate non frequent items.

        Args:
            c_kp1: Candidate itemsets for C_{k+1}.
            ls: A nested list, where each element is a basket of POIs for a grid.
            minsup: Minimum support threshold
    """
    # print('\tcandidate elimination...')

    sup_count = support_counting(c_kp1, ls)
    to_remove = []
    for index, count in enumerate(sup_count):
        if count < minsup: to_remove.append(index)
    for i in sorted(to_remove, reverse=True):
        c_kp1.pop(i)
    
    # print(f'\t\t{len(to_remove)} infrequent candidates eliminated.')

def f_1(ls: list, distinct_category: list, minsup: int) -> list:
    """Generate freuqent itemset of length 1.
    
        Args:
            ls: A nested list, where each element is a basket of POIs for a grid.
            distinct_category: All distinct categories in city.
            minsup: Minimum support threshold.
        Returns:
            f_1: Freuqent itemset of length 1.
    """
    f_1 = distinct_category.copy()
    candidate_elimination(f_1, ls, minsup)
    
    return f_1

def add_freq_itemset(c_kp1: list, freq_itemset: list) -> None:
    """Add frequent itemsets of length k into the list of final frequent itemsets, and remove any subsets of length k-1.
    
        Args:
            c_kp1: Candidate itemsets for C_{k+1}.
            freq_itemset: A list of frequent itemsets of all lengths.
    """
    for itemset in c_kp1:
        subsets = generate_subset(itemset, len(itemset) - 1)
        for subset in subsets:
            if subset in freq_itemset:
                freq_itemset.remove(subset)
        freq_itemset.append(itemset)

def for_checking():
    """A function used to check on the correctness of the other functions. This function runs on a very small subset of data from a city.
    The generated frequent itemsets can be manually counted to verify correctness.
    """

    # wd: Working directory that contain the 'dataset' folder. All datasets are in stored in the 'dataset' folder.
    wd = '/Users/limjunyu/Library/Mobile Documents/com~apple~CloudDocs/file/ntu/semester 1/sc4020 data anlytics and mining/project 2'

    city = 'A'
    support_threshold = 0.3
    head = 60
    categories = categories_to_list(wd)

    ls, distinct_category = data_preparation(name_format(wd, city), head)

    print(f'CITY {city}:')
    print(f'support_threshold: {support_threshold}')

    index = 1
    print(f'baskets in first {head} rows of data')
    for pois in ls:
        print(f'\t{index}.\t', end="")
        for poi in pois:
            print(categories[poi - 1], end=', ')
        print()
        index += 1

    k = 1
    c_kp1 = []
    minsup = round(len(ls) * support_threshold)
    f_k = f_1(ls, distinct_category, minsup)
    freq_itemset = []

    while f_k:
        print(f'\tk: {k}')
        c_kp1 = candidate_generation(f_k, k)
        candidate_pruning(c_kp1, f_k, k)
        candidate_elimination(c_kp1, ls, minsup)
        add_freq_itemset(c_kp1, freq_itemset)
        f_k = c_kp1
        k += 1

    if freq_itemset:
        print(f'\tfrequent itemset(s) in city {city} for minsup of {minsup}:')
        index = 1
        sup_count = support_counting(freq_itemset, ls)
        for itemset in freq_itemset:

            print(f'\t{index}. [count: {sup_count[index - 1]}]\t', end="")
            for item in itemset:
                print(categories[item - 1], end=", ")
            print()
            index += 1
    else:
        print(f'\tthere are no frequent itemsets in city {city} for minsup of {minsup}')

def main():
    """Main mining function."""

    # wd: Working directory that contain the 'dataset' folder. All datasets are in stored in the 'dataset' folder.
    wd = '/Users/limjunyu/Library/Mobile Documents/com~apple~CloudDocs/file/ntu/semester 1/sc4020 data anlytics and mining/project 2'

    cities = ['A', 'B', 'C', 'D']
    support_thresholds = [0.15, 0.2, 0.3, 0.4]
    categories = categories_to_list(wd)

    for city in cities:
        ls, distinct_category = data_preparation(name_format(wd, city))
        for support_threshold in support_thresholds:
            print(f'CITY {city}:')
            print(f'support_threshold: {support_threshold}')

            ## MINING LOOP ##
            k = 1
            c_kp1 = []
            minsup = round(len(ls) * support_threshold)
            f_k = f_1(ls, distinct_category, minsup)
            freq_itemset = []

            while f_k:
                print(f'\tk: {k}')
                c_kp1 = candidate_generation(f_k, k)
                candidate_pruning(c_kp1, f_k, k)
                candidate_elimination(c_kp1, ls, minsup)
                add_freq_itemset(c_kp1, freq_itemset)
                f_k = c_kp1
                k += 1
            ## == ##

            if freq_itemset:
                print(f'\tfrequent itemset(s) in city {city} for minsup of {minsup}:')
                index = 1
                for itemset in freq_itemset:
                    print(f'\t{index}.\t', end="")
                    index += 1
                    for item in itemset:
                        print(categories[item - 1], end=", ")
                    print()
            else:
                print(f'\tthere are no frequent itemsets in city {city} for minsup of {minsup}')

if __name__ == '__main__':
    main()
    # for_checking()

