"""Unit tests for RegexFSM class"""
import unittest
from regex import RegexFSM


class TestRegexPatterns(unittest.TestCase):
    def test_simple_characters(self):
        """Test basic character matching"""
        pattern = "abc"
        regex = RegexFSM(pattern)
        
        # Should match
        self.assertTrue(regex.check_string("abc"))
        
        # Should not match
        self.assertFalse(regex.check_string(""))
        self.assertFalse(regex.check_string("a"))
        self.assertFalse(regex.check_string("ab"))
        self.assertFalse(regex.check_string("abcd"))
        self.assertFalse(regex.check_string("xabc"))
        self.assertFalse(regex.check_string("abd"))

    def test_dot_operator(self):
        """Test dot operator that matches any character"""
        pattern = "a.c"
        regex = RegexFSM(pattern)
        
        # Should match
        self.assertTrue(regex.check_string("abc"))
        self.assertTrue(regex.check_string("a1c"))
        self.assertTrue(regex.check_string("a c"))
        self.assertTrue(regex.check_string("a#c"))
        
        # Should not match
        self.assertFalse(regex.check_string("ac"))
        self.assertFalse(regex.check_string("a"))
        self.assertFalse(regex.check_string("c"))
        self.assertFalse(regex.check_string("abbc"))

    def test_star_operator(self):
        """Test star operator (zero or more)"""
        pattern = "a*b"
        regex = RegexFSM(pattern)
        
        # Should match
        self.assertTrue(regex.check_string("b"))      # Zero a's
        self.assertTrue(regex.check_string("ab"))     # One a
        self.assertTrue(regex.check_string("aab"))    # Multiple a's
        self.assertTrue(regex.check_string("aaab"))   # Multiple a's
        
        # Should not match
        self.assertFalse(regex.check_string(""))
        self.assertFalse(regex.check_string("a"))
        self.assertFalse(regex.check_string("ba"))
        self.assertFalse(regex.check_string("aba"))

    def test_plus_operator(self):
        """Test plus operator (one or more)"""
        pattern = "a+b"
        regex = RegexFSM(pattern)
        
        # Should match
        self.assertTrue(regex.check_string("ab"))     # One a
        self.assertTrue(regex.check_string("aab"))    # Multiple a's
        self.assertTrue(regex.check_string("aaaab"))  # Multiple a's
        
        # Should not match
        self.assertFalse(regex.check_string(""))
        self.assertFalse(regex.check_string("b"))     # Zero a's
        self.assertFalse(regex.check_string("a"))
        self.assertFalse(regex.check_string("ba"))
        self.assertFalse(regex.check_string("aba"))

    def test_multiple_operators(self):
        """Test combinations of operators"""
        pattern = "a*b+c."
        regex = RegexFSM(pattern)
        
        # Should match
        self.assertTrue(regex.check_string("bcx"))    # Zero a's, one b
        self.assertTrue(regex.check_string("abcx"))   # One a, one b
        self.assertTrue(regex.check_string("aabbbcx"))# Multiple a's, multiple b's
        self.assertTrue(regex.check_string("bbc0"))   # Zero a's, multiple b's
        
        # Should not match
        self.assertFalse(regex.check_string("ac"))    # Missing b
        self.assertFalse(regex.check_string("abc"))   # Missing character after c
        self.assertFalse(regex.check_string("aabcxy"))# Extra characters

    def test_complex_pattern_1(self):
        """Test pattern a*b*c"""
        pattern = "a*b*c"
        regex = RegexFSM(pattern)
        
        # Should match
        self.assertTrue(regex.check_string("c"))      # Zero a's, zero b's
        self.assertTrue(regex.check_string("ac"))     # One a, zero b's
        self.assertTrue(regex.check_string("bc"))     # Zero a's, one b
        self.assertTrue(regex.check_string("abc"))    # One a, one b
        self.assertTrue(regex.check_string("aaaabc")) # Multiple a's, one b
        self.assertTrue(regex.check_string("abbbc"))  # One a, multiple b's
        self.assertTrue(regex.check_string("aaaabbbbc")) # Multiple of both
        
        # Should not match
        self.assertFalse(regex.check_string(""))
        self.assertFalse(regex.check_string("a"))
        self.assertFalse(regex.check_string("b"))
        self.assertFalse(regex.check_string("ab"))
        self.assertFalse(regex.check_string("bac"))   # Wrong order
        self.assertFalse(regex.check_string("cab"))   # Wrong order
        self.assertFalse(regex.check_string("abcd"))  # Extra character

    def test_complex_pattern_2(self):
        """Test pattern a*4.+hi"""
        pattern = "a*4.+hi"
        regex = RegexFSM(pattern)
        
        # Should match
        self.assertTrue(regex.check_string("4zhi"))    # Zero a's, one char after 4
        self.assertTrue(regex.check_string("a4zhi"))   # One a
        self.assertTrue(regex.check_string("aaa4zhi")) # Multiple a's
        self.assertTrue(regex.check_string("4zzhi"))   # Multiple chars after 4
        self.assertTrue(regex.check_string("a4zzzhi")) # Multiple chars after 4
        
        # Should not match
        self.assertFalse(regex.check_string(""))
        self.assertFalse(regex.check_string("a"))
        self.assertFalse(regex.check_string("4"))
        self.assertFalse(regex.check_string("hi"))
        self.assertFalse(regex.check_string("a4hi"))   # Missing char after 4
        self.assertFalse(regex.check_string("a4zhix")) # Extra character

    def test_dot_star_pattern(self):
        """Test pattern .*abc - match abc anywhere"""
        pattern = ".*abc"
        regex = RegexFSM(pattern)
        
        # Should match
        self.assertTrue(regex.check_string("abc"))     # Just abc
        self.assertTrue(regex.check_string("xabc"))    # Prefix + abc
        self.assertTrue(regex.check_string("xxxabc"))  # Longer prefix
        self.assertTrue(regex.check_string("123abc"))  # Numbers as prefix
        
        # Should not match
        self.assertFalse(regex.check_string(""))
        self.assertFalse(regex.check_string("a"))
        self.assertFalse(regex.check_string("ab"))
        self.assertFalse(regex.check_string("abcx"))   # Extra after
        self.assertFalse(regex.check_string("abx"))    # Different char
    
    def test_edge_cases(self):
        """Test edge cases and corner patterns"""
        # Single character with star
        pattern1 = "a*"
        regex1 = RegexFSM(pattern1)
        self.assertTrue(regex1.check_string(""))      # Zero a's
        self.assertTrue(regex1.check_string("a"))     # One a
        self.assertTrue(regex1.check_string("aaaaa")) # Many a's
        self.assertFalse(regex1.check_string("b"))    # Different character
        
        # Single character with plus
        pattern2 = "a+"
        regex2 = RegexFSM(pattern2)
        self.assertFalse(regex2.check_string(""))     # Zero a's not allowed
        self.assertTrue(regex2.check_string("a"))     # One a
        self.assertTrue(regex2.check_string("aaaaa")) # Many a's
        self.assertFalse(regex2.check_string("b"))    # Different character
        
        # Star at end of pattern
        pattern3 = "abc*"
        regex3 = RegexFSM(pattern3)
        self.assertTrue(regex3.check_string("ab"))    # Zero c's
        self.assertTrue(regex3.check_string("abc"))   # One c
        self.assertTrue(regex3.check_string("abccc")) # Many c's
        self.assertFalse(regex3.check_string("a"))    # Incomplete
        
        # Dot with star
        pattern4 = "a.*z"
        regex4 = RegexFSM(pattern4)
        self.assertTrue(regex4.check_string("az"))    # No chars between
        self.assertTrue(regex4.check_string("abcz"))  # Some chars between
        self.assertFalse(regex4.check_string("a"))    # Missing z
        self.assertFalse(regex4.check_string("z"))    # Missing a
    
    def test_basic_char_classes(self):
        """Test basic character classes with individual characters"""
        pattern = "[abc]"
        regex = RegexFSM(pattern)
        
        # Should match
        self.assertTrue(regex.check_string("a"))
        self.assertTrue(regex.check_string("b"))
        self.assertTrue(regex.check_string("c"))
        
        # Should not match
        self.assertFalse(regex.check_string(""))
        self.assertFalse(regex.check_string("d"))
        self.assertFalse(regex.check_string("ab"))
        self.assertFalse(regex.check_string("abc"))

    def test_char_ranges(self):
        """Test character class ranges"""
        pattern = "[a-e]"
        regex = RegexFSM(pattern)
        
        # Should match
        self.assertTrue(regex.check_string("a"))
        self.assertTrue(regex.check_string("b"))
        self.assertTrue(regex.check_string("e"))
        
        # Should not match
        self.assertFalse(regex.check_string(""))
        self.assertFalse(regex.check_string("f"))
        self.assertFalse(regex.check_string("ab"))
        
        # Test numeric range
        pattern2 = "[0-9]"
        regex2 = RegexFSM(pattern2)
        self.assertTrue(regex2.check_string("0"))
        self.assertTrue(regex2.check_string("5"))
        self.assertTrue(regex2.check_string("9"))
        self.assertFalse(regex2.check_string("a"))

    def test_negated_char_classes(self):
        """Test negated character classes"""
        pattern = "[^abc]"
        regex = RegexFSM(pattern)
        
        # Should match
        self.assertTrue(regex.check_string("d"))
        self.assertTrue(regex.check_string("z"))
        self.assertTrue(regex.check_string("0"))
        
        # Should not match
        self.assertFalse(regex.check_string(""))
        self.assertFalse(regex.check_string("a"))
        self.assertFalse(regex.check_string("b"))
        self.assertFalse(regex.check_string("c"))
        self.assertFalse(regex.check_string("ab"))

    def test_mixed_char_classes(self):
        """Test mixed character classes"""
        pattern = "[a-zA-Z0-9]"
        regex = RegexFSM(pattern)
        
        # Should match
        self.assertTrue(regex.check_string("a"))
        self.assertTrue(regex.check_string("Z"))
        self.assertTrue(regex.check_string("5"))
        
        # Should not match
        self.assertFalse(regex.check_string(""))
        self.assertFalse(regex.check_string("_"))
        self.assertFalse(regex.check_string("#"))
        self.assertFalse(regex.check_string("ab"))

    def test_char_class_with_operators(self):
        """Test character classes with operators"""
        # Star operator with char class
        pattern1 = "[0-9]*a"
        regex1 = RegexFSM(pattern1)
        self.assertTrue(regex1.check_string("a"))       # Zero digits
        self.assertTrue(regex1.check_string("5a"))      # One digit
        self.assertTrue(regex1.check_string("123a"))    # Multiple digits
        self.assertFalse(regex1.check_string(""))
        self.assertFalse(regex1.check_string("5"))
        self.assertFalse(regex1.check_string("b"))
        
        # Plus operator with char class
        pattern2 = "[0-9]+a"
        regex2 = RegexFSM(pattern2)
        self.assertTrue(regex2.check_string("5a"))      # One digit
        self.assertTrue(regex2.check_string("123a"))    # Multiple digits
        self.assertFalse(regex2.check_string("a"))      # Zero digits
        self.assertFalse(regex2.check_string(""))
        self.assertFalse(regex2.check_string("b5a"))
        
        # Dot with char class
        pattern3 = "a.[0-9]"
        regex3 = RegexFSM(pattern3)
        self.assertTrue(regex3.check_string("ab5"))
        self.assertTrue(regex3.check_string("a%9"))
        self.assertFalse(regex3.check_string("a5"))
        self.assertFalse(regex3.check_string("abc"))

    def test_char_class_edge_cases(self):
        """Test edge cases with character classes"""
        # Single char in class
        pattern1 = "[x]"
        regex1 = RegexFSM(pattern1)
        self.assertTrue(regex1.check_string("x"))
        self.assertFalse(regex1.check_string("y"))
        
        # Multiple ranges
        pattern2 = "[a-cx-z]"
        regex2 = RegexFSM(pattern2)
        self.assertTrue(regex2.check_string("a"))
        self.assertTrue(regex2.check_string("b"))
        self.assertTrue(regex2.check_string("x"))
        self.assertTrue(regex2.check_string("z"))
        self.assertFalse(regex2.check_string("d"))
        
        # Char class at start and end
        pattern3 = "[0-9][a-z][0-9]"
        regex3 = RegexFSM(pattern3)
        self.assertTrue(regex3.check_string("5a7"))
        self.assertTrue(regex3.check_string("0z9"))
        self.assertFalse(regex3.check_string("5aa"))
        self.assertFalse(regex3.check_string("a57"))
        
        # Negated class with range
        pattern4 = "[^a-m]"
        regex4 = RegexFSM(pattern4)
        self.assertTrue(regex4.check_string("n"))
        self.assertTrue(regex4.check_string("z"))
        self.assertTrue(regex4.check_string("5"))
        self.assertFalse(regex4.check_string("a"))
        self.assertFalse(regex4.check_string("m"))


if __name__ == "__main__":
    unittest.main()
