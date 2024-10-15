# Завдання 3
# Порівняйте ефективність алгоритмів пошуку підрядка: Боєра-Мура, 
# Кнута-Морріса-Пратта та Рабіна-Карпа на основі двох текстових 
# файлів (стаття 1, стаття 2). Використовуючи timeit, треба виміряти 
# час виконання кожного алгоритму для двох видів підрядків: одного, що 
# дійсно існує в тексті, та іншого — вигаданого (вибір підрядків за вашим бажанням). 
# На основі отриманих даних визначте найшвидший алгоритм 
# для кожного тексту окремо та в цілому.

import timeit
import random
import tracemalloc

class Search_Kmp:
    def algo(self):
        return "Алгоритм Кнута-Морріса-Пратта"

    def compute_lps(self, pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1

        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1

        return lps

    def search(self, main_string, pattern):
        M = len(pattern)
        N = len(main_string)

        lps = self.compute_lps(pattern)

        i = j = 0

        while i < N:
            if pattern[j] == main_string[i]:
                i += 1
                j += 1
            elif j != 0:
                j = lps[j - 1]
            else:
                i += 1

            if j == M:
                return i - j

        return -1  # якщо підрядок не знайдено

class Search_Bm:
    def algo(self):
        return "Алгоритм Боєра-Мура"
    
    def build_shift_table(self, pattern):
        #Створити таблицю зсувів для алгоритму Боєра-Мура.
        table = {}
        length = len(pattern)
        # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
        for index, char in enumerate(pattern[:-1]):
            table[char] = length - index - 1
        # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
        table.setdefault(pattern[-1], length)
        return table

    def search(self, text, pattern):
        # Створюємо таблицю зсувів для патерну (підрядка)
        shift_table = self.build_shift_table(pattern)
        i = 0 # Ініціалізуємо початковий індекс для основного тексту

        # Проходимо по основному тексту, порівнюючи з підрядком
        while i <= len(text) - len(pattern):
            j = len(pattern) - 1 # Починаємо з кінця підрядка

            # Порівнюємо символи від кінця підрядка до його початку
            while j >= 0 and text[i + j] == pattern[j]:
                j -= 1 # Зсуваємось до початку підрядка

            # Якщо весь підрядок збігається, повертаємо його позицію в тексті
            if j < 0:
                return i # Підрядок знайдено

            # Зсуваємо індекс i на основі таблиці зсувів
            # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
            i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

        # Якщо підрядок не знайдено, повертаємо -1
        return -1

class Search_Rk:
    def algo(self):
        return "Алгоритм Рабіна-Карпа"

    def polynomial_hash(self, s, base=256, modulus=101):
        # Повертає поліноміальний хеш рядка s.
        n = len(s)
        hash_value = 0
        for i, char in enumerate(s):
            power_of_base = pow(base, n - i - 1) % modulus
            hash_value = (hash_value + ord(char) * power_of_base) % modulus
        return hash_value

    def search(self, main_string, substring):
        # Довжини основного рядка та підрядка пошуку
        substring_length = len(substring)
        main_string_length = len(main_string)
        
        # Базове число для хешування та модуль
        base = 256 
        modulus = 101  
        
        # Хеш-значення для підрядка пошуку та поточного відрізка в основному рядку
        substring_hash = self.polynomial_hash(substring, base, modulus)
        current_slice_hash = self.polynomial_hash(main_string[:substring_length], base, modulus)
        
        # Попереднє значення для перерахунку хешу
        h_multiplier = pow(base, substring_length - 1) % modulus
        
        # Проходимо крізь основний рядок
        for i in range(main_string_length - substring_length + 1):
            if substring_hash == current_slice_hash:
                if main_string[i:i+substring_length] == substring:
                    return i

            if i < main_string_length - substring_length:
                current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
                current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
                if current_slice_hash < 0:
                    current_slice_hash += modulus

        return -1


def main():

    inputs = [
        ("article1.txt", "метод розв'язання"), 
        ("article1.txt", "not in file"), 
        ("article2.txt", "діаграми рішень (BDD)"),
        ("article2.txt", "not in file")
    ]

    search_algos = [Search_Kmp(), Search_Bm(), Search_Rk()]

    for input in inputs:
        print(f"Haystack: '{input[0]}'") 
        
        haystack = ""
        file = open(input[0], "r")
        for line in file.readlines():
            haystack += line.strip()
        file.close() 
        
        #print(haystack)
        
        quiqest = (0, '')
        for search_algo in search_algos:
            print(f"Needle is: '{input[1]}' search  by '{search_algo.algo()}'")
            tracemalloc.start()
            start_time = timeit.default_timer()
            
            position = search_algo.search(haystack, input[1])
            
            execution_time = timeit.default_timer() - start_time
            
            print(f"Used memory: {tracemalloc.get_traced_memory()}")
            tracemalloc.stop()

            if position != -1:
                print(f"Substring found at index {position}")
            else:
                print("Substring not found")
            
            print(f"Execution time: {execution_time}")

            if quiqest[0] == 0 or quiqest[0] > execution_time:
                quiqest = (execution_time, search_algo.algo())

        print("Швидший алгоритм в цьому блоці '" + quiqest[1] + "'")

if __name__ == "__main__":
    main()
