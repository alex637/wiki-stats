#!/usr/bin/python3

import os
import sys
import math
import array
import statistics


class WikiGraph:

   def load_from_file(self, filename):
       print('Загружаю граф из файла: ' + filename)
       with open(filename) as f:
           s = f.readline().split()
           self._n = int(s[0])
           self._nlinks = int(s[1])

           self._titles = []
           self._sizes = array.array('L', [0]*self._n)
           self._links = array.array('L', [0]*self._nlinks)
           self._redirect = array.array('B', [0]*self._n)
           self._offset = array.array('L', [0]*(self._n+1))

           for i in range(self._n):
               self._titles.append(f.readline().strip())
               s = f.readline().strip().split()
               self._sizes[i] = int(s[0])
               self._redirect[i] = int(s[1])
               self._offset[i+1] = self._offset[i]+int(s[2])
               for j in range(self._offset[i], self._offset[i+1]):
                   self._links.append(int(f.readline()))

       print('Граф загружен')
       f.close()

   def get_number_of_links_from(self, _id):
       return self._offset[_id + 1] - self._offset[_id]

   def get_links_from(self, _id):
       return self._links[self._offset[_id]:self._offset[_id+1]]  # returns array.array object

   def get_id(self, title):
       for i, t in enumerate(self._titles):
           if t == title:
               return i
       return -1

   def get_number_of_pages(self):
       return self._n

   def is_redirect(self, _id):
       return self._redirect[_id]

   def get_title(self, _id):
       return self._titles[_id]

   def get_page_size(self, _id):
       return self._sizes[_id]


w = WikiGraph()
w.load_from_file('/home/student/PycharmProjects/wiki-stats/wiki_small.txt')


print('Кол-во статей с перенаправлением равно', sum(w._redirect))
minimum = float("+inf")
maximum = float("-inf")
count_max = count_min = 0
article_max = ''
for i in range(w._n):
   current = w.get_number_of_links_from(i)
   if current == minimum:
       count_min += 1
   elif current < minimum:
       minimum = current
       count_min = 1
   if current == maximum:
       count_max += 1
   elif current > maximum:
       maximum = current
       article_max = w.get_title(i)
       count_max = 1
print('Минимальное кол-во ссылок из статьи:', minimum)
print('Кол-во статей с минимальным кол-вом ссылок:', count_min)
print('Максимальное кол-во ссылок из статьи:', maximum)
print('Кол-во статей с максимальным кол-вом ссылок:', count_max)
print('Статья с наибольшим кол-вом ссылок:', article_max)
print('Среднее кол-во ссылок в статье:', w._nlinks / w._n)


parent_vertex = array.array('H', [0 for i in range(w._n)])
for i in w._links:
   parent_vertex[i] += 1   # number of parents, including redirected
for i in range(w._n):
   if w.is_redirect(i):
       for v in w._links[w._offset[i]:w._offset[i + 1]]:
           parent_vertex[v] -= 1   # number of parents without redirected

minimum = float("+inf")
maximum = float("-inf")
count_max = count_min = 0
article_max = ''
for i in range(w._n):
   current = parent_vertex[i]
   if current == minimum:
       count_min += 1
   elif current < minimum:
       minimum = current
       count_min = 1
   if current == maximum:
       count_max += 1
   elif current > maximum:
       maximum = current
       article_max = w.get_title(i)
       count_max = 1
print('Минимальное кол-во ссылок на статью:', minimum)
print('Кол-во статей с минимальным кол-вом ссылок на неё:', count_min)
print('Максимальное кол-во ссылок на статью:', maximum)
print('Кол-во статей с максимальным кол-вом ссылок на неё:', count_max)
print('Статья с наибольшим кол-вом ссылок на неё:', article_max)
# print('Среднее кол-во ссылок в статье:', w._nlinks / w._n)
