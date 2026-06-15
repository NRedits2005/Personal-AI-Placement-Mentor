# Authentic LeetCode Questions by Topic and Difficulty

LEETCODE_QUESTIONS = {
    # 1. ARRAYS
    ("Easy", "Arrays"): {
        "question_id": "two_sum",
        "title": "Two Sum",
        "description": "Given an array of integers `nums` and an integer `target`, return *indices of the two numbers such that they add up to `target`*.\n\nYou may assume that each input would have **exactly one solution**, and you may not use the *same* element twice.\n\nYou can return the answer in any order.",
        "difficulty": "Easy",
        "company_tags": ["Google", "Amazon", "Microsoft", "Meta", "Apple"],
        "sample_input": "nums = [2,7,11,15], target = 9",
        "sample_output": "[0,1]",
        "constraints": "2 <= nums.length <= 10^4\n-10^9 <= nums[i] <= 10^9\n-10^9 <= target <= 10^9\nOnly one valid answer exists."
    },
    ("Medium", "Arrays"): {
        "question_id": "3sum",
        "title": "3Sum",
        "description": "Given an integer array `nums`, return all the triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.\n\nNotice that the solution set must not contain duplicate triplets.",
        "difficulty": "Medium",
        "company_tags": ["Google", "Amazon", "Meta", "Adobe", "Microsoft"],
        "sample_input": "nums = [-1,0,1,2,-1,-4]",
        "sample_output": "[[-1,-1,2],[-1,0,1]]",
        "constraints": "3 <= nums.length <= 3000\n-10^5 <= nums[i] <= 10^5"
    },
    ("Hard", "Arrays"): {
        "question_id": "first_missing_positive",
        "title": "First Missing Positive",
        "description": "Given an unsorted integer array `nums`, return the smallest missing positive integer.\n\nYou must implement an algorithm that runs in `O(n)` time and uses `O(1)` auxiliary space.",
        "difficulty": "Hard",
        "company_tags": ["Google", "Amazon", "Microsoft", "ByteDance"],
        "sample_input": "nums = [1,2,0]",
        "sample_output": "3",
        "constraints": "1 <= nums.length <= 10^5\n-2^31 <= nums[i] <= 2^31 - 1"
    },

    # 2. STRINGS
    ("Easy", "Strings"): {
        "question_id": "valid_parentheses",
        "title": "Valid Parentheses",
        "description": "Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.\n\nAn input string is valid if:\n1. Open brackets must be closed by the same type of brackets.\n2. Open brackets must be closed in the correct order.\n3. Every close bracket has a corresponding open bracket of the same type.",
        "difficulty": "Easy",
        "company_tags": ["Amazon", "Microsoft", "Meta", "Google", "Bloomberg"],
        "sample_input": "s = \"()[]{}\"",
        "sample_output": "true",
        "constraints": "1 <= s.length <= 10^4\ns consists of parentheses only '()[]{}'."
    },
    ("Medium", "Strings"): {
        "question_id": "longest_substring_without_repeating_characters",
        "title": "Longest Substring Without Repeating Characters",
        "description": "Given a string `s`, find the length of the **longest substring** without repeating characters.",
        "difficulty": "Medium",
        "company_tags": ["Amazon", "Google", "Microsoft", "Meta", "Uber"],
        "sample_input": "s = \"abcabcbb\"",
        "sample_output": "3 (The substring is \"abc\")",
        "constraints": "0 <= s.length <= 5 * 10^4\ns consists of English letters, digits, symbols and spaces."
    },
    ("Hard", "Strings"): {
        "question_id": "minimum_window_substring",
        "title": "Minimum Window Substring",
        "description": "Given two strings `s` and `t` of lengths `m` and `n` respectively, return the *minimum window substring* of `s` such that every character in `t` (including duplicates) is included in the window. If there is no such substring, return the empty string `\"\"`.\n\nThe test cases will be generated such that the answer is **unique**.",
        "difficulty": "Hard",
        "company_tags": ["Google", "Meta", "Amazon", "Microsoft", "LinkedIn"],
        "sample_input": "s = \"ADOBECODEBANC\", t = \"ABC\"",
        "sample_output": "\"BANC\"",
        "constraints": "m == s.length, n == t.length\n1 <= m, n <= 10^5\ns and t consist of uppercase and lowercase English letters."
    },

    # 3. HASHMAPS
    ("Easy", "HashMaps"): {
        "question_id": "contains_duplicate",
        "title": "Contains Duplicate",
        "description": "Given an integer array `nums`, return `true` if any value appears **at least twice** in the array, and return `false` if every element is distinct.",
        "difficulty": "Easy",
        "company_tags": ["Amazon", "Adobe", "Apple", "Google"],
        "sample_input": "nums = [1,2,3,1]",
        "sample_output": "true",
        "constraints": "1 <= nums.length <= 10^5\n-10^9 <= nums[i] <= 10^9"
    },
    ("Medium", "HashMaps"): {
        "question_id": "group_anagrams",
        "title": "Group Anagrams",
        "description": "Given an array of strings `strs`, group the **anagrams** together. You can return the answer in **any order**.\n\nAn **Anagram** is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.",
        "difficulty": "Medium",
        "company_tags": ["Amazon", "Google", "Meta", "Microsoft", "Salesforce"],
        "sample_input": "strs = [\"eat\",\"tea\",\"tan\",\"ate\",\"nat\",\"bat\"]",
        "sample_output": "[[\"bat\"],[\"nat\",\"tan\"],[\"ate\",\"eat\",\"tea\"]]",
        "constraints": "1 <= strs.length <= 10^4\n0 <= strs[i].length <= 100\nstrs[i] consists of lowercase English letters."
    },
    ("Hard", "HashMaps"): {
        "question_id": "insert_delete_getrandom_o1_duplicates_allowed",
        "title": "Insert Delete GetRandom O(1) - Duplicates allowed",
        "description": "RandomizedCollection is a data structure that contains a collection of numbers, possibly duplicates (i.e., a multiset). It should support insert, remove, and getRandom operations in average O(1) time complexity.\n\nImplement the RandomizedCollection class:\n- `insert(val)`: Inserts an item val to the collection.\n- `remove(val)`: Removes an item val from the collection if present.\n- `getRandom()`: Returns a random element from the current collection of elements.",
        "difficulty": "Hard",
        "company_tags": ["Affirm", "Google", "Amazon", "LinkedIn"],
        "sample_input": "[\"RandomizedCollection\", \"insert\", \"insert\", \"insert\", \"getRandom\", \"remove\", \"getRandom\"] \n[[], [1], [1], [2], [], [1], []]",
        "sample_output": "[null, true, false, true, 1, true, 2]",
        "constraints": "-2^31 <= val <= 2^31 - 1\nAt most 2 * 10^5 calls will be made to insert, remove, and getRandom."
    },

    # 4. LINKED LISTS
    ("Easy", "Linked Lists"): {
        "question_id": "reverse_linked_list",
        "title": "Reverse Linked List",
        "description": "Given the `head` of a singly linked list, reverse the list, and return *the reversed list*.",
        "difficulty": "Easy",
        "company_tags": ["Amazon", "Microsoft", "Apple", "Facebook", "Adobe"],
        "sample_input": "head = [1,2,3,4,5]",
        "sample_output": "[5,4,3,2,1]",
        "constraints": "The number of nodes in the list is the range [0, 5000].\n-5000 <= Node.val <= 5000"
    },
    ("Medium", "Linked Lists"): {
        "question_id": "add_two_numbers",
        "title": "Add Two Numbers",
        "description": "You are given two **non-empty** linked lists representing two non-negative integers. The digits are stored in **reverse order**, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.\n\nYou may assume the two numbers do not contain any leading zero, except the number 0 itself.",
        "difficulty": "Medium",
        "company_tags": ["Amazon", "Google", "Microsoft", "Meta", "Bloomberg"],
        "sample_input": "l1 = [2,4,3], l2 = [5,6,4]",
        "sample_output": "[7,0,8] (representing 342 + 465 = 807)",
        "constraints": "The number of nodes in each linked list is in the range [1, 100].\n0 <= Node.val <= 9\nIt is guaranteed that the list represents a number that does not have leading zeros."
    },
    ("Hard", "Linked Lists"): {
        "question_id": "merge_k_sorted_lists",
        "title": "Merge k Sorted Lists",
        "description": "You are given an array of `k` linked-lists `lists`, each linked-list is sorted in ascending order.\n\n*Merge all the linked-lists into one sorted linked-list and return it.*",
        "difficulty": "Hard",
        "company_tags": ["Amazon", "Google", "Meta", "Microsoft", "ByteDance"],
        "sample_input": "lists = [[1,4,5],[1,3,4],[2,6]]",
        "sample_output": "[1,1,2,3,4,4,5,6]",
        "constraints": "k == lists.length\n0 <= k <= 10^4\n0 <= lists[i].length <= 500\n-10^4 <= lists[i][j] <= 10^4\nlists[i] is sorted in ascending order."
    },

    # 5. TREES
    ("Easy", "Trees"): {
        "question_id": "maximum_depth_of_binary_tree",
        "title": "Maximum Depth of Binary Tree",
        "description": "Given the `root` of a binary tree, return *its maximum depth*.\n\nA binary tree's **maximum depth** is the number of nodes along the longest path from the root node down to the farthest leaf node.",
        "difficulty": "Easy",
        "company_tags": ["Amazon", "Google", "Microsoft", "LinkedIn"],
        "sample_input": "root = [3,9,20,null,null,15,7]",
        "sample_output": "3",
        "constraints": "The number of nodes in the tree is in the range [0, 10^4].\n-100 <= Node.val <= 100"
    },
    ("Medium", "Trees"): {
        "question_id": "validate_binary_search_tree",
        "title": "Validate Binary Search Tree",
        "description": "Given the `root` of a binary tree, determine if it is a valid binary search tree (BST).\n\nA **valid BST** is defined as follows:\n- The left subtree of a node contains only nodes with keys **less than** the node's key.\n- The right subtree of a node contains only nodes with keys **greater than** the node's key.\n- Both the left and right subtrees must also be binary search trees.",
        "difficulty": "Medium",
        "company_tags": ["Amazon", "Microsoft", "Bloomberg", "Google", "Facebook"],
        "sample_input": "root = [2,1,3]",
        "sample_output": "true",
        "constraints": "The number of nodes in the tree is in the range [1, 10^4].\n-2^31 <= Node.val <= 2^31 - 1"
    },
    ("Hard", "Trees"): {
        "question_id": "binary_tree_maximum_path_sum",
        "title": "Binary Tree Maximum Path Sum",
        "description": "A **path** in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them. A node can only appear in the sequence **at most once**. Note that the path does not need to pass through the root.\n\nThe **path sum** of a path is the sum of the node's values in the path.\n\nGiven the `root` of a binary tree, return *the maximum path sum of any non-empty path*.",
        "difficulty": "Hard",
        "company_tags": ["Facebook", "Google", "Amazon", "Microsoft"],
        "sample_input": "root = [-10,9,20,null,null,15,7]",
        "sample_output": "42 (The path is [15, 20, 7] which sums to 15 + 20 + 7 = 42)",
        "constraints": "The number of nodes in the tree is in the range [1, 3 * 10^4].\n-1000 <= Node.val <= 1000"
    },

    # 6. GRAPHS
    ("Easy", "Graphs"): {
        "question_id": "find_center_of_star_graph",
        "title": "Find Center of Star Graph",
        "description": "There is an undirected **star graph** consisting of `n` nodes labeled from `1` to `n`. A star graph is a graph where there is one **center** node and exactly `n - 1` edges that connect the center node with every other node.\n\nYou are given a 2D integer array `edges` where each `edges[i] = [ui, vi]` indicates that there is an edge between the nodes `ui` and `vi`. Return the center of the given star graph.",
        "difficulty": "Easy",
        "company_tags": ["Google", "MS", "Uber"],
        "sample_input": "edges = [[1,2],[5,1],[1,3],[1,4]]",
        "sample_output": "1",
        "constraints": "3 <= n <= 10^5\nedges.length == n - 1\nedges[i].length == 2\n1 <= ui, vi <= n\nui != vi\nThe given edges represent a valid star graph."
    },
    ("Medium", "Graphs"): {
        "question_id": "number_of_islands",
        "title": "Number of Islands",
        "description": "Given an `m x n` 2D binary grid `grid` which represents a map of `'1'`s (land) and `'0'`s (water), return *the number of islands*.\n\nAn **island** is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.",
        "difficulty": "Medium",
        "company_tags": ["Amazon", "Google", "Microsoft", "Meta", "Bloomberg", "Qualtrics"],
        "sample_input": "grid = [\n  [\"1\",\"1\",\"1\",\"1\",\"0\"],\n  [\"1\",\"1\",\"0\",\"1\",\"0\"],\n  [\"1\",\"1\",\"0\",\"0\",\"0\"],\n  [\"0\",\"0\",\"0\",\"0\",\"0\"]\n]",
        "sample_output": "1",
        "constraints": "m == grid.length\nn == grid[i].length\n1 <= m, n <= 300\ngrid[i][j] is '0' or '1'."
    },
    ("Hard", "Graphs"): {
        "question_id": "word_ladder",
        "title": "Word Ladder",
        "description": "A **transformation sequence** from word `beginWord` to word `endWord` using a dictionary `wordList` is a sequence of words `beginWord -> s1 -> s2 -> ... -> sk` such that:\n- Every adjacent pair of words differs by a single letter.\n- Every `si` for `1 <= i <= k` is in `wordList`. Note that `beginWord` does not need to be in `wordList`.\n- `sk == endWord`\n\nGiven two words, `beginWord` and `endWord`, and a dictionary `wordList`, return *the number of words in the shortest transformation sequence from `beginWord` to `endWord`, or `0` if no such sequence exists.*",
        "difficulty": "Hard",
        "company_tags": ["Amazon", "Google", "Facebook", "Microsoft", "Yelp"],
        "sample_input": "beginWord = \"hit\", endWord = \"cog\", wordList = [\"hot\",\"dot\",\"dog\",\"lot\",\"log\",\"cog\"]",
        "sample_output": "5 (The sequence is \"hit\" -> \"hot\" -> \"dot\" -> \"dog\" -> \"cog\")",
        "constraints": "1 <= beginWord.length <= 10\nendWord.length == beginWord.length\n1 <= wordList.length <= 5000\nwordList[i].length == beginWord.length\nbeginWord, endWord, and wordList[i] consist of lowercase English letters."
    },

    # 7. DYNAMIC PROGRAMMING
    ("Easy", "Dynamic Programming"): {
        "question_id": "climbing_stairs",
        "title": "Climbing Stairs",
        "description": "You are climbing a staircase. It takes `n` steps to reach the top.\n\nEach time you can either climb `1` or `2` steps. In how many distinct ways can you climb to the top?",
        "difficulty": "Easy",
        "company_tags": ["Amazon", "Adobe", "Google", "Apple", "Uber"],
        "sample_input": "n = 3",
        "sample_output": "3 (1+1+1, 1+2, 2+1)",
        "constraints": "1 <= n <= 45"
    },
    ("Medium", "Dynamic Programming"): {
        "question_id": "coin_change",
        "title": "Coin Change",
        "description": "You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money.\n\nReturn *the fewest number of coins that you need to make up that amount*. If that amount of money cannot be made up by any combination of the coins, return `-1`.\n\nYou may assume that you have an infinite number of each kind of coin.",
        "difficulty": "Medium",
        "company_tags": ["Amazon", "Google", "Microsoft", "Facebook", "Bloomberg"],
        "sample_input": "coins = [1,2,5], amount = 11",
        "sample_output": "3 (11 = 5 + 5 + 1)",
        "constraints": "1 <= coins.length <= 12\n1 <= coins[i] <= 2^31 - 1\n0 <= amount <= 10^4"
    },
    ("Hard", "Dynamic Programming"): {
        "question_id": "edit_distance",
        "title": "Edit Distance",
        "description": "Given two strings `word1` and `word2`, return *the minimum number of operations required to convert `word1` to `word2`*.\n\nYou have the following three operations permitted on a word:\n1. Insert a character\n2. Delete a character\n3. Replace a character",
        "difficulty": "Hard",
        "company_tags": ["Google", "Amazon", "Microsoft", "LinkedIn"],
        "sample_input": "word1 = \"horse\", word2 = \"ros\"",
        "sample_output": "3 (horse -> rorse -> rose -> ros)",
        "constraints": "0 <= word1.length, word2.length <= 500\nword1 and word2 consist of lowercase English letters."
    }
}
